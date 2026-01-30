from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.cache.rate_limit import ip_key, rate_limit, user_key
from app.deps.db import get_db
from app.deps.auth import get_current_user
from app.schema.user import UserOut, UserCreate
from app.services.auth_service import (
    create_user, 
    authenticate_user, 
    create_tokens, 
    verify_refresh_token,  
    email_verification_process,
    verify_email_token
)
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/account", tags=["Account"])

@router.post("/register", response_model=UserOut)
async def register(user:UserCreate, _:None=Depends(rate_limit(3,60,ip_key)), db:Session=Depends(get_db)):
    db_user = create_user(db, user)
    if not db_user:
        raise HTTPException(status_code=400, detail="E-mail already registered")
    return db_user

@router.post("/login")
async def login(form_data:OAuth2PasswordRequestForm=Depends(), _:None=Depends(rate_limit(10,60,ip_key)), db:Session=Depends(get_db)):
    db_user = authenticate_user(db, form_data.username, form_data.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_tokens(db, db_user)
    response = JSONResponse(content={"access_token": token["access_token"]})
    response.set_cookie("refresh_token", token["refresh_token"], httponly=True, secure=True, samesite="lax")
    return response

@router.post("/refresh")
async def refresh(request:Request, _:None=Depends(rate_limit(10,60,ip_key)), db:Session=Depends(get_db)):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Missing refresh token")
    user = verify_refresh_token(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    new_token = create_tokens(db, user)
    response = JSONResponse(content={"msg":"Token refreshed successfully", "access_token":new_token["access_token"]})
    response.set_cookie("refresh_token", new_token["refresh_token"], httponly=True, secure=True, samesite="lax")
    return response

@router.post("/verify-request")
async def send_verification_link(background_tasks:BackgroundTasks, user=Depends(get_current_user), _:None=Depends(rate_limit(5,60,user_key))):
    return email_verification_process(background_tasks, user)

@router.get("/verify")
async def verify_email(token:str, _:None=Depends(rate_limit(5,60,ip_key)), db:Session=Depends(get_db)):
    result = verify_email_token(db, token)
    if result is None:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    if result is False:
        raise HTTPException(status_code=401, detail="user not found or account already verified")
    return {"msg" : "Email verified successfully"}