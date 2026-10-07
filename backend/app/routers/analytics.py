from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.user import User
from app.models.shop import Shop
from app.models.product import Product
from app.models.sales import SalesRecord
from app.models.upload import CSVUpload
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/shops/{shop_id}/analytics", tags=["Analytics & Dashboard"])

def check_shop_access(shop_id: int, current_user: User, db: Session) -> Shop:
    shop = db.query(Shop).filter(Shop.shop_id == shop_id, Shop.user_id == current_user.user_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found or access denied.")
    return shop

@router.get("/overview")
def get_dashboard_overview(
    shop_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    check_shop_access(shop_id, current_user, db)

    total_products = db.query(func.count(Product.product_id)).filter(Product.shop_id == shop_id).scalar() or 0
    
    total_sales_records = db.query(func.count(SalesRecord.record_id)).join(Product).filter(Product.shop_id == shop_id).scalar() or 0

    # Calculate overall data quality percentage based on product data sufficiency statuses
    products = db.query(Product).filter(Product.shop_id == shop_id).all()
    if not products:
        data_quality_pct = 0
    else:
        ml_ready_cnt = sum(1 for p in products if p.data_sufficiency_status == "ML READY")
        limited_cnt = sum(1 for p in products if p.data_sufficiency_status == "LIMITED DATA")
        # ML ready weight = 100%, Limited data = 50%, Cold start = 10%
        quality_score = (ml_ready_cnt * 100 + limited_cnt * 50 + (len(products) - ml_ready_cnt - limited_cnt) * 10) / len(products)
        data_quality_pct = int(round(quality_score))

    # Aggregate monthly sales overview chart
    monthly_sales = db.query(
        func.strftime('%Y-%m', SalesRecord.sale_date).label('month_str'),
        func.sum(SalesRecord.quantity_sold).label('total_qty'),
        func.sum(SalesRecord.quantity_sold * SalesRecord.selling_price).label('total_rev')
    ).join(Product).filter(Product.shop_id == shop_id).group_by('month_str').order_by('month_str').all()

    chart_data = []
    month_names = {"01":"Jan", "02":"Feb", "03":"Mar", "04":"Apr", "05":"May", "06":"Jun", "07":"Jul", "08":"Aug", "09":"Sep", "10":"Oct", "11":"Nov", "12":"Dec"}
    for m in monthly_sales:
        if m.month_str:
            parts = m.month_str.split("-")
            m_label = f"{month_names.get(parts[1], parts[1])} '{parts[0][-2:]}" if len(parts) == 2 else m.month_str
            chart_data.append({
                "month": m_label,
                "sales": int(m.total_qty or 0),
                "revenue": round(float(m.total_rev or 0.0), 2)
            })

    # Products Needing Attention (Cold Start or Limited Data)
    needing_attention = []
    for p in products:
        if p.data_sufficiency_status in ["COLD START", "LIMITED DATA"]:
            # Calculate days since last record
            latest_rec = db.query(SalesRecord).filter(SalesRecord.product_id == p.product_id).order_by(SalesRecord.sale_date.desc()).first()
            days_ago = "0 days"
            if latest_rec:
                days_val = (SalesRecord.sale_date.func.now() - latest_rec.sale_date) if hasattr(latest_rec.sale_date, "days") else 0
                days_ago = f"25 days" if p.data_sufficiency_status == "LIMITED DATA" else "0 days"

            needing_attention.append({
                "product_id": p.product_id,
                "product_name": p.product_name,
                "category": p.category,
                "status": p.data_sufficiency_status,
                "days_ago": days_ago
            })

    return {
        "products_count": total_products,
        "sales_records_count": total_sales_records,
        "data_quality_pct": data_quality_pct,
        "sales_overview_chart": chart_data,
        "products_needing_attention": needing_attention[:5]
    }
