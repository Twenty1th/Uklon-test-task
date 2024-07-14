import time

from prometheus_client import Counter, Gauge
from domain.entities import DriverId


api_start_time = Gauge(
    "api_start_time",
    "Time when the api started"
)
received_coordinates = Counter(
    "received_coordinates",
    "Total number of coordinates received"
)
unique_drivers = Gauge(
    "unique_drivers",
    "Total number of unique drivers"
)
speed_violations = Counter(
    "speed_violations",
    "Total number of speed violations"
)
altitude_anomalies = Counter(
    "altitude_anomalies",
    "Total number of altitude_limit anomalies"
)
db_writes = Counter(
    "db_writes", "Total number of writes to the database"
)


def json_metrics() -> dict:
    return {
        "lifetime": float(time.time() - api_start_time._value.get()),
        "unique_drivers": unique_drivers._value.get(),
        "speed_violations": speed_violations._value.get(),
        "altitude_anomalies": altitude_anomalies._value.get(),
        "db_writes": db_writes._value.get(),
        "received_coordinates": received_coordinates._value.get(),
    }
