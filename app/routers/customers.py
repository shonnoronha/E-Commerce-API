from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app import schemas, models, database, hash_utils, oauth2

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("", response_model=List[schemas.CustomerOut])
def get_all_customers(
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.get_current_customer),
):
    customers = db.query(models.Customer).all()
    return customers


@router.post(
    "", response_model=schemas.CustomerOut, status_code=status.HTTP_201_CREATED
)
def create_customer(
    customer: schemas.CustomerIn, db: Session = Depends(database.get_db)
):
    customer.password = hash_utils.hash_password(customer.password)
    new_customer = models.Customer(**customer.dict())
    try:
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"customer with email {customer.email} already exists",
        )
    return new_customer
