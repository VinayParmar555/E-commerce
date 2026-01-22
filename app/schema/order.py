from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

class Order(BaseModel):
    id : int
    user_id : int
    shipping_address_id :int
    total_price : float
    status : OrderStatus
    created_at : datetime