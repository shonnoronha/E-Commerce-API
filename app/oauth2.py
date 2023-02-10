from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app import models, schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.access_token_expire_minutes)


def create_access_token(data: dict):
    encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({"exp": expire})
    encoded_jwt = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    """
    return customer_id if the token is valid
    raises excetion if the token is invalid
    """
    try:
        data: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = data.get("customer_id")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return id


def get_current_customer(token=Depends(oauth2_scheme), db: Session = Depends(get_db)):
    customer_id = verify_access_token(token)
    customer = (
        db.query(models.Customer)
        .filter(models.Customer.customer_id == customer_id)
        .first()
    )
    return schemas.CustomerOut(**vars(customer))
