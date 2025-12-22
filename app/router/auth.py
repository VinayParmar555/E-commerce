from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schema.user import UserOut, UserCreate
from app.services.auth_service import (
    create_user, 
    authenticate_user, 
    create_tokens, 
    verify_refresh_token,  
    email_verification_process)
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/account", tags=["Account"])

@router.post("/register", response_model=UserOut)
def register(user : UserCreate, db:Session = Depends(get_db)):
    db_user = create_user(db, user)
    if db_user is False:
        raise HTTPException(status_code=400, detail="E-mail already registered")
    return db_user

@router.post("/login")
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = authenticate_user(db, form_data.username, form_data.password)
    if db_user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_tokens(db, db_user)
    response = JSONResponse(content={"access_token": token["access_token"]})
    response.set_cookie("refresh_token", token["refresh_token"], httponly=True, secure=True, samesite="lax")
    return response

@router.post("/refresh")
def refresh(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    user = verify_refresh_token(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    return create_tokens(db, user)
