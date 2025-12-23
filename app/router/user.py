from fastapi import APIRouter,HTTPException, Depends
from sqlalchemy.orm import Session
from app.deps.db import get_db
from app.schema.user import UserOut
from app.deps.auth import get_current_user
from app.services.user_service import change_password_process, reset_password_process
from app.db.models.user import Users

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/me", response_model=UserOut)
def me(user = Depends(get_current_user)):
    return user

@router.post("/change-password")
def change_password(old_password: str, new_password: str, db: Session = Depends(get_db), user:Users = Depends(get_current_user)):
    changed_password = change_password_process(db, user, old_password, new_password)
    if not changed_password:
        raise HTTPException(status_code=404, detail="Invalid password")
    return changed_password

@router.get("/reset-link")
def reset_link(email: str, db: Session = Depends(get_db)):
    result = reset_password_process(db, email)
    if not result:
        raise HTTPException(status_code=404, detail="Invalid email")
    return result
