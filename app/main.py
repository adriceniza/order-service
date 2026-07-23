from fastapi import FastAPI
from app.health.router import health_router
from app.orders.router import orders_router

app = FastAPI()

app.include_router(health_router)
app.include_router(orders_router, prefix='/orders')