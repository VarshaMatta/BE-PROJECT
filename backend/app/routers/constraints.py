from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.shop import Shop
from app.models.product import Product
from app.models.constraint import ProductConstraint
from app.schemas.constraint import ConstraintInput, ConstraintEvaluationResponse
from app.constraint_engine.evaluator import ConstraintEngine
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/shops/{shop_id}/products/{product_id}/constraints", tags=["Constraint Engine"])

def check_shop_product_access(shop_id: int, product_id: int, current_user: User, db: Session) -> Product:
    shop = db.query(Shop).filter(Shop.shop_id == shop_id, Shop.user_id == current_user.user_id).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found or access denied.")
    product = db.query(Product).filter(Product.product_id == product_id, Product.shop_id == shop_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found.")
    return product

@router.get("", response_model=ConstraintInput)
def get_product_constraints(
    shop_id: int,
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    product = check_shop_product_access(shop_id, product_id, current_user, db)
    constraint = db.query(ProductConstraint).filter(ProductConstraint.product_id == product_id).first()
    if not constraint:
        curr_price = product.current_price if product.current_price > 0 else 50.0
        return ConstraintInput(
            cost_price=round(curr_price * 0.75, 2),
            mrp=round(curr_price * 1.15, 2),
            max_discount_pct=15.0,
            min_margin_pct=10.0,
            available_stock=100
        )
    return ConstraintInput(
        cost_price=constraint.cost_price,
        mrp=constraint.mrp,
        max_discount_pct=constraint.max_discount_pct,
        min_margin_pct=constraint.min_margin_pct,
        available_stock=constraint.available_stock
    )

@router.post("/evaluate", response_model=ConstraintEvaluationResponse)
def evaluate_constraints(
    shop_id: int,
    product_id: int,
    constraint_in: ConstraintInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    check_shop_product_access(shop_id, product_id, current_user, db)
    res = ConstraintEngine.evaluate(constraint_in)
    return res

@router.post("/save")
def save_product_constraints(
    shop_id: int,
    product_id: int,
    constraint_in: ConstraintInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    product = check_shop_product_access(shop_id, product_id, current_user, db)
    
    # Run evaluation first to ensure validity
    eval_res = ConstraintEngine.evaluate(constraint_in)
    
    existing = db.query(ProductConstraint).filter(ProductConstraint.product_id == product_id).first()
    if existing:
        existing.cost_price = constraint_in.cost_price
        existing.mrp = constraint_in.mrp
        existing.max_discount_pct = constraint_in.max_discount_pct
        existing.min_margin_pct = constraint_in.min_margin_pct
        existing.available_stock = constraint_in.available_stock
    else:
        new_c = ProductConstraint(
            product_id=product_id,
            cost_price=constraint_in.cost_price,
            mrp=constraint_in.mrp,
            max_discount_pct=constraint_in.max_discount_pct,
            min_margin_pct=constraint_in.min_margin_pct,
            available_stock=constraint_in.available_stock
        )
        db.add(new_c)
    
    db.commit()
    return {
        "message": "Constraints saved successfully.",
        "evaluation": eval_res
    }
