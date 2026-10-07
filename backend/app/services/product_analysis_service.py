from datetime import date
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.product import Product
from app.models.sales import SalesRecord

class ProductAnalysisService:
    @staticmethod
    def evaluate_sufficiency(record_count: int, distinct_prices: int, history_days: int, non_zero_sales: int) -> str:
        """
        Rule-based data sufficiency classifier:
        - ML READY: history >= 60 days, distinct_prices >= 3, non_zero_sales >= 15, record_count >= 30
        - LIMITED DATA: record_count > 0 but not meeting ML READY
        - COLD START: record_count == 0
        """
        if record_count == 0:
            return "COLD START"
        
        if record_count >= 30 and history_days >= 60 and distinct_prices >= 3 and non_zero_sales >= 15:
            return "ML READY"
        
        return "LIMITED DATA"

    @staticmethod
    def update_product_stats(db: Session, product_id: int):
        records = db.query(SalesRecord).filter(SalesRecord.product_id == product_id).order_by(SalesRecord.sale_date.asc()).all()
        if not records:
            product = db.query(Product).filter(Product.product_id == product_id).first()
            if product:
                product.data_sufficiency_status = "COLD START"
                db.commit()
            return

        record_count = len(records)
        distinct_prices = len(set(r.selling_price for r in records))
        
        start_date = records[0].sale_date
        end_date = records[-1].sale_date
        history_days = max(1, (end_date - start_date).days)
        non_zero_sales = len([r for r in records if r.quantity_sold > 0])

        status = ProductAnalysisService.evaluate_sufficiency(record_count, distinct_prices, history_days, non_zero_sales)
        latest_price = records[-1].selling_price

        product = db.query(Product).filter(Product.product_id == product_id).first()
        if product:
            product.data_sufficiency_status = status
            product.current_price = latest_price
            db.commit()
