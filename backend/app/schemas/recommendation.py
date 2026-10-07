from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class ScenarioOut(BaseModel):
    scenario_id: Optional[int] = None
    candidate_price: float
    predicted_demand: float
    estimated_revenue: float
    estimated_profit: float
    profit_margin_pct: float
    is_feasible: bool
    rank: int

class RecommendationResponse(BaseModel):
    product_id: int
    product_name: str
    current_price: float
    cost_price: float
    mrp: float
    min_allowed_price: float
    max_allowed_price: float
    recommended_scenario: Optional[ScenarioOut] = None
    scenarios: List[ScenarioOut] = []
    model_used: str
    generated_at: datetime
