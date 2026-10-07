import random
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models.user import User
from app.models.shop import Shop
from app.models.product import Product
from app.models.sales import SalesRecord
from app.models.constraint import ProductConstraint
from app.models.upload import CSVUpload
from app.auth.password import hash_password

def seed_database():
    db = SessionLocal()
    try:
        # Check if user already exists
        user = db.query(User).filter(User.email == "alex@freshmart.com").first()
        if not user:
            user = User(
                name="Alex Kumar",
                email="alex@freshmart.com",
                password_hash=hash_password("Password123!")
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        # Create FreshMart shop
        shop = db.query(Shop).filter(Shop.user_id == user.user_id, Shop.shop_name == "FreshMart").first()
        if not shop:
            shop = Shop(
                user_id=user.user_id,
                shop_name="FreshMart",
                business_type="Grocery Store"
            )
            db.add(shop)
            db.commit()
            db.refresh(shop)

        # Create City Grocery shop
        city_shop = db.query(Shop).filter(Shop.user_id == user.user_id, Shop.shop_name == "City Grocery").first()
        if not city_shop:
            city_shop = Shop(
                user_id=user.user_id,
                shop_name="City Grocery",
                business_type="Retail Store"
            )
            db.add(city_shop)
            db.commit()

        # Seed sample CSV Upload record
        upload = db.query(CSVUpload).filter(CSVUpload.shop_id == shop.shop_id).first()
        if not upload:
            upload = CSVUpload(
                shop_id=shop.shop_id,
                filename="freshmart_sales_history.csv",
                total_rows=12450,
                valid_rows=12310,
                duplicate_rows=83,
                invalid_rows=57
            )
            db.add(upload)
            db.commit()
            db.refresh(upload)

        # Sample Products list with exact reference data
        sample_products = [
            {"code": "MLK101", "name": "Amul Milk 1L", "category": "Dairy", "price": 64.0, "status": "ML READY", "cost": 52.0, "mrp": 68.0, "history_days": 730, "price_points": [58.0, 60.0, 62.0, 64.0, 68.0]},
            {"code": "BRD202", "name": "Bread", "category": "Bakery", "price": 35.0, "status": "ML READY", "cost": 25.0, "mrp": 40.0, "history_days": 620, "price_points": [30.0, 32.0, 35.0, 40.0]},
            {"code": "BIS303", "name": "Biscuits", "category": "Snacks", "price": 20.0, "status": "ML READY", "cost": 14.0, "mrp": 25.0, "history_days": 400, "price_points": [18.0, 20.0, 25.0]},
            {"code": "JUC404", "name": "Mango Juice", "category": "Beverage", "price": 45.0, "status": "LIMITED DATA", "cost": 32.0, "mrp": 50.0, "history_days": 42, "price_points": [42.0, 45.0]},
            {"code": "CHP505", "name": "New Chips", "category": "Snacks", "price": 15.0, "status": "COLD START", "cost": 10.0, "mrp": 20.0, "history_days": 0, "price_points": [15.0]},
        ]

        today = datetime.utcnow().date()

        for pdata in sample_products:
            prod = db.query(Product).filter(Product.shop_id == shop.shop_id, Product.external_code == pdata["code"]).first()
            if not prod:
                prod = Product(
                    shop_id=shop.shop_id,
                    external_code=pdata["code"],
                    product_name=pdata["name"],
                    category=pdata["category"],
                    current_price=pdata["price"],
                    data_sufficiency_status=pdata["status"]
                )
                db.add(prod)
                db.commit()
                db.refresh(prod)

                # Add constraints
                c = ProductConstraint(
                    product_id=prod.product_id,
                    cost_price=pdata["cost"],
                    mrp=pdata["mrp"],
                    max_discount_pct=15.0,
                    min_margin_pct=10.0,
                    available_stock=120
                )
                db.add(c)
                db.commit()

                # Generate historical sales records if history_days > 0
                if pdata["history_days"] > 0:
                    sales_list = []
                    start_date = today - timedelta(days=pdata["history_days"])
                    curr = start_date
                    step = 5 if pdata["history_days"] > 100 else 2
                    
                    while curr <= today:
                        p_point = random.choice(pdata["price_points"])
                        qty = random.randint(5, 50)
                        s_rec = SalesRecord(
                            product_id=prod.product_id,
                            upload_id=upload.upload_id,
                            sale_date=curr,
                            selling_price=p_point,
                            quantity_sold=qty,
                            promotion="None" if random.random() > 0.2 else "Discount"
                        )
                        sales_list.append(s_rec)
                        curr += timedelta(days=step)
                    
                    db.bulk_save_objects(sales_list)
                    db.commit()

        print("Database seeded successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
