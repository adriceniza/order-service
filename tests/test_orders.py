from uuid import uuid4

from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.orders.domain import OrderStatus

client = TestClient(app)

# CREATE ORDER

def test_create_order_returns_201_created(create_order, base_order_body):
    response = create_order(base_order_body())
    
    assert response.status_code == status.HTTP_201_CREATED

def test_create_order_returns_order_id(create_order, base_order_body):
    response = create_order(base_order_body())

    body = response.json()

    assert 'order_id' in body
    assert body["order_id"]
    assert isinstance(body["order_id"], str)

def test_create_order_returns_status(create_order, base_order_body):
    response = create_order(base_order_body())
    
    body = response.json()

    assert 'status' in body
    assert body["status"]
    assert isinstance(body["status"], str)

def test_create_order_requires_user_id(create_order, base_order_body):
    response = create_order(base_order_body(user_id=None))

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

def test_create_order_requires_possitive_quantity(create_order, base_order_body):
    response = create_order(base_order_body(quantity=-2))

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


# READ ORDER


def test_create_order_returns_200_ok(create_order, base_order_body):
    create_response = create_order(base_order_body())

    order_id = create_response.json()["order_id"]

    get_response = client.get(f"/orders/{order_id}")

    assert get_response.status_code == status.HTTP_200_OK

def test_get_order_returns_order_id(create_order, base_order_body):
    create_response = create_order(base_order_body())

    order_id = create_response.json()["order_id"]

    get_response = client.get(f"/orders/{order_id}")

    assert get_response.json()["order_id"] == order_id

def test_create_order_is_idempotent(create_order, base_order_body):
    first_response = create_order(base_order_body(), headers={
        "Idempotency-Key": "same-key"
    })
    
    first_response_body = first_response.json()

    second_response = create_order(base_order_body(),headers={
        "Idempotency-Key": "same-key"
    })
        
    second_response_body = second_response.json()

    assert first_response_body == second_response_body

def test_create_order_idempotency_key_is_required(create_order, base_order_body):
    response = create_order(base_order_body(), headers=None)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

# PAY ORDER

def test_pay_order_returns_200(create_order, base_order_body):
    create_response = create_order(base_order_body()).json()

    pay_response = client.post(f'/orders/{create_response["order_id"]}/pay', headers={
        "Idempotency-Key": str(uuid4())
    })

    assert pay_response.status_code == status.HTTP_200_OK

def test_pay_order_returns_status_paid(create_order, base_order_body):
    create_response = create_order(base_order_body()).json()
    pay_response = client.post(f'/orders/{create_response["order_id"]}/pay', headers={
        "Idempotency-Key": str(uuid4())
    }).json()

    assert pay_response["status"] == OrderStatus.PAID

def test_pay_not_found_order_returns_404():
    pay_response = client.post(f'/orders/{str(uuid4())}/pay', headers={
        "Idempotency-Key": str(uuid4())
    })

    assert pay_response.status_code == status.HTTP_404_NOT_FOUND

def test_pay_order_twice_returns_409(create_order, base_order_body):
    create_response = create_order(base_order_body()).json()
    order_id = create_response["order_id"]

    client.post(f'/orders/{order_id}/pay', headers={
        "Idempotency-Key": str(uuid4())
    })

    pay_response = client.post(f'/orders/{order_id}/pay', headers={
        "Idempotency-Key": str(uuid4())
    })

    assert pay_response.status_code == status.HTTP_409_CONFLICT
