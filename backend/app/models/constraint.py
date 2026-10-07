from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class ProductConstraint(Base):
    __tablename__ = "product_constraints"

    constraint_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id", ondelete="CASCADE"), unique=True, nullable=False)
    cost_price = Column(Float, nullable=False)
    mrp = Column(Float, nullable=False)
    max_discount_pct = Column(Float, default=0.0)
    min_margin_pct = Column(Float, default=0.0)
    available_stock = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    product = relationship("Product", back_populates="constraint")
