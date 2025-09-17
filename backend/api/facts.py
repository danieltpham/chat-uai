from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from backend.database import get_db
from backend.models.star_schema import FactSales
from backend.schemas.schemas import Sales, SalesCreate, SalesUpdate

router = APIRouter()

@router.get("/sales", response_model=List[Sales])
def get_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all sales with pagination and related data"""
    sales = db.query(FactSales)\
              .options(joinedload(FactSales.customer), 
                      joinedload(FactSales.product), 
                      joinedload(FactSales.date))\
              .offset(skip).limit(limit).all()
    return sales

@router.get("/sales/{sale_id}", response_model=Sales)
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    """Get a specific sale by ID"""
    sale = db.query(FactSales)\
             .options(joinedload(FactSales.customer), 
                     joinedload(FactSales.product), 
                     joinedload(FactSales.date))\
             .filter(FactSales.sale_id == sale_id).first()
    if sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale

@router.post("/sales", response_model=Sales)
def create_sale(sale: SalesCreate, db: Session = Depends(get_db)):
    """Create a new sale"""
    # Get the next sale_id
    max_id = db.query(FactSales).order_by(FactSales.sale_id.desc()).first()
    next_id = (max_id.sale_id + 1) if max_id else 1
    
    db_sale = FactSales(sale_id=next_id, **sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    
    # Reload with relationships
    return db.query(FactSales)\
             .options(joinedload(FactSales.customer), 
                     joinedload(FactSales.product), 
                     joinedload(FactSales.date))\
             .filter(FactSales.sale_id == db_sale.sale_id).first()

@router.put("/sales/{sale_id}", response_model=Sales)
def update_sale(sale_id: int, sale: SalesUpdate, db: Session = Depends(get_db)):
    """Update a sale"""
    db_sale = db.query(FactSales).filter(FactSales.sale_id == sale_id).first()
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    update_data = sale.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_sale, field, value)
    
    db.commit()
    db.refresh(db_sale)
    
    # Reload with relationships
    return db.query(FactSales)\
             .options(joinedload(FactSales.customer), 
                     joinedload(FactSales.product), 
                     joinedload(FactSales.date))\
             .filter(FactSales.sale_id == sale_id).first()

@router.delete("/sales/{sale_id}")
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    """Delete a sale"""
    db_sale = db.query(FactSales).filter(FactSales.sale_id == sale_id).first()
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    db.delete(db_sale)
    db.commit()
    return {"message": "Sale deleted successfully"}

@router.get("/sales/by-customer/{customer_id}", response_model=List[Sales])
def get_sales_by_customer(customer_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all sales for a specific customer"""
    sales = db.query(FactSales)\
              .options(joinedload(FactSales.customer), 
                      joinedload(FactSales.product), 
                      joinedload(FactSales.date))\
              .filter(FactSales.customer_id == customer_id)\
              .offset(skip).limit(limit).all()
    return sales

@router.get("/sales/by-product/{product_id}", response_model=List[Sales])
def get_sales_by_product(product_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all sales for a specific product"""
    sales = db.query(FactSales)\
              .options(joinedload(FactSales.customer), 
                      joinedload(FactSales.product), 
                      joinedload(FactSales.date))\
              .filter(FactSales.product_id == product_id)\
              .offset(skip).limit(limit).all()
    return sales