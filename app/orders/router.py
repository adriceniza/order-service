from typing import Annotated
from fastapi import APIRouter, status, Header, HTTPException
from app.orders.schemas import OrderCreateRequest, OrderResponse
from app.orders.service import OrderService

def create_orders_router(service: OrderService) -> APIRouter:
    orders_router = APIRouter(tags=['orders'])

    @orders_router.post('', status_code=status.HTTP_201_CREATED)
    async def create_order(req: OrderCreateRequest, idempotency_key: Annotated[str, Header()]):
        return service.create(idempotency_key, req.user_id, req.line_items)

    @orders_router.get('/{order_id}', status_code=status.HTTP_200_OK)
    async def read_order(order_id: str) -> OrderResponse:
        order = service.get(order_id)

        return OrderResponse.from_order(order)

    return orders_router