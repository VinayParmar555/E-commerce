from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.models.user import Users
from app.utils.jwt_manager import decode_token
from app.deps.db import get_db

oauth_scheme = OAuth2PasswordBearer(tokenUrl="account/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth_scheme)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    user_id = int(payload.get("sub"))
    user = db.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user