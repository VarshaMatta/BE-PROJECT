from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.sales import SalesRecord
from app.models.constraint import ProductConstraint
from app.models.recommendation import RecommendationScenario
from app.constraint_engine.evaluator import ConstraintEngine
from app.schemas.constraint import ConstraintInput
from app.ml.demand_model import DemandModel
from app.ml.scenario_generator import ScenarioGenerator
from app.schemas.recommendation import RecommendationResponse, ScenarioOut

class ScenarioOptimizer:
    @staticmethod
    def generate_recommendations(db: Session, product_id: int, model_preference: str = "sklearn") -> RecommendationResponse:
        product = db.query(Product).filter(Product.product_id == product_id).first()
        if not product:
            raise ValueError(f"Product with ID {product_id} not found.")

        constraint = db.query(ProductConstraint).filter(ProductConstraint.product_id == product_id).first()
        if not constraint:
            # Fallback default constraint
            cost = round(product.current_price * 0.75, 2) if product.current_price > 0 else 50.0
            mrp = round(product.current_price * 1.15, 2) if product.current_price > 0 else 70.0
            max_disc = 15.0
            min_margin = 10.0
            stock = 100
        else:
            cost = constraint.cost_price
            mrp = constraint.mrp
            max_disc = constraint.max_discount_pct
            min_margin = constraint.min_margin_pct
            stock = constraint.available_stock

        constraint_input = ConstraintInput(
            cost_price=cost,
            mrp=mrp,
            max_discount_pct=max_disc,
            min_margin_pct=min_margin,
            available_stock=stock
        )
        eval_result = ConstraintEngine.evaluate(constraint_input)

        if not eval_result.is_valid:
            return RecommendationResponse(
                product_id=product_id,
                product_name=product.product_name,
                current_price=product.current_price,
                cost_price=cost,
                mrp=mrp,
                min_allowed_price=eval_result.min_allowed_price or cost,
                max_allowed_price=eval_result.max_allowed_price or mrp,
                recommended_scenario=None,
                scenarios=[],
                model_used=model_preference,
                generated_at=datetime.utcnow()
            )

        min_price = eval_result.min_allowed_price
        max_price = eval_result.max_allowed_price

        # Fetch sales records for demand model
        sales_records = db.query(SalesRecord).filter(SalesRecord.product_id == product_id).all()
        avg_qty = float(sum(r.quantity_sold for r in sales_records) / max(1, len(sales_records))) if sales_records else 10.0

        model = DemandModel(model_type=model_preference)
        model.fit(sales_records)

        candidate_prices = ScenarioGenerator.generate_candidate_prices(min_price, max_price, product.current_price, num_steps=10)

        scenarios_data = []
        for p in candidate_prices:
            pred_demand = model.predict_demand(p, product.current_price, avg_qty)
            rev = round(p * pred_demand, 2)
            profit = round((p - cost) * pred_demand, 2)
            margin_pct = round(((p - cost) / p * 100.0), 1) if p > 0 else 0.0

            scenarios_data.append({
                "candidate_price": p,
                "predicted_demand": pred_demand,
                "estimated_revenue": rev,
                "estimated_profit": profit,
                "profit_margin_pct": margin_pct,
                "is_feasible": True
            })

        # Sort descending by estimated profit
        scenarios_data.sort(key=lambda s: s["estimated_profit"], reverse=True)

        scenarios_out: List[ScenarioOut] = []
        for idx, s in enumerate(scenarios_data):
            scenarios_out.append(ScenarioOut(
                scenario_id=idx + 1,
                candidate_price=s["candidate_price"],
                predicted_demand=s["predicted_demand"],
                estimated_revenue=s["estimated_revenue"],
                estimated_profit=s["estimated_profit"],
                profit_margin_pct=s["profit_margin_pct"],
                is_feasible=s["is_feasible"],
                rank=idx + 1
            ))

        # Clear existing saved scenarios and persist top 5 in DB
        db.query(RecommendationScenario).filter(RecommendationScenario.product_id == product_id).delete()
        for s in scenarios_out[:5]:
            db_scenario = RecommendationScenario(
                product_id=product_id,
                candidate_price=s.candidate_price,
                predicted_demand=s.predicted_demand,
                estimated_revenue=s.estimated_revenue,
                estimated_profit=s.estimated_profit,
                profit_margin_pct=s.profit_margin_pct,
                is_feasible=s.is_feasible,
                rank=s.rank
            )
            db.add(db_scenario)
        db.commit()

        top_recommended = scenarios_out[0] if scenarios_out else None

        return RecommendationResponse(
            product_id=product_id,
            product_name=product.product_name,
            current_price=product.current_price,
            cost_price=cost,
            mrp=mrp,
            min_allowed_price=min_price,
            max_allowed_price=max_price,
            recommended_scenario=top_recommended,
            scenarios=scenarios_out,
            model_used="Scikit-Learn (Ridge)" if not model.is_trained else ("XGBoost" if model_preference == "xgboost" else "Scikit-Learn Regression"),
            generated_at=datetime.utcnow()
        )
