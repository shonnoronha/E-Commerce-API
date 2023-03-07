from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import database
from app import models
from app import oauth2
from app import schemas
from app import utils

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("", response_model=List[schemas.CustomerOut])
def get_all_customers(
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.is_customer_admin),
):
    customers = db.query(models.Customer).all()
    return customers


@router.post(
    "", response_model=schemas.CustomerOut, status_code=status.HTTP_201_CREATED
)
def create_customer(
    customer: schemas.CustomerIn, db: Session = Depends(database.get_db)
):
    customer.password = utils.hash_password(customer.password)
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
