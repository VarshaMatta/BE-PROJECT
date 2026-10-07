from datetime import datetime
from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class RecommendationScenario(Base):
    __tablename__ = "recommendation_scenarios"

    scenario_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id", ondelete="CASCADE"), nullable=False)
    candidate_price = Column(Float, nullable=False)
    predicted_demand = Column(Float, nullable=False)
    estimated_revenue = Column(Float, nullable=False)
    estimated_profit = Column(Float, nullable=False)
    profit_margin_pct = Column(Float, nullable=False)
    is_feasible = Column(Boolean, default=True)
    rank = Column(Integer, nullable=False)
    generated_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="recommendations")
