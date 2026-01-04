from pydantic import BaseModel

class CartOut(BaseModel):
    id : int
    user_id : int
    product_id : int