import logging
from typing import Annotated

import sqlalchemy
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.repository.postgresql import get_session

router = APIRouter(
    prefix="/healthcheck",
)


@router.get("")
async def healthcheck(
        session: Annotated[AsyncSession, Depends(get_session)],
):
    try:
        async with session.begin():
            await session.execute(text('SELECT 1'))
            return JSONResponse({"status": "ok"})

    except (sqlalchemy.exc.InterfaceError, ConnectionRefusedError):
        logging.error("Failed to connect to database")
        return JSONResponse({"status": "error"}, status_code=500)
