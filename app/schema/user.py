from pydantic import BaseModel, EmailStr

class User(BaseModel): 
    user_id : int
    name : str
    email : EmailStr
    password : str

class UserCreate(User):
    pass

class UserRead(User):
    pass

class UserUpdate(User):
    pass
