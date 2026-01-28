from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class PaymentStatus(str, Enum):
    pending = "pending"
    success = "success"
    failed = "failed"
    cancelled = "cancelled"

class PaymentGateway(Enum):
    mock = "mock"
    razorpay = "razorpay"

class PaymentCreate(BaseModel):
    amount : int
    shipping_address_id : int
    gateway : PaymentGateway = PaymentGateway.mock
    simulate_succ : bool | None = None

class PaymentResponse(BaseModel):
    id : int
    order_id : int
    user_id : int
    amount : int
    status : PaymentStatus
    payment_gateway : PaymentGateway
    is_paid : bool
    pg_order_id : str | None
    pg_payment_id : str | None
    pg_signature : str | None
    created_at : datetime
    updated_at : datetime

    model_config = {"from_attributes" : True}

class PaymentResponseRazorpay(BaseModel):
    payment : PaymentResponse
    rz_data : dict | None = None

    model_config = {"from_attributes" : True}