from sqlalchemy.orm import declarative_base

Base = declarative_base()

# from app.db.models.cart import Cart
from app.db.models.products import Product
from app.db.models.category import Category