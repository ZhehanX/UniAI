from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import UserCreate, User
from app.models import User as UserModel
from app.crud.user_crud import (
    create_user,
    get_user,
    get_users,
    update_user,
    delete_user
)

router = APIRouter()

@router.post("/users/", response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if the username or email already exists
        # Witch this check we ensure that the username and the email are unique
        existing_user = db.query(UserModel).filter(
            (UserModel.email == user.email) | 
            (UserModel.username == user.username)
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username or email already exists")
        return create_user(db=db, user=user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_users(db=db, skip=skip, limit=limit)

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=User)
def update_existing_user(user_id: int, user_data: dict, db: Session = Depends(get_db)):
    updated_user = update_user(db=db, user_id=user_id, user_data=user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/users/{user_id}")
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = delete_user(db=db, user_id=user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}