from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Product(Base):
   
    __tablename__ = "products"
   
    id = Column(Integer, primary_key=True, index= True)
    name = Column(String)
    price = Column(Float)
    description = Column(String)
    quantity = Column(Integer)

    cart_items = relationship("Cart", back_populates="product")
    category = relationship("Category", back_populates="products")