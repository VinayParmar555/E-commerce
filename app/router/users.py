from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schema.user import UserOut, UserCreate
from app.services.auth_service import create_user

router = APIRouter(prefix="/account", tags=["Account"])

@router.post("/register", response_model=UserOut)
def register(user : UserCreate, db:Session = Depends(get_db)):
    db_user = create_user(db, user)
    if db_user is False:
        raise HTTPException(status_code=400, detail="E-mail already registered")
    return db_user

# @router.delete("/")
# def delete(email : str, db: Session = Depends(get_db)):
#     db_user = delete_user(db, email)
#     if db_user is False:
#         raise HTTPException(status_code=400, detail="E-mail already registered")
#     return db_user