from fastapi import FastAPI, Depends
from app.schema.products import ProductRead
from app.db.session import session, engine
from sqlalchemy.orm import Session
from app.db import models

app = FastAPI(title="Radha Krishna")

models.Base.metadata.create_all(bind=engine)

products = [
    ProductRead(id=1, name="Laptop", price=999, description="gaming laptop", quantity=10),
    ProductRead(id=2, name="Mouse", price=29, description="wireless mouse", quantity=10),
    ProductRead(id=3, name="Keyboard", price=99, description="mechanical keyboard", quantity=10),
    ProductRead(id=4, name="Table", price=299, description="wood", quantity=10) 
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = session()

    count = db.query(models.Product).count()

    if count  == 0:
        for product in products:
            db.add(models.Product(**product.model_dump()))

        db.commit()

init_db()

@app.get("/products",tags=["Operations"])
def List_of_products(db:Session = Depends(get_db)):
    
    db_products = db.query(models.Product).all()

    return db_products

@app.get("/products/{id}",tags=["Operations"])
def search_product(id: int, db:Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if db_product:
        return db_product
    return ("Product not found")

@app.post("/products",tags=["Operations"])
def add_product(product: ProductRead, db: Session = Depends(get_db)):
    db.add(models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products",tags=["Operations"])
def update_product(id: int, product: ProductRead, db:Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product Updated"
    else:
        return "No product found"

@app.delete("/products",tags=["Operations"])        
def delete_product(id: int, db:Session = Depends(get_db)):                            
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted"
    return "Product not found"

