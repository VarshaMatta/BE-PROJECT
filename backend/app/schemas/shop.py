from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ShopCreate(BaseModel):
    shop_name: str
    business_type: Optional[str] = "Retail Store"

class ShopOut(BaseModel):
    shop_id: int
    user_id: int
    shop_name: str
    business_type: str
    created_at: datetime
    product_count: Optional[int] = 0
    sales_record_count: Optional[int] = 0
    last_upload: Optional[str] = None

    class Config:
        from_attributes = True
