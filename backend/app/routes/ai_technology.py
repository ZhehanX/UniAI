from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import AITechnology, AITechnologyCreate
from app.crud.ai_technology_crud import (
    create_ai_technology,
    get_ai_technology,
    get_ai_technologies,
    update_ai_technology,
    delete_ai_technology
)

router = APIRouter()

#create new AI technology
@router.post("/ai-technologies/", response_model=AITechnology)
def create_new_ai_technology(ai_tech: AITechnologyCreate, db: Session = Depends(get_db)):
    try:
        return create_ai_technology(db=db, ai_tech=ai_tech)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

#get all AI technologies
@router.get("/ai-technologies/", response_model=List[AITechnology])
def read_ai_technologies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_ai_technologies(db=db, skip=skip, limit=limit)

#get AI technology by ID
@router.get("/ai-technologies/{ai_tech_id}", response_model=AITechnology)
def read_ai_technology(ai_tech_id: int, db: Session = Depends(get_db)):
    db_ai_tech = get_ai_technology(db=db, ai_tech_id=ai_tech_id)
    if not db_ai_tech:
        raise HTTPException(status_code=404, detail="AI Technology not found")
    return db_ai_tech

#update AI technology
@router.put("/ai-technologies/{ai_tech_id}", response_model=AITechnology)
def update_ai_technology_endpoint(ai_tech_id: int, ai_tech_data: dict, db: Session = Depends(get_db)):
    updated_ai_tech = update_ai_technology(db=db, ai_tech_id=ai_tech_id, ai_tech_data=ai_tech_data)
    if not updated_ai_tech:
        raise HTTPException(status_code=404, detail="AI Technology not found")
    return updated_ai_tech

#delete AI technology
@router.delete("/ai-technologies/{ai_tech_id}")
def delete_ai_technology_endpoint(ai_tech_id: int, db: Session = Depends(get_db)):
    deleted_ai_tech = delete_ai_technology(db=db, ai_tech_id=ai_tech_id)
    if not deleted_ai_tech:
        raise HTTPException(status_code=404, detail="AI Technology not found")
    return {"message": "AI Technology deleted successfully"}