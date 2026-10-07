from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.shop_id", ondelete="CASCADE"), nullable=False)
    external_code = Column(String(100), nullable=False)
    product_name = Column(String(200), nullable=False)
    category = Column(String(100), default="General")
    data_sufficiency_status = Column(String(50), default="COLD START") # ML READY, LIMITED DATA, COLD START
    current_price = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    shop = relationship("Shop", back_populates="products")
    sales_records = relationship("SalesRecord", back_populates="product", cascade="all, delete-orphan")
    constraint = relationship("ProductConstraint", back_populates="product", uselist=False, cascade="all, delete-orphan")
    recommendations = relationship("RecommendationScenario", back_populates="product", cascade="all, delete-orphan")
