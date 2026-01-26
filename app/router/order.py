from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.db.models.user import Users
from app.deps.db import get_db
from app.deps.auth import get_current_user
from app.schema.order import Order
from app.schema.payment import PaymentCreate
from app.services.order_service import cancel_placed_order, checkout, fetch_placed_order, fetch_single_placed_order, get_user_shipping_status
from app.exception.checkout import (
    CartItemError, 
    PaymentFailedError, 
    InsufficientStockError, 
    AddressIdError, 
    PaymentAmountMismatch
)

router = APIRouter(prefix="/order", tags=["Order"])

@router.post("/checkout", response_model=List[Order])
async def checkout_order(data:PaymentCreate, user:Users=Depends(get_current_user), db:Session=Depends(get_db)):
    try:
        order = checkout(db, user.id, data)
        db.commit()
        return order
    except (CartItemError, AddressIdError) as e:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(e))
    except PaymentFailedError as e:
        db.rollback()
        raise HTTPException(status_code=402, detail=str(e))
    except (InsufficientStockError, PaymentAmountMismatch) as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/fetch_placed_order", response_model=List[Order])
async def fetch_placed_order_for_user(user:Users=Depends(get_current_user), db:Session=Depends(get_db)):
    order = fetch_placed_order(db, user.id)
    if not order:
        raise HTTPException(status_code=404, detail="Place order!")
    return order

@router.get("/single_placed_order/{order_id}", response_model=Order)
async def single_placed_order(order_id:int, user:Users=Depends(get_current_user), db:Session=Depends(get_db)):
    order = fetch_single_placed_order(db, user.id, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Place order!")
    return order

@router.patch("/cancel_placed_order/{order_id}", response_model=Order)
async def cancel_order(order_id:int,user:Users=Depends(get_current_user), db:Session=Depends(get_db)):
    order = cancel_placed_order(db, user.id, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found!")
    if order is False:
        raise HTTPException(status_code=400, detail="Order is already shipped")
    return order

@router.get("/shipping_status/{order_id}")
async def shipping_status(order_id:int,user:Users=Depends(get_current_user), db:Session=Depends(get_db)):
    shipstat = get_user_shipping_status(db, user.id, order_id)
    if shipstat is None:
        raise HTTPException(status_code=404, detail="Order not found or not authorized")
    return shipstat