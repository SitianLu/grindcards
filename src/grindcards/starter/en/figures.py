# -*- coding: utf-8 -*-
# Figures for the reasoning section, lc -> "<svg …>". Drawn with grindcards.svgdia:
# colours are CSS variables, so dark mode follows automatically.
from grindcards.svgdia import Fig, INK, MUTE, AC, HI, FILL, BAD, GOOD, PAD

FIG = {}

# ── 1 Two Sum: from "scan ahead" to "look it up" ─────────────────
f = Fig()
f.title("nums = [3, 8, 11, 4]     target = 12")
f.gap(22)
r = f.row(["3", "8", "11", "4"], cw=48, idx=True, hl={3})
f.ptr(r, 3, "I'm here", color=AC)
f.gap(14)
f.caption("Don't scan ahead for 8 — ask: seen 12 − 4 = 8 yet?", fill=AC,
          weight="600")
f.gap(10)
f.row(["3 → 0", "8 → 1", "11 → 2"], cw=60, x0=20)
f.text(216, f.y - 6, "seen (left of me only)", size=9.5, fill=MUTE,
       anchor="start")
f.gap(10)
f.caption("Hit → return [1, 3]. Lookup went from O(n) to O(1).", fill=GOOD,
          weight="600")
f.gap(14)
f.caption("Check first, insert after — so at check time", fill=INK)
f.caption("only numbers left of me are in the map:", fill=INK)
f.caption("no self-pairing, [6,6] for 12 needs no special case.", fill=INK)
FIG[1] = f.done()


# ── 49 Group Anagrams: compute a key, don't compare ──────────────
f = Fig()
f.title('["care", "race", "cat"]')
f.gap(12)
f.caption("Pairwise: every pair re-asks 'same letter counts?'", fill=BAD,
          weight="600")
f.gap(10)
f.caption("Instead, give each word a canonical form as key:", fill=INK,
          weight="600")
f.gap(8)
for w, key, col in (("care", "(1,0,1,0,1,…,1,…)", AC),
                    ("race", "(1,0,1,0,1,…,1,…)", AC),
                    ("cat", "(1,0,1,0,0,…,1,…)", GOOD)):
    f.row(list(w), cw=26, x0=16, strokes=[col] * len(w))
    f.text(130, f.y - 6, key, size=9, fill=col, anchor="start", mono=True)
    f.gap(8)
f.gap(6)
f.caption("First two keys match → same group, zero comparisons.", fill=GOOD,
          weight="600")
f.gap(12)
f.caption("26-slot count key: O(k), vs O(k log k) for sorted(s).",
          fill=INK, weight="600")
f.gap(6)
f.caption("A list can't be a dict key — turn it into a tuple.")
FIG[49] = f.done()


# ── 11 Container With Most Water: why dropping the short side is safe ──
f = Fig()
f.title("height = [3, 9, 4, 7, 2, 8]")
f.gap(10)
f.bars([3, 9, 4, 7, 2, 8], hl={0, 5}, h=50,
       labels=["l", "", "", "", "", "r"])
f.gap(12)
f.caption("Start from the widest pair. Width only shrinks now —",
          fill=INK, weight="600")
f.caption("so the only hope for more area is height.", fill=INK,
          weight="600")
f.gap(12)
f.caption("And height is capped by the short post (l = 3).", fill=AC)
f.gap(12)
f.caption("Keep the short side and move only the tall one:", fill=BAD,
          weight="600")
f.gap(6)
f.bars([3, 9, 4, 7, 2], hl={0, 4}, h=40, color=BAD,
       labels=["l", "", "", "", "r−1"])
f.gap(10)
f.caption("Cap is still 3, width is smaller — always worse.", fill=BAD)
f.gap(10)
f.caption("The short post beats nothing on its far side, so",
          fill=GOOD, weight="600")
f.caption("all its pairs go in one batch — that's why it's linear.",
          fill=GOOD)
FIG[11] = f.done()


# ── 3 Longest Substring Without Repeats: jump the left end in one step ──
f = Fig()
f.title('s = "abba"     no repeats inside the window')
f.gap(22)
r = f.row("abba", cw=44, idx=True, hl={2})
f.ptr(r, 2, "r hits b: collides with index 1", color=AC)
f.gap(14)
f.caption("Crawling the left end is slow, and I know exactly", fill=INK,
          weight="600")
f.caption("where it hit: last[b] = 1 → jump l straight to 2.", fill=GOOD)
f.gap(26)
r2 = f.row("abba", cw=44, idx=True, hl={3})
f.ptr(r2, 3, "r reaches the last a", color=BAD)
f.gap(14)
f.caption("Map says last[a] = 0 — but the window is [2, 3],",
          fill=BAD, weight="600")
f.caption("so 0 is already outside it.", fill=BAD, weight="600")
f.gap(4)
f.caption("Jump anyway: l goes from 2 back to 1. Not a window.", fill=BAD)
f.gap(10)
f.caption("So the guard is last[ch] >= l. That's the one trap.", fill=INK,
          weight="600")
FIG[3] = f.done()


# ── 560 Subarray Sum Equals K: a range sum becomes a difference ──
f = Fig()
f.title("nums = [1, 2, 3, -3, 3]    k = 3")
f.gap(10)
f.caption("Prefix sums (pre[-1] = 0 is the empty prefix):", fill=INK,
          weight="600")
f.gap(6)
r = f.row(["0", "1", "3", "6", "3", "6"], cw=48,
          idx=["∅", "0", "1", "2", "3", "4"], hl={2, 5})
f.gap(8)
f.caption("At j=4, pre = 6, so I look for 6 − 3 = 3.",
          fill=AC, weight="600")
f.gap(6)
f.caption("3 appeared twice (indices 1 and 3) → 2 ranges here.",
          fill=GOOD)
f.gap(12)
f.caption("So store counts, not indices — the ask is 'how many'.",
          fill=INK, weight="600")
f.gap(12)
f.caption("Negatives → no sliding window: [1,-1,0], k=0 fails —", fill=BAD)
f.caption("eat one more cell and the sum can drop, so", fill=BAD)
f.caption("'too big → shrink' means nothing.", fill=BAD)
FIG[560] = f.done()


# ── 33 Search in Rotated Sorted Array: one half is always sorted ──
f = Fig()
f.title("nums = [6,8,9,1,3,4]     one cliff only: 9 | 1")
f.gap(20)
r = f.row(["6", "8", "9", "1", "3", "4"], cw=40, idx=True)
f.line(f.edge(r, 3), r[1] - 6, f.edge(r, 3), r[1] + r[5] + 4, stroke=BAD,
       sw=1.6, dash="3 2")
f.text(f.edge(r, 3), r[1] - 10, "cliff", size=9, fill=BAD)
f.gap(16)
f.caption("Cut at mid = 2:", fill=INK, weight="600")
f.gap(6)
r2 = f.row(["6", "8", "9", "1", "3", "4"], cw=40,
           hl={0, 1, 2})
f.span(r2, 0, 2, "sorted → test endpoints", color=GOOD, drop=8)
f.span(r2, 3, 5, "cliff → can't tell", color=BAD, drop=8)
f.gap(14)
f.caption("One cliff can wreck at most one half; the other", indent=2)
f.caption("half is sorted. Binary search never needed the whole", indent=2)
f.caption("array sorted — only a way to pick which half to go to.", indent=2)
FIG[33] = f.done()

# ── 227 Basic Calculator II: the stack holds terms ───────────────
f = Fig()
f.title('"3+2*2-6/4"    the stack holds finished terms')
f.gap(10)
STEPS = [
    ("read 3, previous op +", ["3"], "push"),
    ("read 2, previous op +", ["3", "2"], "push"),
    ("read 2, previous op *", ["3", "4"], "pop 2, push 2*2"),
    ("read 6, previous op −", ["3", "4", "-6"], "push −6"),
    ("read 4, previous op /", ["3", "4", "-1"], "pop −6, push int(−6/4)"),
]
for i, (head, st, note) in enumerate(STEPS):
    f.caption(head, fill=INK, weight="600" if i in (2, 4) else None)
    f.gap(4)
    f.row(st, cw=30, h=19, x0=14, mono=True,
          hl={len(st) - 1} if i in (2, 4) else set())
    f.text(14 + len(st) * 31 + 8, f.y - 5, note, size=9,
           fill=AC if i in (2, 4) else MUTE, anchor="start")
    f.gap(9)
f.gap(2)
f.caption("Sum the stack at the end: 3 + 4 − 1 = 6", fill=GOOD, weight="600")
f.gap(4)
f.caption("Note int(−6/4) = −1, but −6 // 4 = −2.", fill=BAD)
FIG[227] = f.done()


# ── 236 Lowest Common Ancestor: let the recursion report bottom-up ──
f = Fig()
f.title("LCA of p=1 and q=7")
f.gap(6)
T = ("8", ("3", ("1", None, None), ("6", ("4", None, None),
                                     ("7", None, None))),
     ("10", None, ("14", None, None)))
f.tree(T, hl={"1", "7", "3"}, hledge={("3", "1"), ("3", "6"), ("6", "7")},
       vgap=30)
f.gap(12)
f.caption("Each subtree answers one question:",
          fill=INK, weight="600")
f.caption("what's the best I can hand up from inside me?",
          fill=INK, weight="600")
f.gap(8)
f.caption("1 is a target → returns itself", fill=AC, indent=4)
f.caption("6: only the right side non-empty → passes 7 up", fill=AC, indent=4)
f.caption("3: both sides non-empty → targets split → LCA", fill=GOOD,
          indent=4, weight="600")
f.caption("8: only the left side non-empty → passes 3 up", fill=MUTE, indent=4)
f.gap(12)
f.caption("Return-on-hit also covers p being q's ancestor —", fill=INK)
f.caption("the answer just lands on p, no special case.", fill=INK)
FIG[236] = f.done()


# ── 124 Max Path Sum: return one leg, record two ─────────────────
T124 = ("1", ("2", ("4", None, None), ("5", None, None)), ("3", None, None))
f = Fig()
f.gap(6)
f.tree(T124, hl={"2", "4", "5"}, hledge={("2", "4"), ("2", "5")})
f.gap(12)
f.caption("Path 4–2–5 bends at 2: 4 + 2 + 5 = 11", fill=AC, weight="600")
f.caption("← this value only goes into the answer", fill=AC, indent=10)
f.gap(3)
f.caption("Reported up to parent 1: 2 + max(4, 5) = 7", fill=INK, weight="600")
f.caption("← one leg only", fill=INK, indent=10)
f.gap(16)
f.caption("If 2 reported both legs (11) instead:", fill=BAD, weight="600")
f.gap(8)
f.tree(T124, r=11, vgap=28, hl={"2"}, color=BAD,
       hledge={("2", "4"), ("2", "5"), ("1", "2")})
f.gap(10)
f.caption("Node 2 now has three edges — a fork, not a path.", fill=BAD)
FIG[124] = f.done()


# ── 207 Course Schedule: finishable ⟺ acyclic ────────────────────
f = Fig()
f.title("prereqs = [[1,0], [2,1]]   arrow → the later course")
f.gap(14)
f.graph({"0": (74, 12), "1": (170, 12), "2": (266, 12)},
        [("0", "1"), ("1", "2")], hl={"0"})
f.gap(14)
f.caption("In-degree 0 = all prerequisites done → take it now.", fill=GOOD,
          weight="600")
f.caption("Done: each course it points to loses one in-degree;", fill=GOOD)
f.caption("whoever drops to 0 joins the queue.", fill=GOOD)
f.gap(16)
f.caption("With a cycle: [[1,0], [0,1]]", fill=BAD, weight="600")
f.gap(14)
f.graph({"0": (122, 12), "1": (218, 12)},
        [("0", "1"), ("1", "0")], color=BAD, hledge={("0", "1"), ("1", "0")})
f.gap(14)
f.caption("Both in-degrees stay 1, never 0 — nobody queues.", fill=BAD)
f.gap(6)
f.caption("So the final test is \"pops == numCourses\".", fill=INK,
          weight="600")
FIG[207] = f.done()


# ── 139 Word Break: greedy dead end + dp[0] is the spark ─────────
f = Fig()
f.title('s = "cars"    dict = ["car", "ca", "rs"]')
f.gap(12)
f.caption("Greedy \"always match the longest word\":", fill=BAD, weight="600")
f.gap(8)
r = f.row("cars", cw=44, idx=True, strokes=[BAD, BAD, BAD, INK])
f.gap(6)
f.span(r, 0, 2, "eat car … one s left, stuck", color=BAD, drop=2)
f.gap(20)
f.caption("Answer is ca + rs — so no greed; allow backing up.", fill=GOOD,
          weight="600")
f.gap(14)
f.caption("dp[i] = can the first i characters be fully split:", fill=INK, weight="600")
f.gap(8)
f.row(["T", "F", "T", "F", "T"], cw=48,
      idx=["dp0", "dp1", "dp2", "dp3", "dp4"], hl={0, 2, 4})
f.gap(10)
f.caption("dp[2] ← dp[0] and \"ca\" in the dictionary", fill=AC, indent=4)
f.caption("dp[4] ← dp[2] and \"rs\" in the dictionary", fill=AC, indent=4)
f.gap(12)
f.caption("dp[0] = True is the spark — \"\" always splits.", fill=GOOD,
          weight="600")
f.caption("Without it all False — even s=car comes back false.", fill=GOOD)
FIG[139] = f.done()
