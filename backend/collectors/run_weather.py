import sys
from datetime import datetime, timezone

from collectors import db, weather

MODES = {
    "observations": {"source": "weather_observations", "past_hours": 3, "forecast_hours": 1},
    "forecast": {"source": "weather_forecast", "past_hours": 1, "forecast_hours": 72},
}


def run(mode: str) -> None:
    settings = MODES[mode]

    with db.connect() as conn:
        for resort_id, slug, latitude, longitude in db.get_active_resorts(conn):
            started_at = datetime.now(timezone.utc)

            try:
                data = weather.fetch(latitude, longitude,
                                     settings["past_hours"], settings["forecast_hours"])
                rows = weather.parse(data, fetched_at=started_at)
            except Exception as e:
                db.save_scrape_run(conn, resort_id, settings["source"], started_at,
                                   datetime.now(timezone.utc), "failed", str(e))
                print(f"{slug}: FAILED - {e}")
                continue

            db.save_scrape_run(conn, resort_id, settings["source"], started_at,
                               datetime.now(timezone.utc), "success")

            if mode == "observations":
                past = [o for o in rows if not o.is_forecast]
                db.save_observations(conn, past, resort_id, started_at)
                print(f"{slug}: saved {len(past)} observation rows")
            else:
                future = [o for o in rows if o.is_forecast]
                db.save_forecasts(conn, future, resort_id, started_at)
                print(f"{slug}: saved {len(future)} forecast rows")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "observations"
    if mode not in MODES:
        sys.exit(f"Unknown mode {mode!r}. Use one of: {', '.join(MODES)}")
    run(mode)