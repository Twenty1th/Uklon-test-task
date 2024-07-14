from fastapi import APIRouter
from starlette.responses import JSONResponse

from adapters.metrics.api.prometheus import json_metrics

router = APIRouter(
    prefix="/metrics",
)


@router.get("")
async def metrics():
    return JSONResponse(
        content=json_metrics()
    )