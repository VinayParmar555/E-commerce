from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings

engine = create_engine(settings.DATABASE_URL)

session = sessionmaker(autocommit = False,autoflush=False,bind=engine)

#Database dependency
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

