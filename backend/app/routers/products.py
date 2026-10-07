from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.user import User
from app.models.shop import Shop
from app.models.product import Product
from app.models.sales import SalesRecord
from app.models.constraint import ProductConstraint
from app.schemas.product import ProductOut, ProductDetailResponse, SalesHistoryPoint, PriceHistoryPoint
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/shops/{shop_id}/products", tags=["Products"])

def check_shop_access(shop_id: int, current_user: User, db: Session) -> Shop:
    shop = db.query(Shop).filter(Shop.shop_id == shop_id, Shop.user_id == current_user.user_id).first()
    if not shop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found or access denied.")
    return shop

@router.get("", response_model=List[ProductOut])
def list_products(
    shop_id: int,
    status_filter: Optional[str] = Query(None, description="All, ML READY, LIMITED DATA, COLD START"),
    search: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    check_shop_access(shop_id, current_user, db)
    query = db.query(Product).filter(Product.shop_id == shop_id)

    if status_filter and status_filter.upper() != "ALL":
        query = query.filter(Product.data_sufficiency_status == status_filter.upper())
    
    if search:
        s_pattern = f"%{search}%"
        query = query.filter((Product.product_name.ilike(s_pattern)) | (Product.external_code.ilike(s_pattern)) | (Product.category.ilike(s_pattern)))

    products = query.order_by(Product.product_id.desc()).all()
    res = []
    for p in products:
        rec_count = db.query(func.count(SalesRecord.record_id)).filter(SalesRecord.product_id == p.product_id).scalar() or 0
        price_pts = db.query(func.count(func.distinct(SalesRecord.selling_price))).filter(SalesRecord.product_id == p.product_id).scalar() or 0

        res.append(ProductOut(
            product_id=p.product_id,
            shop_id=p.shop_id,
            external_code=p.external_code,
            product_name=p.product_name,
            category=p.category,
            data_sufficiency_status=p.data_sufficiency_status,
            current_price=p.current_price,
            record_count=rec_count,
            price_point_count=price_pts,
            created_at=p.created_at
        ))
    return res

@router.get("/{product_id}", response_model=ProductDetailResponse)
def get_product_detail(
    shop_id: int,
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    check_shop_access(shop_id, current_user, db)
    product = db.query(Product).filter(Product.product_id == product_id, Product.shop_id == shop_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")

    constraint = db.query(ProductConstraint).filter(ProductConstraint.product_id == product_id).first()
    mrp = constraint.mrp if constraint else None
    cost = constraint.cost_price if constraint else None

    records = db.query(SalesRecord).filter(SalesRecord.product_id == product_id).order_by(SalesRecord.sale_date.asc()).all()
    rec_count = len(records)
    price_pts = len(set(r.selling_price for r in records))
    
    history_days = 0
    start_str = None
    end_str = None
    if records:
        start_date = records[0].sale_date
        end_date = records[-1].sale_date
        history_days = max(1, (end_date - start_date).days)
        start_str = start_date.strftime("%d %b %Y")
        end_str = end_date.strftime("%d %b %Y")

    return ProductDetailResponse(
        product_id=product.product_id,
        product_name=product.product_name,
        external_code=product.external_code,
        category=product.category,
        data_sufficiency_status=product.data_sufficiency_status,
        current_price=product.current_price,
        mrp=mrp,
        cost_price=cost,
        history_days=history_days,
        price_point_count=price_pts,
        record_count=rec_count,
        date_range_start=start_str,
        date_range_end=end_str
    )

@router.get("/{product_id}/charts")
def get_product_charts(
    shop_id: int,
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    check_shop_access(shop_id, current_user, db)
    records = db.query(SalesRecord).filter(SalesRecord.product_id == product_id).order_by(SalesRecord.sale_date.asc()).all()

    sales_history = []
    price_history = []
    for r in records:
        d_str = r.sale_date.strftime("%b %Y")
        sales_history.append({"date": d_str, "quantity_sold": r.quantity_sold, "selling_price": r.selling_price})
        price_history.append({"date": d_str, "selling_price": r.selling_price})

    return {
        "sales_history": sales_history,
        "price_history": price_history
    }
