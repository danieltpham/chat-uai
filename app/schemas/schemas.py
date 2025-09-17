from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional

# Customer schemas
class CustomerBase(BaseModel):
    customer_name: str
    email: str
    phone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    customer_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None

class Customer(CustomerBase):
    customer_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Product schemas
class ProductBase(BaseModel):
    product_name: str
    category: Optional[str] = None
    subcategory: Optional[str] = None
    brand: Optional[str] = None
    unit_price: float

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    brand: Optional[str] = None
    unit_price: Optional[float] = None

class Product(ProductBase):
    product_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Date schemas
class DateBase(BaseModel):
    date: date
    year: int
    quarter: int
    month: int
    month_name: str
    week: int
    day: int
    day_name: str
    is_weekend: int

class DateCreate(DateBase):
    pass

class DateDimension(DateBase):
    date_id: int

    class Config:
        from_attributes = True

# Sales schemas
class SalesBase(BaseModel):
    customer_id: int
    product_id: int
    date_id: int
    quantity: int
    unit_price: float
    total_amount: float
    discount_amount: Optional[float] = 0.0
    tax_amount: Optional[float] = 0.0

class SalesCreate(SalesBase):
    pass

class SalesUpdate(BaseModel):
    customer_id: Optional[int] = None
    product_id: Optional[int] = None
    date_id: Optional[int] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None
    total_amount: Optional[float] = None
    discount_amount: Optional[float] = None
    tax_amount: Optional[float] = None

class Sales(SalesBase):
    sale_id: int
    created_at: datetime
    
    # Include related objects
    customer: Optional[Customer] = None
    product: Optional[Product] = None
    date: Optional[DateDimension] = None

    class Config:
        from_attributes = True

# Analytics response schemas
class SalesByCategory(BaseModel):
    category: str
    total_sales: float
    total_quantity: int
    average_order_value: float

class SalesByMonth(BaseModel):
    year: int
    month: int
    month_name: str
    total_sales: float
    total_orders: int
    total_quantity: int

class TopCustomer(BaseModel):
    customer_id: int
    customer_name: str
    total_sales: float
    total_orders: int

class TopProduct(BaseModel):
    product_id: int
    product_name: str
    category: str
    total_sales: float
    total_quantity: int

# Analytics response containers
class CategoryAnalytics(BaseModel):
    data: list[SalesByCategory]
    total_categories: int

class MonthlyAnalytics(BaseModel):
    data: list[SalesByMonth]
    total_months: int