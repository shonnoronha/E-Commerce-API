from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from faker import Faker
from random import randint, choice
import pytest

from app.main import app
from app.models import Base, Product
from app.database import SQLALCHEMY_URL, get_db
from app.oauth2 import create_access_token
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


@pytest.fixture
def create_test_user(client: TestClient):
    user_creds = {
        "name": "tester",
        "email": "test@example.com",
        "address": "heaven",
        "password": "password",
    }
    res = client.post("/customers", json=user_creds)
    assert res.status_code == 201
    return {**res.json()}


@pytest.fixture
def create_test_user2(client):
    user_creds = {
        "name": "tester2",
        "email": "test2@example.com",
        "address": "heaven",
        "password": "password",
    }
    res = client.post("/customers", json=user_creds)
    assert res.status_code == 201
    return {**res.json()}


@pytest.fixture
def token(create_test_user):
    return create_access_token({"customer_id": create_test_user["customer_id"]})


@pytest.fixture
def authorized_client(client: TestClient, token):
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture()
def create_test_products(session: Session, create_test_user, create_test_user2):
    def convert(x):
        return Product(
            **{
                "name": x[0],
                "price": x[1],
                "description": x[2],
                "customer_id": x[3],
            }
        )

    products = list(
        map(
            convert,
            [
                [
                    fake.word(),
                    randint(1, 1000),
                    fake.catch_phrase(),
                    choice(
                        [
                            create_test_user["customer_id"],
                            create_test_user2["customer_id"],
                        ]
                    ),
                ]
                for _ in range(10)
            ],
        )
    )

    session.add_all(products)
    session.commit()

    return session.query(Product).all()
