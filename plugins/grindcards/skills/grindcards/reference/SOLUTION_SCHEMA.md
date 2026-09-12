# The problem-card back — writing spec

Every problem gets one entry in `<lang>/solutions.py`:
`SOL[lc] = dict(idea=[...], dia="...", code="...", keys=[...], test="...", want=...)`.

The back of the card always renders as four sections, in a fixed order:

1. **Pattern** — the engine attaches this from `deep.py`. **You do not write it here.**
2. **Reasoning** — `idea` (plus an optional figure: `fig` from `figures.py`, or `dia`)
3. **Full implementation** — `code`
4. **Remember** — `keys`

then Follow-ups and Variants, also from `deep.py`. You never lay the back out by hand.

---

## `idea` — Reasoning (required, 3–6 bullets)

**This is a person seeing the problem for the first time, thinking out loud at a whiteboard.**
Not a solution write-up, not a retrospective written once the optimal answer is known. When
you finish, ask: *following these bullets, could I walk through a problem I have never
seen?* If not, it is not written yet.

### Voice

First person, present tense, plain words. Talking to someone, not filling in a form.

- Yes: "Fix the right end r and try every left end 0…r. But once `[l, r]` is already
  enough, going further left only makes it longer — all of that is wasted work."
- No: "**Wasted work:** with r fixed, only one left end is worth considering."
  — the same fact, but the conclusion has been filed back into a slot; it reads like a table.

**Never open a bullet with `<b>Label:</b>`.** Learned the hard way: the first version turned
the CtCI method (brute force first / bottleneck / repeated work / unused constraint /
hand-run an example) into a row of labels stuck on the front of every bullet, believing that
taught the method. It made the reasoning stiffer, because a label is a **category name**,
and nobody thinking about a problem says "wasted work" — they say "I tried every left end
and most of them didn't need trying". **The method lives in the moves, not in their names.**

### The moves (hidden in the sentences, never labelled)

- **Say the dumb way first**, in one sentence, including why it fails (memory blows up /
  which layer is slow)
- **Give yourself a target**: every character has to be looked at once, so the floor is
  O(n) — the extra layer is the thing to kill
- **Stare at the constraint the problem hands you**: single-threaded, BST, no parentheses,
  positive weights. It is written down because you are meant to use it
- **Hand-run a small concrete example** so the traps surface by themselves
  (`["0:start:0","0:end:0"]` gives 1, not 0)
- **Walk into the dead-end and back out.** This is the most human part:
  "Recurse for both legs and it looks done. Then try passing that value upward and it
  won't go —"
- Design problems: **lay out the operations to support first**, then pick the structure;
  whatever the structure is missing, add it
- The user's own wrong turn (see the three questions in `SKILL.md`) goes in here as
  *I tried … and it broke on …*

### Length

**Each bullet ≤ 110 visible characters** (count after stripping HTML tags); aim for a
median around 65. When a bullet runs long it is usually because `keys` material has leaked
in — the concrete trap, the counterexample and the complexity all belong to `keys`.
`idea` keeps only the thinking; do not say the same thing in both places.

### Also

- Explain **why you would think of it**, not what the code does.
  No: `"create a hash map seen"` — that is reading the code aloud.
- `<b>` and `<code>` are fine; no `<br>` or any other block-level tag (the verifier
  rejects them). `<b>` marks a keyword, it does not make a heading.

## `fig` — Figure (SVG, preferred over `dia`)

Drawn with `grindcards.svgdia`, written in `<lang>/figures.py` as `FIG[lc] = f.done()`.
The loader merges figures into the matching `SOL` entry automatically (a figure for a problem
with no solution is an error). A problem with a `fig` never renders its `dia` — drawing the
same thing twice only makes the back longer.

```python
from grindcards.svgdia import Fig, INK, MUTE, AC, HI, FILL, BAD, GOOD

f = Fig()                                    # viewBox is 340 wide
f.title('s = "abba"     no repeats inside the window')
f.gap(22)                                    # ← the next row hangs a ptr above it: leave room
r = f.row("abba", cw=44, idx=True, hl={2})   # a row of cells
f.ptr(r, 2, "r hits b: collides with index 1", color=AC)
f.gap(14)
f.caption("Map says last[a] = 0 — but the window is [2, 3].", fill=BAD)
FIG[3] = f.done()
```

Available primitives:

| primitive | draws | starter deck |
|---|---|---|
| `row` + `span` / `ptr` | arrays, strings, timelines (`fills`/`strokes` per cell), bracketed ranges, pointers | 1 3 33 139 560 |
| `tree` | binary tree; x by inorder, y by depth, so no shape overlaps | 124 236 |
| `chain` + `hop` | linked list plus curved arrows (random pointers, back edges, cycles) | — |
| `bars` | bar chart ("high vs low" problems: peaks, water, stock prices) | 11 |
| `graph` | free-placed graph (constraint graphs, dependency graphs, account–email) | 207 |
| `grid` | grid (island flooding, layered matrix BFS, diagonals) | — |
| `bands` | interval bars sharing one axis | — |
| `stack` / `title` / `caption` | a stack, the header line, annotations | — |

**All 11 problems in the starter deck have a figure.** `dia` remains a valid fallback —
the assembler prefers `fig` when both exist, and the two can coexist in one deck for good.

**There are exactly five colour meanings; do not invent more**: `AC` what I am looking at
now / the correct route, `GOOD` holds, keep it, `BAD` the counterexample and the rejected
route, `MUTE` background, `INK` main strokes. They are all `var(--fig-*)`, so dark mode
follows automatically — **never draw two versions of a figure**.

### What to draw

**Only the one step in the reasoning that is hardest to say out loud**, not a replay of the
whole algorithm. The test: is this the step where "three sentences" loses to "one picture"?
Most good figures are a **contrast**: the right move next to the natural-but-wrong one
(LC 124's three edges on one node, LC 11 moving the tall side, LC 3 jumping blindly to
`last[a] = 0`).

### Layout

`Fig` records the real vertical extent of every primitive and `gap(h)` always starts from
`ymax`, so **sequential calls never overlap**. The only thing you manage yourself is anything
drawn **above the current row** (`ptr(above=True)`, `hop(up=True)`) — those sit above the
cursor, so call `gap()` first to leave headroom. This one was hit: the first `span` label
landed on top of the next row's `ptr`, because the cursor had only been pushed past the
bracket. Keep captions under ~52 characters or they run off the 340px canvas.

## `dia` — Figure (ASCII, the fallback when there is no SVG)

Plain text, rendered monospace. **At most 52 half-width columns and 8 lines**; anything
wider turns to mush on a phone.

Worth drawing: a window expanding and shrinking, two pointers meeting, a monotonic stack's
pushes and pops, a prefix-sum range, a tree's traversal order, directions in a matrix,
overlapping intervals, how a DP table fills.
If the picture carries no information, write `dia=None` — a padded diagram is worse than none.

The standard for a good one: **looking at it, you can replay one execution of the algorithm.**

```
nums = [3, 8, 11, 4]   target = 12
i=0  x=3  need 9  seen={}             miss -> {3:0}
i=3  x=4  need 8  seen={3:0,8:1,11:2} hit  -> [1, 3]
```

Align with spaces, never tabs. CJK glyphs take two columns — count the width yourself.

## `code` — Full implementation (required)

**Must be Python 3 that runs as-is** — not a skeleton, not pseudocode. This was the point of
the rewrite: the old cards gave "the shape of the solution", the new ones give **the version
you can write out character for character in an interview**.

- Full function signature, with LeetCode's official method name (`twoSum`,
  `lengthOfLongestSubstring`, …).
- Imports at the top of the block (`from collections import defaultdict, deque`, etc.).
- **Do not** define `TreeNode` / `ListNode` / `Node` — assume they exist, as on LeetCode.
- Handle the edges (empty input, one element), but do not pile up unrelated defensive `if`s.
- Comment the key steps, and make the comment say **why**, not what the line does.
- **Readability beats line count.** This should look like the code you would really write on
  a whiteboard, not a compressed version:
  - meaningful names (`missing_kinds` rather than `have`, `best_left` rather than a packed tuple)
  - branches spelled out; no `for...else`, no walrus — syntax that saves characters and costs reading
  - three more lines are better than two intentions on one line
  - up to about 40 lines is fine (the back scrolls, and the code block has a full-screen
    button); the verifier only warns past 55
- **Every line ≤ 64 characters.** The card picks its font size from the widest line, so one
  wide line shrinks the whole block. This is a hard limit and matters far more than the line
  count (80 terminal columns is a soft one — CJK comments count double).
- Type annotations may stay: the build strips them before the code ships (a fully annotated
  `def twoSum(...)` wraps to three lines on a phone) and tests the stripped version.

## `keys` — Remember (required, 2–6 items)

The only sentences you carry away from the card. **The last item is always the complexity.**

- First: the crux of this problem, as a positive statement —
  `"Check, then insert — reversed, [3,3] pairs an index with itself"`
- Middle: the traps, written as **mistakes actually made**, not advice.
  Yes: `"Mistake: two maps plus a duplicate special-case → [3,2,4], t=6 returned (0,0)"`
  No: `"Be careful with duplicate elements"`
- Last: `"O(n) time · O(n) space"`, in exactly that shape.

`<b>` and `<code>` are allowed; no block-level tags.

## `test` / `want` — make the code checkable (required)

`test` is a Python expression string, evaluated after `code`; its value must equal `want`.
`grindcards verify` really runs it, and a card that fails or gets the wrong answer does not
ship. Cover the front's example, the input that broke the user, and the degenerate case — a
tuple of calls is the usual shape.

When the result order is not defined, normalise it inside `test`:

```python
test="sorted(map(sorted, groupAnagrams(['care','race','acre','bat','tab','cat'])))",
want=[['acre','care','race'], ['bat','tab'], ['cat']]
```

The verifier pre-defines these (use them directly; do not redefine):

```python
class ListNode: def __init__(self, val=0, next=None)
class TreeNode: def __init__(self, val=0, left=None, right=None)
build_list([1,2,3])      -> ListNode        to_list(head)      -> [1,2,3]
build_tree([3,9,20,None,None,15,7]) -> TreeNode   (LeetCode level order, None = gap)
# plus Optional, List, collections, heapq, bisect, math, itertools, functools
```

For a design problem, write a call sequence:

```python
test="(lambda c=LRUCache(2): [c.put(1,1), c.put(2,2), c.get(1), c.put(3,3), c.get(2)])()[2::2]",
want=[1, -1]
```

If something truly cannot be tested automatically (it needs a LeetCode-private interface
like `NestedInteger`), write `test=None, want=None` and say so honestly in `keys`.
**Anything that can be tested must be.**

---

## Complete example (write yours like this)

This is the real LC 1 entry from the starter deck's `en/solutions.py`:

```python
    1: dict(
        idea=[
            'Dumb way first: for each x, scan everything to its right for '
            '<code>target − x</code>. O(n²).',
            'All the cost is in the <b>searching</b> — and the slice I scan each round is '
            'nearly the same slice as last round.',
            'Flip it around: when I reach x, don\'t look ahead — ask "have I '
            '<b>already</b> seen <code>target − x</code>?"',
            'That turns a search into a memory lookup, O(1) a step. One pass and I\'m done.',
            'Bonus: at check time <code>seen</code> only holds what\'s <b>left</b> of x, '
            'so nothing pairs with itself. No special case.',
        ],
        code="""
def twoSum(nums: list[int], target: int) -> list[int]:
    seen = {}                          # value -> index
    for i, x in enumerate(nums):
        if target - x in seen:         # ① check: left side only
            return [seen[target - x], i]
        seen[x] = i                    # ② insert after
    return []
""",
        keys=[
            '<b>Check, then insert</b>. Reverse the order and <code>[3,3], t=6</code> '
            'pairs an index with itself.',
            'Mistake I made: two maps plus a duplicate special-case → <code>[3,2,4], t=6</code> '
            'returned <code>(0,0)</code>. Check-then-insert handles it in one pass; don\'t patch.',
            'O(n) time · O(n) space',
        ],
        test='twoSum([3, 8, 11, 4], 12)',
        want=[1, 3],
    ),
```

## Language

Write in the language of the folder you are in; keep the technical terms as they are
(pattern / sliding window / DP). Code comments are translated per language; the code itself
is identical in every language, and `verify` checks that. Match the voice of the existing
cards: direct, concrete, always a counterexample — never "we could consider".
