# app/routes/use_cases.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.database import get_db
from backend.app.schemas import UseCaseCreate, UseCase
from backend.app.crud import (
    create_usecase,
    get_usecase,
    get_usecases,
    update_usecase,
    delete_usecase
)

router = APIRouter()

@router.post("/usecases/", response_model=UseCase)
def create_new_usecase(usecase: UseCaseCreate, db: Session = Depends(get_db)):
    try:
        return create_usecase(db=db, usecase=usecase)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/usecases/", response_model=List[UseCase])
def read_usecases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_usecases(db=db, skip=skip, limit=limit)



@router.get("/usecases/{usecase_id}", response_model=UseCase)
def read_usecase(usecase_id: int, db: Session = Depends(get_db)):
    db_usecase = get_usecase(db=db, usecase_id=usecase_id)
    if not db_usecase:
        raise HTTPException(status_code=404, detail="Use case not found")
    return db_usecase


@router.put("/usecases/{usecase_id}", response_model=UseCase)
def update_existing_usecase(usecase_id: int, usecase: UseCaseCreate, db: Session = Depends(get_db)):
    updated_usecase = update_usecase(db=db, usecase_id=usecase_id, usecase_data=usecase.model_dump())
    if not updated_usecase:
        raise HTTPException(status_code=404, detail="Use case not found")
    return updated_usecase

@router.delete("/usecases/{usecase_id}")
def delete_existing_usecase(usecase_id: int, db: Session = Depends(get_db)):
    deleted_usecase = delete_usecase(db=db, usecase_id=usecase_id)
    if not deleted_usecase:
        raise HTTPException(status_code=404, detail="Use case not found")
    return {"message": "Use case deleted successfully"}