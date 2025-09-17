import pytest
from sqlalchemy.orm import Session
from app.models.star_schema import DimCustomer, DimProduct, DimDate, FactSales
from app.database import SessionLocal
from datetime import datetime, date

class TestORM:
    """Test SQLAlchemy ORM operations"""
    
    def test_create_customer(self, db_session: Session):
        """Test creating a customer"""
        customer = DimCustomer(
            customer_id=1,
            customer_name="John Doe",
            email="john@example.com",
            phone="123-456-7890",
            city="New York",
            state="NY",
            country="USA"
        )
        db_session.add(customer)
        db_session.commit()
        db_session.refresh(customer)
        
        assert customer.customer_id == 1
        assert customer.customer_name == "John Doe"
        assert customer.email == "john@example.com"
    
    def test_create_product(self, db_session: Session):
        """Test creating a product"""
        product = DimProduct(
            product_id=1,
            product_name="Test Product",
            category="Electronics",
            subcategory="Smartphones",
            brand="TestBrand",
            unit_price=299.99
        )
        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)
        
        # Check that product was created successfully
        retrieved_product = db_session.query(DimProduct).filter(DimProduct.product_id == 1).first()
        assert retrieved_product is not None
        assert retrieved_product.product_name == "Test Product"
        assert abs(retrieved_product.unit_price - 299.99) < 0.01
    
    def test_create_date(self, db_session: Session):
        """Test creating a date dimension"""
        test_date = date(2023, 1, 1)
        date_dim = DimDate(
            date_id=1,
            date=test_date,
            year=2023,
            quarter=1,
            month=1,
            month_name="January",
            week=1,
            day=1,
            day_name="Sunday",
            is_weekend=1
        )
        db_session.add(date_dim)
        db_session.commit()
        db_session.refresh(date_dim)
        
        assert date_dim.date_id == 1
        assert date_dim.year == 2023
        assert date_dim.month_name == "January"
    
    def test_create_sale_with_relationships(self, db_session: Session):
        """Test creating a sale with foreign key relationships"""
        # Create dimensions first
        customer = DimCustomer(
            customer_id=1,
            customer_name="Jane Doe",
            email="jane@example.com"
        )
        product = DimProduct(
            product_id=1,
            product_name="Test Product",
            category="Electronics",
            unit_price=199.99
        )
        date_dim = DimDate(
            date_id=1,
            date=date(2023, 1, 1),
            year=2023,
            quarter=1,
            month=1,
            month_name="January",
            week=1,
            day=1,
            day_name="Sunday",
            is_weekend=1
        )
        
        db_session.add_all([customer, product, date_dim])
        db_session.commit()
        
        # Create sale
        sale = FactSales(
            sale_id=1,
            customer_id=1,
            product_id=1,
            date_id=1,
            quantity=2,
            unit_price=199.99,
            total_amount=399.98,
            discount_amount=0.0,
            tax_amount=32.00
        )
        db_session.add(sale)
        db_session.commit()
        db_session.refresh(sale)
        
        # Check that sale was created successfully  
        retrieved_sale = db_session.query(FactSales).filter(FactSales.sale_id == 1).first()
        assert retrieved_sale is not None
        assert retrieved_sale.customer_id == 1
        assert retrieved_sale.product_id == 1
        assert abs(retrieved_sale.total_amount - 399.98) < 0.01
        
        # Test relationships
        assert sale.customer.customer_name == "Jane Doe"
        assert sale.product.product_name == "Test Product"
        assert sale.date.month_name == "January"
    
    def test_query_operations(self, db_session: Session):
        """Test various query operations"""
        # Create test data
        customers = [
            DimCustomer(customer_id=1, customer_name="Alice", email="alice@example.com"),
            DimCustomer(customer_id=2, customer_name="Bob", email="bob@example.com")
        ]
        db_session.add_all(customers)
        db_session.commit()
        
        # Test queries
        all_customers = db_session.query(DimCustomer).all()
        assert len(all_customers) == 2
        
        alice = db_session.query(DimCustomer).filter(DimCustomer.customer_name == "Alice").first()
        assert alice.email == "alice@example.com"
        
        customer_count = db_session.query(DimCustomer).count()
        assert customer_count == 2