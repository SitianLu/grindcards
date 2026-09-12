# -*- coding: utf-8 -*-
"""Turn a Deck into the final card list for one language.

Every card comes out as a 6-tuple: (kind, section, title, hook_html, [blocks], extra).

Concept cards pass through as written. Problem cards are *rebuilt* from the
structured content (statement, hints, pattern, solution) into a fixed back:

    ① pattern → ② reasoning (+ figure) → ③ code → ④ keys → [deeper] follow-ups → variants

That fixed shape is the product: every problem card answers the same four
questions in the same order, so a reader always knows where to look.

Nothing here touches the filesystem; it raises on any inconsistency it can detect.
"""
from __future__ import annotations

import re

from .codefmt import strip_hints
from .deck import Deck, DeckError
from .helpers import C, DIA, FIG, FQ, IDEA, KEYS, MORE, PAT, VAR
from .i18n import t

LEAD_RE = re.compile(r"<span class='lead'>(.*?)</span>", re.S)
LC_IN_NAME = re.compile(r"LC\s*(\d+(?:\s*/\s*\d+)*)")


def _var_rows(pairs, owner_title, owner_lc, deck_title, variants):
    """Variant rows in deep.py are written casually ('LC 159 / 340 at most K distinct').
    Normalise to (lc, display title, difference), one row per problem: deck cards get
    their card title (the app jumps to them), others get the official title (the app
    links to LeetCode)."""
    out, seen = [], set()
    for name, diff in pairs:
        nums = [int(n) for g in LC_IN_NAME.findall(name) for n in re.split(r"\s*/\s*", g)]
        if not nums:                          # a follow-up with no number: plain text
            out.append((0, name, diff))
            continue
        for n in nums:
            if n == owner_lc:
                continue
            if n in deck_title:
                title = deck_title[n]
            elif n in variants:
                title = "LC %d · %s" % (n, variants[n][0])
            else:
                raise DeckError(f"variant LC {n} on {owner_title!r} has no entry in variants.py")
            seen.add(n)
            out.append((n, title, diff))
    return out, seen


def assemble(deck: Deck, lang: str):
    c = deck.content[lang]
    deck_title = {p["lc"]: deck.problem_title(p) for p in deck.problems}
    cards = []
    var_seen = set()

    # ── concept cards: pass through, but check the front has a lead line ──
    for card in c.concepts:
        if len(card) != 5:
            raise DeckError(f"{lang}/concepts.py: {card[2]!r} must be a 5-tuple (kind, section, title, hook, blocks)")
        kind, sec, title, hook, blocks = card
        if kind != "C":
            raise DeckError(f"{lang}/concepts.py: {title!r} has kind {kind!r}, expected 'C'")
        if sec not in deck.sections:
            raise DeckError(f"{lang}/concepts.py: {title!r} uses unknown section {sec!r}")
        if not LEAD_RE.search(hook):
            raise DeckError(f"{lang}/concepts.py: {title!r} front is missing LEAD(...)")
        cards.append((kind, sec, title, hook, list(blocks), {}))

    concept_titles = {card[2] for card in cards}

    # ── problem cards: rebuilt from structured content ──
    for p in deck.problems:
        lc, title = p["lc"], deck_title[p["lc"]]
        for name, store in (("statements", c.stmt), ("hints", c.hints),
                            ("deep", c.deep), ("solutions", c.sol)):
            if lc not in store:
                raise DeckError(f"{lang}/{name}.py has no entry for LC {lc} ({p['title']})")
        stmt, ex = c.stmt[lc]
        hints = list(c.hints[lc])
        d, sol = c.deep[lc], c.sol[lc]

        why, concept = d["pat"]
        if concept not in concept_titles:
            raise DeckError(f"LC {lc} ({lang}) points at concept card {concept!r}, which is not in the deck")

        hook = ("<span class='stmt'>" + stmt + "</span>"
                + (f"<span class='ex'>{ex}</span>" if ex else "")
                + f"<span class='prompt'>{t(lang, 'front.prompt')}</span>")

        blocks = [PAT(why, concept), IDEA(list(sol["idea"]))]
        if sol.get("fig"):
            blocks.append(FIG(sol["fig"]))
        elif sol.get("dia"):
            blocks.append(DIA(sol["dia"]))
        rows, seen = _var_rows(d.get("var", []), title, lc, deck_title, deck.variants)
        var_seen |= seen
        blocks += [C(strip_hints(sol["code"])), KEYS(list(sol["keys"])),
                   MORE(), FQ(list(d.get("fq", []))), VAR(rows)]

        extra = {"lc": lc, "slug": p["slug"], "hints": hints}
        if p.get("tag"):                      # small badge on the front, e.g. "META"
            extra["tag"] = str(p["tag"])
        cards.append(("P", p["section"], title, hook, blocks, extra))

    # ── order: by section, concepts before problems inside each section ──
    order = deck.order
    cards.sort(key=lambda card: (order.index(card[1]), 0 if card[0] == "C" else 1))

    # Variants the app should list: referenced somewhere, not themselves in the deck.
    listed = {n: deck.variants[n] for n in sorted(var_seen) if n not in deck_title}
    return cards, listed


def check_cross_language(deck: Deck, built: dict):
    """Progress is stored per card position and per card title, and the language switch
    swaps the whole deck in place — so every language must produce the *same* cards in
    the *same* order. A card that exists in one language but not another would silently
    shift every index after it and orphan the reader's progress."""
    langs = list(built)
    ref = [(k, s, tt) for k, s, tt, *_ in built[langs[0]][0]]
    for lang in langs[1:]:
        cur = [(k, s, tt) for k, s, tt, *_ in built[lang][0]]
        if cur != ref:
            a, b = set(ref), set(cur)
            raise DeckError(
                f"languages {langs[0]!r} and {lang!r} do not build the same card list.\n"
                f"  only in {langs[0]}: {sorted(x[2] for x in a - b)}\n"
                f"  only in {lang}: {sorted(x[2] for x in b - a)}\n"
                "  Card titles are language-neutral by design; translate the content, not the title.")
