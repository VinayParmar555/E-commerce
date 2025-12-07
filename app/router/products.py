from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.db.models import products
from app.schema.products import ProductBase

router = APIRouter()

@router.get("/products",tags=["Operations"])
def List_of_products(db:Session = Depends(get_db)):
    
    db_products = db.query(products.Product).all()

    return db_products

@router.get("/products/{id}",tags=["Operations"])
def search_product(id: int, db:Session = Depends(get_db)):
    db_product = db.query(products.Product).filter(products.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.post("/products",tags=["Operations"])
def add_product(product: ProductBase, db: Session = Depends(get_db)):
    db.add(products.Product(**product.model_dump()))
    db.commit()
    return product

@router.put("/products",tags=["Operations"])
def update_product(id: int, product: ProductBase, db:Session = Depends(get_db)):
    db_product = db.query(products.Product).filter(products.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product Updated"
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@router.delete("/products",tags=["Operations"])        
def delete_product(id: int, db:Session = Depends(get_db)):                            
    db_product = db.query(products.Product).filter(products.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted"
    raise HTTPException(status_code=404, detail="Product not found")

