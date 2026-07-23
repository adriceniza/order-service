from fastapi import FastAPI
from app.routers.health import health_router
from app.routers.orders import orders_router

app = FastAPI()

app.include_router(health_router)
app.include_router(orders_router, prefix='/orders')