import json
from fastapi import APIRouter, HTTPException, Depends, Header, Request
from sqlalchemy.orm import Session
from app.cache.rate_limit import ip_key, rate_limit, user_key
from app.deps.auth import get_current_user
from app.deps.db import get_db
from app.db.models.user import Users
from app.exception.checkout import OrderError, PaymentError
from app.schema.payment import PaymentResponse
from app.services.payment_service import (
    fetch_all_payments, 
    fetch_payment_status, 
    process_razorpay_webhook, 
    verify_razorpay_signature
)

router = APIRouter(prefix="/payment", tags=["Payment"])

@router.post("/razorpay/webhook")
async def razorpay_webhook(request:Request, x_razorpay_signature:str=Header(None), _:None=Depends(rate_limit(200,60,ip_key)), db:Session=Depends(get_db)):
    raw_body = await request.body()

    if not x_razorpay_signature:
        raise HTTPException(status_code=400, detail="Missing Razorpay signature")

    if not verify_razorpay_signature(raw_body, x_razorpay_signature):
        raise HTTPException(status_code=400, detail="Invalid Razorpay signature")

    payload = json.loads(raw_body)
    try:
        process = process_razorpay_webhook(db, payload, x_razorpay_signature)
        return process
    except (OrderError, PaymentError) as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/status/{order_id}", response_model=PaymentResponse)
async def check_payment_status(order_id:int, user:Users=Depends(get_current_user), _:None=Depends(rate_limit(5,60,user_key)), db:Session=Depends(get_db)):
    payment = fetch_payment_status(db, user.id, order_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found!")
    return payment

@router.patch("/status/all", response_model=list[PaymentResponse])
async def check_payment_status_all(user:Users=Depends(get_current_user), _:None=Depends(rate_limit(5,60,user_key)), db:Session=Depends(get_db)):
    payment = fetch_all_payments(db, user.id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found!")
    return payment