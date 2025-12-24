from fastapi import APIRouter,HTTPException, Depends
from sqlalchemy.orm import Session
from app.deps.db import get_db
from app.schema.user import UserOut
from app.deps.auth import get_current_user
from app.services.user_service import change_password_process, reset_password_process, verify_rtoken
from app.db.models.user import Users

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/me", response_model=UserOut)
def me(user = Depends(get_current_user)):
    return user

@router.put("/change-password")
def change_password(old_password: str, new_password: str, db: Session = Depends(get_db), user:Users = Depends(get_current_user)):
    result = change_password_process(db, user, old_password, new_password)
    if not result:
        raise HTTPException(status_code=400, detail="Incorrect old password")
    return result

@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    result = reset_password_process(db, email)
    if not result:
        raise HTTPException(status_code=400, detail="Email not registered")
    return result

@router.post("/set-password")
def set_new_password(new_password:str, token:str, db: Session = Depends(get_db)):
    result = verify_rtoken(db, token, new_password)
    if result is False:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    if result is None:
        raise HTTPException(status_code=404, detail="user not found")
    return result