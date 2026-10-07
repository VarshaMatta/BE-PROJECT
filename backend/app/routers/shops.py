from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.user import User
from app.models.shop import Shop
from app.models.product import Product
from app.models.sales import SalesRecord
from app.models.upload import CSVUpload
from app.schemas.shop import ShopCreate, ShopOut
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/shops", tags=["Shops"])

@router.get("", response_model=List[ShopOut])
def get_user_shops(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    shops = db.query(Shop).filter(Shop.user_id == current_user.user_id).all()
    res = []
    for s in shops:
        prod_count = db.query(func.count(Product.product_id)).filter(Product.shop_id == s.shop_id).scalar() or 0
        
        sales_count = db.query(func.count(SalesRecord.record_id)).join(Product).filter(Product.shop_id == s.shop_id).scalar() or 0
        
        last_up = db.query(CSVUpload).filter(CSVUpload.shop_id == s.shop_id).order_by(CSVUpload.uploaded_at.desc()).first()
        last_up_str = last_up.uploaded_at.strftime("%b %Y") if last_up else "No uploads"

        res.append(ShopOut(
            shop_id=s.shop_id,
            user_id=s.user_id,
            shop_name=s.shop_name,
            business_type=s.business_type,
            created_at=s.created_at,
            product_count=prod_count,
            sales_record_count=sales_count,
            last_upload=last_up_str
        ))
    return res

@router.post("", response_model=ShopOut, status_code=status.HTTP_201_CREATED)
def create_shop(shop_in: ShopCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_shop = Shop(
        user_id=current_user.user_id,
        shop_name=shop_in.shop_name,
        business_type=shop_in.business_type or "Retail Store"
    )
    db.add(new_shop)
    db.commit()
    db.refresh(new_shop)
    return ShopOut(
        shop_id=new_shop.shop_id,
        user_id=new_shop.user_id,
        shop_name=new_shop.shop_name,
        business_type=new_shop.business_type,
        created_at=new_shop.created_at,
        product_count=0,
        sales_record_count=0,
        last_upload="No uploads"
    )
