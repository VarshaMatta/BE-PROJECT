import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple, Optional
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor

try:
    from xgboost import XGBRegressor
    HAS_XGBOOST = True
except Exception:
    HAS_XGBOOST = False

class DemandModel:
    """
    ML Demand Model for PriceWise.
    Trains regression models (Scikit-learn Ridge/RandomForest or XGBoost) 
    to estimate quantity sold based on selling price and features.
    """

    def __init__(self, model_type: str = "sklearn"):
        self.model_type = model_type
        if model_type == "xgboost" and HAS_XGBOOST:
            try:
                self.model = XGBRegressor(n_estimators=50, max_depth=3, learning_rate=0.1, random_state=42)
            except Exception:
                self.model = RandomForestRegressor(n_estimators=50, random_state=42)
                self.model_type = "sklearn"
        elif model_type == "rf":
            self.model = RandomForestRegressor(n_estimators=50, random_state=42)
        else:
            self.model = Ridge(alpha=1.0)
            
        self.is_trained = False
        self.mean_demand = 10.0

    def fit(self, sales_records: List[Any]):
        if not sales_records or len(sales_records) < 5:
            self.is_trained = False
            return

        df = pd.DataFrame([{
            "price": r.selling_price,
            "quantity": r.quantity_sold,
            "month": r.sale_date.month if hasattr(r.sale_date, "month") else 1,
            "dayofweek": r.sale_date.weekday() if hasattr(r.sale_date, "weekday") else 0
        } for r in sales_records])

        X = df[["price", "month", "dayofweek"]]
        y = df["quantity"]

        self.mean_demand = float(y.mean())
        
        if X["price"].nunique() < 2:
            self.is_trained = False
            return

        try:
            self.model.fit(X, y)
            self.is_trained = True
        except Exception:
            self.is_trained = False

    def predict_demand(self, candidate_price: float, current_price: float, avg_quantity: float) -> float:
        if self.is_trained:
            try:
                features = pd.DataFrame([{
                    "price": candidate_price,
                    "month": 6,
                    "dayofweek": 3
                }])
                pred = float(self.model.predict(features)[0])
                return max(0.0, round(pred, 2))
            except Exception:
                pass

        if current_price <= 0:
            return float(avg_quantity)
        
        elasticity = -1.2
        ratio = candidate_price / current_price
        predicted_q = avg_quantity * (ratio ** elasticity)
        return max(0.0, round(predicted_q, 2))
