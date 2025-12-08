from sqlalchemy import String, Integer, Column
from app.db.base import Base


class Users(Base):

    __tablename__ = "Users"

    user_id = Column(Integer, primary_key=True, nullable=False),
    name = Column(String, nullable=False),
    email = Column(String, nullable=False, unique=True)

