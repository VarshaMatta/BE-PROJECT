from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class CSVUpload(Base):
    __tablename__ = "csv_uploads"

    upload_id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.shop_id", ondelete="CASCADE"), nullable=False)
    filename = Column(String(255), nullable=False)
    total_rows = Column(Integer, default=0)
    valid_rows = Column(Integer, default=0)
    duplicate_rows = Column(Integer, default=0)
    invalid_rows = Column(Integer, default=0)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    shop = relationship("Shop", back_populates="uploads")
    sales_records = relationship("SalesRecord", back_populates="upload", cascade="all, delete-orphan")
