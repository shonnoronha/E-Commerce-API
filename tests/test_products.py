from fastapi.testclient import TestClient


def test_all_products(authorized_client: TestClient, create_test_products):
    res = authorized_client.get("/products")
    assert len(create_test_products) == len(res.json())
    assert res.status_code == 200


def test_unauthorized_client(client: TestClient, create_test_products):
    res = client.get("/products")
    assert res.status_code == 401


def test_unauthorized_single_product(client: TestClient, create_test_products):
    res = client.get(f"/products/{create_test_products[0].product_id}")
    assert res.status_code == 401


def test_single_product_not_exist(authorized_client: TestClient):
    res = authorized_client.get("/products/2222")
    assert res.status_code == 404


def test_single_product_authorized_customer(
    authorized_client: TestClient, create_test_products
):
    product = create_test_products[0]
    res = authorized_client.get(f"/products/{product.product_id}")
    res_product = res.json()
    assert res_product.get("product_id") == product.product_id
    assert res_product.get("name") == product.name
    assert res_product.get("description") == product.description
    assert res.status_code == 200
