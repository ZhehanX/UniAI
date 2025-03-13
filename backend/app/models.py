# app/models.py
from sqlalchemy import Column, Integer, String, Date, JSON, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False, default='user')
    use_cases = relationship("UseCase", back_populates="submitter", cascade="all, delete")

class Institution(Base):
    __tablename__ = "institutions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    coordinates = Column(Float, nullable=False)
    use_cases = relationship("UseCase", back_populates="institution")

class AITechnology(Base):
    __tablename__ = "ai_technology"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    use_cases = relationship("UseCaseAITechnology", back_populates="ai_technology")

class UseCase(Base):
    __tablename__ = "use_cases"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    short_description = Column(String, nullable=False)
    full_description = Column(JSON, nullable=False)
    contact = Column(String)
    url = Column(String)
    logo_filename = Column(String)
    status = Column(String, nullable=False, default='pending')
    date_created = Column(DateTime, default=datetime.utcnow)
    project_initiation_date = Column(Date)
    institution_id = Column(Integer, ForeignKey("institutions.id"), nullable=False)
    submitted_by = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    
    institution = relationship("Institution", back_populates="use_cases")
    submitter = relationship("User", back_populates="use_cases")
    ai_technologies = relationship("UseCaseAITechnology", back_populates="use_case")

class UseCaseAITechnology(Base):
    __tablename__ = "use_case_ai_technology"
    use_case_id = Column(Integer, ForeignKey("use_cases.id"), primary_key=True)
    ai_technology_id = Column(Integer, ForeignKey("ai_technology.id"), primary_key=True)
    use_case = relationship("UseCase", back_populates="ai_technologies")
    ai_technology = relationship("AITechnology", back_populates="use_cases")