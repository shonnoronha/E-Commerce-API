from fastapi.testclient import TestClient


def test_all_products(client: TestClient, create_test_products):
    res = client.get("/products")
    assert len(create_test_products) == len(res.json())
    assert res.status_code == 200
