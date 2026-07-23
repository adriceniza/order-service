from fastapi.testclient import TestClient
from fastapi import status
from app.main import app

client = TestClient(app)

def test_create_order_returns_201_created():
    response = client.post(
        "/orders",
        json={
            "user_id": "u1",
            "line_items": [
                {
                    "product_id": "p1",
                    "quantity": 1,
                }
            ]
        }
        )
    
    assert response.status_code == status.HTTP_201_CREATED