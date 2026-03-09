from pydantic import BaseModel, Field

class CartItem(BaseModel):
    quantity : int = Field(..., ge=1)
    product_id : int

class CartOut(CartItem):
    user_id : int

class CartRead(CartOut):
    id : int
    total_price : float
    price : float