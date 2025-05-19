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
    #This will delete all the Project records associated with the User
    projects = relationship("Project", back_populates="submitter", cascade="all, delete")

class Institution(Base):
    __tablename__ = "institutions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    country = Column(String, nullable=False)
    state = Column(String, nullable=False)
    city = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    projects = relationship("Project", back_populates="institution")

class AITechnology(Base):
    __tablename__ = "ai_technology"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    projects = relationship("ProjectAITechnology", back_populates="ai_technology")

class Project(Base):
    __tablename__ = "projects"
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
    
    institution = relationship("Institution", back_populates="projects")
    submitter = relationship("User", back_populates="projects")
    # By adding cascade="all, delete-orphan", the related ProjectAITechnology records will be automatically delete
    ai_technologies = relationship("ProjectAITechnology", back_populates="project", cascade="all, delete-orphan")

class ProjectAITechnology(Base):
    __tablename__ = "project_ai_technology"
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True)
    ai_technology_id = Column(Integer, ForeignKey("ai_technology.id"), primary_key=True)
    project = relationship("Project", back_populates="ai_technologies")
    ai_technology = relationship("AITechnology", back_populates="projects")