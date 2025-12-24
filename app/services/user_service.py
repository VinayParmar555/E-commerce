from sqlalchemy.orm import Session
from app.db.models.user import Users
from app.db.models.refresh_token import RefreshToken
from app.utils.hashing import hash_password, verify_password
from app.utils.jwt_manager import create_password_reset_token, verify_rtoken_and_get_user_id

def change_password_process(db: Session, user:Users, old_password: str, new_password: str):
    password_verification = verify_password(old_password, user.hashed_password)
    if not password_verification:
        return None
    user.hashed_password = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return {"msg" : "Password changed succesfully"}

def reset_password_process(db: Session, email: str):
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        return None
    token = create_password_reset_token(user.id)
    link = f"http://localhost:8000/app/reset-password?token={token}"
    print(link)
    return {"msg" : "reset link sent successfully"}

def verify_rtoken(db: Session, token: str, new_password: str):
    user_id = verify_rtoken_and_get_user_id(token, "reset")
    if not user_id:
        return False
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user: 
        return None
    user.hashed_password = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return {"msg" : "password changed successfully"}

def promote_admin(db: Session, user_id: int):
    user = db.get(Users, user_id)
    if not user:
        return None
    if user.is_admin:
        return False
    user.is_admin = True
    db.commit()
    db.refresh(user)
    return {"msg" : f"{user.name} promoted to admin successfully"}

def revoke_token(db:Session, token: str):
    db_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if not db_token:
        return False
    db_token.revoked = True
    db.commit()
    db.refresh(db_token)
    return True