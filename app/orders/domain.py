from dataclasses import dataclass
from uuid import uuid4


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
            status="created"
        )
