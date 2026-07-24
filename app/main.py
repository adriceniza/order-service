from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.health.router import health_router
from app.orders.domain import Order
from app.orders.exceptions import OrderNotFound, ShippedOrderCannotBePaid, OrderAlreadyPaid, CancelledOrderCannotBePaid
from app.orders.router import create_orders_router

from app.orders.repository import InMemoryOrderRepository
from app.shared.idempotency.in_memory import InMemoryIdempotencyRepository
from app.orders.service import OrderService

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('log.txt'),
        logging.StreamHandler()
    ]
)

app = FastAPI()

idempotency_respository = InMemoryIdempotencyRepository[Order]()
order_repository = InMemoryOrderRepository()

order_service = OrderService(order_repository, idempotency_respository)

app.include_router(health_router)
app.include_router(create_orders_router(order_service), prefix='/orders')

## Exceptions

@app.exception_handler(OrderNotFound)
async def order_not_found_handler(request: Request,exc: Exception):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
        "detail": f"Order '{exc.order_id}' not found"
    })


@app.exception_handler(ShippedOrderCannotBePaid)
async def shipped_order_cannot_be_paid_handler(request: Request,exc: Exception):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={
        "detail": f"Order '{exc.order_id}' cannot be paid because it's shipped"
    })


@app.exception_handler(CancelledOrderCannotBePaid)
async def cancelled_order_cannot_be_paid_handler(request: Request,exc: Exception):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={
        "detail": f"Order '{exc.order_id}' cannot be paid because it's cancelled"
    })


@app.exception_handler(OrderAlreadyPaid)
async def order_already_paid_handler(request: Request,exc: Exception):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={
        "detail": f"Order '{exc.order_id}' is already paid"
    })