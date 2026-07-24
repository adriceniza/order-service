from dataclasses import dataclass
from uuid import uuid4

from app.orders.exceptions import CancelledOrderCannotBePaid, OrderAlreadyPaid, ShippedOrderCannotBePaid

class OrderStatus(str):
    CREATED = "created"
    PAID = "paid"
    SHIPPED = "shipped"
    CANCELLED = "cancelled"

@dataclass
class LineItem:
    product_id: str
    quantity: str

@dataclass
class Order:
    order_id: str
    user_id: str
    line_items: list["LineItem"]
    status: str

    @classmethod
    def create(cls, user_id: str, line_items: list["LineItem"]):
        return cls(
            order_id= "order_" + str(uuid4()),
            user_id=user_id,
            line_items=line_items,
            status=OrderStatus.CREATED
        )

    def pay(self) -> None:
        if self.status == OrderStatus.CANCELLED:
            raise CancelledOrderCannotBePaid(self.order_id)

        if self.status == OrderStatus.SHIPPED:
            raise ShippedOrderCannotBePaid(self.order_id)

        if self.status == OrderStatus.PAID:
            raise OrderAlreadyPaid(self.order_id)

        self.status = OrderStatus.PAID

        return