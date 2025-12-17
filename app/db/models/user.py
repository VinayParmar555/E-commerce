from sqlalchemy import String, Integer, Column, DateTime, Boolean, func
from app.db.base import Base

class Users(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True,index=True, nullable=False)
    is_active = Column(Boolean, server_default=func.true(), nullable=False)
    is_admin = Column(Boolean, server_default=func.false(), nullable=False)
    hashed_password = Column(String, nullable=False)
    is_verified = Column(Boolean, server_default=func.false(), nullable=False)
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        server_onupdate=func.now(), 
        nullable=False
    )

