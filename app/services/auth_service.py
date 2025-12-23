from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.schema.user import UserCreate
from app.db.models.user import Users
from app.db.models.refresh_token import RefreshToken
from app.utils.hashing import hash_password, verify_password
from app.utils.jwt_manager import (
    create_access_token, 
    decode_token, 
    verify_token_and_get_user_id, 
    create_email_verification_token
)
from datetime import datetime, timedelta, timezone
from app.config.settings import settings
from app.db.session import get_db
import uuid

def create_user(db:Session, user: UserCreate):
    check_existing_user = db.query(Users).filter(Users.email == user.email).first()
    if check_existing_user:
        return False
    new_user = Users(
        name = user.name,
        email = user.email,
        hashed_password = hash_password(user.password),
        is_verified = False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, email: str, password: str):
    db_user = db.query(Users).filter(Users.email == email).first()
    if not db_user or not verify_password(password, db_user.hashed_password):
        return None
    return db_user

def create_tokens(db: Session, user: Users):
    access_token = create_access_token(data={"sub" : str(user.id)})
    refresh_token_str = str(uuid.uuid4())
    expires = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = RefreshToken(
        user_id = user.id,
        token = refresh_token_str,
        expires_at = expires
    )
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)
    return{
        "access_token" : access_token,
        "refresh_token" : refresh_token_str,
        "token" : "bearer"
    }

def verify_refresh_token(db: Session, token: str):
    db_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if db_token and not db_token.revoked:
        expires = db_token.expires_at
        if expires > datetime.now(timezone.utc):
            db_user = db.query(Users).filter(Users.id == db_token.user_id).first()
            return db_user
    return None

def email_verification_process(user: Users):
    token = create_email_verification_token(user.id)
    link = f"http://localhost:8000/app/verify?token={token}"
    print (f"Verify your email: {link}")
    return {"msg" : "email verification link sent"}

def verify_email_token(db: Session, token: str):
    user_id = verify_token_and_get_user_id(token, "verify")
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    db_user = db.query(Users).filter(Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.is_verified = True
    db.commit()
    db.refresh(db_user)
    return {"msg" : "Email verified successfully"}