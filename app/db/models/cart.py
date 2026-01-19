from app.db.base import Base
from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

class Cart(Base):
    
    __tablename__ = "cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, server_default="1", nullable=False)
    price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    
    product = relationship("Product", back_populates="cart_items")
    user  = relationship("Users", back_populates="cart")