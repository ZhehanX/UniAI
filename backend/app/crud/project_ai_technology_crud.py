from sqlalchemy.orm import Session
from app.models import ProjectAITechnology as ProjectAITechnologyModel

def create_project_ai_technology(db: Session, project_id: int, ai_tech_id: int):
    try:
        db_assoc = ProjectAITechnologyModel(
            project_id=project_id,
            ai_technology_id=ai_tech_id
        )
        db.add(db_assoc)
        db.commit()
        db.refresh(db_assoc)
        return db_assoc
    except Exception as e:
        db.rollback()
        raise e

def delete_project_ai_technology(db: Session, project_id: int, ai_tech_id: int):
    db_assoc = db.query(ProjectAITechnologyModel).filter(
        ProjectAITechnologyModel.project_id == project_id,
        ProjectAITechnologyModel.ai_technology_id == ai_tech_id
    ).first()
    if not db_assoc:
        return None
    db.delete(db_assoc)
    db.commit()
    return db_assoc

def get_project_ai_technologies(db: Session, project_id: int, skip: int = 0, limit: int = 100):
    return db.query(ProjectAITechnologyModel).filter(
        ProjectAITechnologyModel.project_id == project_id
    ).offset(skip).limit(limit).all()