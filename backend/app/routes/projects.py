from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import ProjectCreate, Project
from app.crud import project_crud, institutions_crud, ai_technology_crud
from fastapi import Depends, HTTPException, status
from app.routes.auth import get_current_user
from app.models import User
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

router = APIRouter()

# create new project
@router.post("/projects/", response_model=Project, dependencies=[Security(get_current_user)])
async def create_new_project(
    project: ProjectCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await project_crud.create_project(db=db, project=project, user_id=current_user.id)

# get all projects
@router.get("/projects/", response_model=List[Project])
def read_projects(status=None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return project_crud.get_projects(db=db, status=status, skip=skip, limit=limit)

# get projects by user id
@router.get("/projects/user/{user_id}", response_model=List[Project])
def read_projects_by_user(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all projects submitted by a specific user"""
    return project_crud.get_projects_by_user(db=db, user_id=user_id, skip=skip, limit=limit)

# get project by id
@router.get("/projects/{project_id}", response_model=Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = project_crud.get_project(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

# update project
@router.put("/projects/{project_id}", response_model=Project, dependencies=[Security(get_current_user)])
async def update_project(
    project_id: int, 
    project_data: ProjectCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated_project = await project_crud.update_project(
        db=db, 
        project_id=project_id, 
        project_data=project_data.model_dump()
    )
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project

# delete project
@router.delete("/projects/{project_id}", dependencies=[Security(get_current_user)])
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    deleted_project = await project_crud.delete_project(db=db, project_id=project_id)
    if not deleted_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}