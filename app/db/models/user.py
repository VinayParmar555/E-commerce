from sqlalchemy import String, Integer, Column, DateTime
from app.db.base import Base
from datetime import datetime, timezone

class Users(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(bool = True)
    is_admin = Column(bool = False)
    password = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_verified = Column(bool = False)
    created_at = Column(DateTime(timezone=True), default=lambda : datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda : datetime.now(timezone.utc), onupdate=lambda : datetime.now(timezone.utc))

