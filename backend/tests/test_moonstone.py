from datetime import datetime, timezone
from pathlib import Path

from collectors.adapters.moonstone import parse
from collectors.snow_report import ResortStatus

FIXTURE = Path(__file__).parent / "fixtures" / "moonstone.html"


def test_parse_closed_page():
    html = FIXTURE.read_text(encoding="utf-8")
    report = parse(html, datetime.now(timezone.utc))

    assert report.status == ResortStatus.CLOSED
    assert report.runs_open == 0
    assert report.runs_total == 37
    assert report.lifts_open == 0
    assert report.lifts_total == 12
    assert report.base_depth_cm is None
    assert report.new_snow_24h_cm is None