from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class SalesRecord(Base):
    __tablename__ = "sales_records"

    record_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id", ondelete="CASCADE"), nullable=False)
    upload_id = Column(Integer, ForeignKey("csv_uploads.upload_id", ondelete="CASCADE"), nullable=True)
    sale_date = Column(Date, nullable=False, index=True)
    selling_price = Column(Float, nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    promotion = Column(String(100), default="None")

    product = relationship("Product", back_populates="sales_records")
    upload = relationship("CSVUpload", back_populates="sales_records")
