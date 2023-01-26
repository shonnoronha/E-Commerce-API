from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app import schemas, models, database

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("", response_model=List[schemas.CustomerOut])
def get_all_customers(db: Session = Depends(database.get_db)):
    customers = db.query(models.Customer).all()
    return customers


@router.post("", response_model=schemas.CustomerOut)
def create_customer(
    customer: schemas.CustomerIn, db: Session = Depends(database.get_db)
):
    new_customer = models.Customer(**customer.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer
