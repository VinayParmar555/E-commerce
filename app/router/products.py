from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.deps.db import get_db
from app.deps.auth import get_current_user
from app.schema.products import ProductBase
from app.db.models.user import Users
from app.services.product_service import (
    add_product, search_product, update_product, delete_product
)
from app.cache.cache_service import get_cached_products, delete_cached_product

router = APIRouter(prefix="/products", tags=["Operations"])

@router.get("/")
def List_of_existing_products(db:Session = Depends(get_db)):
    db_products = get_cached_products(db)
    if not db_products:
        raise HTTPException(status_code=404, detail="Products not found")
    return db_products

@router.get("/{id}")
def search_existing_product(id: int, db:Session = Depends(get_db)) -> ProductBase:
    db_product = search_product(db, id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.post("/")
def add_new_product(product:ProductBase, db:Session = Depends(get_db), current_user:Users = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admins Only")
    db_product = add_product(db, product)
    delete_cached_product(db_product.id)
    if not db_product:
        raise HTTPException(status_code=400, detail="Unable to add product")
    return db_product

@router.put("/{id}")
def update_existing_product(id: int, product: ProductBase, db:Session = Depends(get_db), current_user:Users = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admins Only")
    db_product = update_product(db, id, product)
    delete_cached_product(id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/{id}")        
def delete_existing_product(id: int, db:Session = Depends(get_db), current_user:Users = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admins Only")                           
    db_product = delete_product(db, id)
    delete_cached_product(id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product
