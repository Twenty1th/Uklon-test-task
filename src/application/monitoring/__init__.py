__all__ = [
    'monitoring_router'
]

from fastapi import APIRouter
from .healthcheck import router as healthcheck_router

monitoring_router = APIRouter(
    prefix="",
)

monitoring_router.include_router(healthcheck_router)
