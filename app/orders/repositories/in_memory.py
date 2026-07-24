from app.orders.domain import Order
from app.orders.repositories.repository import OrderRepository


class InMemoryOrderRepository(OrderRepository):

    def __init__(self):
        self._orders: dict[str, Order] = {}

    def get(self, order_id: str) -> Order | None:
        return self._orders.get(order_id)

    def save(self, order: Order) -> None:
        self._orders[order.order_id] = order