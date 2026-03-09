from pydantic import BaseModel, Field
from enum import Enum

class ShippingBase(BaseModel):
    address_line1:str = Field(..., min_length=1, max_length=300)
    address_line2:str | None = Field(None, max_length=300)
    city:str = Field(..., min_length=1, max_length=100)
    postal_code:int
    state:str = Field(..., min_length=1, max_length=100)
    country:str = Field(..., min_length=1, max_length=100)

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