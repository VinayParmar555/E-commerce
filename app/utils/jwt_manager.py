from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.config.settings import settings

def create_access_token(data: dict):
    to_encode = data.copy()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expires_at})

    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

def decode_token(token: str):
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None
    
def create_email_verification_token(user_id: int):
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.EMAIL_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub" : str(user_id), "type":"verify", "exp":expires}
    return jwt.encode(to_encode, settings.JWT_EMAIL_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def verify_token(token: str):
    payload = jwt.decode(token, settings.JWT_EMAIL_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    if not payload:
        return False
    return {"msg" : "Email verified successfully"}