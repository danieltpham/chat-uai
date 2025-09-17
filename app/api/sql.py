from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any
import re
from app.database import get_db

router = APIRouter()

# List of allowed SQL keywords for read-only operations
ALLOWED_KEYWORDS = {
    'SELECT', 'FROM', 'WHERE', 'JOIN', 'INNER', 'LEFT', 'RIGHT', 'OUTER', 
    'ON', 'GROUP', 'BY', 'ORDER', 'HAVING', 'LIMIT', 'OFFSET', 'AS', 
    'AND', 'OR', 'NOT', 'IN', 'LIKE', 'BETWEEN', 'IS', 'NULL', 'DISTINCT',
    'COUNT', 'SUM', 'AVG', 'MIN', 'MAX', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END',
    'CAST', 'EXTRACT', 'DATE', 'TIMESTAMP', 'UNION', 'ALL', 'EXISTS',
    'WITH', 'RECURSIVE', 'CTE'
}

# Dangerous keywords that should never be allowed
FORBIDDEN_KEYWORDS = {
    'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER', 'TRUNCATE',
    'EXEC', 'EXECUTE', 'CALL', 'PROCEDURE', 'FUNCTION', 'TRIGGER',
    'GRANT', 'REVOKE', 'COMMIT', 'ROLLBACK', 'SAVEPOINT',
    'PRAGMA', 'ATTACH', 'DETACH', 'VACUUM', 'ANALYZE', 'EXPLAIN'
}

# Allowed table names (our star schema tables)
ALLOWED_TABLES = {
    'dim_customer', 'dim_product', 'dim_date', 'fact_sales'
}

def sanitize_sql(sql_query: str) -> str:
    """
    Sanitize SQL query to prevent malicious operations.
    Returns the cleaned query or raises HTTPException if invalid.
    """
    if not sql_query or not sql_query.strip():
        raise HTTPException(status_code=400, detail="SQL query cannot be empty")
    
    # Convert to uppercase for keyword checking
    query_upper = sql_query.upper()
    
    # Check for forbidden keywords
    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(r'\b' + keyword + r'\b', query_upper):
            raise HTTPException(
                status_code=400, 
                detail=f"Forbidden keyword '{keyword}' detected. Only SELECT queries are allowed."
            )
    
    # Must start with SELECT (after whitespace)
    if not re.match(r'^\s*SELECT\b', query_upper):
        raise HTTPException(
            status_code=400, 
            detail="Query must start with SELECT. Only read operations are allowed."
        )
    
    # Check for dangerous patterns
    dangerous_patterns = [
        r'--',           # SQL comments
        r'/\*.*?\*/',    # Block comments
        r';\s*\w',       # Multiple statements
        r'\bxp_\w+',     # Extended stored procedures
        r'\bsp_\w+',     # Stored procedures
        r'@@\w+',        # System variables
        r'\$\$',         # Dollar quoting
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, query_upper, re.DOTALL):
            raise HTTPException(
                status_code=400, 
                detail=f"Potentially dangerous SQL pattern detected: {pattern}"
            )
    
    # Extract table names from the query
    table_pattern = r'\bFROM\s+(\w+)|\bJOIN\s+(\w+)'
    table_matches = re.findall(table_pattern, query_upper)
    referenced_tables = set()
    
    for match in table_matches:
        for table in match:
            if table:
                referenced_tables.add(table.lower())
    
    # Check if all referenced tables are allowed
    for table in referenced_tables:
        if table not in ALLOWED_TABLES:
            raise HTTPException(
                status_code=400, 
                detail=f"Access to table '{table}' is not allowed. "
                       f"Allowed tables: {', '.join(ALLOWED_TABLES)}"
            )
    
    # Limit query length to prevent resource exhaustion
    if len(sql_query) > 2000:
        raise HTTPException(
            status_code=400, 
            detail="Query too long. Maximum length is 2000 characters."
        )
    
    return sql_query.strip()

@router.get("/sql")
def execute_custom_sql(
    q: str = Query(..., description="SQL query to execute (SELECT only)"),
    limit: int = Query(100, le=1000, description="Maximum number of rows to return"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Execute a custom SQL query with safety restrictions.
    
    **Restrictions:**
    - Only SELECT queries are allowed
    - Only access to: dim_customer, dim_product, dim_date, fact_sales tables
    - No comments, multiple statements, or dangerous patterns
    - Maximum query length: 2000 characters
    - Maximum result rows: 1000 (default: 100)
    
    **Example queries:**
    - `SELECT * FROM dim_customer LIMIT 10`
    - `SELECT category, COUNT(*) FROM dim_product GROUP BY category`
    - `SELECT c.customer_name, SUM(f.total_amount) FROM fact_sales f JOIN dim_customer c ON f.customer_id = c.customer_id GROUP BY c.customer_name ORDER BY SUM(f.total_amount) DESC LIMIT 5`
    """
    try:
        # Sanitize the SQL query
        clean_query = sanitize_sql(q)
        
        # Add LIMIT clause if not present
        if not re.search(r'\bLIMIT\s+\d+', clean_query.upper()):
            clean_query += f" LIMIT {limit}"
        else:
            # Ensure existing LIMIT doesn't exceed maximum
            limit_match = re.search(r'\bLIMIT\s+(\d+)', clean_query.upper())
            if limit_match:
                existing_limit = int(limit_match.group(1))
                if existing_limit > 1000:
                    clean_query = re.sub(r'\bLIMIT\s+\d+', 'LIMIT 1000', clean_query, flags=re.IGNORECASE)
        
        # Execute the query
        result = db.execute(text(clean_query))
        
        # Convert result to list of dictionaries
        columns = result.keys()
        rows = result.fetchall()
        
        data = []
        for row in rows:
            row_dict = {}
            for i, col in enumerate(columns):
                value = row[i]
                # Convert special types to JSON-serializable formats
                if hasattr(value, 'isoformat'):  # datetime/date objects
                    value = value.isoformat()
                elif isinstance(value, (bytes, bytearray)):
                    value = value.decode('utf-8', errors='ignore')
                row_dict[col] = value
            data.append(row_dict)
        
        return {
            "query": clean_query,
            "columns": list(columns),
            "data": data,
            "row_count": len(data),
            "status": "success"
        }
        
    except HTTPException:
        # Re-raise our custom HTTP exceptions
        raise
    except Exception as e:
        # Handle database errors
        error_msg = str(e)
        if "syntax error" in error_msg.lower():
            raise HTTPException(status_code=400, detail=f"SQL syntax error: {error_msg}")
        elif "no such table" in error_msg.lower():
            raise HTTPException(status_code=400, detail=f"Table not found: {error_msg}")
        elif "no such column" in error_msg.lower():
            raise HTTPException(status_code=400, detail=f"Column not found: {error_msg}")
        else:
            raise HTTPException(status_code=500, detail=f"Database error: {error_msg}")

@router.get("/sql/tables")
def get_available_tables(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Get information about available tables and their schemas.
    """
    try:
        tables_info = {}
        
        for table_name in ALLOWED_TABLES:
            # Get column information for each table
            query = f"""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = '{table_name}'
                ORDER BY ordinal_position
            """
            
            try:
                result = db.execute(text(query))
                columns = [
                    {
                        "name": row[0],
                        "type": row[1],
                        "nullable": row[2] == 'YES'
                    }
                    for row in result.fetchall()
                ]
                tables_info[table_name] = {
                    "columns": columns,
                    "column_count": len(columns)
                }
            except:
                # Fallback if information_schema is not available
                sample_query = f"SELECT * FROM {table_name} LIMIT 0"
                result = db.execute(text(sample_query))
                columns = [{"name": col, "type": "unknown", "nullable": True} for col in result.keys()]
                tables_info[table_name] = {
                    "columns": columns,
                    "column_count": len(columns)
                }
        
        return {
            "available_tables": list(ALLOWED_TABLES),
            "table_schemas": tables_info,
            "total_tables": len(ALLOWED_TABLES)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving table information: {str(e)}")

@router.get("/sql/examples")
def get_sql_examples() -> Dict[str, Any]:
    """
    Get example SQL queries that users can try.
    """
    examples = [
        {
            "title": "Get all customers",
            "description": "Retrieve all customer records",
            "query": "SELECT * FROM dim_customer LIMIT 10"
        },
        {
            "title": "Product categories",
            "description": "Count products by category",
            "query": "SELECT category, COUNT(*) as product_count FROM dim_product GROUP BY category ORDER BY product_count DESC"
        },
        {
            "title": "Top customers by sales",
            "description": "Find customers with highest total sales",
            "query": "SELECT c.customer_name, SUM(f.total_amount) as total_sales FROM fact_sales f JOIN dim_customer c ON f.customer_id = c.customer_id GROUP BY c.customer_name ORDER BY total_sales DESC LIMIT 10"
        },
        {
            "title": "Monthly sales summary",
            "description": "Sales summary by month",
            "query": "SELECT d.month_name, d.year, COUNT(*) as order_count, SUM(f.total_amount) as total_sales FROM fact_sales f JOIN dim_date d ON f.date_id = d.date_id GROUP BY d.year, d.month, d.month_name ORDER BY d.year, d.month"
        },
        {
            "title": "Weekend vs Weekday sales",
            "description": "Compare sales between weekends and weekdays",
            "query": "SELECT CASE WHEN d.is_weekend = 1 THEN 'Weekend' ELSE 'Weekday' END as period, COUNT(*) as order_count, AVG(f.total_amount) as avg_order_value FROM fact_sales f JOIN dim_date d ON f.date_id = d.date_id GROUP BY d.is_weekend"
        },
        {
            "title": "Product performance",
            "description": "Best selling products with details",
            "query": "SELECT p.product_name, p.category, p.brand, COUNT(*) as times_sold, SUM(f.quantity) as total_quantity, SUM(f.total_amount) as total_revenue FROM fact_sales f JOIN dim_product p ON f.product_id = p.product_id GROUP BY p.product_name, p.category, p.brand ORDER BY total_revenue DESC LIMIT 15"
        }
    ]
    
    return {
        "examples": examples,
        "total_examples": len(examples),
        "usage_tips": [
            "All queries must start with SELECT",
            "Maximum query length is 2000 characters",
            "Maximum 1000 rows returned per query",
            "Only tables: dim_customer, dim_product, dim_date, fact_sales are accessible",
            "Comments (-- or /* */) are not allowed",
            "Use LIMIT to control result size"
        ]
    }