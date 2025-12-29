from sqlalchemy.orm import Session
from app.db.models.products import Product
from app.schema.products import ProductBase

def List_of_products(db:Session):
    db_products = db.query(Product).all()
    if not db_products:
        return False
    return db_products

def search_product(db:Session, id: int):
    db_product = db.get(Product, id)
    if not db_product:
        return False
    return db_product

def add_product(db: Session, product: ProductBase):

    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db:Session, id: int, product: ProductBase):
    db_product = db.get(Product, id)
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        db.refresh(db_product)
        return {"msg" : "Product Updated successfully"}

    return False

def delete_product( db:Session, id: int):                            
    db_product = db.get(Product, id)
    if not db_product:
        return False
    
    db.delete(db_product)
    db.commit()
    return {"detail" : "Product Deleted successfully"}
