from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import database
from app import hash_utils
from app import models
from app import oauth2
from app import schemas

router = APIRouter(tags=["Auth"])


@router.post("/login", response_model=schemas.TokenOut)
def login_customer(
    data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    db: Session = Depends(database.get_db),
):
    customer = (
        db.query(models.Customer).filter(models.Customer.email == data.username).first()
    )
    if not customer or not (hash_utils.verify(data.password, customer.password)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials"
        )
    access_token = oauth2.create_access_token({"customer_id": customer.customer_id})
    return {"access_token": access_token, "token_type": "bearer"}
