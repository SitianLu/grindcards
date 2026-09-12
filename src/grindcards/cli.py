# -*- coding: utf-8 -*-
"""grindcards — build coding-interview flashcards from a deck directory.

    grindcards init  mydeck [--lang en zh] [--name "My Deck"]
    grindcards verify [deck]
    grindcards build  [deck] [-o build/]        # offline web app + PWA files
    grindcards pdf    [deck] [-o build/] [--lang en]
    grindcards serve  [deck] [-p 8000]          # build, then open in a browser
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .deck import DeckError, load_deck


def _die(msg: str, code: int = 2):
    print(f"grindcards: {msg}", file=sys.stderr)
    sys.exit(code)


def _load(path):
    try:
        return load_deck(path)
    except DeckError as ex:
        _die(str(ex))


def _verify(deck, quiet=False):
    """Run verification; print the report; return (ok, built)."""
    from .verify import verify
    problems, built = verify(deck)
    fatal = [p for p in problems if p.fatal]
    warn = [p for p in problems if not p.fatal]
    if not quiet or fatal:
        for p in problems:
            print(" ", p)
    n_cards = len(next(iter(built.values()))[0]) if built else 0
    n_prob = len(deck.problems)
    langs = "/".join(built) if built else "-"
    if fatal:
        print(f"\n✗ {len(fatal)} error(s), {len(warn)} warning(s) — {n_cards} cards, {n_prob} problems, [{langs}]")
    elif not quiet:
        print(f"\n✓ {n_cards} cards, {n_prob} problems executed, [{langs}] — "
              f"{len(warn)} warning(s)" if warn else
              f"\n✓ {n_cards} cards, {n_prob} problems executed, [{langs}]")
    return not fatal, built


def cmd_init(a):
    from .scaffold import init_deck
    root = Path(a.deck)
    try:
        written = init_deck(root, a.name or root.name, a.lang, a.default)
    except DeckError as ex:
        _die(str(ex))
    print(f"created {root}/ with {len(written)} files:")
    for w in written:
        print("  ", w)
    print(f"\nnext:  grindcards build {root}   →  open {root}/build/index.html")


def cmd_verify(a):
    ok, _ = _verify(_load(a.deck))
    sys.exit(0 if ok else 1)


def cmd_build(a):
    from .render_app import render_app
    deck = _load(a.deck)
    ok, built = _verify(deck, quiet=not a.verbose)
    if not ok and not a.force:
        _die("not building a deck that fails verification (use --force to override)", 1)
    out = Path(a.out) if a.out else deck.root / "build"
    out.mkdir(parents=True, exist_ok=True)
    info = render_app(deck, built, out / "index.html")
    print(f"→ {out / 'index.html'}  ({info['bytes'] / 1024:.0f} KB, {info['cards']} cards, "
          f"languages: {', '.join(info['langs'])})")
    if a.pdf:
        _pdf(deck, built, out, a.lang or deck.default_lang)


def _pdf(deck, built, out: Path, lang: str):
    from .render_pdf import render_pdf
    if lang not in built:
        _die(f"language {lang!r} is not in this deck ({', '.join(built)})")
    cards, _ = built[lang]
    target = out / (f"{deck.root.name}-{lang}.pdf")
    try:
        info = render_pdf(deck, cards, lang, target)
    except RuntimeError as ex:
        _die(str(ex), 1)
    print(f"→ {target}  ({info['bytes'] / 1024:.0f} KB, {info['pages']} pages)")
    if info["overflow"]:
        print("  panels that still overflow (shorten these cards for print):")
        for title, px in info["overflow"]:
            print(f"    {title}  (+{px}px)")


def cmd_pdf(a):
    deck = _load(a.deck)
    ok, built = _verify(deck, quiet=True)
    if not ok and not a.force:
        _die("deck fails verification (run `grindcards verify`; --force to override)", 1)
    out = Path(a.out) if a.out else deck.root / "build"
    out.mkdir(parents=True, exist_ok=True)
    _pdf(deck, built, out, a.lang or deck.default_lang)


def cmd_serve(a):
    import http.server
    import threading
    import webbrowser
    from functools import partial

    from .render_app import render_app
    deck = _load(a.deck)
    ok, built = _verify(deck, quiet=True)
    if not ok:
        _die("deck fails verification (run `grindcards verify`)", 1)
    out = Path(a.out) if a.out else deck.root / "build"
    out.mkdir(parents=True, exist_ok=True)
    render_app(deck, built, out / "index.html")
    handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(out))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", a.port), handler)
    url = f"http://127.0.0.1:{a.port}/"
    print(f"serving {out} at {url}  (Ctrl-C to stop)")
    if not a.no_open:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


def main(argv=None):
    ap = argparse.ArgumentParser(prog="grindcards", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", action="version", version=f"grindcards {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init", help="create a new deck directory with a sample card")
    p.add_argument("deck")
    p.add_argument("--name", help="display name (default: directory name)")
    p.add_argument("--lang", nargs="+", default=["en"], help="languages to scaffold, e.g. --lang en zh")
    p.add_argument("--default", help="default language (default: first of --lang)")
    p.set_defaults(fn=cmd_init)

    p = sub.add_parser("verify", help="run every card's code and check card structure")
    p.add_argument("deck", nargs="?", default=".")
    p.set_defaults(fn=cmd_verify)

    p = sub.add_parser("build", help="verify, then build the offline web app")
    p.add_argument("deck", nargs="?", default=".")
    p.add_argument("-o", "--out", help="output directory (default: <deck>/build)")
    p.add_argument("--pdf", action="store_true", help="also render the printable PDF")
    p.add_argument("--lang", help="language for the PDF (default: deck default)")
    p.add_argument("-v", "--verbose", action="store_true", help="print the full verification report")
    p.add_argument("--force", action="store_true", help="build even if verification fails")
    p.set_defaults(fn=cmd_build)

    p = sub.add_parser("pdf", help="render the printable PDF (needs `pip install grindcards[render]`)")
    p.add_argument("deck", nargs="?", default=".")
    p.add_argument("-o", "--out", help="output directory (default: <deck>/build)")
    p.add_argument("--lang", help="language to print (default: deck default)")
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_pdf)

    p = sub.add_parser("serve", help="build and open the app in a browser")
    p.add_argument("deck", nargs="?", default=".")
    p.add_argument("-o", "--out")
    p.add_argument("-p", "--port", type=int, default=8000)
    p.add_argument("--no-open", action="store_true")
    p.set_defaults(fn=cmd_serve)

    a = ap.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
