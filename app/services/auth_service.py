from sqlalchemy.orm import Session
from app.schema.user import UserCreate
from app.db.models.user import Users
from app.utils.hashing import hash_password

def create_user(db:Session, user: UserCreate):
    check_existing_user = db.query(Users).filter(Users.email == user.email).first()
    if check_existing_user:
        return False
    new_user = Users(
        name = user.name,
        email = user.email,
        hashed_password = hash_password(user.password),
        is_verified = False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# def delete_user(db: Session, email : str):
#     db_user = db.query(Users).filter(Users.email == email).first()
#     if not db_user:
#         return False
#     db.delete(db_user)
#     db.commit()
#     return {"detail" : "User Deleted"}