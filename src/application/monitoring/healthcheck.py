from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from adapters.repository.postgresql import database_is_alive

router = APIRouter(
    tags=["Monitoring"]
)


@router.get("/healthcheck")
async def healthcheck():
    if await database_is_alive():
        return JSONResponse({"status": "ok"})
    else:
        return JSONResponse({"status": "error"}, status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
