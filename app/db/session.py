from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings

connect_args = {
    "sslmode": "require"
}

hostaddr = settings.DATABASE_HOSTADDR
if hostaddr:
    connect_args["hostaddr"] = hostaddr

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args
)

session = sessionmaker(autocommit = False, autoflush=False, bind=engine)