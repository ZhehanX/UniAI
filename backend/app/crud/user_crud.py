from sqlalchemy.orm import Session
from app.models import User as UserModel
from app.schemas import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: UserCreate):
    try:
        hashed_password = pwd_context.hash(user.password)
        db_user = UserModel(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            role=user.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise e

def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user_data: dict):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    if 'password' in user_data:
        user_data['hashed_password'] = pwd_context.hash(user_data.pop('password'))
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    # Delete associated use cases
    for use_case in db_user.use_cases:
        db.delete(use_case)

    db.delete(db_user)
    db.commit()
    return db_user