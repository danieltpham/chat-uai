# DuckDB Analytics API

A comprehensive Python project featuring a FastAPI-based analytics API with DuckDB backend, implementing a star schema data warehouse with SQLAlchemy ORM.

## 🏗️ Architecture

This project implements a **star schema** data warehouse with:
- **3 Dimension Tables**: Customers, Products, Dates
- **1 Fact Table**: Sales transactions
- **FastAPI** REST API with full CRUD operations
- **DuckDB** as the analytical database
- **SQLAlchemy ORM** for all database interactions
- **Pydantic** models for request/response validation
- **Comprehensive pytest** test suite

## 📊 Star Schema Design

```
        DimCustomer         DimProduct         DimDate
        +-----------+       +-----------+      +-----------+
        | customer_id|       | product_id|      | date_id   |
        | name       |       | name      |      | date      |
        | email      |       | category  |      | year      |
        | city       |       | brand     |      | month     |
        | ...        |       | price     |      | quarter   |
        +-----------+       +-----------+      | ...       |
              |                   |            +-----------+
              |                   |                  |
              +-------------------+------------------+
                                  |
                            +-----------+
                            | FactSales |
                            +-----------+
                            | sale_id   |
                            | customer_id (FK)
                            | product_id (FK)
                            | date_id (FK)
                            | quantity  |
                            | total_amount
                            | discount  |
                            | tax       |
                            +-----------+
```

## 🚀 Features

### API Endpoints

#### Dimension Tables (CRUD Operations)
- **Customers**: `/api/v1/dimensions/customers`
  - GET, POST, PUT, DELETE operations
  - Customer management with contact information

- **Products**: `/api/v1/dimensions/products`
  - Full product catalog management
  - Category and pricing information

- **Dates**: `/api/v1/dimensions/dates`
  - Date dimension with calendar attributes
  - Weekend/weekday classification

#### Fact Tables
- **Sales**: `/api/v1/facts/sales`
  - Complete sales transaction management
  - Related data loading (customers, products, dates)
  - Sales filtering by customer/product

#### Analytics Endpoints
- **Sales by Category**: `/api/v1/analytics/sales-by-category`
  - Revenue analysis by product category
  - Quantity and average order value metrics

- **Monthly Sales**: `/api/v1/analytics/sales-by-month`
  - Time-series sales analysis
  - Monthly trends and patterns

- **Top Customers**: `/api/v1/analytics/top-customers`
  - Customer ranking by total sales
  - Purchase frequency analysis

- **Top Products**: `/api/v1/analytics/top-products`
  - Product performance ranking
  - Category-wise product analysis

- **Sales Summary**: `/api/v1/analytics/sales-summary`
  - Overall business metrics
  - Key performance indicators

- **Weekend vs Weekday**: `/api/v1/analytics/weekend-vs-weekday-sales`
  - Temporal sales pattern analysis

#### Custom SQL Endpoint
- **Execute SQL**: `/api/v1/sql?q=SELECT * FROM dim_customer LIMIT 10`
  - Execute custom SQL queries with security restrictions
  - **Security Features**:
    - Only SELECT statements allowed
    - Access limited to star schema tables only
    - No comments, multiple statements, or dangerous patterns
    - Query length limit (2000 characters)
    - Result limit (max 1000 rows)
    - SQL injection protection

- **Available Tables**: `/api/v1/sql/tables`
  - Get schema information for accessible tables
  - Column names, types, and constraints

- **SQL Examples**: `/api/v1/sql/examples`
  - Pre-built example queries for common analytics
  - Usage tips and best practices

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### 1. Clone and Setup
```bash
cd "d:\Nifinity\Personal Website 2025\chat-uai"
pip install -r requirements.txt
```

### 2. Install Dependencies
The project includes these key dependencies:
- `fastapi` - Modern web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - Python ORM
- `duckdb` - Analytical database
- `duckdb-engine` - SQLAlchemy DuckDB adapter
- `pydantic` - Data validation
- `pytest` - Testing framework
- `faker` - Test data generation

### 3. Run the Application
```bash
# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc`

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test files
pytest tests/test_api.py
pytest tests/test_orm.py
pytest tests/test_analytics.py

# Run with verbose output
pytest -v
```

### Test Coverage
- **ORM Tests**: Database operations and relationships
- **API Tests**: All endpoints with success/error cases
- **Analytics Tests**: Data aggregation and business logic
- **Integration Tests**: End-to-end workflows

## 📋 Project Structure

```
chat-uai/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── database.py          # DuckDB connection & setup
│   ├── models/
│   │   ├── __init__.py
│   │   └── star_schema.py   # SQLAlchemy ORM models
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic models
│   └── api/
│       ├── __init__.py
│       ├── dimensions.py    # Dimension CRUD endpoints
│       ├── facts.py         # Fact table endpoints
│       └── analytics.py     # Analytics endpoints
├── tests/
│   ├── conftest.py         # Pytest configuration
│   ├── test_orm.py         # ORM tests
│   ├── test_api.py         # API tests
│   └── test_analytics.py   # Analytics tests
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🎯 Sample Data

The application automatically generates sample data on startup:
- **100 customers** with realistic profile information
- **50 products** across 5 categories (Electronics, Clothing, Home & Garden, Sports, Books)
- **365 date records** (full year 2023)
- **1000 sales transactions** with realistic business relationships

## 📊 Analytics Examples

### Sales by Category
```json
{
  "data": [
    {
      "category": "Electronics",
      "total_sales": 125430.50,
      "total_quantity": 234,
      "average_order_value": 535.85
    }
  ],
  "total_categories": 5
}
```

### Monthly Sales Trends
```json
{
  "data": [
    {
      "year": 2023,
      "month": 1,
      "month_name": "January",
      "total_sales": 45230.75,
      "total_orders": 89,
      "total_quantity": 156
    }
  ],
  "total_months": 12
}
```

## 🔧 Configuration

### Database
- **Engine**: DuckDB (file-based: `analytics.db`)
- **Connection**: SQLAlchemy with DuckDB engine
- **Test DB**: In-memory DuckDB for testing

### API Settings
- **Host**: `0.0.0.0` (configurable)
- **Port**: `8000` (configurable)
- **Reload**: Enabled in development

## 🎉 Key Benefits

1. **Analytical Performance**: DuckDB optimized for OLAP workloads
2. **Type Safety**: Pydantic ensures data validation
3. **ORM Benefits**: SQLAlchemy provides database abstraction
4. **Star Schema**: Optimized for analytical queries
5. **Comprehensive Testing**: Full test coverage for reliability
6. **Modern API**: FastAPI with automatic documentation
7. **Scalable Architecture**: Clean separation of concerns

## 🚦 API Usage Examples

### Create a Customer
```bash
curl -X POST "http://localhost:8000/api/v1/dimensions/customers" \
     -H "Content-Type: application/json" \
     -d '{
       "customer_name": "John Doe",
       "email": "john@example.com",
       "city": "New York"
     }'
```

### Get Sales Analytics
```bash
curl "http://localhost:8000/api/v1/analytics/sales-by-category"
```

### Monthly Sales Report
```bash
curl "http://localhost:8000/api/v1/analytics/sales-by-month?year=2023"
```

### Execute Custom SQL Queries
```bash
# Simple query
curl "http://localhost:8000/api/v1/sql?q=SELECT * FROM dim_customer LIMIT 5"

# Analytics query
curl "http://localhost:8000/api/v1/sql?q=SELECT category, COUNT(*) FROM dim_product GROUP BY category"

# Complex join query
curl "http://localhost:8000/api/v1/sql?q=SELECT c.customer_name, SUM(f.total_amount) as total_sales FROM fact_sales f JOIN dim_customer c ON f.customer_id = c.customer_id GROUP BY c.customer_name ORDER BY total_sales DESC LIMIT 10"

# Get available tables and schemas
curl "http://localhost:8000/api/v1/sql/tables"

# Get example queries
curl "http://localhost:8000/api/v1/sql/examples"
```

This project demonstrates modern Python development practices with a focus on data analytics, type safety, and comprehensive testing.
Chat AI - the new way to do UI
