# Product: Southern Ontario Snow Conditions Map

*Working name TBD. Last updated: October 29, 2026.*

## The problem

The ski and snowboard season in southern Ontario is short, and it's getting shorter. To decide where to go, you have to check each resort's website one at a time. Each site reports conditions differently, nobody compares them side by side, and people rarely try hills outside their usual radius, even when those hills have better snow.

## The goal

A **free, public web page** where anyone can see conditions at every major southern Ontario hill on one map and decide **where and when to go**, in seconds instead of twenty minutes of tab-switching.

## Who it's for

| User | Situation | What they need |
|---|---|---|
| Day-tripper (primary) | Saturday morning, deciding where to drive today | Current conditions, distance, how busy it is |
| Planner (secondary) | Midweek, planning next weekend | Forecasts, snow trends, comparisons |

**Open decision:** which user the main screen is designed for first. See `DECISIONS.md`.

## Core experience (MVP)

- An interactive map of southern Ontario with a marker at each resort.
- Clicking a marker opens a sidebar with:
  - Resort name, website link, location
  - Distance from the user (with location permission)
  - Snow depth and terrain or lifts open (from the resort's snow report)
  - Current weather and recent snowfall at the resort's coordinates
  - Open hours and pricing (see the note below)
  - When the data was last updated (always shown, so users can trust it)
- Shows a clear "closed / no report yet" state. This matters because the site launches before the season starts.

**Note on hours and pricing:** these change rarely and vary in format across sites. The MVP treats them as manually maintained resort info (plus a link to the resort's own pricing page), not scraped data.

## Add-on layers (after MVP)

Each layer is independent and can ship separately.

1. **Map overlays:** temperature, precipitation and snowfall layers on the map.
2. **Personalized ranking:** a "where should I go today?" list based on distance, snow depth, recent snowfall, temperature, rain, busyness and the user's own priorities.
3. **Busyness and wait-time estimates:** computer vision on resort webcams that show lift lines.
4. **Historical trends:** charts of each resort's conditions over the season, from the app's own collected data.
5. **Community features (only with real traffic):** user photos, ratings and reviews.

## Principles

- **Honest data.** Always show the source and the timestamp. Label estimates as estimates.
- **Fast answer first.** Someone should get a useful answer within 10 seconds of opening the page.
- **Respectful scraping.** A few requests a day per resort, follow `robots.txt` and terms, link back to resort sites.
- **Free to use, cheap to run.** Run on free tiers wherever possible.

## Non-goals (for now)

- Mobile app (the site should still work well on a phone)
- User accounts (until community features are needed)
- Resorts outside southern Ontario
- Ticket booking or anything transactional

## What success looks like

- **By end of November 2026:** a deployed, public site showing all target resorts on a map, with live weather and working scrapers, ready to collect data the day hills open. Good enough to put on a resume with a live link.
- **During the season:** snow reports collected several times a day for the whole season, and a ranking that friends actually use.
- **Long term:** a busyness estimate nobody else provides, and enough history to predict conditions.
