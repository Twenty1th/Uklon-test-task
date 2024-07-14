from fastapi import APIRouter
from starlette.responses import JSONResponse

from adapters.metrics.api.prometheus import json_metrics

router = APIRouter(
    tags=["Monitoring"]
)


@router.get("/metrics")
async def metrics():
    return JSONResponse(
        content=json_metrics()
    )