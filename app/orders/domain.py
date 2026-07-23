from dataclasses import dataclass


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