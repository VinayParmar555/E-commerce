from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schema.user import UserOut, UserCreate
from app.services.auth_service import create_user, authenticate_user, create_tokens
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