from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.deps.auth import get_current_user
from app.deps.db import get_db
from app.db.models.user import Users
from app.schema.payment import PaymentResponse
from app.services.payment_service import fetch_payment_status

router = APIRouter(prefix="/payment", tags=["Payment"])

@router.patch("/payment_status/{order_id}", response_model=PaymentResponse)
async def check_payment_status(order_id:int, user:Users=Depends(get_current_user), db:Session=Depends(get_db)):
    payment = fetch_payment_status(db, user.id, order_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found!")
    return payment