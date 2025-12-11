from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.products import Product
from app.schema.products import ProductBase

router = APIRouter(prefix="/products", tags=["Operations"])

@router.get("/")
def List_of_products(db:Session = Depends(get_db)):
    
    db_products = db.query(Product).all()

    return db_products

@router.get("/{id}")
def search_product(id: int, db:Session = Depends(get_db)) -> ProductBase:
    db_product = db.get(Product, id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.post("/")
def add_product(product: ProductBase, db: Session = Depends(get_db)):
    db_product = db.add(Product(**product.model_dump()))
    db.commit()
    db.refresh(db_product)
    return product

@router.put("/")
def update_product(id: int, product: ProductBase, db:Session = Depends(get_db)):
    db_product = db.get(Product, id)
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        db.refresh(db_product)
        return "Product Updated"

    raise HTTPException(status_code=404, detail="Product not found")

@router.delete("/")        
def delete_product(id: int, db:Session = Depends(get_db)):                            
    db_product = db.get(Product, id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"detail" : "Product Deleted"}

