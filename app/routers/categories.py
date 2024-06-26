from typing import List

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app import database
from app import models
from app import oauth2
from app import schemas

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/{category_id}/products", response_model=List[schemas.ProductOut])
def get_customers_products(
    category_id: int,
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.is_customer_admin),
):
    products = (
        db.query(
            models.Product.product_id,
            models.Product.name.label("product_name"),
            models.Product.description,
            models.Product.quantity,
            models.Product.price,
            models.Category.name.label("category_name"),
            models.Category.category_id,
            models.Product.created_at,
        )
        .join(
            models.productCategory,
            models.Product.product_id == models.productCategory.product_id,
            isouter=True,
        )
        .join(
            models.Category,
            models.Category.category_id == models.productCategory.category_id,
            isouter=True,
        )
        .filter(models.productCategory.category_id == category_id)
        .all()
    )
    return products


@router.get("", response_model=List[schemas.CategoryOut])
def get_all_parent_categories(
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.is_customer_admin),
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
    category: schemas.CategoryIn,
    db: Session = Depends(database.get_db),
    customer: schemas.CustomerOut = Depends(oauth2.is_customer_admin),
):
    new_category = models.Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category
