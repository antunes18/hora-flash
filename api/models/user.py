from sqlalchemy import Column, Integer, String, Boolean
from api.core.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, unique=True, nullable=False)
    disabled = Column(Boolean, default=False)
