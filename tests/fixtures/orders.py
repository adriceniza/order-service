import pytest

from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4

client = TestClient(app)

@pytest.fixture
def base_order_body():
    def _build(
        user_id="u1",
        product_id="p1",
        quantity=1,
    ):
        return {
            "user_id": user_id,
            "line_items": [
                {
                    "product_id": product_id,
                    "quantity": quantity,
                }
            ],
        }

    return _build


@pytest.fixture
def create_order(create_order_headers):
    def _create(body, headers = create_order_headers):
        return client.post(
            "/orders",
            json=body,
            headers=headers
        )
    return _create

@pytest.fixture
def create_order_headers():
    return {
        "Idempotency-Key": str(uuid4())
    }