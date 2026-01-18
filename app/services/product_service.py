from sqlalchemy.orm import Session, joinedload
from app.db.models.products import Product
from app.db.models.category import Category
from app.schema.products import ProductRead, ProductCreate
from typing import List

def List_of_products(db:Session):
    db_products = db.query(Product).options(joinedload(Product.category)).all()
    if not db_products:
        return False
    return db_products

def search_product(db:Session, id:int):
    db_product = db.query(Product).options(joinedload(Product.category)).filter(Product.id==id).first()
    if not db_product:
        return False
    return {
        "name": db_product.name,
        "price": db_product.price,
        "description": db_product.description,
        "quantity": db_product.quantity,
        "category": db_product.category
    }

def add_product(db: Session, product:ProductCreate):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db:Session, id:int, product:ProductCreate):
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
    products = db.query(Product).offset(offset).limit(limit).all()
    return products

def filter_products(
        db:Session, 
        category:str, 
        name:str | None = None, 
        min_price:int | None = None, 
        max_price:int | None = None, 
        limit:int=5, page:int=1
    ):
    stmt = db.query(Product).options(joinedload(Product.category))
    filters=[]
    if category:
        stmt = stmt.join(Product.category)
        filters.append(Category.name.ilike(f"%{category}%"))
    if name:
        filters.append(Product.name.ilike(f"%{name}%"))
    if min_price is not None:
        filters.append(Product.price>=min_price)
    if max_price is not None:
        filters.append(Product.price<=max_price)
    if filters:
        stmt = stmt.filter(*filters).distinct()
    offset=(page-1)*limit
    products=stmt.offset(offset).limit(limit).all()
    return products