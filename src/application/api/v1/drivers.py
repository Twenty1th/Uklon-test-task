import logging
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Response, status

from adapters.internal.cache import FallBackQueue
from adapters.metrics.api.prometheus import received_coordinates, db_writes, speed_violations, altitude_anomalies, \
    unique_drivers
from application.api.v1.depends import save_driver_info_use_case, get_last_driver_info_use_case, \
    get_unique_drivers_use_case
from application.api.v1.schemas import SaveDriverInfoResponse, \
    ServerErrorResponse, DriverInfoIn, DriverInfoAcceptedResponse
from domain.entities import DriverInfo
from domain.use_cases.drivers import SaveDriverInfoUseCase, GetLastDriverInfo, GetUniqueDriversUseCase

router = APIRouter(
    prefix="/v1",
    tags=["Drivers"],
)

fallback_queue = FallBackQueue()


@router.post("/driver-geo")
async def handle_driver_info(
        data: DriverInfoIn,
        response: Response,
        background_tasks: BackgroundTasks,
        get_driver_last_info: Annotated[GetLastDriverInfo, Depends(get_last_driver_info_use_case)],
        save_driver_use_case: Annotated[SaveDriverInfoUseCase, Depends(save_driver_info_use_case)],
        unique_drivers_use_case: Annotated[GetUniqueDriversUseCase, Depends(get_unique_drivers_use_case)],
):
    driver_info = DriverInfo(**data.model_dump())

    # Increase received coordinates metrics
    received_coordinates.inc()

    # Increase invalid speed metrics
    if not driver_info.is_valid_speed():
        logging.info(
            f"[Driver {driver_info.driver_id}]: has no valid speed({driver_info.driver_speed})"
        )
        speed_violations.inc()
        driver_info.is_correct = False

    # Increase altitude anomalies metrics
    if not driver_info.is_valid_altitude():
        logging.info(
            f"[Driver {driver_info.driver_id}]: has no valid altitude({driver_info.driver_pos.altitude})"
        )
        altitude_anomalies.inc()
        driver_info.is_correct = False

    try:
        # Check driver distance from last position
        last_driver_info = await get_driver_last_info.execute(driver_id=driver_info.driver_id)
        if last_driver_info and not driver_info.is_valid_distance(last_driver_info):
            logging.info(
                f"[Driver {driver_info.driver_id}]: has no valid distance"
            )
            driver_info.is_correct = False

        # Save driver info
        record_id = await save_driver_use_case.execute(driver_info)

        if not fallback_queue.empty():
            # I do this for ordered insertion, taking into the data
            # that was located while the database was inaccessible
            await fallback_queue.put(driver_info)
            background_tasks.add_task(fallback_queue.dump)
            response.status_code = status.HTTP_202_ACCEPTED
            response_schema = DriverInfoAcceptedResponse(
                driver_id=data.driver_id
            )
        else:
            response.status_code = status.HTTP_201_CREATED
            # Increase db writes metrics
            db_writes.inc()
            response_schema = SaveDriverInfoResponse(
                record_id=record_id,
                driver_id=data.driver_id
            )

        # Set unique drivers metrics
        unique_drivers.set(await unique_drivers_use_case.execute())
        return response_schema

    except ConnectionError:
        await fallback_queue.put(driver_info)
        response.status_code = status.HTTP_202_ACCEPTED
        background_tasks.add_task(fallback_queue.dump)
        return DriverInfoAcceptedResponse(
            driver_id=data.driver_id
        )

    except Exception as e:
        logging.error(e)
        raise ServerErrorResponse()
