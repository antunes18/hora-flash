from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

SQL_ALCHEMY_DATABASE_URL = os.getenv("DB_URL")


engine = create_engine(
    SQL_ALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()
