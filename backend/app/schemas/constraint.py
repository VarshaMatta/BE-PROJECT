from typing import Optional, List
from pydantic import BaseModel, Field

class ConstraintInput(BaseModel):
    cost_price: float = Field(..., gt=0, description="Cost price of product")
    mrp: float = Field(..., gt=0, description="Maximum retail price")
    max_discount_pct: float = Field(default=0.0, ge=0.0, le=100.0)
    min_margin_pct: float = Field(default=0.0, ge=0.0, lt=100.0)
    available_stock: int = Field(default=0, ge=0)

class ConstraintCheckItem(BaseModel):
    label: str
    passed: bool
    detail: str

class ConstraintEvaluationResponse(BaseModel):
    is_valid: bool
    min_allowed_price: Optional[float] = None
    max_allowed_price: Optional[float] = None
    status_title: str
    status_description: str
    checks: List[ConstraintCheckItem] = []
    conflict_reasons: List[str] = []
