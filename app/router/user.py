from fastapi import APIRouter,HTTPException, Depends, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.cache.rate_limit import ip_key, rate_limit, user_key
from app.deps.db import get_db
from app.schema.user import UserOut
from app.deps.auth import get_current_user
from app.services.user_service import (
    change_password_process, 
    reset_password_process, 
    verify_rtoken, 
    promote_admin, 
    revoke_token
)
from app.db.models.user import Users

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/me", response_model=UserOut)
async def me(user=Depends(get_current_user), _:None=Depends(rate_limit(10,60,user_key))):
    return user

@router.put("/change-password")
async def change_password(old_password:str, new_password:str, user:Users=Depends(get_current_user), _:None=Depends(rate_limit(5,60,user_key)), db:Session=Depends(get_db)):
    result = change_password_process(db, user, old_password, new_password)
    if not result:
        raise HTTPException(status_code=400, detail="Incorrect old password")
    return {"msg" : "Password changed succesfully"}

@router.post("/forgot-password")
async def forgot_password(email:str, background_tasks:BackgroundTasks, _:None=Depends(rate_limit(3,60,ip_key)), db:Session=Depends(get_db)):
    result = reset_password_process(db, email, background_tasks)
    if not result:
        raise HTTPException(status_code=400, detail="Email not registered")
    return {"msg" : "reset link sent successfully"}

@router.post("/set-password")
async def set_new_password(new_password:str, token:str, _:None=Depends(rate_limit(5,60,ip_key)), db:Session=Depends(get_db)):
    result = verify_rtoken(db, token, new_password)
    if result is False:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    if result is None:
        raise HTTPException(status_code=404, detail="user not found")
    return {"msg" : "password changed successfully"}

@router.post("/make-admin")
async def make_admin(user_id:int, current_user:Users=Depends(get_current_user), _:None=Depends(rate_limit(3,60,user_key)), db:Session=Depends(get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    result = promote_admin(db, user_id)
    if result is None:
        raise HTTPException(status_code=404, detail="user not found")
    if result is False:
        raise HTTPException(status_code=400, detail="user is already admin")
    return {"msg" : f"user {user_id} promoted to admin successfully"}

@router.post("/logout")
async def logout(request:Request, db:Session=Depends(get_db)):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="not logged in")
    revoked = revoke_token(db, token)
    if not revoked:
        raise HTTPException(status_code=404, detail="refresh token not found")
    response = JSONResponse(content={"detail" : "Logged out successfully"})
    response.delete_cookie("refresh_token")
    response.delete_cookie("access_token")
    return response