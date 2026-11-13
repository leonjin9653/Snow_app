from datetime import datetime, timezone

from collectors import db
from collectors.adapters import moonstone


def scrape(adapter) -> None:
    started_at = datetime.now(timezone.utc)

    with db.connect() as conn:
        resort_id = db.get_resort_id(conn, adapter.SLUG)

        try:
            html = adapter.fetch()
            report = adapter.parse(html, scraped_at=started_at)
        except Exception as e:
            db.save_scrape_run(conn, resort_id, "snow_report", started_at,
                               datetime.now(timezone.utc), "failed", str(e))
            print(f"{adapter.SLUG}: FAILED - {e}")
            return

        run_id = db.save_scrape_run(conn, resort_id, "snow_report", started_at,
                                    datetime.now(timezone.utc), "success")
        db.save_snow_report(conn, report, resort_id, run_id)
        print(f"{adapter.SLUG}: saved {report}")


if __name__ == "__main__":
    scrape(moonstone)