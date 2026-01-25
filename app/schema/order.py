from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from app.schema.shipping import ShippingStatusResponse, ShippingAddress

class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

class OrderItem(BaseModel): 
    order_id : int
    product_id : int
    quantity : int
    price : int

    model_config = {"from_attributes" : True}

class Order(BaseModel):
    id : int
    user_id : int
    shipping_address_id :int
    total_price : float
    status : OrderStatus
    created_at : datetime
    items : list[OrderItem]
    shippingstatus : ShippingStatusResponse
    shippingaddress : ShippingAddress

    model_config = {"from_attributes" : True}