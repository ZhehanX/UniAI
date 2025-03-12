from sqlalchemy.orm import Session
from app.models import UseCaseAITechnology as UseCaseAITechnologyModel

def create_use_case_ai_technology(db: Session, use_case_id: int, ai_tech_id: int):
    try:
        db_assoc = UseCaseAITechnologyModel(
            use_case_id=use_case_id,
            ai_technology_id=ai_tech_id
        )
        db.add(db_assoc)
        db.commit()
        db.refresh(db_assoc)
        return db_assoc
    except Exception as e:
        db.rollback()
        raise e

def delete_use_case_ai_technology(db: Session, use_case_id: int, ai_tech_id: int):
    db_assoc = db.query(UseCaseAITechnologyModel).filter(
        UseCaseAITechnologyModel.use_case_id == use_case_id,
        UseCaseAITechnologyModel.ai_technology_id == ai_tech_id
    ).first()
    if not db_assoc:
        return None
    db.delete(db_assoc)
    db.commit()
    return db_assoc

def get_use_case_ai_technologies(db: Session, use_case_id: int, skip: int = 0, limit: int = 100):
    return db.query(UseCaseAITechnologyModel).filter(
        UseCaseAITechnologyModel.use_case_id == use_case_id
    ).offset(skip).limit(limit).all()