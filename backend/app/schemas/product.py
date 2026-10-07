from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel

class ProductOut(BaseModel):
    product_id: int
    shop_id: int
    external_code: str
    product_name: str
    category: str
    data_sufficiency_status: str
    current_price: float
    record_count: Optional[int] = 0
    price_point_count: Optional[int] = 0
    created_at: datetime

    class Config:
        from_attributes = True

class ProductDetailResponse(BaseModel):
    product_id: int
    product_name: str
    external_code: str
    category: str
    data_sufficiency_status: str
    current_price: float
    mrp: Optional[float] = None
    cost_price: Optional[float] = None
    history_days: int
    price_point_count: int
    record_count: int
    date_range_start: Optional[str] = None
    date_range_end: Optional[str] = None

class SalesHistoryPoint(BaseModel):
    date: str
    quantity_sold: int
    selling_price: float

class PriceHistoryPoint(BaseModel):
    date: str
    selling_price: float
