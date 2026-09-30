"""Browser regression tests for the built app: spaced-repetition scheduling.

Needs the [render] extra and a Chromium (`python -m playwright install chromium`);
skipped otherwise. GRINDCARDS_CHROMIUM overrides the browser executable.

The clock is pinned with Playwright's fixed time and the timezone with the context,
so "due tomorrow at 04:00" is the same instant on every machine.
"""
import datetime as dt
import os
from zoneinfo import ZoneInfo

import pytest

sync_api = pytest.importorskip("playwright.sync_api")

from grindcards.deck import load_deck
from grindcards.render_app import render_app
from grindcards.scaffold import copy_starter
from grindcards.verify import verify

TZ = "America/Los_Angeles"
DAY = 86_400_000


def at(y, m, d, h, mi=0):
    """Epoch ms of a wall-clock time in TZ."""
    return int(dt.datetime(y, m, d, h, mi, tzinfo=ZoneInfo(TZ)).timestamp() * 1000)


T0 = at(2026, 10, 1, 10)                     # Thursday 10:00


@pytest.fixture(scope="module")
def starter(tmp_path_factory):
    root = tmp_path_factory.mktemp("deck")
    copy_starter(root)
    deck = load_deck(root)
    _, built = verify(deck)
    return deck, built, root


@pytest.fixture(scope="module")
def app_url(starter):
    deck, built, root = starter
    out = root / "build" / "index.html"
    render_app(deck, built, out)
    return out.as_uri()


@pytest.fixture(scope="module")
def nosync_url(starter):
    deck, built, root = starter
    out = root / "demo" / "index.html"
    render_app(deck, built, out, sync=False)
    return out.as_uri()


@pytest.fixture(scope="module")
def browser():
    with sync_api.sync_playwright() as p:
        exe = os.environ.get("GRINDCARDS_CHROMIUM") or None
        try:
            b = p.chromium.launch(executable_path=exe)
        except Exception as e:                 # browser binary not installed
            pytest.skip(f"no Chromium for Playwright: {e}")
        yield b
        b.close()


@pytest.fixture
def page(browser, app_url):
    ctx = browser.new_context(timezone_id=TZ)
    pg = ctx.new_page()
    errors = []
    pg.on("pageerror", lambda e: errors.append(str(e)))
    set_time(pg, T0)
    pg.goto(app_url)
    pg.evaluate("localStorage.clear()")
    pg.reload()
    yield pg
    assert not errors, errors
    ctx.close()


def set_time(pg, ms):
    pg.clock.set_fixed_time(ms / 1000)       # the Python API takes seconds


def entry(pg, i=0):
    return pg.evaluate(f"S.cards[CARDS[{i}].t]")


def press(pg, key):
    pg.keyboard.press(key)
    pg.wait_for_function("!busy")


def test_interval_ladder(page):
    pg = page
    pg.evaluate("setKnown(0, true)")
    e = entry(pg)
    assert (e["k"], e["i"], e["d"]) == (1, 1, at(2026, 10, 2, 4))
    assert not pg.evaluate("isDue(0)")

    # "got it" again before it is due leaves the schedule alone (no 1d -> 3d -> 8d in one sitting)
    pg.evaluate("setKnown(0, true)")
    assert entry(pg) == e

    day, ladder = at(2026, 10, 2, 9), []
    for _ in range(6):
        set_time(pg, day)
        assert pg.evaluate("isDue(0)")
        pg.evaluate("setKnown(0, true)")
        e = entry(pg)
        ladder.append(e["i"])
        assert e["d"] == pg.evaluate(f"dayStart({day})") + e["i"] * DAY
        day = e["d"] + 5 * 3_600_000
    assert ladder == [3, 8, 20, 50, 90, 90]

    # "again" lapses to interval 0, due right now; the next "got it" starts over at 1 day
    pg.evaluate("setKnown(0, false)")
    e = entry(pg)
    assert (e["k"], e["i"]) == (0, 0) and pg.evaluate("isDue(0)")
    pg.evaluate("setKnown(0, true)")
    assert entry(pg)["i"] == 1


def test_day_rolls_over_at_4am(page):
    set_time(page, at(2026, 10, 2, 1))       # 01:00 still belongs to Oct 1
    page.evaluate("setKnown(1, true)")
    assert entry(page, 1)["d"] == at(2026, 10, 2, 4)
    set_time(page, at(2026, 10, 2, 23))      # 23:00 belongs to Oct 2
    page.evaluate("setKnown(2, true)")
    assert entry(page, 2)["d"] == at(2026, 10, 3, 4)


def test_legacy_entries_without_schedule(page):
    """v0.1 wrote {k, t}; a "got it" from then is due one rolled-over day after it was marked."""
    pg = page
    pg.evaluate(f"""() => {{
        S.cards[CARDS[0].t] = {{k: 1, t: {T0 - 2 * DAY}}};
        S.cards[CARDS[1].t] = {{k: 1, t: {T0}}};
        S.cards[CARDS[2].t] = {{k: 0, t: {T0}}};
    }}""")
    assert pg.evaluate("[isDue(0), isDue(1), isDue(2), isDue(3)]") == [True, False, True, True]
    pg.evaluate("setKnown(0, true)")         # legacy counts as a 1-day interval: next is 3
    assert entry(pg)["i"] == 3


def test_due_flow_in_the_app(page):
    pg = page
    n = pg.evaluate("CARDS.length")
    assert pg.inner_text("#hcnt").startswith(f"1 / {n}")
    assert pg.inner_text("#yes").split() == ["✓", "Got", "it", "1d"]

    press(pg, "k")                           # card 1: again
    for _ in range(n - 1):
        press(pg, "j")
    assert "1 still due" in pg.inner_text("#donetxt")

    pg.click("#again")                       # round 2 holds only the card marked "again"
    assert pg.inner_text("#hcnt").startswith("1 / 1")
    press(pg, "j")
    assert f"Next up: {n} due tomorrow." in pg.inner_text("#donetxt")

    pg.click("#again")                       # nothing due: caught-up screen
    assert pg.inner_text("#donetitle") == "All caught up ✓"
    assert pg.inner_text("#again") == "Review ahead anyway"

    pg.click("#again")                       # review ahead shows everything, schedule untouched
    assert pg.inner_text("#hcnt").startswith(f"1 / {n}")
    assert pg.inner_text("#yes").split() == ["✓", "Got", "it"]
    before = entry(pg)
    press(pg, "j")
    assert entry(pg) == before

    # next morning, a fresh load: the whole deck is due again, progress kept
    # (the reload reopens on the last card viewed, so only the deck size is checked)
    set_time(pg, at(2026, 10, 2, 8))
    pg.reload()
    assert f" / {n}\u3000" in pg.inner_text("#hcnt")
    assert pg.inner_text("#yes").split() == ["✓", "Got", "it", "3d"]
    assert f"known {n}/{n}" in pg.inner_text("#hcnt")


def test_due_filter_toggle_is_a_synced_pref(page):
    pg = page
    pg.evaluate("CARDS.forEach((c, i) => setKnown(i, true)); save(); buildDeck(false); paint()")
    assert pg.inner_text("#donetitle") == "All caught up ✓"
    pg.click("#menu")
    assert "(0 now)" in pg.inner_text("#dueTxt")
    pg.click("#onlyDue")
    assert not pg.is_visible("#done")
    assert pg.evaluate("S.onlyDue") is False and "onlyDue" in pg.evaluate("prefsOut()")


KEY = "0123456789abcdef0123456789abcdef"


def test_sync_build_reads_the_key(page, app_url):
    page.goto(app_url + "#k=" + KEY)
    page.reload()                              # a hash-only goto doesn't reload the page
    assert page.evaluate("SK") == KEY
    page.click("#menu")
    assert page.is_visible("#keyRow") and page.is_visible("#syncLink")
    assert page.text_content("#syncSh") == "Cross-device sync"


def test_no_sync_build_hides_key_controls(browser, nosync_url):
    """--no-sync (the GitHub Pages demo): no key is read or pinned, key controls are hidden,
    export/import stay."""
    ctx = browser.new_context(timezone_id=TZ)
    pg = ctx.new_page()
    errors = []
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.goto(nosync_url + "#k=" + KEY)
    assert pg.evaluate("SK") == "" and pg.evaluate("canSync()") is False
    pg.click("#menu")
    for sel in ("#keyRow", "#syncLink", "#copyKey"):
        assert not pg.is_visible(sel), sel
    assert pg.is_visible("#expProg") and pg.is_visible("#impSet")
    assert pg.text_content("#syncSh") == "Progress"
    assert "saved in this browser only" in pg.inner_text("#syncTxt")
    assert not errors, errors
    ctx.close()
