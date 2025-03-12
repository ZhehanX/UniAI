from sqlalchemy.orm import Session
from app.models import AITechnology as AITechnologyModel
from app.schemas import AITechnologyCreate

def create_ai_technology(db: Session, ai_tech: AITechnologyCreate):
    try:
        db_ai_tech = AITechnologyModel(name=ai_tech.name)
        db.add(db_ai_tech)
        db.commit()
        db.refresh(db_ai_tech)
        return db_ai_tech
    except Exception as e:
        db.rollback()
        raise e

def get_ai_technology(db: Session, ai_tech_id: int):
    return db.query(AITechnologyModel).filter(AITechnologyModel.id == ai_tech_id).first()

def get_ai_technologies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AITechnologyModel).offset(skip).limit(limit).all()

def update_ai_technology(db: Session, ai_tech_id: int, ai_tech_data: dict):
    db_ai_tech = get_ai_technology(db, ai_tech_id)
    if not db_ai_tech:
        return None
    for key, value in ai_tech_data.items():
        setattr(db_ai_tech, key, value)
    db.commit()
    db.refresh(db_ai_tech)
    return db_ai_tech

def delete_ai_technology(db: Session, ai_tech_id: int):
    db_ai_tech = get_ai_technology(db, ai_tech_id)
    if not db_ai_tech:
        return None
    db.delete(db_ai_tech)
    db.commit()
    return db_ai_tech