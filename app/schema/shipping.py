from pydantic import BaseModel

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
