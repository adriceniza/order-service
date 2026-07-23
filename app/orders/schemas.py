from pydantic import BaseModel, PositiveInt

from app.orders.domain import Order

class LineItem(BaseModel):
    product_id: str
    quantity: PositiveInt

class OrderCreateRequest(BaseModel):
    user_id: str
    line_items: list[LineItem]

class OrderCreateResponse(BaseModel):
    order_id: str
    status: str

class OrderResponse(BaseModel):
    order_id: str
    status: str
    user_id: str
    line_items: list[LineItem]

    @classmethod
    def from_order(cls, order: Order):
        return OrderResponse(
            order_id=order.order_id,
            status=order.status,
            line_items=order.line_items,
            user_id=order.user_id
        )