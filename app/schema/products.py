from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    price: float
    description: str
    quantity: int

class ProductUpdate(ProductBase):
    id : int

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    pass