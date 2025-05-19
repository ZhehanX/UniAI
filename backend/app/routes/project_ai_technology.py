from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import AITechnology
from app.models import ProjectAITechnology as ProjectAITechnologyModel
from app.crud import (
    project_ai_technology_crud,
    ai_technology_crud,
    project_crud
)


router = APIRouter()

# create new project AI technology association
@router.post("/projects/{project_id}/ai-technologies/{ai_tech_id}", response_model=AITechnology)
def add_ai_tech_to_project(project_id: int, ai_tech_id: int, db: Session = Depends(get_db)):
    try:
        # Verify both entities exist
        project = project_crud.get_project(db, project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
            
        ai_tech = ai_technology_crud.get_ai_technology(db, ai_tech_id)
        if not ai_tech:
            raise HTTPException(status_code=404, detail="AI Technology not found")
        
        # Check if association already exists
        existing_assoc = db.query(ProjectAITechnologyModel).filter(
            ProjectAITechnologyModel.project_id == project_id,
            ProjectAITechnologyModel.ai_technology_id == ai_tech_id
        ).first()
        if existing_assoc:
            raise HTTPException(status_code=400, detail="AI Technology already associated with this project")
        
        # Create association
        association = project_ai_technology_crud.create_project_ai_technology(
            db, project_id, ai_tech_id
        )
        return ai_tech
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# remove AI technology from project
@router.delete("/projects/{project_id}/ai-technologies/{ai_tech_id}")
def remove_ai_tech_from_project(project_id: int, ai_tech_id: int, db: Session = Depends(get_db)):
    deleted = project_ai_technology_crud.delete_project_ai_technology(
        db, project_id, ai_tech_id
    )
    if not deleted:
        raise HTTPException(status_code=404, detail="Association not found")
    return {"message": "AI Technology removed from project"}

# get all AI technologies for a project
@router.get("/projects/{project_id}/ai-technologies/", response_model=List[AITechnology])
def get_project_ai_techs(project_id: int, db: Session = Depends(get_db)):
    associations = project_ai_technology_crud.get_project_ai_technologies(db, project_id)
    return [assoc.ai_technology for assoc in associations]