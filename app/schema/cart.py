from pydantic import BaseModel

class CartItem(BaseModel):
    quantity : int
    product_id : int

class CartOut(CartItem):
    user_id : int

class CartRead(CartOut):
    id : int
    total_price : float
    price : float