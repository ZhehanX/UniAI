# app/models.py
from sqlalchemy import Column, Integer, String, Date, JSON, ARRAY
from app.database import Base

class UseCase(Base):
    __tablename__ = "use_cases"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    short_description = Column(String, nullable=False)
    full_description = Column(String)
    institution = Column(String, nullable=False)
    ai_technologies = Column(ARRAY(String))
    contact = Column(String)
    url = Column(String)