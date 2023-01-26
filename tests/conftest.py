from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from faker import Faker
from random import randint
import pytest

from app.main import app
from app.models import Base, Product
from app.database import SQLALCHEMY_URL, get_db
from app import schemas

SQLALCHEMY_URL += "_test"

fake = Faker()

engine = create_engine(SQLALCHEMY_URL)

TestSesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSesionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def create_test_products(session: Session):
    def convert(x):
        return Product(**{"name": x[0], "price": x[1], "description": x[2]})

    products = list(
        map(
            convert,
            [[fake.word(), randint(1, 1000), fake.catch_phrase()] for _ in range(10)],
        )
    )

    session.add_all(products)
    session.commit()

    return session.query(Product).all()
