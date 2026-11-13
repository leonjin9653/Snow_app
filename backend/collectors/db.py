import os

import psycopg
from dotenv import load_dotenv

from collectors.snow_report import SnowReport

load_dotenv() 


def connect() -> psycopg.Connection:
    return psycopg.connect(os.environ["DATABASE_URL"])


def get_resort_id(conn, slug: str) -> int:
    row = conn.execute("SELECT id FROM resorts WHERE slug = %s", (slug,)).fetchone()
    if row is None:
        raise ValueError(f"No resort with slug {slug!r}. Did you run seed.sql?")
    return row[0]


def save_scrape_run(conn, resort_id, source, started_at, finished_at, status, error_message=None) -> int:
    row = conn.execute(
        """
        INSERT INTO scrape_runs (resort_id, source, started_at, finished_at, status, error_message)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
        """,
        (resort_id, source, started_at, finished_at, status, error_message),
    ).fetchone()
    return row[0]


def save_snow_report(conn, report: SnowReport, resort_id: int, scrape_run_id: int) -> None:
    conn.execute(
        """
        INSERT INTO snow_reports (
            resort_id, scrape_run_id, scraped_at, reported_at, status,
            base_depth_cm, new_snow_24h_cm, new_snow_7d_cm,
            runs_open, runs_total, lifts_open, lifts_total
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            resort_id, scrape_run_id, report.scraped_at, report.reported_at, report.status.value,
            report.base_depth_cm, report.new_snow_24h_cm, report.new_snow_7d_cm,
            report.runs_open, report.runs_total, report.lifts_open, report.lifts_total,
        ),
    )