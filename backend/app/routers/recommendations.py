from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.shop import Shop
from app.schemas.recommendation import RecommendationResponse
from app.ml.optimizer import ScenarioOptimizer
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/shops/{shop_id}/products/{product_id}/recommendations", tags=["ML Recommendations"])

def check_shop_access(shop_id: int, current_user: User, db: Session) -> Shop:
    shop = db.query(Shop).filter(Shop.shop_id == shop_id, Shop.user_id == current_user.user_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found or access denied.")
    return shop

@router.post("/generate", response_model=RecommendationResponse)
def generate_recommendations(
    shop_id: int,
    product_id: int,
    model_type: Optional[str] = Query("sklearn", description="sklearn or xgboost"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    check_shop_access(shop_id, current_user, db)
    try:
        res = ScenarioOptimizer.generate_recommendations(db, product_id, model_preference=model_type or "sklearn")
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
