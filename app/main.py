from fastapi import FastAPI
from app.health.router import health_router
from app.orders.router import create_orders_router

from app.orders.repository import InMemoryOrderRepository
from app.orders.service import OrderService

app = FastAPI()

order_repository = InMemoryOrderRepository()
order_service = OrderService(order_repository)

app.include_router(health_router)
app.include_router(create_orders_router(order_service), prefix='/orders')