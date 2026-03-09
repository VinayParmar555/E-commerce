from pydantic import BaseModel, Field

class CategoryBase(BaseModel):
    name:str = Field(..., min_length=1, max_length=100)

class CategoryCreate(CategoryBase):
    id:int