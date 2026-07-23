from pydantic import BaseModel, PositiveInt

class LineItem(BaseModel):
    product_id: str
    quantity: PositiveInt

class OrderCreateRequest(BaseModel):
    user_id: str
    line_items: list[LineItem]

class OrderCreateResponse(BaseModel):
    order_id: str
    status: str