from sqlalchemy.orm import Session
from app.db.models.user import Users
from app.utils.hashing import hash_password, verify_password

def change_password_process(db: Session, user:Users, old_password: str, new_password: str):
    password_verification = verify_password(old_password, user.hashed_password)
    if not password_verification:
        return None
    user.hashed_password = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return {"msg" : "Password changed succesfully"}