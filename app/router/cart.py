from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.deps.db import get_db
from app.schema.cart import CartOut
from app.services.cart_service import add_to_cart

router = APIRouter(prefix="/Cart", tags=["Cart"])

@router.post("/add_cart")
async def add_in_cart(cart_item:CartOut, db:Session=Depends(get_db)):
    cart = add_to_cart(db, cart_item)
    if cart is None:
        raise HTTPException(status_code=404, detail="Insufficient stock")
    if cart is False:
        raise HTTPException(status_code=404, detail="user not found")
    return cart