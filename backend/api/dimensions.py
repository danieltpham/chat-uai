from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models.star_schema import DimCustomer, DimProduct, DimDate
from backend.schemas.schemas import Customer, CustomerCreate, CustomerUpdate, Product, ProductCreate, ProductUpdate, DateDimension

router = APIRouter()

# Customer dimension routes
@router.get("/customers", response_model=List[Customer])
def get_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all customers with pagination"""
    customers = db.query(DimCustomer).offset(skip).limit(limit).all()
    return customers

@router.get("/customers/{customer_id}", response_model=Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """Get a specific customer by ID"""
    customer = db.query(DimCustomer).filter(DimCustomer.customer_id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.post("/customers", response_model=Customer)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """Create a new customer"""
    # Get the next customer_id
    max_id = db.query(DimCustomer).order_by(DimCustomer.customer_id.desc()).first()
    next_id = (max_id.customer_id + 1) if max_id else 1
    
    db_customer = DimCustomer(customer_id=next_id, **customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.put("/customers/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    """Update a customer"""
    db_customer = db.query(DimCustomer).filter(DimCustomer.customer_id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    update_data = customer.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_customer, field, value)
    
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """Delete a customer"""
    db_customer = db.query(DimCustomer).filter(DimCustomer.customer_id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db.delete(db_customer)
    db.commit()
    return {"message": "Customer deleted successfully"}

# Product dimension routes
@router.get("/products", response_model=List[Product])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all products with pagination"""
    products = db.query(DimProduct).offset(skip).limit(limit).all()
    return products

@router.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID"""
    product = db.query(DimProduct).filter(DimProduct.product_id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/products", response_model=Product)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product"""
    # Get the next product_id
    max_id = db.query(DimProduct).order_by(DimProduct.product_id.desc()).first()
    next_id = (max_id.product_id + 1) if max_id else 1
    
    db_product = DimProduct(product_id=next_id, **product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    """Update a product"""
    db_product = db.query(DimProduct).filter(DimProduct.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product"""
    db_product = db.query(DimProduct).filter(DimProduct.product_id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}

# Date dimension routes
@router.get("/dates", response_model=List[DateDimension])
def get_dates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all dates with pagination"""
    dates = db.query(DimDate).offset(skip).limit(limit).all()
    return dates

@router.get("/dates/{date_id}", response_model=DateDimension)
def get_date(date_id: int, db: Session = Depends(get_db)):
    """Get a specific date by ID"""
    date_record = db.query(DimDate).filter(DimDate.date_id == date_id).first()
    if date_record is None:
        raise HTTPException(status_code=404, detail="Date not found")
    return date_record