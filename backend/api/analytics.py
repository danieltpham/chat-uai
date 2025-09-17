from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from backend.database import get_db
from backend.models.star_schema import FactSales, DimCustomer, DimProduct, DimDate
from backend.schemas.schemas import CategoryAnalytics, MonthlyAnalytics, SalesByCategory, SalesByMonth

router = APIRouter()

@router.get("/sales-by-category", response_model=CategoryAnalytics)
def get_sales_by_category(db: Session = Depends(get_db)):
    """Analytics: Get sales performance by product category"""
    
    results = db.query(
        DimProduct.category,
        func.sum(FactSales.total_amount).label('total_sales'),
        func.sum(FactSales.quantity).label('total_quantity'),
        func.avg(FactSales.total_amount).label('average_order_value')
    ).join(
        DimProduct, FactSales.product_id == DimProduct.product_id
    ).group_by(
        DimProduct.category
    ).order_by(
        func.sum(FactSales.total_amount).desc()
    ).all()
    
    sales_data = []
    for row in results:
        sales_data.append(SalesByCategory(
            category=row.category,
            total_sales=float(row.total_sales),
            total_quantity=int(row.total_quantity),
            average_order_value=float(row.average_order_value)
        ))
    
    return CategoryAnalytics(
        data=sales_data,
        total_categories=len(sales_data)
    )

@router.get("/sales-by-month", response_model=MonthlyAnalytics)
def get_sales_by_month(year: int = 2023, db: Session = Depends(get_db)):
    """Analytics: Get monthly sales performance for a given year"""
    
    results = db.query(
        DimDate.year,
        DimDate.month,
        DimDate.month_name,
        func.sum(FactSales.total_amount).label('total_sales'),
        func.count(FactSales.sale_id).label('total_orders'),
        func.sum(FactSales.quantity).label('total_quantity')
    ).join(
        DimDate, FactSales.date_id == DimDate.date_id
    ).filter(
        DimDate.year == year
    ).group_by(
        DimDate.year,
        DimDate.month,
        DimDate.month_name
    ).order_by(
        DimDate.month
    ).all()
    
    monthly_data = []
    for row in results:
        monthly_data.append(SalesByMonth(
            year=row.year,
            month=row.month,
            month_name=row.month_name,
            total_sales=float(row.total_sales),
            total_orders=int(row.total_orders),
            total_quantity=int(row.total_quantity)
        ))
    
    return MonthlyAnalytics(
        data=monthly_data,
        total_months=len(monthly_data)
    )

@router.get("/top-customers")
def get_top_customers(limit: int = 10, db: Session = Depends(get_db)):
    """Analytics: Get top customers by total sales"""
    
    results = db.query(
        DimCustomer.customer_id,
        DimCustomer.customer_name,
        func.sum(FactSales.total_amount).label('total_sales'),
        func.count(FactSales.sale_id).label('total_orders')
    ).join(
        DimCustomer, FactSales.customer_id == DimCustomer.customer_id
    ).group_by(
        DimCustomer.customer_id,
        DimCustomer.customer_name
    ).order_by(
        func.sum(FactSales.total_amount).desc()
    ).limit(limit).all()
    
    top_customers = []
    for row in results:
        top_customers.append({
            "customer_id": row.customer_id,
            "customer_name": row.customer_name,
            "total_sales": float(row.total_sales),
            "total_orders": int(row.total_orders)
        })
    
    return {
        "data": top_customers,
        "total_customers": len(top_customers),
        "limit": limit
    }

@router.get("/top-products")
def get_top_products(limit: int = 10, db: Session = Depends(get_db)):
    """Analytics: Get top products by total sales"""
    
    results = db.query(
        DimProduct.product_id,
        DimProduct.product_name,
        DimProduct.category,
        func.sum(FactSales.total_amount).label('total_sales'),
        func.sum(FactSales.quantity).label('total_quantity')
    ).join(
        DimProduct, FactSales.product_id == DimProduct.product_id
    ).group_by(
        DimProduct.product_id,
        DimProduct.product_name,
        DimProduct.category
    ).order_by(
        func.sum(FactSales.total_amount).desc()
    ).limit(limit).all()
    
    top_products = []
    for row in results:
        top_products.append({
            "product_id": row.product_id,
            "product_name": row.product_name,
            "category": row.category,
            "total_sales": float(row.total_sales),
            "total_quantity": int(row.total_quantity)
        })
    
    return {
        "data": top_products,
        "total_products": len(top_products),
        "limit": limit
    }

@router.get("/weekend-vs-weekday-sales")
def get_weekend_vs_weekday_sales(db: Session = Depends(get_db)):
    """Analytics: Compare weekend vs weekday sales performance"""
    
    results = db.query(
        DimDate.is_weekend,
        func.sum(FactSales.total_amount).label('total_sales'),
        func.count(FactSales.sale_id).label('total_orders'),
        func.avg(FactSales.total_amount).label('average_order_value')
    ).join(
        DimDate, FactSales.date_id == DimDate.date_id
    ).group_by(
        DimDate.is_weekend
    ).all()
    
    weekend_weekday_data = []
    for row in results:
        period = "Weekend" if row.is_weekend == 1 else "Weekday"
        weekend_weekday_data.append({
            "period": period,
            "total_sales": float(row.total_sales),
            "total_orders": int(row.total_orders),
            "average_order_value": float(row.average_order_value)
        })
    
    return {
        "data": weekend_weekday_data,
        "analysis": "Comparison of sales performance between weekends and weekdays"
    }

@router.get("/sales-summary")
def get_sales_summary(db: Session = Depends(get_db)):
    """Analytics: Get overall sales summary statistics"""
    
    # Overall totals
    total_sales = db.query(func.sum(FactSales.total_amount)).scalar()
    total_orders = db.query(func.count(FactSales.sale_id)).scalar()
    total_quantity = db.query(func.sum(FactSales.quantity)).scalar()
    
    # Average order value
    avg_order_value = db.query(func.avg(FactSales.total_amount)).scalar()
    
    # Total customers and products
    total_customers = db.query(func.count(DimCustomer.customer_id)).scalar()
    total_products = db.query(func.count(DimProduct.product_id)).scalar()
    
    # Best selling category
    best_category = db.query(
        DimProduct.category,
        func.sum(FactSales.total_amount).label('total_sales')
    ).join(
        DimProduct, FactSales.product_id == DimProduct.product_id
    ).group_by(
        DimProduct.category
    ).order_by(
        func.sum(FactSales.total_amount).desc()
    ).first()
    
    return {
        "total_sales": float(total_sales) if total_sales else 0,
        "total_orders": int(total_orders) if total_orders else 0,
        "total_quantity": int(total_quantity) if total_quantity else 0,
        "average_order_value": float(avg_order_value) if avg_order_value else 0,
        "total_customers": int(total_customers) if total_customers else 0,
        "total_products": int(total_products) if total_products else 0,
        "best_selling_category": {
            "category": best_category.category if best_category else None,
            "total_sales": float(best_category.total_sales) if best_category else 0
        }
    }