from passlib.context import CryptContext

from app import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def convert_to_dict(product: models.Product):
    product_dict = dict(product.__dict__)
    product_dict["product_name"] = product_dict["name"]
    del product_dict["name"]
    del product_dict["_sa_instance_state"]
    return product_dict
