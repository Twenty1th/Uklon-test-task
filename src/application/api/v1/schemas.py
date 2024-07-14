from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel

from domain.entities import DriverId, DriverPos


class DriverInfoIn(BaseModel):
    driver_id: DriverId
    driver_pos: DriverPos
    driver_speed: int


class SaveDriverInfoResponse(BaseModel):
    record_id: Optional[int]
    driver_id: DriverId
    status_code: int = 201
    msg: str = "Driver info successfully saved"


class DriverInfoAcceptedResponse(BaseModel):
    driver_id: DriverId
    status_code: int = 202
    msg: str = "Driver information will be saved later"


class ServerErrorResponse(HTTPException):
    status_code: int = 500

    def __init__(self, detail: Optional[str] = "Internal Server Error"):
        super().__init__(
            status_code=self.status_code,
            detail={"err": detail}
        )
