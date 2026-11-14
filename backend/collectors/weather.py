from datetime import datetime, timezone

import httpx
from pydantic import AwareDatetime, BaseModel

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
HOURLY_VARS = ["temperature_2m", "precipitation", "snowfall", "wind_speed_10m"]


class WeatherObservation(BaseModel):
    valid_at: AwareDatetime
    temperature_c: float | None
    precipitation_mm: float | None
    snowfall_cm: float | None
    wind_kmh: float | None
    is_forecast: bool


def fetch(latitude: float, longitude: float, past_hours: int, forecast_hours: int) -> dict:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ",".join(HOURLY_VARS),
        "timeformat": "unixtime",
        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh",
        "precipitation_unit": "mm",
        "past_hours": past_hours,
        "forecast_hours": forecast_hours,
    }
    headers = {"User-Agent": "snow-app (student project; github.com/leonjin9653/snow_app)"}
    response = httpx.get(OPEN_METEO_URL, params=params, headers=headers, timeout=20)
    response.raise_for_status()
    return response.json()


def parse(data: dict, fetched_at: datetime) -> list[WeatherObservation]:
    hourly = data["hourly"]
    observations = []
    for i, unix_time in enumerate(hourly["time"]):
        valid_at = datetime.fromtimestamp(unix_time, tz=timezone.utc)
        observations.append(
            WeatherObservation(
                valid_at=valid_at,
                temperature_c=hourly["temperature_2m"][i],
                precipitation_mm=hourly["precipitation"][i],
                snowfall_cm=hourly["snowfall"][i],
                wind_kmh=hourly["wind_speed_10m"][i],
                is_forecast=valid_at > fetched_at,
            )
        )
    return observations