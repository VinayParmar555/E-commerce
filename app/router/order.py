from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.db.models.user import Users
from app.deps.db import get_db
from app.deps.auth import get_current_user
from app.schema.order import Order
from app.schema.payment import PaymentCreate
from app.services.order_service import checkout, fetch_placed_order
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