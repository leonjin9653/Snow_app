from pydantic import BaseModel, AwareDatetime
from enum import Enum

class ResortStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"
    UNKNOWN = "unknown"


class SnowReport(BaseModel):

    """One resort's snow report, as parsed by an adapter.

    Units: cm. Timestamps: UTC. Values the resort doesn't report are None, never 0.
    Sanity checks (negative values, runs_open > runs_total, etc.) live in validate.py.
    """

    resort_slug: str
    status: ResortStatus
    scraped_at: AwareDatetime
    reported_at: AwareDatetime | None = None
    base_depth_cm: int | None = None
    new_snow_24h_cm : int | None = None
    new_snow_7d_cm : int | None = None 
    runs_open : int | None = None
    runs_total : int | None = None
    lifts_open : int | None = None
    lifts_total : int | None = None


