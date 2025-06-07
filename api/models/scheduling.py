from sqlalchemy import Column, Integer, DateTime, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from api.core.database import Base

class Scheduling(Base):
    __tablename__ = "scheduling"
    id = Column(Integer, primary_key=True, autoincrement=True)
    hour = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    user_id = Column(ForeignKey("users.id"))
    user = relationship("User", back_populates="scheduling")
    is_deleted = Column(Boolean, default=False)
