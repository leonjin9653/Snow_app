# Roadmap

*Last updated: October 29, 2026. Hard target: a deployed public MVP by **November 30, 2026**, ready to collect data the day hills open.*

## Guiding rules

- Build one thin slice that works end to end before going wide: one resort, scraped → stored → served → shown on the map.
- Ship something deployed and public early. A live link on a resume beats a polished local project.
- Each phase ends with something that works.
- Midterms and coursework come first. Each week has a "minimum" so a bad week doesn't derail the plan.

---

## Phase 0: Foundations (Oct 29 – Nov 4)

- [ ] Make the decisions marked "needed by Phase 0" in `DECISIONS.md` (D1–D3 done; D4 open)
- [x] Create the GitHub repo, add these docs, set up the folder structure
- [x] Data audit for all 12 resorts, off-season pass (`docs/data-audit.md`). Re-check in December.
- [ ] Build the resort seed file: name, coordinates, URLs, hours, pricing link
- [ ] Open-Meteo script: fetch weather for 3 resorts with Python

**Minimum:** repo exists, audit done for the 3 resorts you'll scrape first.

## Phase 1: Data pipeline (Nov 5 – Nov 11)

- [ ] Set up Postgres (local first, hosted later). Write the schema in SQL by hand.
- [ ] Define the common `SnowReport` format
- [ ] Write scraper adapters for **3 resorts**, tested against saved pages
- [ ] Validation + `scrape_runs` logging
- [ ] Weather fetcher writing to the database

**Minimum:** 1 adapter + weather writing to the database.

## Phase 2: Backend API (Nov 12 – Nov 15)

- [ ] FastAPI app with `GET /resorts` and `GET /resorts/{slug}`
- [ ] Queries that join each resort with its latest report and weather

**Minimum:** `GET /resorts` returns real data from the database.

## Phase 3: Frontend map (Nov 16 – Nov 22)

- [ ] React + Leaflet map of southern Ontario with resort markers
- [ ] Sidebar with resort details, "last updated" times and "closed" states
- [ ] Distance from the user (browser geolocation)
- [ ] Mobile-friendly layout

**Minimum:** map with clickable markers showing real data.

## Phase 4: Deploy and automate (Nov 23 – Nov 30)

- [ ] Deploy the database, backend and frontend
- [ ] GitHub Actions cron jobs for scraping and weather
- [ ] Failure alerts
- [ ] Remaining scraper adapters (as many of the 12 as time allows)
- [ ] README with screenshots, architecture diagram and live link
- [ ] Resume bullet

**Minimum:** public URL, scheduled jobs running, README done. **This is the November deliverable.**

---

## After November (in-season)

| When | Phase | Notes |
|---|---|---|
| December (hills open) | **Phase 5: Fix and collect** | Scrapers will hit real in-season pages for the first time. Expect fixes. Keep data flowing every day. |
| December – January | **Phase 6: Ranking v1** | Design it once you've seen real data. Deterministic, explainable, user-adjustable weights. |
| January | **Phase 7: Map overlays** | Temperature and precipitation layers |
| January – February | **Phase 8: Busyness estimation** | Webcam computer vision. Start with 1–2 cameras that clearly show a lift line. |
| Late season | **Phase 9: History and trends** | Charts from collected data |
| Next season | **Phase 10: Predictions** | Needs a full season of history |
| Only if traffic | **Phase 11: Community** | Accounts, photos, reviews, moderation |

## Resume milestones

- **Nov 30:** "Built and deployed a full-stack web app (Python/FastAPI, PostgreSQL, React) aggregating live conditions for 12 Ontario ski resorts via scheduled scrapers and a weather API." (Adjust to what's actually true.)
- **Later:** add the ranking algorithm, the computer vision busyness estimates, and real usage numbers.
