from pydantic import BaseModel

class ProductBase(BaseModel):
    id: int
    name: str
    price: float
    description: str
    quantity: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

