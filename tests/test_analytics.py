import pytest
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.star_schema import DimCustomer, DimProduct, DimDate, FactSales
from datetime import date

class TestAnalytics:
    """Test analytics and aggregation functions"""
    
    def setup_test_data(self, db_session: Session):
        """Setup test data for analytics tests"""
        # Create customers
        customers = [
            DimCustomer(customer_id=1, customer_name="Alice", email="alice@test.com"),
            DimCustomer(customer_id=2, customer_name="Bob", email="bob@test.com")
        ]
        
        # Create products
        products = [
            DimProduct(product_id=1, product_name="Phone", category="Electronics", unit_price=500.0),
            DimProduct(product_id=2, product_name="Shirt", category="Clothing", unit_price=50.0),
            DimProduct(product_id=3, product_name="Laptop", category="Electronics", unit_price=1000.0)
        ]
        
        # Create dates
        dates = [
            DimDate(date_id=1, date=date(2023, 1, 15), year=2023, quarter=1, month=1, 
                   month_name="January", week=3, day=15, day_name="Sunday", is_weekend=1),
            DimDate(date_id=2, date=date(2023, 2, 10), year=2023, quarter=1, month=2, 
                   month_name="February", week=6, day=10, day_name="Friday", is_weekend=0)
        ]
        
        db_session.add_all(customers + products + dates)
        db_session.commit()
        
        # Create sales
        sales = [
            FactSales(sale_id=1, customer_id=1, product_id=1, date_id=1, 
                     quantity=1, unit_price=500.0, total_amount=500.0),
            FactSales(sale_id=2, customer_id=2, product_id=2, date_id=1, 
                     quantity=2, unit_price=50.0, total_amount=100.0),
            FactSales(sale_id=3, customer_id=1, product_id=3, date_id=2, 
                     quantity=1, unit_price=1000.0, total_amount=1000.0)
        ]
        
        db_session.add_all(sales)
        db_session.commit()
    
    def test_sales_by_category_aggregation(self, db_session: Session):
        """Test sales aggregation by category"""
        self.setup_test_data(db_session)
        
        results = db_session.query(
            DimProduct.category,
            func.sum(FactSales.total_amount).label('total_sales'),
            func.sum(FactSales.quantity).label('total_quantity')
        ).join(
            DimProduct, FactSales.product_id == DimProduct.product_id
        ).group_by(
            DimProduct.category
        ).all()
        
        # Convert to dict for easier testing
        category_sales = {row.category: (float(row.total_sales), int(row.total_quantity)) for row in results}
        
        assert "Electronics" in category_sales
        assert "Clothing" in category_sales
        assert category_sales["Electronics"][0] == 1500.0  # Phone + Laptop
        assert category_sales["Clothing"][0] == 100.0  # Shirt
        assert category_sales["Electronics"][1] == 2  # Phone + Laptop quantities
        assert category_sales["Clothing"][1] == 2  # Shirt quantity
    
    def test_sales_by_customer_aggregation(self, db_session: Session):
        """Test sales aggregation by customer"""
        self.setup_test_data(db_session)
        
        results = db_session.query(
            DimCustomer.customer_name,
            func.sum(FactSales.total_amount).label('total_sales'),
            func.count(FactSales.sale_id).label('total_orders')
        ).join(
            DimCustomer, FactSales.customer_id == DimCustomer.customer_id
        ).group_by(
            DimCustomer.customer_name
        ).all()
        
        customer_sales = {row.customer_name: (float(row.total_sales), int(row.total_orders)) for row in results}
        
        assert "Alice" in customer_sales
        assert "Bob" in customer_sales
        assert customer_sales["Alice"][0] == 1500.0  # Phone + Laptop
        assert customer_sales["Bob"][0] == 100.0  # Shirt
        assert customer_sales["Alice"][1] == 2  # 2 orders
        assert customer_sales["Bob"][1] == 1  # 1 order
    
    def test_monthly_sales_aggregation(self, db_session: Session):
        """Test monthly sales aggregation"""
        self.setup_test_data(db_session)
        
        results = db_session.query(
            DimDate.month_name,
            func.sum(FactSales.total_amount).label('total_sales'),
            func.count(FactSales.sale_id).label('total_orders')
        ).join(
            DimDate, FactSales.date_id == DimDate.date_id
        ).group_by(
            DimDate.month_name
        ).all()
        
        monthly_sales = {row.month_name: (float(row.total_sales), int(row.total_orders)) for row in results}
        
        assert "January" in monthly_sales
        assert "February" in monthly_sales
        assert monthly_sales["January"][0] == 600.0  # Phone + Shirt
        assert monthly_sales["February"][0] == 1000.0  # Laptop
        assert monthly_sales["January"][1] == 2  # 2 orders
        assert monthly_sales["February"][1] == 1  # 1 order
    
    def test_weekend_vs_weekday_analysis(self, db_session: Session):
        """Test weekend vs weekday sales analysis"""
        self.setup_test_data(db_session)
        
        results = db_session.query(
            DimDate.is_weekend,
            func.sum(FactSales.total_amount).label('total_sales'),
            func.count(FactSales.sale_id).label('total_orders')
        ).join(
            DimDate, FactSales.date_id == DimDate.date_id
        ).group_by(
            DimDate.is_weekend
        ).all()
        
        weekend_data = {}
        for row in results:
            period = "weekend" if row.is_weekend == 1 else "weekday"
            weekend_data[period] = (float(row.total_sales), int(row.total_orders))
        
        assert "weekend" in weekend_data or "weekday" in weekend_data
        if "weekend" in weekend_data:
            assert weekend_data["weekend"][0] == 600.0  # January sales (weekend)
        if "weekday" in weekend_data:
            assert weekend_data["weekday"][0] == 1000.0  # February sales (weekday)
    
    def test_top_products_by_sales(self, db_session: Session):
        """Test finding top products by sales"""
        self.setup_test_data(db_session)
        
        results = db_session.query(
            DimProduct.product_name,
            func.sum(FactSales.total_amount).label('total_sales')
        ).join(
            DimProduct, FactSales.product_id == DimProduct.product_id
        ).group_by(
            DimProduct.product_name
        ).order_by(
            func.sum(FactSales.total_amount).desc()
        ).limit(3).all()
        
        # Top product should be Laptop with 1000.0 sales
        assert results[0].product_name == "Laptop"
        assert float(results[0].total_sales) == 1000.0
        
        # Second should be Phone with 500.0 sales
        assert results[1].product_name == "Phone"
        assert float(results[1].total_sales) == 500.0
    
    def test_overall_statistics(self, db_session: Session):
        """Test calculation of overall statistics"""
        self.setup_test_data(db_session)
        
        # Total sales
        total_sales = db_session.query(func.sum(FactSales.total_amount)).scalar()
        assert float(total_sales) == 1600.0
        
        # Total orders
        total_orders = db_session.query(func.count(FactSales.sale_id)).scalar()
        assert int(total_orders) == 3
        
        # Average order value
        avg_order_value = db_session.query(func.avg(FactSales.total_amount)).scalar()
        assert abs(float(avg_order_value) - 533.33) < 0.01  # 1600/3 ≈ 533.33
        
        # Total customers
        total_customers = db_session.query(func.count(DimCustomer.customer_id)).scalar()
        assert int(total_customers) == 2
        
        # Total products
        total_products = db_session.query(func.count(DimProduct.product_id)).scalar()
        assert int(total_products) == 3