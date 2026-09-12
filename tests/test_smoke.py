"""End-to-end smoke tests: the scaffold and the starter deck load, verify and build."""
import subprocess
import sys
from pathlib import Path

import pytest

from grindcards.deck import load_deck
from grindcards.render_app import render_app
from grindcards.scaffold import copy_starter, init_deck
from grindcards.verify import verify


@pytest.fixture(params=["scaffold", "starter"])
def deck_dir(request, tmp_path):
    root = tmp_path / request.param
    if request.param == "scaffold":
        init_deck(root, "Smoke", ["en", "zh"])
    else:
        copy_starter(root)
    return root


def test_verify_and_build(deck_dir, tmp_path):
    deck = load_deck(deck_dir)
    problems, built = verify(deck)
    fatal = [p for p in problems if p.fatal]
    assert not fatal, "\n".join(map(str, fatal))
    assert set(built) == {"en", "zh"}
    # every language yields the same card list, in the same order
    titles = {lang: [c[2] for c in cards] for lang, (cards, _) in built.items()}
    assert titles["en"] == titles["zh"]
    out = tmp_path / "build" / "index.html"
    info = render_app(deck, built, out)
    html = out.read_text(encoding="utf-8")
    assert info["cards"] == len(titles["en"])
    for placeholder in ("__DECKS__", "__I18N__", "__LANGS__", "__LANG__", "__APPNAME__"):
        assert placeholder not in html
    assert (out.parent / "sw.js").exists() and (out.parent / "manifest.webmanifest").exists()


def test_cli_help_runs():
    r = subprocess.run([sys.executable, "-m", "grindcards", "--help"], capture_output=True, text=True)
    assert r.returncode == 0 and "init" in r.stdout


def test_missing_solution_is_reported(tmp_path):
    root = tmp_path / "d"
    init_deck(root, "Broken", ["en"])
    sol = root / "en" / "solutions.py"
    sol.write_text(sol.read_text().replace("    1: dict(", "    999: dict("))
    problems, built = verify(load_deck(root))
    assert any(p.fatal and "LC 1" in p.what for p in problems)
