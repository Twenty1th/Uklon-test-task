import logging
from typing import Annotated

from fastapi import APIRouter
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


@router.post(
    "/driver-geo",
    response_model=SaveDriverInfoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def handle_driver_info(
        data: DriverInfoIn,
        use_case: Annotated[
            SaveDriverInfoUseCase, Depends(save_driver_info_use_case)
        ]
):
    try:
        record_id = await use_case.execute(
            DriverInfo(**data.model_dump())
        )
        return SaveDriverInfoResponse(
            record_id=record_id,
            driver_id=data.driver_id,
            status_code=200,
            msg="Driver info successfully saved",
        )

    except Exception as e:
        logging.error(e, exc_info=True)
        raise ServerErrorResponse()
