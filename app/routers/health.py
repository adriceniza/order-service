from fastapi import APIRouter, status
from app.schemas.health import HealthResponse

health_router = APIRouter()

@health_router.get('/health', tags=['health'], status_code=status.HTTP_200_OK)
def health() -> HealthResponse:
    return { "status": "ok" }