from pydantic import BaseModel
from enum import Enum

class ShippingBase(BaseModel):
    address_line1:str
    address_line2:str | None = None
    city:str
    postal_code:int
    state:str
    country:str

class ShippingAddress(ShippingBase):
    id:int
    user_id:int

    model_config = {"from_attributes" : True}

class ShippingStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class ShippingStatusResponse(BaseModel):
    status : ShippingStatus

    model_config = {"from_attributes" : True}