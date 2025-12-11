from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://postgres:VVii12%40%40@localhost:5432/HONEY"
engine = create_engine(db_url)

session = sessionmaker(autocommit = False,autoflush=False,bind=engine)

from app.db.session import session        #Database dependency

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

