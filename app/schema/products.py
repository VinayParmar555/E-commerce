from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    price: float = Field(..., gt=0)
    description: str = Field(..., min_length=1, max_length=1000)
    quantity: int = Field(..., ge=0)

class ProductUpdate(ProductBase):
    id : int

class ProductCreate(ProductBase):
    category_id : int | None = None

class ProductRead(ProductBase):
    category : str | None