from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone

class User(BaseModel): 
    id : int
    name : str
    email : EmailStr
    is_active : bool = True
    is_admin : bool = False
    password : str
    hashed_password : str
    is_verified : bool = False
    created_at : datetime = Field(default_factory=lambda : datetime.now(timezone.utc))
    updated_at : datetime = Field(default_factory=lambda : datetime.now(timezone.utc))

class UserCreate(User):
    pass

class UserOut(User):
    pass
