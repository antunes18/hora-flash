from sqlalchemy import Column, Integer, DateTime, String, Boolean

from api.core.database import Base

class Scheduling(Base):
    __tablename__ = "scheduling"
    id = Column(Integer, primary_key=True, autoincrement=True)
    hour = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)
