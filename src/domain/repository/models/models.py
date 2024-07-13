import datetime

from sqlalchemy import Column, Integer, BigInteger
from sqlalchemy.orm import Mapped, declarative_base

Base = declarative_base()


class DriverInfo(Base):
    __tablename__ = "driver_info"

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    driver_id: Mapped[int]
    driver_speed: Mapped[int]
    latitude: Mapped[float]
    longitude: Mapped[float]
    altitude: Mapped[float]
    created_at = Column(BigInteger,
                        default=datetime.datetime.now(datetime.UTC))
    is_correct: Mapped[bool]

    def __repr__(self):
        return (f"<DriverInfo(record_id='%s', "
                f"driver_id='%s' "
                f"latitude='%s', "
                f"longitude='%s', "
                f"altitude='%s', "
                f"created_at='%s', "
                f"is_correct='%s')>"
                ) % (self.record_id,
                     self.driver_id,
                     self.latitude,
                     self.longitude,
                     self.altitude,
                     self.created_at,
                     self.is_correct)
