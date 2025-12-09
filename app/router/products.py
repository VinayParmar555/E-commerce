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
def search_product(id: int, db:Session = Depends(get_db)) -> ProductBase:
    db_product = db.get(products.Product, id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.post("/products",tags=["Operations"])
def add_product(product: ProductBase, db: Session = Depends(get_db)):
    db_product = db.add(products.Product(**product.model_dump()))
    db.commit()
    db.refresh(db_product)
    return product

@router.put("/products",tags=["Operations"])
def update_product(id: int, product: ProductBase, db:Session = Depends(get_db)):
    db_product = db.get(products.Product, id)
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        db.refresh(db_product)
        return "Product Updated"
    
    raise HTTPException(status_code=404, detail="Product not found")

@router.delete("/products",tags=["Operations"])        
def delete_product(id: int, db:Session = Depends(get_db)):                            
    db_product = db.get(products.Product, id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"detail" : "Product Deleted"}

