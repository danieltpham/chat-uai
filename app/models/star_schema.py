from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship
from datetime import UTC
from datetime import datetime

Base = declarative_base()

class DimCustomer(Base):
    """Customer dimension table"""
    __tablename__ = "dim_customer"
    
    customer_id = Column(Integer, primary_key=True, autoincrement=False, index=True)
    customer_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    city = Column(String(50))
    state = Column(String(50))
    country = Column(String(50))
    created_at = Column(DateTime, default=datetime.now(UTC))
    
    # Relationship to fact table
    sales = relationship("FactSales", back_populates="customer")

class DimProduct(Base):
    """Product dimension table"""
    __tablename__ = "dim_product"
    
    product_id = Column(Integer, primary_key=True, autoincrement=False, index=True)
    product_name = Column(String(100), nullable=False)
    category = Column(String(50))
    subcategory = Column(String(50))
    brand = Column(String(50))
    unit_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC))
    
    # Relationship to fact table
    sales = relationship("FactSales", back_populates="product")

class DimDate(Base):
    """Date dimension table"""
    __tablename__ = "dim_date"
    
    date_id = Column(Integer, primary_key=True, autoincrement=False, index=True)
    date = Column(Date, nullable=False, unique=True)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    month_name = Column(String(20), nullable=False)
    week = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    day_name = Column(String(20), nullable=False)
    is_weekend = Column(Integer, default=0)  # 0 = False, 1 = True
    
    # Relationship to fact table
    sales = relationship("FactSales", back_populates="date")

class FactSales(Base):
    """Sales fact table"""
    __tablename__ = "fact_sales"
    
    sale_id = Column(Integer, primary_key=True, autoincrement=False, index=True)
    customer_id = Column(Integer, ForeignKey("dim_customer.customer_id"), nullable=False)
    product_id = Column(Integer, ForeignKey("dim_product.product_id"), nullable=False)
    date_id = Column(Integer, ForeignKey("dim_date.date_id"), nullable=False)
    
    # Measures
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    discount_amount = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.now(UTC))
    
    # Relationships
    customer = relationship("DimCustomer", back_populates="sales")
    product = relationship("DimProduct", back_populates="sales")
    date = relationship("DimDate", back_populates="sales")