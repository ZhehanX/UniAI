# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class UseCaseBase(BaseModel):
    title: str
    short_description: str
    full_description: str
    institution: str
    ai_technologies: List[str]
    contact: str
    url: str

class UseCaseCreate(UseCaseBase):
    pass

class UseCase(UseCaseBase):
    id: int

    # Pydantic v2 syntax for ORM mode
    model_config = {
        "from_attributes": True
    }