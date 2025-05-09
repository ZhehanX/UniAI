from sqlalchemy.orm import Session
from app.models import Project as ProjectModel, ProjectAITechnology
from app.schemas import ProjectCreate
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload
from datetime import datetime
from services.event_service import event_dispatcher, PROJECT_CREATED, PROJECT_UPDATED, PROJECT_DELETED
import asyncio

async def create_project(db: Session, project: ProjectCreate, user_id: int): 
    # Check for existing project with same title
    existing = db.query(ProjectModel).filter(
        ProjectModel.title == project.title
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project with this title already exists"
        )

    try:
        init_date = datetime.strptime(
            project.project_initiation_date, 
            "%d-%m-%Y"
        ).date()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use dd-mm-yyyy."
        )
 
    try:
        db_project = ProjectModel(
            title=project.title,
            short_description=project.short_description,
            full_description=project.full_description,
            institution_id=project.institution_id,
            contact=project.contact,
            url=project.url,
            logo_filename=project.logo_filename,
            status="pending",
            submitted_by=user_id,
            project_initiation_date=init_date
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        
        # Create AI Technology associations
        tech_ids = []
        for ai_tech_id in project.ai_technologies:
            association = ProjectAITechnology(
                project_id=db_project.id,
                ai_technology_id=ai_tech_id
            )
            db.add(association)
            tech_ids.append(ai_tech_id)

        db.commit()
        
        # Dispatch event for Elasticsearch indexing
        await event_dispatcher.dispatch(PROJECT_CREATED, db_project)
        
        return db_project
    except Exception as e:
        db.rollback()
        raise e

def get_projects(db: Session, status: str = None, skip: int = 0, limit: int = 100):
    query = db.query(ProjectModel).options(joinedload(ProjectModel.ai_technologies))
    
    if status:
        query = query.filter(ProjectModel.status == status)
    
    return query.offset(skip).limit(limit).all()

def get_project(db: Session, project_id: int):
    return (
        db.query(ProjectModel)
        .options(joinedload(ProjectModel.ai_technologies))
        .filter(ProjectModel.id == project_id)
        .first()
    )


async def update_project(db: Session, project_id: int, project_data: dict):
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    
    # Handle date conversion if present
    if 'project_initiation_date' in project_data:
        try:
            project_data['project_initiation_date'] = datetime.strptime(
                project_data['project_initiation_date'],
                "%d-%m-%Y"
            ).date()
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid date format. Use dd-mm-yyyy."
            )
    
    for key, value in project_data.items():
        if key not in ['ai_technologies', 'project_initiation_date']:
            setattr(db_project, key, value)
    
    # Update project_initiation_date separately if present
    if 'project_initiation_date' in project_data:
        db_project.project_initiation_date = project_data['project_initiation_date']
    
    if 'ai_technologies' in project_data:
        # Update AI Technology associations
        db.query(ProjectAITechnology).filter(
            ProjectAITechnology.project_id == project_id
        ).delete()
        
        for ai_tech_id in project_data['ai_technologies']:
            association = ProjectAITechnology(
                project_id=project_id,
                ai_technology_id=ai_tech_id
            )
            db.add(association)
    
    db.commit()
    db.refresh(db_project)
    
    # Dispatch event for Elasticsearch updating
    await event_dispatcher.dispatch(PROJECT_UPDATED, db_project)
    
    return db_project

async def delete_project(db: Session, project_id: int):
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    
    db.delete(db_project)
    db.commit()
    
    # Dispatch event for Elasticsearch deletion
    await event_dispatcher.dispatch(PROJECT_DELETED, project_id)
    
    return db_project

def get_projects_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """Get all projects submitted by a specific user"""
    return (
        db.query(ProjectModel)
        .options(joinedload(ProjectModel.ai_technologies))
        .filter(ProjectModel.submitted_by == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )