from fastapi.testclient import TestClient
from fastapi import status
from app.main import app

client = TestClient(app)

# CREATE ORDER

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

def test_create_order_returns_order_id():
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

    body = response.json()

    assert 'order_id' in body
    assert body["order_id"]
    assert isinstance(body["order_id"], str)

def test_create_order_returns_status():
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
    
    body = response.json()

    assert 'status' in body
    assert body["status"]
    assert isinstance(body["status"], str)

def test_create_order_requires_user_id():
    response = client.post(
                "/orders",
                json={
                    "line_items": [
                        {
                            "product_id": "p1",
                            "quantity": 1,
                        }
                    ]
                }
                )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

def test_create_order_requires_possitive_quantity():
    response = client.post(
                "/orders",
                json={
                    "user_id": "u1",
                    "line_items": [
                        {
                            "product_id": "p1",
                            "quantity": -2,
                        }
                    ]
                }
                )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


# READ ORDER


def test_create_order_returns_200_ok():
    create_response = client.post(
        "/orders",
        json={
            "user_id": "u1",
            "line_items": [
                {
                    "product_id": "milk",
                    "quantity": 1
                }
            ]
        }
    )

    order_id = create_response.json()["order_id"]

    get_response = client.get(f"/orders/{order_id}")

    assert get_response.status_code == status.HTTP_200_OK

def test_get_order_returns_order_id():
    create_response = client.post(
        "/orders",
        json={
            "user_id": "u1",
            "line_items": [
                {
                    "product_id": "milk",
                    "quantity": 1
                }
            ]
        }
    )

    order_id = create_response.json()["order_id"]

    get_response = client.get(f"/orders/{order_id}")

    assert get_response.json()["order_id"] == order_id

def test_create_order_is_idempotent():
    first_response = client.post(
            "/orders",
            json={
                "user_id": "u1",
                "line_items": [
                    {
                        "product_id": "milk",
                        "quantity": 1
                    }
                ]
            }
        )
    
    first_response_body = first_response.json()

    second_response = client.post(
                "/orders",
                json={
                    "user_id": "u1",
                    "line_items": [
                        {
                            "product_id": "milk",
                            "quantity": 1
                        }
                    ]
                }
            )
        
    second_response_body = second_response.json()

    assert first_response_body == second_response_body