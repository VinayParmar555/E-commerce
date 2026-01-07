from pydantic import BaseModel

class CategoryBase(BaseModel):
    name:str

class CategoryCreate(CategoryBase):
    id:int