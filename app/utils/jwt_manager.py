from jose import jwt
from datetime import datetime, timedelta, timezone
from app.config.settings import settings

def create_access_token(data: dict):
    to_encode = data.copy()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expires_at})

    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        settings.JWT_ALGORITHM
    )
