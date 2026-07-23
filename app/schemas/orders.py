from pydantic import BaseModel

class LineItem(BaseModel):
    product_id: str
    quantity: int

class OrderCreateRequest(BaseModel):
    user_id: str
    line_items: list[LineItem]

class OrderCreateResponse(BaseModel):
    order_id: str