# Data Audit

*Done October 29, 2026, off-season. Every resort was closed, so most pages showed "closed" states or values left over from last season. Fields and page structure were checked; real in-season values were not. Re-check each page in December when hills open.*

**How it was checked:** each report page was loaded in a browser, and its visible content was compared with the raw HTML the server sends (before JavaScript runs). If the numbers are in the raw HTML, the page is **static**: a plain HTTP request plus an HTML parser is enough. If they only appear after JavaScript runs, the page is **JS-loaded**, and the data comes from a separate request (often a JSON feed).

---

## Summary

| Resort | Report URL | Page type | Snow depth? | Webcams | Lift-line cam? | `robots.txt` |
|---|---|---|---|---|---|---|
| Blue Mountain | [mountain-report](https://www.bluemountain.ca/mountain/mountain-report) | **JS-loaded, JSON feed** | Yes (cm + in) | 8 YouTube + 2 Skaping | Check names | Allowed |
| Mount St. Louis Moonstone | [status](https://www.mountstlouis.com/status/) | Static | Yes (base) | 8 (still image + YouTube each) | **Likely** (lift base cams) | Allowed |
| Horseshoe | [ski-report-trails](https://horseshoeresort.com/ski-report-trails/) | Static | Yes (base) | 5 YouTube | **Likely** (Copeland Express chairlift) | Allowed |
| Snow Valley | [weather-webcams](https://www.skisnowvalley.com/plan/weather-webcams/) | Static (+ print page) | Yes (base, cm) | 4 | **Likely** (Wide Load chair) | Allowed |
| Chicopee | [activity-report](https://www.chicopee.ca/activity-report) | JS app (Nuxt) + CMS API | Yes (average base, cm) | None found | — | **No real file** |
| Boler | **Not found off-season** | — | Unknown | 2 Google Nest live | Check | Allowed, crawl-delay 10 |
| Glen Eden | [slope-conditions](https://gleneden.on.ca/at-glen-eden/slope-conditions/) | Static | Yes (base, cm) | 2 live streams (off for season) | Possible (bottom of runs) | Allowed |
| Lakeridge | [trail-status](https://ski-lakeridge.com/skiing-snowboarding/trail-status/) | Static | **No** (per-trail open/closed only) | None found | — | Allowed, crawl-delay 10 |
| Dagmar | [trailmap](https://www.skidagmar.com/trailmap/) | Static | Yes (base, cm) | None found | — | Allowed |
| Batawa | [homepage](https://www.batawaskihill.com/) (report posted there in season) | Squarespace | Unknown | None found | — | Allowed for normal pages |
| Sir Sam's | [winter/conditions](https://www.sirsams.ca/winter/conditions) | Wix (JS-heavy) | Unknown | None found | — | Allowed |
| Brimacombe | [snow-conditions-and-trails](https://brimacombe.ca/at-the-brim/snow-conditions-and-trails/) | Static | **No** (snow type only) | None found | — | Allowed |

**Totals:** 7 static pages, 1 JSON feed, 4 unknown until the season starts. 8 of 12 show a snow depth. 6 resorts have webcams, and 3–4 have a camera likely aimed at a lift.

---

## Per-resort notes

### Blue Mountain
- **Data source:** the page loads its data from a JSON feed run by a third party (MTNPowder / MTNfeed), not from the HTML. The feed request includes an access token embedded in Blue Mountain's page. **Using that feed directly is a terms-of-use question:** it's not a published public API. Decide before relying on it (`DECISIONS.md`).
- **Fields in the feed** (richest of all 12): base depth by area (base / mid-mountain), new snow over 24h / 48h / 72h / 7 days, season total, storm total, trails and lifts open vs. total, trails by difficulty, trails making snow, groomed trails, terrain acres open, night trails, parks. Every snow value is given in **both cm and inches**.
- **Webcams:** 8 embedded YouTube streams (true video) plus 2 Skaping cams (village, mountain top), which are periodic panoramic stills. Camera names weren't readable from the embeds: check them by eye.

### Mount St. Louis Moonstone
- **Fields:** status (Today: Closed), base, natural snow in last 24h, snowmaking in last 24h, slopes open (0/37), parks open (0/5), lifts open (0/12), features open.
- **Webcams (8):** Elfie Huter Express Top, **Elfie Huter Express Base**, Adventure Top, Moonstone Base, **MSLM Base**, The JunkYard, Beginner Area, Josl Huter Express. Each has a refreshing still image on the resort's server *and* a YouTube link (likely a live stream). **Strongest candidate for the tracking feature.**
- Site also calls a leaderboard API (`api.mountstlouis.com`), which isn't needed.

### Horseshoe
- **Fields:** last-updated date, current weather, snowfall past 24h (cm), alpine hours, base depth, and per-run status for **both day and night sessions** (9:00–4:30 and 3:30–9:00). Nordic trails listed separately.
- **Webcams (5, YouTube):** Eye in the Sky, hill base cam, **Copeland Express chairlift**, beach, tubing park.

### Snow Valley
- **Fields:** report date, operating day, new snow (cm), base depth (cm), snow surface, runs open (0/21), lifts open (0/8), tubing zones, special events, and a daily note.
- Has a **print version** of the report (`/weather-webcams/print/`), which is likely the cleanest page to scrape.
- **Webcams (4):** **Wide Load Chair**, Tube Park, Adventure Learning Centre, Tube Summit. They open in popups. At least one is a YouTube live stream.

### Chicopee
- **Fields:** status, date and time, surface conditions, lifts open (0/5), trails open (0/13), freestyle park, average base (cm), snowmaking in last 24h (Yes/No), natural snow (cm), and per-lift status.
- The site is a JavaScript app (Nuxt) whose content comes from a headless CMS (Prismic). Try plain HTML first, since the server may render the data into the HTML; otherwise use a headless browser.
- `/robots.txt` returns a web page instead of a robots file, so there are no stated rules. Read the terms of use.
- Note: the report says "0 / 5" lifts but lists 6 lifts. Small inconsistencies like this are normal.

### Boler Mountain
- **No conditions page found** in the menu or the sitemap off-season. Aggregator sites (OpenSnow, SnoCountry) have Boler reports, so Boler publishes one somewhere in season. Re-check in December, or look at an archived January copy on the Wayback Machine.
- **Webcams (2):** Google Nest live-video embeds. True video. Nest embeds may be harder to capture programmatically than YouTube.

### Glen Eden
- **Fields:** surface (e.g. Machine Groomed Granular), base depth (cm), new snow last 24h (**Yes/No, not cm**), snowmaking last 24h (Yes/No), runs and lifts by area.
- **Stale data:** base depth still reads **40 cm** while the hill is closed for the season.
- **Webcams (2 live streams, off for the season):** West Lodge (looks west at the bottom of Challenger and Night Hawk runs) and East Lodge.

### Lakeridge
- **Fields:** per-trail open/closed only. **No snow depth shown** (possibly only off-season). Check in December.
- Only a YouTube channel link, no webcam page. Official site is `ski-lakeridge.com` (the old `ski-lakeridge.on.ca` doesn't load).

### Dagmar
- **Fields:** snow base (cm), new snow (cm), conditions, per-lift status, per-run status.
- **Stale data:** shows "Snow Base: 70cm" while fully closed.
- No webcams found.

### Batawa
- Squarespace site. The ski map page says the **daily trail report is posted on the homepage** in season, so the format is unknown until December.
- `robots.txt`: Squarespace's default. It blocks named AI crawlers and some URL patterns (including the `?format=json` versions of pages), but allows normal pages for everyone else.
- No webcams found.

### Sir Sam's
- Wix site (JavaScript-heavy). The conditions URL currently shows only a winter landing page. Format unknown until the season starts.
- `robots.txt` contains `Disallow: /`, but **only for one specific crawler (PetalBot)**. Everyone else is allowed.
- No webcams found.

### Brimacombe
- **Fields:** trails open (day / night), lifts open ("0 of 3", though 7 lifts are listed), parks open, snow type, conditions date, conditions note, and per-trail, per-park and per-lift status for day and night.
- **No snow depth field.**
- Only a YouTube channel link, no webcam page.

---

## What this means for the design

1. **Common format (open question #1):** depth is reported as cm almost everywhere, but **new snow** comes as cm, Yes/No (Glen Eden) or not at all. Runs and lifts come as "X / Y" counts, or as per-item lists you'd count yourself. Lakeridge and Brimacombe have **no depth**, so the format needs nullable depth and the UI needs a "not reported" state.
2. **Stale values off-season:** Glen Eden (40 cm) and Dagmar (70 cm) show depths while closed. Validation should treat **status = closed** as overriding the depth, and store the resort's own report date so old reports can be detected.
3. **Scraping approach:** 7 static pages can use `requests` + BeautifulSoup. Blue Mountain needs a decision about the JSON feed. Chicopee, Batawa and Sir Sam's may need a headless browser (e.g. Playwright). Boler is unknown.
4. **Politeness:** two sites ask for a 10-second crawl delay. At 3–4 scrapes a day that's irrelevant, but put a delay in the scraper anyway. Use a descriptive User-Agent.
5. **Busyness feature:** the best tracking candidates are **Mount St. Louis** (2 lift-base cams), **Horseshoe** (Copeland Express chair) and **Snow Valley** (Wide Load chair), all on YouTube. Look at each in person in December to confirm the camera actually shows a lift line.
6. **Competition note:** aggregators (OpenSnow, SnoCountry, Snow-Forecast) already list all 12 hills. This doesn't kill the idea, since none of them offers the Ontario-focused map, ranking or busyness estimate, but it's worth knowing, and it's a good interview point to address head-on.

## To do in December

- [ ] Re-check every report page with real in-season data
- [ ] Find Boler's report page
- [ ] See what Batawa's homepage report and Sir Sam's conditions page look like in season
- [ ] Check whether Lakeridge shows snow depth in season
- [ ] Save a copy of each report page into `backend/tests/fixtures/` for parser tests
- [ ] Watch the candidate lift cameras and confirm which show a lift line
- [ ] Read each resort's terms of use (not checked here)
