from app.orders.domain import LineItem, Order
from app.orders.repository import InMemoryOrderRepository
from uuid import uuid4

class OrderService:

    def __init__(self, repository: InMemoryOrderRepository):
        self._repository = repository

    def get(self, order_id: str) -> Order:
        return self._repository.get(order_id)

    def create(self, user_id: str, line_items: list[LineItem]) -> Order:
        new_order_id = "order_" + str(uuid4())

        order = Order(
            order_id=new_order_id,
            user_id=user_id,
            line_items=line_items,
            status="creted"
        )

        self._repository.save(order)
        return order