from sqlalchemy.orm import Session
from app.models import UseCase as UseCaseModel, UseCaseAITechnology
from app.schemas import UseCaseCreate
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload
from datetime import datetime

def create_use_case(db: Session, use_case: UseCaseCreate, user_id: int): 
    # Check for existing use case with same title
    existing = db.query(UseCaseModel).filter(
        UseCaseModel.title == use_case.title
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Use case with this title already exists"
        )

    try:
        init_date = datetime.strptime(
            use_case.project_initiation_date, 
            "%d-%m-%Y"
        ).date()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid date format. Use dd-mm-yyyy."
        )
 
    try:
        db_use_case = UseCaseModel(
            title=use_case.title,
            short_description=use_case.short_description,
            full_description=use_case.full_description,
            institution_id=use_case.institution_id,
            contact=use_case.contact,
            url=use_case.url,
            logo_filename=use_case.logo_filename,
            status="pending",
            submitted_by=user_id,
            project_initiation_date=init_date
        )
        db.add(db_use_case)
        db.commit()
        db.refresh(db_use_case)
        
        # Create AI Technology associations
        tech_ids = []
        for ai_tech_id in use_case.ai_technologies:
            association = UseCaseAITechnology(
                use_case_id=db_use_case.id,
                ai_technology_id=ai_tech_id
            )
            db.add(association)
            tech_ids.append(ai_tech_id)

        db.commit()
        return db_use_case
    except Exception as e:
        db.rollback()
        raise e

def get_use_cases(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(UseCaseModel)
        .options(joinedload(UseCaseModel.ai_technologies))
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_use_case(db: Session, use_case_id: int):
    return (
        db.query(UseCaseModel)
        .options(joinedload(UseCaseModel.ai_technologies))
        .filter(UseCaseModel.id == use_case_id)
        .first()
    )


def update_use_case(db: Session, use_case_id: int, use_case_data: dict):
    db_use_case = get_use_case(db, use_case_id)
    if not db_use_case:
        return None
    
    # Handle date conversion if present
    if 'project_initiation_date' in use_case_data:
        try:
            use_case_data['project_initiation_date'] = datetime.strptime(
                use_case_data['project_initiation_date'],
                "%d-%m-%Y"
            ).date()
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid date format. Use dd-mm-yyyy."
            )
    
    for key, value in use_case_data.items():
        if key not in ['ai_technologies', 'project_initiation_date']:
            setattr(db_use_case, key, value)
    
    # Update project_initiation_date separately if present
    if 'project_initiation_date' in use_case_data:
        db_use_case.project_initiation_date = use_case_data['project_initiation_date']
    
    if 'ai_technologies' in use_case_data:
        # Update AI Technology associations
        db.query(UseCaseAITechnology).filter(
            UseCaseAITechnology.use_case_id == use_case_id
        ).delete()
        
        for ai_tech_id in use_case_data['ai_technologies']:
            association = UseCaseAITechnology(
                use_case_id=use_case_id,
                ai_technology_id=ai_tech_id
            )
            db.add(association)
    
    db.commit()
    db.refresh(db_use_case)
    return db_use_case

def delete_use_case(db: Session, use_case_id: int):
    db_use_case = get_use_case(db, use_case_id)
    if not db_use_case:
        return None
    
    db.delete(db_use_case)
    db.commit()
    return db_use_case