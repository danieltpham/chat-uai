import pytest
import httpx

class TestAPI:
    """Test FastAPI endpoints via integration tests"""
    
    def test_root_endpoint(self, client: httpx.Client):
        """Test the root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "DuckDB Analytics API"
        assert data["version"] == "1.0.0"
    
    def test_health_endpoint(self, client: httpx.Client):
        """Test the health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_create_customer(self, client: httpx.Client):
        """Test creating a customer via API"""
        import time
        import random
        
        # Use unique email to avoid conflicts
        unique_id = int(time.time() * 1000) + random.randint(1, 999)
        customer_data = {
            "customer_name": f"Test Customer {unique_id}",
            "email": f"test{unique_id}@example.com",
            "phone": "123-456-7890",
            "city": "Test City",
            "state": "TS",
            "country": "Test Country"
        }
        response = client.post("/api/v1/dimensions/customers", json=customer_data)
        
        # Add debugging for 500 errors
        if response.status_code == 500:
            print(f"Server error response: {response.text}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["customer_name"] == f"Test Customer {unique_id}"
        assert data["email"] == f"test{unique_id}@example.com"
        assert "customer_id" in data
        assert "created_at" in data
    
    def test_get_customers(self, retry_client):
        """Test getting customers list"""
        import time
        import random
        
        # Use unique data to avoid conflicts
        unique_id = int(time.time() * 1000) + random.randint(1, 999)
        customer_data = {
            "customer_name": f"Test Customer {unique_id}",
            "email": f"test{unique_id}@example.com"
        }
        
        # Create customer with retry logic
        create_response = retry_client.post("/api/v1/dimensions/customers", json=customer_data)
        assert create_response.status_code == 200
        
        # Then get the list with retry logic
        response = retry_client.get("/api/v1/dimensions/customers")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    def test_create_product(self, client: httpx.Client):
        """Test creating a product via API"""
        product_data = {
            "product_name": "Test Product",
            "category": "Electronics",
            "subcategory": "Smartphones",
            "brand": "TestBrand",
            "unit_price": 299.99
        }
        response = client.post("/api/v1/dimensions/products", json=product_data)
        assert response.status_code == 200
        data = response.json()
        assert data["product_name"] == "Test Product"
        assert abs(data["unit_price"] - 299.99) < 0.01  # Allow for floating point precision
        assert "product_id" in data
    
    def test_get_products(self, client: httpx.Client):
        """Test getting products list"""
        response = client.get("/api/v1/dimensions/products")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_create_sale(self, client: httpx.Client):
        """Test creating a sale via API"""
        import time
        import random
        
        # Use unique identifiers to avoid conflicts
        unique_id = int(time.time() * 1000) + random.randint(1, 999)
        
        # First create necessary dimensions with unique data
        customer_data = {
            "customer_name": f"Sale Customer {unique_id}", 
            "email": f"sale{unique_id}@example.com"
        }
        customer_response = client.post("/api/v1/dimensions/customers", json=customer_data)
        
        if customer_response.status_code != 200:
            print(f"Customer creation failed: {customer_response.text}")
        assert customer_response.status_code == 200
        customer_id = customer_response.json()["customer_id"]
        
        product_data = {
            "product_name": f"Sale Product {unique_id}", 
            "category": "Test", 
            "unit_price": 100.0
        }
        product_response = client.post("/api/v1/dimensions/products", json=product_data)
        
        if product_response.status_code != 200:
            print(f"Product creation failed: {product_response.text}")
        assert product_response.status_code == 200
        product_id = product_response.json()["product_id"]
        
        # Get a date_id (assuming date dimension exists)
        dates_response = client.get("/api/v1/dimensions/dates?limit=1")
        if dates_response.status_code == 200 and dates_response.json():
            date_id = dates_response.json()[0]["date_id"]
        else:
            date_id = 1  # fallback
        
        sale_data = {
            "customer_id": customer_id,
            "product_id": product_id,
            "date_id": date_id,
            "quantity": 2,
            "unit_price": 100.0,
            "total_amount": 200.0
        }
        response = client.post("/api/v1/facts/sales", json=sale_data)
        
        if response.status_code != 200:
            print(f"Sale creation failed: {response.text}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["quantity"] == 2
        assert abs(data["total_amount"] - 200.0) < 0.01
        assert "sale_id" in data
    
    def test_get_sales(self, client: httpx.Client):
        """Test getting sales list"""
        response = client.get("/api/v1/facts/sales")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_analytics_sales_by_category(self, client: httpx.Client):
        """Test analytics endpoint for sales by category"""
        response = client.get("/api/v1/analytics/sales-by-category")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "total_categories" in data
        assert isinstance(data["data"], list)
    
    def test_analytics_sales_by_month(self, client: httpx.Client):
        """Test analytics endpoint for sales by month"""
        response = client.get("/api/v1/analytics/sales-by-month?year=2023")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "total_months" in data
        assert isinstance(data["data"], list)
    
    def test_analytics_top_customers(self, client: httpx.Client):
        """Test analytics endpoint for top customers"""
        response = client.get("/api/v1/analytics/top-customers?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
    
    def test_analytics_top_products(self, client: httpx.Client):
        """Test analytics endpoint for top products"""
        response = client.get("/api/v1/analytics/top-products?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
    
    def test_analytics_sales_summary(self, client: httpx.Client):
        """Test analytics endpoint for sales summary"""
        response = client.get("/api/v1/analytics/sales-summary")
        assert response.status_code == 200
        data = response.json()
        assert "total_sales" in data
        assert "total_orders" in data
        assert "total_customers" in data
        assert "best_selling_category" in data
    
    def test_customer_not_found(self, client: httpx.Client):
        """Test 404 error for non-existent customer"""
        response = client.get("/api/v1/dimensions/customers/99999")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Customer not found"
    
    def test_product_not_found(self, client: httpx.Client):
        """Test 404 error for non-existent product"""
        response = client.get("/api/v1/dimensions/products/99999")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Product not found"
    
    def test_update_customer(self, retry_client):
        """Test updating a customer"""
        import time
        import random
        
        # Use unique data to avoid conflicts
        unique_id = int(time.time() * 1000) + random.randint(1, 999)
        
        # Create a customer first with retry logic
        customer_data = {
            "customer_name": f"Update Test {unique_id}", 
            "email": f"update{unique_id}@example.com"
        }
        create_response = retry_client.post("/api/v1/dimensions/customers", json=customer_data)
        assert create_response.status_code == 200
        customer_id = create_response.json()["customer_id"]
        
        # Update the customer with retry logic
        update_data = {"customer_name": f"Updated Name {unique_id}", "city": "New City"}
        response = retry_client.put(f"/api/v1/dimensions/customers/{customer_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["customer_name"] == f"Updated Name {unique_id}"
        assert data["city"] == "New City"
        assert data["email"] == f"update{unique_id}@example.com"  # Should remain unchanged
    
    def test_delete_customer(self, client: httpx.Client):
        """Test deleting a customer"""
        # Create a customer first
        customer_data = {"customer_name": "Delete Test", "email": "delete@example.com"}
        create_response = client.post("/api/v1/dimensions/customers", json=customer_data)
        customer_id = create_response.json()["customer_id"]
        
        # Delete the customer
        response = client.delete(f"/api/v1/dimensions/customers/{customer_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Customer deleted successfully"
        
        # Verify customer is deleted
        get_response = client.get(f"/api/v1/dimensions/customers/{customer_id}")
        assert get_response.status_code == 404
