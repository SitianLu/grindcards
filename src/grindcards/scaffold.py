# -*- coding: utf-8 -*-
"""`grindcards init`: write a minimal, buildable deck directory.

One concept card and one problem card in each requested language, so the very
first `grindcards build` succeeds and the reader has a worked example of every
file to copy from. All sample text is original — no LeetCode statements.
"""
from __future__ import annotations

from pathlib import Path

from .deck import DeckError

DECK_TOML = '''[deck]
name = "{name}"
languages = [{langs}]
default_language = "{default}"
'''

SECTIONS_PY = '''# -*- coding: utf-8 -*-
# Topic -> accent colour. Order here is the order cards appear in the app.
SECTIONS = {
    "HASHING": "#6d28d9",
}
'''

PROBLEMS_PY = '''# -*- coding: utf-8 -*-
# Which problems are in the deck. Language-neutral: the card title is built from
# `lc` and `title`, so it is identical in every language (progress is keyed on it).
#   lc      LeetCode number (any positive int works for non-LeetCode problems)
#   title   short English title, as on LeetCode
#   section key from sections.py
#   slug    LeetCode URL slug (the app links to https://leetcode.com/problems/<slug>/)
#   tag     optional badge on the front, e.g. "META" for company-tagged problems
PROBLEMS = [
    dict(lc=1, title="Two Sum", section="HASHING", slug="two-sum"),
]
'''

VARIANTS_PY = '''# -*- coding: utf-8 -*-
# Problems referenced as "variants" on a card back but not in the deck themselves.
# lc -> (official title, slug). The app lists them in the menu with LeetCode links.
VARIANTS = {
    167: ("Two Sum II - Input Array Is Sorted", "two-sum-ii-input-array-is-sorted"),
    15: ("3Sum", "3sum"),
}
'''

# ── English ──
EN_CONCEPTS = '''# -*- coding: utf-8 -*-
from grindcards.helpers import *

CONCEPTS = [
    ("C", "HASHING", "Complement Lookup",
     LEAD("You need a pair (or a partner) that satisfies a relation.") +
     "Why does a hash map turn a nested loop into one pass?",
     [
        K("Ask each element <b>who would complete me?</b> — then look that partner up "
          "in O(1) instead of scanning for it."),
        C("""
seen = {}                     # value -> index
for i, x in enumerate(nums):
    if target - x in seen:    # my partner already passed by
        return [seen[target - x], i]
    seen[x] = i               # insert AFTER the check
"""),
        L("Store <b>what you would look up later</b>, keyed by the thing you can compute now.",
          "Check before insert — otherwise <code>x</code> pairs with itself when <code>target = 2x</code>.",
          "Same idea generalises: prefix sums, anagram signatures, 'seen this state?'"),
        CX("O(n) time · O(n) space · one pass"),
     ]),
]
'''

EN_STATEMENTS = '''# -*- coding: utf-8 -*-
# lc -> (statement_html, example_line). Write the statement in your own words —
# it is what you will see on the front of the card. Keep the example short.
STMT = {
    1: ("Given an array of integers and a <code>target</code>, return the indices of the "
        "two numbers that add up to <code>target</code>. Exactly one answer exists; "
        "you may not use the same element twice.",
        "nums = [3, 8, 11, 4], target = 12  →  [1, 3]"),
}
'''

EN_HINTS = '''# -*- coding: utf-8 -*-
# lc -> [hint1, hint2, hint3]: progressively stronger nudges, revealed one at a time.
HINTS = {
    1: ["Brute force is O(n²). Which of the two loops is doing 'search' work?",
        "For each x you are looking for exactly one value: target - x.",
        "A hash map answers 'have I seen this value, and where?' in O(1)."],
}
'''

EN_DEEP = '''# -*- coding: utf-8 -*-
# lc -> dict(pat=(why this pattern, concept card title), fq=[(question, answer)],
#            var=[(problem name incl. "LC n", how it differs)])
DEEP = {
    1: dict(
        pat=("The inner loop only ever searches for one specific value — that is a lookup, "
             "and lookups belong in a hash map.", "Complement Lookup"),
        fq=[("What if the array is sorted?",
             "Two pointers from both ends: O(n) time, O(1) space, no map needed."),
            ("What if you need all pairs, not one?",
             "Count occurrences first, then for each value pair it with its complement's count; "
             "handle x == target - x separately.")],
        var=[("LC 167 Two Sum II", "sorted input → two pointers instead of a map"),
             ("LC 15 3Sum", "fix one element, then Two Sum on the rest; dedupe")],
    ),
}
'''

EN_SOLUTIONS = '''# -*- coding: utf-8 -*-
# lc -> dict(idea=[3–6 bullets], code="...", keys=[..., complexity], test="expr", want=value)
#
# `idea` is the derivation, first person, present tense, as if thinking aloud in the
# interview — including the wrong turn. `code` must run: `grindcards verify` executes
# it against `test` and compares with `want`. Keep every code line ≤ 64 characters.
SOL = {
    1: dict(
        idea=[
            "Two nested loops obviously work: try every pair. That is O(n²) — the interviewer will wait.",
            "What is the inner loop actually doing? For a fixed <code>x</code> it scans for one value, "
            "<code>target - x</code>. A scan for one known value is a <i>lookup</i>.",
            "Lookups are what hash maps are for. If I store every value I have passed, "
            "'have I seen <code>target - x</code>?' is O(1).",
            "One pass, check before insert, so nothing pairs with itself. "
            "Map to the index, because the answer wants indices.",
        ],
        code="""
def twoSum(nums, target):
    seen = {}                        # value -> index
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i                  # insert after the check
    return []
""",
        keys=[
            "Turn 'search for a partner' into 'look up a partner': map from value to index.",
            "Check, then insert — order guards against using the same element twice.",
            "O(n) time · O(n) space",
        ],
        test="twoSum([3, 8, 11, 4], 12)",
        want=[1, 3],
    ),
}
'''

EN_FIGURES = '''# -*- coding: utf-8 -*-
# Optional vector figures, lc -> "<svg …>". Build them with grindcards.svgdia so
# they inherit the app's colours and dark mode, e.g.:
#
#   from grindcards.svgdia import Fig
#   f = Fig(); r = f.row([3, 8, 11, 4], idx=True); f.ptr(r, 3, "x")
#   f.caption("seen = {3:0, 8:1, 11:2}  →  12 - 4 = 8 is there")
#   FIG = {1: f.done()}
FIG = {}
'''

# ── 中文 ──
ZH_CONCEPTS = '''# -*- coding: utf-8 -*-
from grindcards.helpers import *

CONCEPTS = [
    ("C", "HASHING", "Complement Lookup",
     LEAD("要找一对（或一个搭档）满足某个关系。") +
     "为什么哈希表能把双重循环变成一趟？",
     [
        K("对每个元素问一句<b>「谁能配上我？」</b>——然后 O(1) 去查那个搭档，"
          "而不是从头扫一遍找它。"),
        C("""
seen = {}                     # 值 -> 下标
for i, x in enumerate(nums):
    if target - x in seen:    # 我的搭档已经出现过了
        return [seen[target - x], i]
    seen[x] = i               # 先查后存：不会和自己配对
"""),
        L("存的是<b>以后要查的东西</b>，键是现在就能算出来的东西。",
          "先查再插——否则 <code>target = 2x</code> 时 <code>x</code> 会和自己配对。",
          "同一思路可以推广：前缀和、异位词签名、「这个状态见过没」。"),
        CX("O(n) 时间 · O(n) 空间 · 一趟"),
     ]),
]
'''

ZH_STATEMENTS = '''# -*- coding: utf-8 -*-
STMT = {
    1: ("给一个整数数组和一个 <code>target</code>，返回和为 <code>target</code> 的两个数的下标。"
        "恰好有一个答案；同一个元素不能用两次。",
        "nums = [3, 8, 11, 4], target = 12  →  [1, 3]"),
}
'''

ZH_HINTS = '''# -*- coding: utf-8 -*-
HINTS = {
    1: ["暴力是 O(n²)。两层循环里，哪一层在做「查找」？",
        "对每个 x，你要找的其实只有一个值：target - x。",
        "哈希表能 O(1) 回答「这个值见过没、在哪」。"],
}
'''

ZH_DEEP = '''# -*- coding: utf-8 -*-
DEEP = {
    1: dict(
        pat=("内层循环始终只在找一个确定的值——那是查找，查找就该交给哈希表。",
             "Complement Lookup"),
        fq=[("如果数组是有序的呢？",
             "双指针从两头夹：O(n) 时间、O(1) 空间，不需要哈希表。"),
            ("如果要所有的对，不止一对？",
             "先计数，再对每个值配上它补数的个数；x == target - x 的情况单独处理。")],
        var=[("LC 167 Two Sum II", "输入有序 → 用双指针替代哈希表"),
             ("LC 15 3Sum", "固定一个数，剩下的做 Two Sum；注意去重")],
    ),
}
'''

ZH_SOLUTIONS = '''# -*- coding: utf-8 -*-
SOL = {
    1: dict(
        idea=[
            "两层循环显然能做：试所有的对。O(n²)——面试官会等着我优化。",
            "内层循环到底在干什么？固定 <code>x</code> 之后，它在扫一个确定的值 "
            "<code>target - x</code>。扫一个已知的值，本质是<i>查找</i>。",
            "查找就是哈希表的活。把走过的值都存起来，「<code>target - x</code> 见过没」就是 O(1)。",
            "一趟走完，先查再存，元素就不会和自己配对。值存下标，因为答案要的是下标。",
        ],
        code="""
def twoSum(nums, target):
    seen = {}                        # 值 -> 下标
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i                  # 查完再插入
    return []
""",
        keys=[
            "把「找搭档」变成「查搭档」：值 → 下标的映射。",
            "先查后插——这个顺序保证同一个元素不会用两次。",
            "O(n) 时间 · O(n) 空间",
        ],
        test="twoSum([3, 8, 11, 4], 12)",
        want=[1, 3],
    ),
}
'''

ZH_FIGURES = '''# -*- coding: utf-8 -*-
# 可选的矢量图，lc -> "<svg …>"。用 grindcards.svgdia 画，自动跟随 app 配色和深色模式。
FIG = {}
'''

LANG_FILES = {
    "en": {"concepts.py": EN_CONCEPTS, "statements.py": EN_STATEMENTS, "hints.py": EN_HINTS,
           "deep.py": EN_DEEP, "solutions.py": EN_SOLUTIONS, "figures.py": EN_FIGURES},
    "zh": {"concepts.py": ZH_CONCEPTS, "statements.py": ZH_STATEMENTS, "hints.py": ZH_HINTS,
           "deep.py": ZH_DEEP, "solutions.py": ZH_SOLUTIONS, "figures.py": ZH_FIGURES},
}

GITIGNORE = '''build/
__pycache__/
'''


def init_deck(root: Path, name: str, langs: list[str], default: str | None = None) -> list[str]:
    root = Path(root)
    if root.exists() and any(root.iterdir()):
        raise DeckError(f"{root} exists and is not empty")
    unknown = [l for l in langs if l not in LANG_FILES]
    if unknown:
        raise DeckError(f"no sample content for language(s) {unknown}; available: {sorted(LANG_FILES)}. "
                        "Init with a supported language, then copy its folder and translate.")
    default = default or langs[0]
    if default not in langs:
        raise DeckError(f"default language {default!r} is not in {langs}")
    root.mkdir(parents=True, exist_ok=True)
    written = []

    def w(rel, text):
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        written.append(rel)

    w("deck.toml", DECK_TOML.format(name=name, langs=", ".join(f'"{l}"' for l in langs), default=default))
    w("sections.py", SECTIONS_PY)
    w("problems.py", PROBLEMS_PY)
    w("variants.py", VARIANTS_PY)
    w(".gitignore", GITIGNORE)
    for lang in langs:
        for fn, text in LANG_FILES[lang].items():
            w(f"{lang}/{fn}", text)
    return written
