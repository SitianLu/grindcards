# -*- coding: utf-8 -*-
"""Prove the deck is what it claims to be.

"Full implementation" on a card is either executable or it is decoration. So every
problem card's code is run — the exact bytes that ship on the card, after hint
stripping — against the card's own test, in every language. On top of that come the
structural rules that keep a card readable on a phone: line width, bullet counts,
no stray markup inside bullets.

Everything returns a list of Problem records; nothing here prints or exits.
"""
from __future__ import annotations

import io
import random
import re
import tokenize
import traceback
import unicodedata
from dataclasses import dataclass

from .assemble import assemble, check_cross_language
from .codefmt import strip_hints
from .deck import Deck, DeckError
from .i18n import check_parity

# Helpers available to every card's code + test. Cards use LeetCode's ListNode/TreeNode
# shapes, and tests build inputs from plain lists.
PRELUDE = '''
from typing import Optional, List
import collections, heapq, bisect, math, itertools, functools
from collections import deque, defaultdict, Counter
class ListNode:
    def __init__(self, val=0, next=None): self.val, self.next = val, next
class TreeNode:
    def __init__(self, val=0, left=None, right=None): self.val, self.left, self.right = val, left, right
def build_list(a):
    head = cur = ListNode(0)
    for v in a: cur.next = ListNode(v); cur = cur.next
    return head.next
def to_list(h):
    out = []
    while h: out.append(h.val); h = h.next
    return out
def build_tree(a):
    if not a: return None
    root = TreeNode(a[0]); q = deque([root]); i = 1
    while q and i < len(a):
        n = q.popleft()
        if i < len(a) and a[i] is not None: n.left = TreeNode(a[i]); q.append(n.left)
        i += 1
        if i < len(a) and a[i] is not None: n.right = TreeNode(a[i]); q.append(n.right)
        i += 1
    return root
'''

CODE_MAX_CHARS = 64       # the card picks its font size from the widest line (hard)
CODE_MAX_COLS = 80        # same, in terminal columns with CJK = 2 (soft: comments in CJK)
CODE_SOFT_LINES = 55
IDEA_RANGE = (3, 6)
KEYS_RANGE = (2, 6)
IDEA_MAX_CHARS = 110      # visible characters; longer bullets read as a paragraph (soft)
FORBIDDEN_TAGS = ("<br", "<p", "<div", "<span", "<ul", "<li", "<ol")


@dataclass
class Problem:
    lang: str
    where: str        # "LC 76" / "concept: Sliding Window" / "deck"
    what: str
    fatal: bool = True

    def __str__(self):
        flag = "ERROR" if self.fatal else "warn "
        return f"{flag}  [{self.lang}] {self.where}: {self.what}"


def cols(s: str) -> int:
    """Terminal-style width: CJK glyphs take two monospace columns."""
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in s)


def visible(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s)


def code_skeleton(code: str) -> str:
    """Code with comments and whitespace removed — what must match across languages."""
    try:
        out, prev = [], None
        skip = (tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT)
        for t in tokenize.generate_tokens(io.StringIO(code).readline):
            # A string that opens a statement is a docstring: prose, like a comment.
            is_doc = t.type == tokenize.STRING and prev in (None, tokenize.NEWLINE, tokenize.INDENT,
                                                            tokenize.DEDENT, tokenize.NL)
            if t.type not in skip and not is_doc:
                out.append(t.string)
            if t.type not in (tokenize.COMMENT, tokenize.NL):
                prev = t.type
        return "".join(out)
    except (tokenize.TokenError, SyntaxError):
        return re.sub(r"\s+", "", code)


def run_code(code: str, test: str, want):
    """Execute card code + test in a fresh namespace. Returns (ok, message)."""
    ns = {}
    random.seed(0)
    try:
        exec(PRELUDE, ns)
        exec(code, ns)
        got = eval(test, ns)
    except Exception:
        return False, "runtime: " + traceback.format_exc().strip().split("\n")[-1]
    if got != want:
        return False, f"wrong answer: got {got!r}, want {want!r}"
    return True, ""


def _code_width(lang, where, lines, out):
    wide = [l for l in lines if len(l) > CODE_MAX_CHARS]
    if wide:
        out.append(Problem(lang, where, f"{len(wide)} code line(s) longer than {CODE_MAX_CHARS} characters "
                                        f"(shrinks the whole block): {wide[0].strip()[:40]}…"))
        return
    wide = [l for l in lines if cols(l) > CODE_MAX_COLS]
    if wide:
        out.append(Problem(lang, where, f"{len(wide)} code line(s) wider than {CODE_MAX_COLS} columns "
                                        f"(CJK comments count double): {wide[0].strip()[:40]}…", fatal=False))


def check_solution(lang: str, lc: int, e: dict, out: list):
    where = f"LC {lc}"
    for f in ("idea", "code", "keys"):
        if not e.get(f):
            out.append(Problem(lang, where, f"empty {f!r}"))
    if not e.get("idea") or not e.get("keys"):
        return
    lo, hi = IDEA_RANGE
    if not lo <= len(e["idea"]) <= hi:
        out.append(Problem(lang, where, f"idea has {len(e['idea'])} bullets (want {lo}–{hi})"))
    lo, hi = KEYS_RANGE
    if not lo <= len(e["keys"]) <= hi:
        out.append(Problem(lang, where, f"keys has {len(e['keys'])} items (want {lo}–{hi}, last = complexity)"))
    for s in list(e["idea"]) + list(e["keys"]):
        for tag in FORBIDDEN_TAGS:
            if tag in s:
                out.append(Problem(lang, where, f"block-level tag {tag!r} inside a bullet: {visible(s)[:50]}…"))
                break
    for s in e["idea"]:
        w = len(visible(s))
        if w > IDEA_MAX_CHARS:
            out.append(Problem(lang, where, f"idea bullet is {w} characters (keep ≤{IDEA_MAX_CHARS}): "
                                            f"{visible(s)[:50]}…", fatal=False))
    if e.get("dia"):
        lines = e["dia"].split("\n")
        if len(lines) > 8:
            out.append(Problem(lang, where, f"ASCII diagram is {len(lines)} lines (max 8)"))
        mx = max(cols(l) for l in lines)
        if mx > 52:
            out.append(Problem(lang, where, f"ASCII diagram is {mx} columns wide (max 52)"))
    if e.get("fig") and not e["fig"].lstrip().startswith("<svg"):
        out.append(Problem(lang, where, "fig does not start with <svg>"))

    shipped = strip_hints(e["code"])
    lines = shipped.strip().split("\n")
    if len(lines) > CODE_SOFT_LINES:
        out.append(Problem(lang, where, f"code is {len(lines)} lines; the back scrolls, but consider trimming",
                           fatal=False))
    _code_width(lang, where, lines, out)
    if not e.get("test"):
        out.append(Problem(lang, where, "no test — the code has never been run"))
        return
    ok, msg = run_code(shipped, e["test"], e.get("want"))
    if not ok:
        out.append(Problem(lang, where, msg))


def check_concepts(lang: str, concepts, out: list):
    for card in concepts:
        if len(card) != 5:
            continue                                # assemble reports the shape error
        _, _, title, _, blocks = card
        where = f"concept {title!r}"
        for kind, v in blocks:
            if kind != "code":
                continue
            _code_width(lang, where, v.strip("\n").split("\n"), out)
            src = strip_hints(v)
            try:
                compile(src, f"<{title}>", "exec")
            except SyntaxError:
                # Templates are often a function *body* (bare `return`), so retry wrapped.
                try:
                    compile("def _():\n" + "".join("    " + l + "\n" for l in src.split("\n")),
                            f"<{title}>", "exec")
                except SyntaxError as ex:
                    # Sketches ("..." bodies, pseudo-code) are allowed: warn, don't fail.
                    out.append(Problem(lang, where, f"template does not parse: {ex.msg} (line {ex.lineno - 1})",
                                       fatal=False))


def verify(deck: Deck) -> tuple[list[Problem], dict]:
    """Returns (problems, built) where built = {lang: (cards, listed_variants)}.
    Fatal deck errors (missing files, dangling links) are reported as Problems too,
    so the CLI can print one list."""
    out: list[Problem] = []
    try:
        check_parity()
    except AssertionError as ex:
        out.append(Problem("*", "engine", str(ex)))

    built = {}
    for lang in deck.langs:
        try:
            built[lang] = assemble(deck, lang)
        except DeckError as ex:
            out.append(Problem(lang, "deck", str(ex)))
            continue
        c = deck.content[lang]
        check_concepts(lang, c.concepts, out)
        for p in deck.problems:
            if p["lc"] in c.sol:
                check_solution(lang, p["lc"], c.sol[p["lc"]], out)
        if lang != deck.default_lang:
            ref = deck.content[deck.default_lang]
            for lc, e in c.sol.items():
                r = ref.sol.get(lc)
                if r and code_skeleton(strip_hints(r["code"])) != code_skeleton(strip_hints(e["code"])):
                    # Same algorithm in every language is the contract; comments differ, code
                    # should not. Compare with comments stripped, so only a real edit trips it.
                    out.append(Problem(lang, f"LC {lc}", "code differs from the default language's "
                                                          "(translate comments, keep the code identical)",
                                       fatal=False))
    if len(built) == len(deck.langs) and len(built) > 1:
        try:
            check_cross_language(deck, built)
        except DeckError as ex:
            out.append(Problem("*", "deck", str(ex)))
    return out, built
