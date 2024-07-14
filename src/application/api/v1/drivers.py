import asyncio
import logging
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks
from fastapi import Depends, status

from application.api.v1.depends import save_driver_info_use_case
from application.api.v1.schemas import SaveDriverInfoResponse, \
    ServerErrorResponse, DriverInfoIn
from domain.entities import DriverInfo
from domain.use_cases.save_driver_info import SaveDriverInfoUseCase

router = APIRouter(
    prefix="/v1",
    tags=["Drivers"],
)

fallback_queue: asyncio.Queue[DriverInfo] = asyncio.Queue()


async def dump_fallback_queue(
        use_case: Annotated[
            SaveDriverInfoUseCase, Depends(save_driver_info_use_case)
        ]
) -> None:
    while fallback_queue.qsize() > 0:
        async with asyncio.timeout(delay=10):
            try:
                data: DriverInfo = await fallback_queue.get()
                await use_case.execute(data)
                fallback_queue.task_done()

            except (asyncio.CancelledError, asyncio.TimeoutError):
                return

            except ConnectionError:
                return

            except Exception as e:
                logging.error(e)
                return


@router.post(
    "/driver-geo",
    response_model=SaveDriverInfoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def handle_driver_info(
        data: DriverInfoIn,
        background_tasks: BackgroundTasks,
        use_case: Annotated[
            SaveDriverInfoUseCase, Depends(save_driver_info_use_case)
        ]
):
    driver_info = DriverInfo(**data.model_dump())
    try:
        record_id = await use_case.execute(driver_info)
        if not fallback_queue.empty():
            background_tasks.add_task(dump_fallback_queue)
        return SaveDriverInfoResponse(
            record_id=record_id,
            driver_id=data.driver_id,
            status_code=status.HTTP_201_CREATED,
            msg="Driver info successfully saved",
        )

    except ConnectionError:
        await fallback_queue.put(driver_info)
        return SaveDriverInfoResponse(
            record_id=None,
            driver_id=data.driver_id,
            status_code=status.HTTP_202_ACCEPTED,
            msg="Driver information will be saved later",
        )

    except Exception as e:
        logging.error(e, exc_info=True)
        raise ServerErrorResponse()
