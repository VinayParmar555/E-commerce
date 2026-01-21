from pydantic import BaseModel

class ShippingAddress(BaseModel):
    id:int
    user_id:int
    address_line1:str
    address_line2:str | None = None
    city:str
    postal_code:int
    state:str
    country:str