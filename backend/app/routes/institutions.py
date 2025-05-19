from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import InstitutionCreate, Institution
from app.crud.institutions_crud import (
    create_institution,
    get_institution,
    get_institutions,
    update_institution,
    delete_institution
)

router = APIRouter()

# create new institution
@router.post("/institutions/", response_model=Institution)
def create_new_institution(institution: InstitutionCreate, db: Session = Depends(get_db)):
    try:
        return create_institution(db=db, institution=institution)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# get all institutions
@router.get("/institutions/", response_model=List[Institution])
def read_institutions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_institutions(db=db, skip=skip, limit=limit)

# get institution by ID
@router.get("/institutions/{institution_id}", response_model=Institution)
def read_institution(institution_id: int, db: Session = Depends(get_db)):
    db_institution = get_institution(db=db, institution_id=institution_id)
    if not db_institution:
        raise HTTPException(status_code=404, detail="Institution not found")
    return db_institution

# update institution
@router.put("/institutions/{institution_id}", response_model=Institution)
def update_institution_endpoint(institution_id: int, institution_data: dict, db: Session = Depends(get_db)):
    updated_institution = update_institution(db=db, institution_id=institution_id, institution_data=institution_data)
    if not updated_institution:
        raise HTTPException(status_code=404, detail="Institution not found")
    return updated_institution

# delete institution
@router.delete("/institutions/{institution_id}")
def delete_institution_endpoint(institution_id: int, db: Session = Depends(get_db)):
    deleted_institution = delete_institution(db=db, institution_id=institution_id)
    if not deleted_institution:
        raise HTTPException(status_code=404, detail="Institution not found")
    return {"message": "Institution deleted successfully"}