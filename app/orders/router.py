from fastapi import APIRouter, status
from app.orders.schemas import OrderCreateRequest
orders_router = APIRouter(tags=['orders'])

@orders_router.post('', status_code=status.HTTP_201_CREATED)
async def create_order(req: OrderCreateRequest):
    return {
        "order_id": "ord_123",
        "status": "created"
    }

@orders_router.get('/{order_id}', status_code=status.HTTP_200_OK)
async def read_order(order_id):
    return