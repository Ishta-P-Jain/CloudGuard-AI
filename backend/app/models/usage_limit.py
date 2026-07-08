from datetime import date
from sqlalchemy import Column, Integer, Date
from app.database import Base

class UsageLimit(Base):
    __tablename__ = "ai_usage_limits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, unique=True, default=date.today)
    request_count = Column(Integer, default=0)
