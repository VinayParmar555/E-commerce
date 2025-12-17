from pydantic import BaseModel
from datetime import datetime

class RefreshTokenCreate(BaseModel):

    id : int
    user_id : int
    token : str
    expires_at : datetime
    created_at : datetime

class RefreshTokenRead(RefreshTokenCreate):
    pass
