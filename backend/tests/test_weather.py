import json
from datetime import datetime, timezone
from pathlib import Path

from collectors.weather import parse

FIXTURE = Path(__file__).parent / "fixtures" / "open_meteo_moonstone.json"


def load():
    return json.loads(FIXTURE.read_text())


def test_one_observation_per_hour():
    data = load()
    obs = parse(data, datetime.now(timezone.utc))
    assert len(obs) == len(data["hourly"]["time"])


def test_timestamps_are_utc_and_in_order():
    obs = parse(load(), datetime.now(timezone.utc))
    assert all(o.valid_at.tzinfo == timezone.utc for o in obs)
    assert [o.valid_at for o in obs] == sorted(o.valid_at for o in obs)


def test_past_vs_forecast_split():
    data = load()
    pivot = datetime.fromtimestamp(data["hourly"]["time"][23], tz=timezone.utc)
    obs = parse(data, fetched_at=pivot)
    assert sum(not o.is_forecast for o in obs) == 24
    assert sum(o.is_forecast for o in obs) == len(obs) - 24