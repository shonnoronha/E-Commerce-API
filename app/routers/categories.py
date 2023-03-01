from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app import models, database, schemas, oauth2

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=List[schemas.CategoryOut])
def get_all_parent_categories(
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.get_current_customer),
):
    res = (
        db.query(models.Category)
        .filter(models.Category.parent_category_id.is_(None))
        .all()
    )
    return res


@router.get("/all", response_model=List[schemas.CategoryOut])
def get_all_categories(
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.get_current_customer),
):
    return db.query(models.Category).all()


@router.post("", response_model=schemas.CategoryOut)
def create_child_category(
    category: schemas.CategoryIn, db: Session = Depends(database.get_db)
):
    new_category = models.Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category
