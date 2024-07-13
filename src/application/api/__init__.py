from fastapi import APIRouter
from .v1.drivers import router as drivers_router


api_router = APIRouter(
    prefix="/api",
)

api_router.include_router(drivers_router)