import re
from datetime import datetime

import httpx
from bs4 import BeautifulSoup

from collectors.snow_report import SnowReport, ResortStatus

SLUG = "moonstone"
REPORT_URL = "https://www.mountstlouis.com/status/" 
USER_AGENT = "SouthernOntarioSnowMap/0.1 (student project; lrjin@uwaterloo.ca)"


def fetch() -> str:
    response = httpx.get(
        REPORT_URL,
        headers={"User-Agent": USER_AGENT},
        timeout=20,
        follow_redirects=True,
    )
    response.raise_for_status()  # raises an error on 404, 500, etc.
    return response.text


def parse(html: str, scraped_at: datetime) -> SnowReport:
    """Turn the page's HTML into a SnowReport. No internet needed, so it's testable."""
    soup = BeautifulSoup(html, "html.parser")
    runs_open, runs_total = _open_and_total(soup, "open-slopes")
    lifts_open, lifts_total = _open_and_total(soup, "open-lifts")

    return SnowReport(
        resort_slug=SLUG,
        status=_status(soup, runs_open),
        scraped_at=scraped_at,
        base_depth_cm=_base_depth_cm(soup),
        runs_open=runs_open,
        runs_total=runs_total,
        lifts_open=lifts_open,
        lifts_total=lifts_total,
    )


def _open_and_total(soup, section_id):
    """Read a heading like '0/37 Open Slopes' and return (0, 37)."""
    link = soup.find("a", href=f"#{section_id}")
    if link is None:
        return None, None
    match = re.search(r"(\d+)\s*/\s*(\d+)", link.get_text())
    if match is None:
        return None, None
    return int(match.group(1)), int(match.group(2))


def _base_depth_cm(soup):
    section = soup.find("div", id="base")
    if section is None:
        return None
    match = re.search(r"\d+", section.get_text())
    return int(match.group()) if match else None


def _status(soup, runs_open):
    if runs_open:  # at least one run open
        return ResortStatus.OPEN
    today = soup.select_one("table.hours tr.active td")
    if today and "closed" in today.get_text().lower():
        return ResortStatus.CLOSED
    return ResortStatus.UNKNOWN