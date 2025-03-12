# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional

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
    address: str

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

class UseCaseCreate(UseCaseBase):
    contact: Optional[str] = None
    url: Optional[str] = None
    logo_filename: Optional[str] = None

class UseCase(UseCaseBase):
    id: int
    status: str
    date_created: str
    submitted_by: int
    model_config = {"from_attributes": True}