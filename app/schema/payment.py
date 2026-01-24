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