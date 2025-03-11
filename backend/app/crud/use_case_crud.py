# app/crud/use_case_crud.py
from sqlalchemy.orm import Session
from app.models import UseCase as UseCaseModel
from app.schemas import UseCaseCreate

def create_usecase(db: Session, usecase: UseCaseCreate):
    try:
        db_usecase = UseCaseModel(**usecase.model_dump())
        db.add(db_usecase)
        db.commit()
        db.refresh(db_usecase)
        return db_usecase
    except Exception as e:
        db.rollback()
        raise e

def get_usecase(db: Session, usecase_id: int):
    return db.query(UseCaseModel).filter(UseCaseModel.id == usecase_id).first()

def get_usecases(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UseCaseModel).offset(skip).limit(limit).all()


def update_usecase(db: Session, usecase_id: int, usecase_data: dict):
    db_usecase = get_usecase(db, usecase_id)
    if not db_usecase:
        return None
    for key, value in usecase_data.items():
        setattr(db_usecase, key, value)
    db.commit()
    db.refresh(db_usecase)
    return db_usecase

def delete_usecase(db: Session, usecase_id: int):
    db_usecase = get_usecase(db, usecase_id)
    if not db_usecase:
        return None
    db.delete(db_usecase)
    db.commit()
    return db_usecase