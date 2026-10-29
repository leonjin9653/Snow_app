# CLAUDE.md

Guidance for Claude Code when working in this repo.

## Project

A free public web app showing ski and snowboard conditions for southern Ontario resorts on an interactive map. Data comes from scraping resort snow reports and from the Open-Meteo weather API. Later add-ons: a personalized ranking, webcam-based busyness estimates, and historical trends.

Read these before starting any non-trivial task:

- `docs/PRODUCT.md`: what we're building and for whom
- `docs/ARCHITECTURE.md`: system design, schema, data flow
- `docs/ROADMAP.md`: current phase and priorities
- `docs/DECISIONS.md`: design decisions and the reasons behind them

## About the developer

Leon is a first-year University of Waterloo student. He's comfortable with Python, pandas, numpy and OOP, but new to web development, SQL, JavaScript and deployment. This project is for learning and for his resume, on a deadline (public MVP by Nov 30, 2026).

## How to work with Leon

- **Leon makes the design decisions.** Before making any architectural choice (new library, schema change, new service, a different data flow), explain the options and trade-offs briefly and ask. Don't decide silently.
- **Record decisions.** When Leon decides something, add it to `docs/DECISIONS.md` with the reason.
- **Explain as you build.** When you introduce a concept that's new to him (a React hook, a SQL join, CORS, environment variables, a cron job), add a short plain-language explanation in your reply. Not in code comments.
- **Leon writes some parts himself.** Don't implement these unless he asks:
  - The SQL schema
  - The `SnowReport` common format
  - The ranking algorithm
  - _(Leon: add or remove items here)_
  For these, give pointers, review his code, and help with debugging.
- **Keep changes small and reviewable.** One feature or fix at a time, so Leon can read and understand each change.
- Format replies as plain structured text: markdown headings, tables, bullet points.

## Engineering rules

- Python tooling: `uv` for dependencies and virtual environments.
- Frontend: React + Leaflet in **JavaScript** (not TypeScript), built with Vite.
- One scraper adapter per resort in `backend/collectors/adapters/`. All adapters return the common `SnowReport` format.
- Units: cm, °C, UTC timestamps. Missing values are `None`/`NULL`, never 0.
- Never overwrite good data with a failed scrape. Log every attempt in `scrape_runs`.
- Scrape politely: a few requests a day per resort, a descriptive User-Agent, respect `robots.txt`.
- Parser tests run against saved pages in `backend/tests/fixtures/`, never live sites.
- Secrets (database URLs, keys) go in environment variables, never in code or commits.
- Deterministic code handles scoring, weighting and aggregation. ML is only for perception (webcams).

## Commands

_(Fill in as the project is set up: run backend, run frontend, run tests, run a scraper manually.)_
