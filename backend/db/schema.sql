
DROP TABLE IF EXISTS weather_observations, snow_reports, scrape_runs, resorts CASCADE;

CREATE TABLE resorts (
    id            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    slug          TEXT NOT NULL UNIQUE,
    name          TEXT NOT NULL,
    latitude      DOUBLE PRECISION NOT NULL,
    longitude     DOUBLE PRECISION NOT NULL,
    website_url   TEXT,
    report_url    TEXT,
    adapter_name  TEXT,
    pricing_url   TEXT,
    hours_text    TEXT,
    notes         TEXT,
    active        BOOLEAN NOT NULL DEFAULT TRUE
);


CREATE TABLE scrape_runs (
    id               BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    resort_id        BIGINT NOT NULL REFERENCES resorts(id),
    source           TEXT NOT NULL,
    started_at       TIMESTAMPTZ NOT NULL,
    finished_at      TIMESTAMPTZ,
    status           TEXT NOT NULL CHECK (status IN ('success', 'failed', 'suspicious')),
    error_message    TEXT,
    raw_payload_path TEXT
);

CREATE TABLE snow_reports (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    resort_id       BIGINT NOT NULL REFERENCES resorts(id),
    scrape_run_id   BIGINT NOT NULL REFERENCES scrape_runs(id),
    scraped_at      TIMESTAMPTZ NOT NULL,
    reported_at     TIMESTAMPTZ,
    status          TEXT NOT NULL CHECK (status IN ('open', 'closed', 'unknown')),
    base_depth_cm   INTEGER,
    new_snow_24h_cm INTEGER,
    new_snow_7d_cm  INTEGER,
    runs_open       INTEGER,
    runs_total      INTEGER,
    lifts_open      INTEGER,
    lifts_total     INTEGER
);

CREATE TABLE weather_observations (
    id                BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    resort_id         BIGINT NOT NULL REFERENCES resorts(id),
    fetched_at        TIMESTAMPTZ NOT NULL,
    valid_at          TIMESTAMPTZ NOT NULL,
    temperature_c     REAL,
    precipitation_mm  REAL,
    snowfall_cm       REAL,
    wind_kmh          REAL,
    is_forecast       BOOLEAN NOT NULL
);