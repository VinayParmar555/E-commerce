from fastapi import APIRouter, Depends
from app.schema.user import UserOut
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/profile", tags=["View Profile"])

@router.get("/me", response_model=UserOut)
def me(user = Depends(get_current_user)):
    return user