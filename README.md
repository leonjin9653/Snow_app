# Snow App

A free web app that shows ski and snowboard conditions for southern Ontario hills on one interactive map, so you can decide where and when to go without checking a dozen resort websites.

**Status:** in progress. Planning and data audit done; building the data pipeline (target: public MVP by end of November 2026).

## Planned features

- Interactive map of 12 southern Ontario resorts with current conditions
- Snow depth and open terrain scraped from resort reports, weather from Open-Meteo
- Later: personalized "where should I go today?" ranking, webcam-based lift wait estimates, historical trends

## Tech stack

Python (FastAPI) · PostgreSQL · React + Leaflet (JavaScript) · GitHub Actions for scheduled scraping

## Docs

- [Product](docs/PRODUCT.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Roadmap](docs/ROADMAP.md)
- [Decisions](docs/DECISIONS.md)
- [Data audit](docs/data-audit.md)
