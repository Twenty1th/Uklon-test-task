import logging
import time
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.responses import JSONResponse

from adapters.repository.postgresql import ENGINE
from application.api import api_router
from application.monitoring import monitoring_router
from adapters.metrics.api.prometheus import api_start_time
from domain.repository.models import Base
from logger import setup_logger
from settings import load_settings, CONFIG

ROUTERS = [
    api_router, monitoring_router
]

setup_logger()
load_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    api_start_time.set(time.time())
    async with ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await ENGINE.dispose()


app = FastAPI(
    lifespan=lifespan
)


@app.post("/reload-config")
async def reload_config():
    try:
        load_settings()
        logging.info(f"Reloading config")
        return JSONResponse(status_code=200, content={"status": "ok"})
    except Exception as e:
        logging.error(e)
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )
    finally:
        logging.debug(f"Config {CONFIG}")


for router in ROUTERS:
    app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        loop="uvloop"
    )
