from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, Column
from app.db.base import Base

class Category(Base):
    
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    products = relationship("Product", back_populates="category")