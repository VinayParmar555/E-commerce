from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.deps.db import get_db
from app.deps.auth import get_current_user
from app.schema.cart import CartItem
from app.db.models.user import Users
from app.services.cart_service import add_to_cart, remove_cart, see_cart

router = APIRouter(prefix="/Cart", tags=["Cart"])

@router.post("/add_cart")
async def add_in_cart(cart_item:CartItem, user:Users=Depends(get_current_user), db:Session=Depends(get_db)):
    cart = add_to_cart(db, cart_item, user.id)
    if cart is None:
        raise HTTPException(status_code=404, detail="Insufficient stock")
    if cart is False:
        raise HTTPException(status_code=404, detail="user not found")
    return cart

@router.get("/see_cart")
async def check_cart(user:Users=Depends(get_current_user), db:Session=Depends(get_db)):
    cart = see_cart(db, user.id)
    if not cart:
        raise HTTPException(status_code=404, detail="add items to see cart")
    return cart

@router.delete("/delete_cart/{cart_id}")
async def delete_cart(cart_id:int, user:Users=Depends(get_current_user), db:Session=Depends(get_db)):
    cart = remove_cart(db, user.id, cart_id)
    if not cart:
        raise HTTPException(status_code=404, detail="cart not found")
    return {"msg":"cart deleted succesfully"}