from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.deps.db import get_db
from app.schema.products import ProductBase
from app.services.product_service import (
    List_of_products, add_product, search_product, update_product, delete_product
)
router = APIRouter(prefix="/products", tags=["Operations"])

@router.get("/")
def List_of_existing_products(db:Session = Depends(get_db)):
    
    db_products = List_of_products(db)

    return db_products

@router.get("/{id}")
def search_existing_product(id: int, db:Session = Depends(get_db)) -> ProductBase:
    db_product = search_product(db, id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.post("/")
def add_new_product(product: ProductBase, db: Session = Depends(get_db)):
    db_product = add_product(db, product)
    
    return db_product

@router.put("/")
def update_existing_product(id: int, product: ProductBase, db:Session = Depends(get_db)):
    db_product = update_product(db, id, product)
    if db_product:
        return "Product Updated"

    raise HTTPException(status_code=404, detail="Product not found")

@router.delete("/")        
def delete_existing_product(id: int, db:Session = Depends(get_db)):                            
    db_product = delete_product(db, id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {"detail" : "Product Deleted"}

