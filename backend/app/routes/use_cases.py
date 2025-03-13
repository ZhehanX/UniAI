from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import UseCaseCreate, UseCase
from app.crud import use_case_crud, institutions_crud, ai_technology_crud
from fastapi import Depends, HTTPException, status
from app.routes.auth import get_current_user
from app.models import User
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

router = APIRouter()

@router.post("/use-cases/", response_model=UseCase, dependencies=[Security(get_current_user)])
def create_new_use_case(
    use_case: UseCaseCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return use_case_crud.create_use_case(db=db, use_case=use_case, user_id=current_user.id)

@router.get("/use-cases/", response_model=List[UseCase])
def read_use_cases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return use_case_crud.get_use_cases(db=db, skip=skip, limit=limit)

@router.get("/use-cases/{use_case_id}", response_model=UseCase)
def read_use_case(use_case_id: int, db: Session = Depends(get_db)):
    db_use_case = use_case_crud.get_use_case(db, use_case_id)
    if not db_use_case:
        raise HTTPException(status_code=404, detail="Use case not found")
    return db_use_case

@router.put("/use-cases/{use_case_id}", response_model=UseCase, dependencies=[Security(get_current_user)])
def update_use_case(use_case_id: int, use_case_data: UseCaseCreate, db: Session = Depends(get_db)):
    updated_use_case = use_case_crud.update_use_case(
        db=db, 
        use_case_id=use_case_id, 
        use_case_data=use_case_data.model_dump()
    )
    if not updated_use_case:
        raise HTTPException(status_code=404, detail="Use case not found")
    return updated_use_case

@router.delete("/use-cases/{use_case_id}", dependencies=[Security(get_current_user)])
def delete_use_case(use_case_id: int, db: Session = Depends(get_db)):
    deleted_use_case = use_case_crud.delete_use_case(db=db, use_case_id=use_case_id)
    if not deleted_use_case:
        raise HTTPException(status_code=404, detail="Use case not found")
    return {"message": "Use case deleted successfully"}