from pydantic import BaseModel, EmailStr
from datetime import datetime

class User(BaseModel): 
    name : str
    email : EmailStr

class UserCreate(User):
    password : str

class UserOut(User):
    id : int
    is_active : bool = True
    is_admin : bool = False
    is_verified : bool = False
    created_at : datetime 
    updated_at : datetime