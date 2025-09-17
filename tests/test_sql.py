import pytest
import httpx
from urllib.parse import quote

class TestSQLEndpoint:
    """Test the custom SQL endpoint with security measures"""
    
    def test_valid_select_query(self, client: httpx.Client):
        """Test a valid SELECT query"""
        query = "SELECT * FROM dim_customer LIMIT 5"
        response = client.get(f"/api/v1/sql?q={query}")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "columns" in data
        assert "query" in data
        assert data["status"] == "success"
        assert len(data["data"]) <= 5
    
    def test_forbidden_insert_query(self, client: httpx.Client):
        """Test that INSERT queries are blocked"""
        query = "INSERT INTO dim_customer (customer_name, email) VALUES ('Test', 'test@example.com')"
        response = client.get(f"/api/v1/sql?q={query}")
        assert response.status_code == 400
        assert "Forbidden keyword 'INSERT'" in response.json()["detail"]
    
    def test_forbidden_update_query(self, client: httpx.Client):
        """Test that UPDATE queries are blocked"""
        query = "UPDATE dim_customer SET customer_name = 'Hacked' WHERE customer_id = 1"
        response = client.get(f"/api/v1/sql?q={query}")
        assert response.status_code == 400
        assert "Forbidden keyword 'UPDATE'" in response.json()["detail"]
    
    def test_forbidden_delete_query(self, client: httpx.Client):
        """Test that DELETE queries are blocked"""
        query = "DELETE FROM dim_customer WHERE customer_id = 1"
        response = client.get(f"/api/v1/sql?q={query}")
        assert response.status_code == 400
        assert "Forbidden keyword 'DELETE'" in response.json()["detail"]
    
    def test_forbidden_drop_query(self, client: httpx.Client):
        """Test that DROP queries are blocked"""
        query = "DROP TABLE dim_customer"
        response = client.get(f"/api/v1/sql?q={query}")
        assert response.status_code == 400
        assert "Forbidden keyword 'DROP'" in response.json()["detail"]
    
    def test_sql_comments_blocked(self, client: httpx.Client):
        """Test that SQL comments are blocked"""
        query = "SELECT * FROM dim_customer -- WHERE customer_id = 1"
        response = client.get(f"/api/v1/sql?q={query}")
        assert response.status_code == 400
        assert "dangerous SQL pattern" in response.json()["detail"]
    
    def test_multiple_statements_blocked(self, client: httpx.Client):
        """Test that multiple statements are blocked"""
        query = "SELECT * FROM dim_customer; DROP TABLE dim_customer"
        response = client.get(f"/api/v1/sql?q={query}")
        assert response.status_code == 400
        assert "Forbidden keyword 'DROP' detected" in response.json()["detail"]
    
    def test_non_select_start_blocked(self, client: httpx.Client):
        """Test that queries not starting with SELECT are blocked"""
        query = "EXPLAIN SELECT * FROM dim_customer" 
        response = client.get(f"/api/v1/sql?q={query}")
        assert response.status_code == 400
        assert "Forbidden keyword 'EXPLAIN' detected" in response.json()["detail"]
    
    def test_invalid_table_access(self, client: httpx.Client):
        """Test that access to non-allowed tables is blocked"""
        query = "SELECT * FROM information_schema.tables"
        response = client.get(f"/api/v1/sql?q={query}")
        assert response.status_code == 400
        assert "not allowed" in response.json()["detail"]
    
    def test_empty_query(self, client: httpx.Client):
        """Test that empty queries are rejected"""
        response = client.get("/api/v1/sql?q=")
        assert response.status_code == 400
        assert "cannot be empty" in response.json()["detail"]
    
    def test_query_length_limit(self, client: httpx.Client):
        """Test that overly long queries are rejected"""
        long_query = "SELECT * FROM dim_customer WHERE customer_name = '" + "x" * 2000 + "'"
        response = client.get(f"/api/v1/sql?q={long_query}")
        assert response.status_code == 400
        assert "too long" in response.json()["detail"]
    
    def test_limit_enforcement(self, client: httpx.Client):
        """Test that LIMIT is enforced"""
        query = "SELECT * FROM dim_customer"
        response = client.get(f"/api/v1/sql?q={query}&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert "LIMIT 10" in data["query"] or len(data["data"]) <= 10
    
    def test_aggregation_query(self, client: httpx.Client):
        """Test a valid aggregation query"""
        query = "SELECT category, COUNT(*) as count FROM dim_product GROUP BY category"
        response = client.get(f"/api/v1/sql?q={query}")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["columns"]) == 2  # category and count
    
    def test_join_query(self, client: httpx.Client):
        """Test a valid JOIN query"""
        query = "SELECT c.customer_name, COUNT(f.sale_id) as order_count FROM dim_customer c LEFT JOIN fact_sales f ON c.customer_id = f.customer_id GROUP BY c.customer_name LIMIT 5"
        from urllib.parse import quote
        response = client.get(f"/api/v1/sql?q={quote(query)}")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert len(data["data"]) <= 5
    
    def test_get_available_tables(self, client: httpx.Client):
        """Test the tables information endpoint"""
        response = client.get("/api/v1/sql/tables")
        assert response.status_code == 200
        data = response.json()
        assert "available_tables" in data
        assert "table_schemas" in data
        expected_tables = {"dim_customer", "dim_product", "dim_date", "fact_sales"}
        assert set(data["available_tables"]) == expected_tables
    
    def test_get_sql_examples(self, client: httpx.Client):
        """Test the SQL examples endpoint"""
        response = client.get("/api/v1/sql/examples")
        assert response.status_code == 200
        data = response.json()
        assert "examples" in data
        assert "usage_tips" in data
        assert len(data["examples"]) > 0
        
        # Check that all examples are valid
        for example in data["examples"]:
            assert "title" in example
            assert "description" in example
            assert "query" in example
            assert example["query"].upper().strip().startswith("SELECT")
    
    def test_case_insensitive_keywords(self, client: httpx.Client):
        """Test that keyword detection is case insensitive"""
        query = "select * from dim_customer limit 5"  # lowercase
        response = client.get(f"/api/v1/sql?q={query}")
        assert response.status_code == 200
        
        # Test forbidden keyword in lowercase
        bad_query = "select * from dim_customer; drop table dim_customer"
        response = client.get(f"/api/v1/sql?q={bad_query}")
        assert response.status_code == 400
