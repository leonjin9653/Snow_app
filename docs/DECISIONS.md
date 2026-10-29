# Decisions

Leon makes the design decisions in this project. Each entry records the options, the trade-offs, a recommendation, and the final choice with the reason for it. Being able to explain these choices matters as much as the code.

**Status key:** 🟡 Open · ✅ Decided

---

## Needed by Phase 0

### D1. Backend language and framework ✅ Python + FastAPI (Oct 29, 2026)

| Option | For | Against |
|---|---|---|
| **Python + FastAPI** | Builds on Leon's Python; same language as the scrapers and future ML; auto-generated API docs | Less "new language" learning on the backend |
| Node + Express (TypeScript) | One language across the whole stack | Learning two new things at once on a deadline |

**Recommendation:** Python + FastAPI. The new-language learning happens in the frontend (JavaScript or TypeScript) and SQL.

**Decision:** Python + FastAPI.
**Why:** Builds on existing Python skills; same language as the scrapers and future ML.

### D2. Frontend ✅ React + Leaflet, JavaScript (Oct 29, 2026)

| Option | For | Against |
|---|---|---|
| **React + Leaflet** | Industry standard; free maps with no key; lots of examples | React has a learning curve |
| Plain HTML/JS + Leaflet | Simpler | Gets messy as the sidebar and ranking grow; less resume value |
| Mapbox instead of Leaflet | Nicer-looking maps | Needs an API key; usage limits |

Also decide: **JavaScript or TypeScript?** TypeScript catches mistakes earlier and is valued by employers, but adds setup.

**Decision:** React + Leaflet, written in JavaScript.
**Why:** Industry standard with lots of examples; free maps with no API key. JavaScript over TypeScript to keep the learning curve manageable on the November deadline; TypeScript can be adopted later.

### D3. Database ✅ PostgreSQL from day one (Oct 29, 2026)

| Option | For | Against |
|---|---|---|
| **PostgreSQL from day one** | What you'll deploy anyway; strong time-series querying; resume value | Slightly more setup |
| SQLite first, move later | Zero setup | You'll do a migration mid-project |

**Recommendation:** Postgres from the start. Hosted Postgres free tiers make SQLite's setup advantage small.

**Decision:** PostgreSQL from day one.
**Why:** It's what gets deployed anyway, and it avoids a mid-project migration.

### D4. Who does the main screen serve first? 🟡

- **Day-tripper ("where today?")**: current conditions and distance first
- **Planner ("next weekend")**: forecasts and trends first

**Decision:** _
**Why:** _

---

## Needed by Phase 1

### D5. Hours and pricing ✅ Manual entry each season (Oct 29, 2026)

Scraping these is fragile, and they rarely change. **Recommendation:** enter them manually each season in the resort seed file, and always link to the resort's own pricing page.

**Decision:** Enter manually each season in the resort seed file, with a link to the resort's pricing page.
**Why:** Rarely changes and is formatted differently on every site, so scraping it would be fragile code for little benefit.

### D6. Store forecasts, or fetch them live? 🟡

Storing forecasts lets you later measure how accurate forecasts were (a good analysis project). Fetching live is simpler.

**Decision:** _

---

## Needed by Phase 3

### D7. Distance: straight-line or driving time? 🟡

Straight-line distance is free and instant. Driving time needs a routing service (free options exist, with rate limits), and roads like Highway 400 vs. back roads make a real difference.

**Recommendation:** straight-line for the MVP, driving time later.

**Decision:** _

---

## Needed by Phase 8 (busyness)

### D8. How to measure lift wait times ✅ Track individuals in short clips (Oct 29, 2026)

**Decision:** Once an hour during operating hours, record a 2–5 minute clip from a webcam that shows a lift line. Detect and track the last ~5 people in line and measure how long they take to reach the chair. Show the average as a wait-time estimate.

**Why:** Tracking specific people through a crowd on a low-resolution, outdoor camera (snow, glare, occlusion, similar-looking riders) is a hard, real multi-object tracking problem. Solving it with measured accuracy is a strong ML project, and Leon chose it deliberately as the challenge.

**Design problems to solve in Phase 8:**

- **Clip length vs. wait length.** If the wait is longer than the clip, the tracked people won't reach the chair before the clip ends. Plan: measure how fast tracked people *advance* during the clip (position in line per minute), then estimate the full wait as line length ÷ advance rate. Direct timing works only when the wait is shorter than the clip.
- **Needs true video.** Still images refreshed every minute can't support tracking. The data audit must record which cameras are real live streams.
- **Don't build from scratch.** Start from a pretrained person detector (e.g. YOLO) and an existing multi-object tracker (e.g. ByteTrack or DeepSORT). The original work is defining each camera's lift-line region, reducing ID switches and lost tracks, fine-tuning on labeled frames from these cameras, and turning tracks into a wait time.
- **Ground truth is what makes it impressive.** Hand-time real people in recorded clips and report the estimate's error (e.g. "mean absolute error of X minutes over N clips"). A measured accuracy number is the evidence the model works.
- **Fallback.** If tracking is unreliable on a given camera, fall back to counting + Little's Law (option B above) for that camera, so the site always shows something.

**Options considered:**

| Option | How it works | Difficulty |
|---|---|---|
| A. Track individuals (original) | Continuous video, person re-identification across frames | Very hard; needs a live stream, not still images |
| **B. Count + Little's Law** | Count people in line in one frame. Wait ≈ people in line ÷ lift throughput (seats per chair × chairs per minute) | Moderate; works with still images |
| C. Short video bursts | Every N minutes, sample the stream for ~1–2 min and measure how fast the line moves | Moderate–hard; needs a live stream |
| D. Busyness index only | Count people and compare to that camera's usual count ("busier than a typical Saturday") | Easiest |

A is the chosen approach, run on short clips as in C; B and D are fallbacks.

### D10. Blue Mountain's JSON feed ✅ Use the feed directly for now (Oct 29, 2026)

Blue Mountain's report is loaded from a third-party JSON feed (MTNPowder) using an access token embedded in its public page. The feed is the richest data source of all 12 resorts, but it isn't a published public API. See `data-audit.md`.

| Option | For | Against |
|---|---|---|
| Use the feed directly | Clean, structured, cm + inches, many fields | Not an offered API; the token can change; terms unclear |
| Render the page in a headless browser and read the visible numbers | Uses only what any visitor sees | Heavier (Playwright), slower, more fragile |
| Ask Blue Mountain for permission | Removes the doubt | May take time or get no reply |

**Decision:** Use the feed directly while the project is small. If the project grows (real traffic, or anything beyond a personal/portfolio project), ask Blue Mountain for permission or switch to reading the rendered page.
**Why:** It's by far the cleanest and richest data source, and the project is non-commercial and low-volume for now.

**Ground rules:**

- Don't hard-code or commit the token. Read it from Blue Mountain's page at scrape time (it's in the page's own request), so a token change doesn't break the scraper and no credential lives in the repo.
- Keep the request rate the same as every other resort (a few times a day).
- Keep this logic inside the Blue Mountain adapter only, so swapping to another approach later touches one file.
- Revisit this decision if the site's terms say otherwise, or if Blue Mountain asks.

### D9. Webcam terms of use 🟡

Check each resort's terms before processing its feeds. Never store or publish identifiable images of people. Only publish counts.

---

## Decided

_(Move entries here as they're decided.)_
