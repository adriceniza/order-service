import logging
from typing import Annotated
from fastapi import APIRouter, status, Header, HTTPException
from app.orders.exceptions import OrderNotFound
from app.orders.schemas import OrderCreateRequest, OrderResponse
from app.orders.service import OrderService

logger = logging.getLogger(__name__)

def create_orders_router(service: OrderService) -> APIRouter:
    orders_router = APIRouter(tags=['orders'])

    @orders_router.post('', status_code=status.HTTP_201_CREATED)
    async def create_order(req: OrderCreateRequest, idempotency_key: Annotated[str, Header()]):
        return service.create(idempotency_key, req.user_id, req.line_items)

    @orders_router.get('/{order_id}', status_code=status.HTTP_200_OK)
    async def read_order(order_id: str) -> OrderResponse:
        order = service.get(order_id)

        if order is not None:
            return OrderResponse.from_order(order)

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    @orders_router.post('/{order_id}/pay', status_code=status.HTTP_200_OK)
    async def pay_order(order_id: str, idempotency_key: Annotated[str, Header()]) -> OrderResponse | None:
        logger.info(f"Pay order request for order {order_id}")
        return service.pay(idempotency_key, order_id)

    return orders_router
