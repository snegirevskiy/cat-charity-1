from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime

from app.core.base import Base


class CharityProject(Base):
    __tablename__ = 'charityproject'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime, nullable=True)
