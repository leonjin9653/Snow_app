# Architecture

*Draft, October 29, 2026. The tech stack and schema below are proposals until confirmed in `DECISIONS.md`. The schema should be revised once the data audit is complete.*

## The big picture

The system has three independent parts that only talk to each other through the database:

```
                    ┌───────────────────────────────┐
                    │   1. COLLECTION (scheduled)    │
                    │                                │
  Resort websites ──►  Scraper adapters (1/resort)   │
  Open-Meteo API ───►  Weather fetcher               │
  Webcams (later) ──►  Busyness estimator            │
                    └───────────────┬────────────────┘
                                    │ writes timestamped rows
                                    ▼
                    ┌───────────────────────────────┐
                    │   2. STORAGE                   │
                    │   PostgreSQL                   │
                    │   resorts, snow_reports,       │
                    │   weather, scrape_runs         │
                    └───────────────┬────────────────┘
                                    │ reads
                                    ▼
                    ┌───────────────────────────────┐
                    │   3. SERVING                   │
                    │   Backend API (FastAPI)        │
                    │   GET /resorts, /resorts/{id}, │
                    │   /rankings (later)            │
                    └───────────────┬────────────────┘
                                    │ JSON over HTTP
                                    ▼
                    ┌───────────────────────────────┐
                    │   Frontend (React + Leaflet)   │
                    │   map, markers, sidebar        │
                    └───────────────────────────────┘
```

**Why split it this way:** scrapers break often, because resort sites change without warning. If collection is separate from serving, a broken scraper never takes the website down. The site keeps showing the last good data, along with its timestamp.

## 1. Collection

### Scraper adapters

- One adapter per resort, because every site is different.
- Each adapter does two things: **fetch** (get the HTML or JSON) and **parse** (turn it into the common format).
- Every adapter returns the same shape, a `SnowReport` object (see below). Nothing downstream needs to know which resort the data came from.
- The raw response is saved too, so parsers can be fixed and old data re-parsed later without losing anything.

```
fetch(resort) -> raw HTML/JSON   ──►   parse(raw) -> SnowReport   ──►   validate   ──►   save
```

### Validation and failure detection

Every scrape is logged in `scrape_runs`, whatever the outcome. A scrape is marked as **failed** or **suspicious** when:

- The request errors or times out
- The parser can't find the expected fields
- The values are impossible (negative depth, more runs open than exist, depth jumped 200 cm overnight)

A failed scrape writes **no** snow report. It never overwrites good data with garbage. Alerting can start simple: a daily summary of failures (for example as a GitHub Actions failure email).

### Weather

- Open-Meteo, queried by each resort's latitude and longitude. Free, no API key.
- Store current conditions and recent snowfall. Forecasts can be fetched live or stored. **Open decision.**

### Schedules

| Source | How often | Why |
|---|---|---|
| Snow reports | 3–4×/day in season | Resorts update about once or twice a day. Polite scraping. |
| Weather | Hourly | Cheap, and the API allows it |
| Webcam busyness (later) | Frequent during operating hours only | See `DECISIONS.md` |

**Proposed scheduler:** GitHub Actions on a cron schedule. It's free, it doesn't need an always-on server, and it fits a project that already lives on GitHub. The alternative is a scheduler inside the backend (APScheduler), but that needs the server to stay awake.

## 2. Storage: draft schema

PostgreSQL. Every snapshot is kept, never overwritten. History is the long-term asset.

```
resorts
  id, slug, name, latitude, longitude, website_url, report_url,
  adapter_name, pricing_url, hours_text, notes, active

snow_reports                -- one row per successful scrape
  id, resort_id, scraped_at, reported_at (resort's own timestamp if given),
  status (open / closed / unknown),
  base_depth_cm, new_snow_24h_cm, new_snow_7d_cm,
  runs_open, runs_total, lifts_open, lifts_total,
  scrape_run_id

weather_observations
  id, resort_id, fetched_at, valid_at,
  temperature_c, precipitation_mm, snowfall_cm, wind_kmh, is_forecast

scrape_runs                 -- one row per attempt, success or failure
  id, resort_id, source, started_at, finished_at,
  status (success / failed / suspicious), error_message, raw_payload_path
```

**Normalization rules (draft):**

- All depths in **cm**, all temperatures in **°C**, all timestamps in **UTC** (converted to Toronto time only for display).
- Store **counts** (`runs_open`, `runs_total`), not percentages. A percentage can always be computed from counts, but not the reverse.
- A field the resort doesn't report is **NULL**, never 0. Zero snow and unknown snow mean different things.

## 3. Serving

### Backend API (FastAPI)

| Endpoint | Returns |
|---|---|
| `GET /resorts` | All resorts with their latest snow report and weather (for map markers) |
| `GET /resorts/{slug}` | Full detail for the sidebar |
| `GET /resorts/{slug}/history` | Time series (later) |
| `GET /rankings?lat=&lon=&weights=` | Personalized ranking (later) |

### Frontend

- React (built with Vite), with Leaflet for the map (free, no API key, OpenStreetMap tiles).
- **Distance from the user:** browser geolocation, computed in the frontend. The MVP shows straight-line distance. Driving time needs a routing service. **Open decision.**
- Weather overlays (later): radar or precipitation tile layers from a free provider. Check current terms before choosing one.

## Hosting (proposal, all free tiers)

| Part | Option | Note |
|---|---|---|
| Frontend | Vercel, Netlify or GitHub Pages | Static site, free |
| Backend | Render or Railway | Free tiers may sleep when idle, so the first load is slow |
| Database | Neon or Supabase (Postgres) | Check free tier storage limits |
| Scheduled jobs | GitHub Actions | Free minutes for public repos |

Check current free-tier terms before committing, because these change often.

## Repo layout (proposal)

```
/
├── CLAUDE.md
├── docs/            PRODUCT.md, ARCHITECTURE.md, ROADMAP.md, DECISIONS.md, data-audit.md
├── backend/
│   ├── app/         FastAPI app, API routes, DB models
│   ├── collectors/  adapters/ (one file per resort), weather.py, validate.py
│   └── tests/       parser tests using saved sample pages
├── frontend/        React + Leaflet app
└── .github/workflows/  scheduled scrape and weather jobs
```

**Testing approach:** save a real copy of each resort's report page in `tests/fixtures/` and test the parser against it. That way parsers can be tested in November, before any hill opens, and a test fails clearly when a site's layout changes.
