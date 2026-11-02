"""The journeys-gate fixture carries exactly its five seeded defects, each visible in what a page shows.

`verification/fixtures/journeys-app/server.js` is the fixed twin; `seeded.patch` plants five journey
defects in it (define's `journeys-gate-*` scenarios drive both). Each numbered test drives the two
apps over HTTP and asserts one defect shows in the seeded app and not in the fixed one. The
twin-only tests hold the other journeys an open journeys gate walks into — many places, no
session, a rejected name, an unknown link, an empty trip — so a FAIL on the fixed twin points at
the gate rather than at a defect the twin was never meant to carry.
"""

from __future__ import annotations

import http.cookiejar
import re
import shutil
import socket
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Iterator
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURE = REPO_ROOT / "verification" / "fixtures" / "journeys-app"


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


class App:
    """One running copy of the fixture, with a browser-like cookie jar."""

    def __init__(self, port: int) -> None:
        self.base = f"http://127.0.0.1:{port}"
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
        )

    def get(self, path: str) -> tuple[str, str]:
        with self.opener.open(self.base + path, timeout=5) as r:
            return urllib.parse.urlparse(r.geturl()).path, r.read().decode()

    def post(self, path: str, **form: str) -> tuple[str, str]:
        data = urllib.parse.urlencode(form).encode()
        with self.opener.open(self.base + path, data=data, timeout=5) as r:
            return urllib.parse.urlparse(r.geturl()).path, r.read().decode()


def _start(directory: Path) -> Iterator[App]:
    port = _free_port()
    proc = subprocess.Popen(
        [shutil.which("node") or "node", "server.js"],
        cwd=directory,
        env={"PATH": "/usr/bin:/bin:/usr/local/bin", "PORT": str(port)},
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    app = App(port)
    try:
        for _ in range(100):
            try:
                app.get("/")
                break
            except (urllib.error.URLError, ConnectionError):
                time.sleep(0.05)
        else:
            pytest.fail(f"the fixture app on port {port} never answered")
        yield app
    finally:
        proc.terminate()
        proc.wait(timeout=5)


@pytest.fixture
def fixed(tmp_path: Path) -> Iterator[App]:
    directory = tmp_path / "fixed"
    directory.mkdir()
    shutil.copy(FIXTURE / "server.js", directory / "server.js")
    yield from _start(directory)


@pytest.fixture
def seeded(tmp_path: Path) -> Iterator[App]:
    directory = tmp_path / "seeded"
    directory.mkdir()
    shutil.copy(FIXTURE / "server.js", directory / "server.js")
    patch = (FIXTURE / "seeded.patch").read_bytes()
    subprocess.run(
        ["patch", "-s", "-p1", "-d", str(directory)], input=patch, check=True
    )
    yield from _start(directory)


pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="needs node")


def _signed_out_arrival(app: App) -> str:
    return app.get("/trips/lisbon?mode=plan")[1]


def test_1_signed_out_visitor_from_a_shared_link(fixed: App, seeded: App) -> None:
    assert "Sign in to see the places your group saved" in _signed_out_arrival(fixed)
    assert "<body></body>" in _signed_out_arrival(seeded)


def _lands_after_sign_in(app: App) -> str:
    # The sign-in link a signed-out visitor meets names the page they came for.
    return app.post("/signin", email="ana@example.com", next="/trips/lisbon?mode=plan")[
        0
    ]


def test_2_sign_in_returns_to_the_page_the_person_was_on(
    fixed: App, seeded: App
) -> None:
    assert "/signin?next=%2Ftrips%2Flisbon%3Fmode%3Dplan" in _signed_out_arrival(fixed)
    assert _lands_after_sign_in(fixed) == "/trips/lisbon"
    assert _lands_after_sign_in(seeded) == "/"


def _after_adding_two(app: App) -> str:
    app.post("/signin", email="ana@example.com", next="/")
    app.post("/trips/lisbon/places", name="Sintra day trip", mode="list")
    return app.post("/trips/lisbon/places", name="Fado at Mesa de Frades", mode="list")[
        1
    ]


def test_3_a_second_added_place_does_not_replace_the_first(
    fixed: App, seeded: App
) -> None:
    page = _after_adding_two(fixed)
    assert "Sintra day trip" in page and "Fado at Mesa de Frades" in page
    page = _after_adding_two(seeded)
    assert "Sintra day trip" not in page and "Fado at Mesa de Frades" in page


def _plan_after_choosing_eight(app: App) -> str:
    app.post("/signin", email="ana@example.com", next="/")
    return app.post("/trips/lisbon/start", hour="8")[1]


def test_4_the_day_plan_applies_its_own_start_setting(fixed: App, seeded: App) -> None:
    assert "08:00 — Belém Tower" in _plan_after_choosing_eight(fixed)
    page = _plan_after_choosing_eight(seeded)
    assert 'value="8" selected' in page and "09:00 — Belém Tower" in page


def _plan(app: App) -> str:
    app.post("/signin", email="ana@example.com", next="/")
    return app.get("/trips/lisbon?mode=plan")[1]


def test_5_the_day_plan_stays_within_the_trips_days(fixed: App, seeded: App) -> None:
    assert "Thu 14 May" in _plan(fixed) and "Fri 15 May" not in _plan(fixed)
    assert "Fri 15 May" in _plan(seeded)


def _signed_in(app: App) -> App:
    app.post("/signin", email="ana@example.com", next="/")
    return app


def test_twin_keeps_a_crowded_plan_within_real_hours(fixed: App) -> None:
    app = _signed_in(fixed)
    for n in range(30):
        app.post("/trips/lisbon/places", name=f"Stop {n}", mode="plan")
    page = app.post("/trips/lisbon/start", hour="10")[1]
    hours = [int(h) for h in re.findall(r"<li>(\d\d):00 — ", page)]
    assert hours and max(hours) <= 20
    assert "Not in the plan" in page and "Stop 29" in page


def test_twin_refuses_an_add_with_no_session_and_keeps_the_text(fixed: App) -> None:
    path, page = fixed.post("/trips/lisbon/places", name="Anon drop", mode="list")
    assert path == "/signin"
    next_field = re.search(r'name="next" value="([^"]+)"', page)
    assert next_field
    next_path = next_field.group(1).replace("&amp;", "&")
    page = fixed.post("/signin", email="ana@example.com", next=next_path)[1]
    assert "wasn&#39;t added" in page or "wasn't added" in page
    assert 'value="Anon drop"' in page
    assert "<li>Anon drop</li>" not in page


def test_twin_trip_pages_are_never_served_from_cache(fixed: App) -> None:
    app = _signed_in(fixed)
    with app.opener.open(app.base + "/trips/lisbon", timeout=5) as r:
        assert r.headers["cache-control"] == "no-store"


def test_twin_says_why_a_name_was_rejected(fixed: App) -> None:
    app = _signed_in(fixed)
    assert (
        "Type a place name"
        in app.post("/trips/lisbon/places", name="   ", mode="list")[1]
    )
    page = app.post("/trips/lisbon/places", name="belém tower", mode="list")[1]
    assert "already saved" in page and page.count("Belém Tower") == 1
    page = app.post("/trips/lisbon/places", name="x" * 81, mode="list")[1]
    assert "up to 80 characters" in page
    page = app.post("/trips/lisbon/places", name="LX  Factory", mode="list")[1]
    assert "already saved" in page and page.count("<li>LX Factory</li>") == 1


def test_twin_gives_an_unknown_link_a_way_out(fixed: App) -> None:
    with pytest.raises(urllib.error.HTTPError) as missing:
        fixed.get("/trips/nowhere")
    assert missing.value.code == 404
    assert 'href="/signin"' in missing.value.read().decode()
    assert fixed.get("/trips/LISBON/")[0] == "/trips/lisbon"
    for key in ("constructor", "__proto__"):
        with pytest.raises(urllib.error.HTTPError) as inherited:
            _signed_in(fixed).get(f"/trips/{key}")
        assert inherited.value.code == 404
    assert fixed.get("/")[0] == "/"


def test_twin_shows_an_empty_trip(fixed: App) -> None:
    app = _signed_in(fixed)
    assert "No places yet" in app.get("/trips/porto")[1]
    assert "No places to plan yet" in app.get("/trips/porto?mode=plan")[1]
