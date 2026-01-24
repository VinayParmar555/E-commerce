from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.db.models.user import Users
from app.deps.db import get_db
from app.deps.auth import get_current_user
from app.schema.order import Order
from app.schema.payment import PaymentCreate
from app.services.order_service import checkout
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