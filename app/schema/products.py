from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    price: float
    description: str
    quantity: int

class ProductUpdate(ProductBase):
    id : int

class ProductCreate(ProductBase):
    category_id : int | None = None

class ProductRead(ProductBase):
    category : str | None