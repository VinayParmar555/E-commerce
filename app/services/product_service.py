from sqlalchemy.orm import Session, joinedload
from app.db.models.products import Product
from app.schema.products import ProductRead
from typing import List

def List_of_products(db:Session):
    db_products = db.query(Product).options(joinedload(Product.category)).all()
    if not db_products:
        return False
    return db_products

def search_product(db:Session, id: int):
    db_product = db.get(Product, id)
    if not db_product:
        return False
    return db_product

def add_product(db: Session, product: ProductRead):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db:Session, id: int, product: ProductRead):
    db_product = db.get(Product, id)
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db_product.category_id = product.category_id
        db.commit()
        db.refresh(db_product)
        return db_product
    return False

def delete_product(db:Session, id: int):                            
    db_product = db.get(Product, id)
    if not db_product:
        return False
    db.delete(db_product)
    db.commit()
    return db_product

def add_bulk_products(db:Session, product:List[ProductRead]):
    db_products = [Product(**p.model_dump()) for p in product]
    if not db_products:
        return False
    db.bulk_save_objects(db_products)
    db.commit()
    return db_products

def pagination_process(db:Session, page:int=1, limit:int=10):
    offset = (page-1)*limit
    products = db.query(Product).order_by(Product.id.asc()).offset(offset).limit(limit).all()
    return products