from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from api.core.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    number = Column(Integer, unique=True, nullable=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, unique=False, nullable=False)
    role = Column(String, unique=False, nullable=False)
    disabled = Column(Boolean, default=False)
    scheduling = relationship("Scheduling", back_populates="user")
