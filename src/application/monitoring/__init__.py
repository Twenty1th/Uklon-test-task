__all__ = [
    'monitoring_router'
]

from fastapi import APIRouter
from .healthcheck import router as healthcheck_router
from .metrics import router as metrics_router

monitoring_router = APIRouter(
    tags=['Monitoring'],
)

monitoring_router.include_router(healthcheck_router)
monitoring_router.include_router(metrics_router)
