from abc import abstractmethod

from app.orders.domain import Order

class OrderRepository:

    @abstractmethod
    def get(self, order_id: str) -> Order | None:
        pass

    @abstractmethod
    def save(self, order: Order) -> None:
        pass