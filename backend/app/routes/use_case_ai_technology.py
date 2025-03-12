from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import AITechnology
from app.crud import use_case_crud
from app.crud import (
    use_case_ai_technology_crud,
    ai_technology_crud
)


router = APIRouter()

@router.post("/use-cases/{use_case_id}/ai-technologies/{ai_tech_id}", response_model=AITechnology)
def add_ai_tech_to_use_case(use_case_id: int, ai_tech_id: int, db: Session = Depends(get_db)):
    try:
        # Verify both entities exist
        use_case = use_case_crud.get_use_case(db, use_case_id)
        if not use_case:
            raise HTTPException(status_code=404, detail="Use Case not found")
            
        ai_tech = ai_technology_crud.get_ai_technology(db, ai_tech_id)
        if not ai_tech:
            raise HTTPException(status_code=404, detail="AI Technology not found")
        
        # Check if association already exists
        existing_assoc = db.query(UseCaseAITechnologyModel).filter(
            UseCaseAITechnologyModel.use_case_id == use_case_id,
            UseCaseAITechnologyModel.ai_technology_id == ai_tech_id
        ).first()
        if existing_assoc:
            raise HTTPException(status_code=400, detail="AI Technology already associated with this use case")
        
        # Create association
        association = use_case_ai_technology_crud.create_use_case_ai_technology(
            db, use_case_id, ai_tech_id
        )
        return ai_tech
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/use-cases/{use_case_id}/ai-technologies/{ai_tech_id}")
def remove_ai_tech_from_use_case(use_case_id: int, ai_tech_id: int, db: Session = Depends(get_db)):
    deleted = use_case_ai_technology_crud.delete_use_case_ai_technology(
        db, use_case_id, ai_tech_id
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Association not found")
    return {"message": "AI Technology removed from use case"}

@router.get("/use-cases/{use_case_id}/ai-technologies/", response_model=List[AITechnology])
def get_use_case_ai_techs(use_case_id: int, db: Session = Depends(get_db)):
    associations = use_case_ai_technology_crud.get_use_case_ai_technologies(db, use_case_id)
    return [assoc.ai_technology for assoc in associations]