from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
   
    __tablename__ = "product"
   
    id = Column(Integer, primary_key=True, index= True)
    name = Column(String)
    price = Column(Float)
    description = Column(String)
    quantity = Column(Integer)

