from sqlalchemy.orm import Session
from app.models import Institution as InstitutionModel
from app.schemas import InstitutionCreate

def create_institution(db: Session, institution: InstitutionCreate):
    try:
        db_institution = InstitutionModel(
            name=institution.name,
            country=institution.country,
            state=institution.state,
            city=institution.city,
            latitude=institution.latitude,
            longitude=institution.longitude
        )
        db.add(db_institution)
        db.commit()
        db.refresh(db_institution)
        return db_institution
    except Exception as e:
        db.rollback()
        raise e

def get_institution(db: Session, institution_id: int):
    return db.query(InstitutionModel).filter(InstitutionModel.id == institution_id).first()

def get_institutions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(InstitutionModel).offset(skip).limit(limit).all()

def update_institution(db: Session, institution_id: int, institution_data: dict):
    db_institution = get_institution(db, institution_id)
    if not db_institution:
        return None
    for key, value in institution_data.items():
        setattr(db_institution, key, value)
    # Add validation for coordinate range
    if 'coordinates' in institution_data:
        if not (-90 <= institution_data['coordinates'] <= 90):
            raise ValueError("Coordinates must be between -90 and 90")
    db.commit()
    db.refresh(db_institution)
    return db_institution

def delete_institution(db: Session, institution_id: int):
    db_institution = get_institution(db, institution_id)
    if not db_institution:
        return None
    db.delete(db_institution)
    db.commit()
    return db_institution