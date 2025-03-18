# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from pydantic import computed_field, PrivateAttr, model_validator, field_validator
from app.models import UseCaseAITechnology

class UserBase(BaseModel):
    username: str
    email: str
    role: Optional[str] = "user"

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: str
    model_config = {"from_attributes": True}

class InstitutionBase(BaseModel):
    name: str
    country: str
    state: str
    city: str
    latitude: float 
    longitude: float

class InstitutionCreate(InstitutionBase):
    pass

class Institution(InstitutionBase):
    id: int
    model_config = {"from_attributes": True}

class AITechnologyBase(BaseModel):
    name: str

class AITechnologyCreate(AITechnologyBase):
    pass

class AITechnology(AITechnologyBase):
    id: int
    model_config = {"from_attributes": True}

class UseCaseBase(BaseModel):
    title: str
    short_description: str
    full_description: dict
    project_initiation_date: str
    institution_id: int
    ai_technologies: List[int]

class UseCaseCreate(BaseModel):
    title: str
    short_description: str
    full_description: dict
    project_initiation_date: str
    institution_id: int
    ai_technologies: List[int] = []
    contact: Optional[str] = None
    url: Optional[str] = None
    logo_filename: Optional[str] = None
    status: str = "pending"

class UseCase(BaseModel):
    id: int
    title: str
    short_description: str
    full_description: dict
    institution_id: int
    contact: Optional[str] = None
    url: Optional[str] = None
    logo_filename: Optional[str] = None
    status: str
    submitted_by: int
    project_initiation_date: str  # Will be dd-mm-yyyy format
    date_created: datetime  # Will include time
    ai_technologies: List[int]
    

    
    @field_validator('project_initiation_date', mode='before')
    @classmethod
    def parse_date(cls, value):
        """Convert date object from DB to dd-mm-yyyy string"""
        if isinstance(value, date):
            return value.strftime("%d-%m-%Y")
        return value

    @field_validator('ai_technologies', mode='before')
    @classmethod
    def extract_tech_ids(cls, value):
        """Convert SQLAlchemy relationships to list of IDs"""
        if value and isinstance(value[0], UseCaseAITechnology):
            return [tech.ai_technology_id for tech in value]
        return value
 
    model_config = {"from_attributes": True}