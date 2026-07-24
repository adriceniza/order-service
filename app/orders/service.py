from fastapi import HTTPException, status
from app.orders.domain import LineItem, Order
from app.orders.repository import InMemoryOrderRepository
from uuid import uuid4

from app.shared.idempotency.repository import IdempotencyRepository

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


        new_order_id = "order_" + str(uuid4())

        order = Order(
            order_id=new_order_id,
            user_id=user_id,
            line_items=line_items,
            status="creted"
        )

        self._repository.save(order)

        self._idempotency_repository.save(idempotency_key, order)

        return order