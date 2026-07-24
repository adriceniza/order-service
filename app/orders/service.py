from fastapi import HTTPException, status
from app.orders.domain import LineItem, Order
from app.orders.exceptions import OrderNotFound
from app.orders.repository import InMemoryOrderRepository

from app.shared.idempotency.repository import IdempotencyRepository

import logging

logger = logging.getLogger(__name__)


class OrderService:

    def __init__(self, repository: InMemoryOrderRepository, idempotency_repository: IdempotencyRepository[Order]):
        self._repository = repository
        self._idempotency_repository = idempotency_repository

    def get(self, order_id: str) -> Order:
        return self._repository.get(order_id)

    def create(self, idempotency_key: str, user_id: str, line_items: list[LineItem]) -> Order:
        existing = self._idempotency_repository.get(idempotency_key)
        
        if existing is not None:
            return existing.response

        order = Order.create(
            user_id=user_id,
            line_items=line_items,
        )

        self._repository.save(order)

        self._idempotency_repository.save(idempotency_key, order)

        return order

    def pay(self, idempotency_key: str, order_id: str) -> Order:
        existing = self._idempotency_repository.get(idempotency_key)
        logger.info(f"IK: {idempotency_key} - {existing}")

        if existing is not None:
            return existing.response

        order = self._repository.get(order_id)
        if order is None:
            raise OrderNotFound(order_id)

        order.pay()

        self._repository.save(order)

        self._idempotency_repository.save(idempotency_key, order)

        return order