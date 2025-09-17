from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.models.star_schema import Base, DimCustomer, DimProduct, DimDate, FactSales
from faker import Faker
from datetime import datetime, date, timedelta
import random

# DuckDB connection string
DATABASE_URL = "duckdb:///analytics.db"

# Create DuckDB engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def populate_sample_data():
    """Populate the database with sample data"""
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(DimCustomer).count() > 0:
            print("Sample data already exists, skipping population.")
            return
        
        fake = Faker()
        print("Populating sample data...")
        
        # Create date dimension data (1 year of dates)
        start_date = date(2023, 1, 1)
        end_date = date(2023, 12, 31)
        
        date_records = []
        current_date = start_date
        date_id = 1
        
        while current_date <= end_date:
            date_record = DimDate(
                date_id=date_id,
                date=current_date,
                year=current_date.year,
                quarter=(current_date.month - 1) // 3 + 1,
                month=current_date.month,
                month_name=current_date.strftime("%B"),
                week=current_date.isocalendar()[1],
                day=current_date.day,
                day_name=current_date.strftime("%A"),
                is_weekend=1 if current_date.weekday() >= 5 else 0
            )
            date_records.append(date_record)
            current_date += timedelta(days=1)
            date_id += 1
        
        db.add_all(date_records)
        print(f"Created {len(date_records)} date records")
        
        # Create customer dimension data
        customers = []
        for i in range(1, 101):  # 100 customers
            customer = DimCustomer(
                customer_id=i,
                customer_name=fake.name(),
                email=fake.email(),
                phone=fake.phone_number(),
                city=fake.city(),
                state=fake.state(),
                country=fake.country()
            )
            customers.append(customer)
        
        db.add_all(customers)
        print(f"Created {len(customers)} customer records")
        
        # Create product dimension data
        categories = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books"]
        subcategories = {
            "Electronics": ["Smartphones", "Laptops", "Tablets", "Headphones"],
            "Clothing": ["Shirts", "Pants", "Dresses", "Shoes"],
            "Home & Garden": ["Furniture", "Decor", "Tools", "Plants"],
            "Sports": ["Equipment", "Apparel", "Accessories", "Footwear"],
            "Books": ["Fiction", "Non-fiction", "Educational", "Comics"]
        }
        brands = ["Brand A", "Brand B", "Brand C", "Brand D", "Brand E"]
        
        products = []
        for i in range(1, 51):  # 50 products
            category = random.choice(categories)
            subcategory = random.choice(subcategories[category])
            
            product = DimProduct(
                product_id=i,
                product_name=f"{fake.word().capitalize()} {subcategory[:-1]}",
                category=category,
                subcategory=subcategory,
                brand=random.choice(brands),
                unit_price=round(random.uniform(10, 500), 2)
            )
            products.append(product)
        
        db.add_all(products)
        print(f"Created {len(products)} product records")
        
        # Commit dimension data first
        db.commit()
        
        # Create fact sales data
        sales = []
        for i in range(1, 1001):  # 1000 sales records
            customer_id = random.randint(1, 100)
            product_id = random.randint(1, 50)
            date_id = random.randint(1, len(date_records))
            quantity = random.randint(1, 10)
            
            # Get unit price from products list (index is product_id - 1)
            unit_price = products[product_id - 1].unit_price
            
            subtotal = quantity * unit_price
            discount_amount = round(subtotal * random.uniform(0, 0.15), 2)  # 0-15% discount
            tax_amount = round((subtotal - discount_amount) * 0.08, 2)  # 8% tax
            total_amount = round(subtotal - discount_amount + tax_amount, 2)
            
            sale = FactSales(
                sale_id=i,
                customer_id=customer_id,
                product_id=product_id,
                date_id=date_id,
                quantity=quantity,
                unit_price=unit_price,
                total_amount=total_amount,
                discount_amount=discount_amount,
                tax_amount=tax_amount
            )
            sales.append(sale)
        
        db.add_all(sales)
        db.commit()
        print(f"Created {len(sales)} sales records")
        print("Sample data population completed!")
        
    except Exception as e:
        print(f"Error populating sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()