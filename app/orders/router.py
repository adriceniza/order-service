from fastapi import APIRouter, status
from app.orders.schemas import OrderCreateRequest
orders_router = APIRouter()

@orders_router.post('', tags=['orders'], status_code=status.HTTP_201_CREATED)
async def create_order(req: OrderCreateRequest):
    return {
        "order_id": "ord_123",
        "status": "created"
    }