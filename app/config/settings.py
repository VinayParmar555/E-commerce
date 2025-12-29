from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    JWT_EMAIL_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    EMAIL_TOKEN_EXPIRE_MINUTES: int
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    
    class Config:
        env_file = ".env"

settings = Settings()
