# Flashcard style spec

The layout is settled. What decides whether a deck is good is the *writing*. Read the
writing rules before authoring `cards.py`.

## Physical format

- **US Letter**, margins `0.42in 0.25in 0.30in 0.25in`. Content width 8.0in.
- Each card is one **8.0 × 3.0 in strip**, split into two 4.0in panels: left = front, right = back.
- **3 strips per page**, 0.085in gap. Thin solid border = cut line. Dashed center line = fold line.
- Fold the right panel *behind* the left. Flipping the finished card around its vertical
  spine shows the back upright — this is why no panel is ever rotated 180°.
- Print **single-sided**. Never duplex: registration drift ruins the alignment.
- Finished card: 4 × 3 in — palm-sized, pocketable, still fits ~20 lines of code.

## Typography

- Sans: `Noto Sans CJK SC, DejaVu Sans`. Mono: `DejaVu Sans Mono, Noto Sans Mono CJK SC`.
- Front hook starts at 14pt and auto-shrinks (min 6.5pt). Back body starts at 8.0pt
  (min 4.3pt). Everything inside the back is sized in `em` so it scales with the body —
  **never give `pre`, `table`, or `.cx` an absolute pt size**, or shrinking silently
  stops working on code-heavy cards.
- The fitter checks vertical overflow **and** horizontal overflow of `pre` (code never
  wraps, so a long line would otherwise be clipped without warning).
- Code is syntax-highlighted by `build/highlight.py` — a deliberately small Python
  tokenizer. Anything it can't classify stays plain text, so a mis-tokenised line degrades
  to unstyled rather than to broken markup. Both outputs use it; the PDF gets the light
  palette, the app switches palettes with the system theme.

## Color

One accent color per section, used on the front section label, the front rule, and the
back's dot. Muted 700-level tones so they survive grayscale printing:

```
ARRAYS & HASHING #1d4ed8   TWO POINTERS  #0369a1   SLIDING WINDOW #047857
PREFIX SUM       #0e7490   BINARY SEARCH #c2410c   STACK          #9f1239
HEAP             #6d28d9   INTERVALS     #b45309   LINKED LIST    #4338ca
TREES            #15803d   GRAPHS        #7e22ce   UNION FIND     #0f766e
BACKTRACKING     #a21caf   DYNAMIC PROG. #a16207   GREEDY         #65a30d
SORT & SELECT    #475569   STRINGS       #db2777   DESIGN         #b91c1c
BIT & MATH       #78716c   INTERVIEW CRAFT #525252
```

Problem-card **fronts** ignore this table and use `var(--mute)` gray. Only backs are colored.

Semantic boxes are fixed regardless of section: **green = 心法/insight**,
**amber = 坑/gotcha**, **gray = code**. Consistency here is what makes a card scannable
in one second.

## Two kinds of card

A deck mixes two kinds, and they are written differently because they train different recall.

| | **Concept card** (`"C"`) | **Problem card** (`"P"`) |
|---|---|---|
| Trains | 看 pattern → 回忆模板、不变量、复杂度 | 看题目 → 回忆<b>该用哪个 pattern</b> + 解法 |
| Title | the pattern's name (`Monotonic Stack`) | `LC 1249 · Minimum Remove to Make Valid Parens` |
| Front label | the section name, in the section color | the word **Problem**, in neutral gray |
| Front accent | section color | gray |
| Back header | the card title | **the pattern name, in the section color** |
| Front body | small lead + the big question, centred at 24px | **full problem statement + one example line**, top-aligned at 18px, then a generic prompt |
| Hints | none | 2–3 hidden hints, revealed one tap at a time |
| Extras | none | LeetCode slug → link + one-tap "加入待练" |

The colour rule is the whole point of the split: **a problem card's front must not leak
which pattern it is** — identifying the pattern is exactly what you're recalling. So the
front is colourless and the back reveals both the pattern name and its colour. A concept
card has nothing to hide, so it shows its pattern up front.

The same logic governs the **front text**. A problem card's front is a mock-interview
prompt, and it has exactly three parts in this order:

1. **The statement** (`<span class='stmt'>`) — what the interviewer would actually say out
   loud. Given what → return what → which boundaries are settled. Name the real parameters
   (`nums`, `s`, `t`, `k`, `root`, `grid`) so the example below lines up with the prose.
   Two to four sentences; a one-line paraphrase is not enough to attempt the problem cold.
2. **One example** (`<span class='ex'>`) — a single mono line, `输入 → 输出`. This is the
   highest-value line on the card: it makes the problem concrete in about a second and
   leaks nothing. Design problems get a short call trace instead
   (`cap=2: put(1,1) put(2,2) get(1)→1 put(3,3) get(2)→-1`). Omit it only when you truly
   can't write one — never pad it.
3. **The fixed prompt** — `Pattern?　关键洞察?　复杂度?`, unchanged on every card.

Constraints belong in the statement **only when the interviewer would state them**: 已排序,
含负数, 元素互不相同, 保证有唯一解, 可能为空. Those are given information. Anything that
points at the approach ("能不能 O(1) 空间做?", "注意窗口不单调") is a hint and belongs in the
ladder. Grep a finished deck for 哈希 / 双指针 / 滑窗 / 前缀和 / 单调栈 / 二分 / 回溯 / 拓扑 —
none of them may appear in a statement.

A fuller statement changes the type scale: the front is now a paragraph, not a headline.
Problem-card hooks start at **18px** (min 13.5) and are **top-aligned** so every card's
first line lands in the same place; concept cards keep 24px and stay vertically centred,
because their one-sentence question earns the big type. Inline `<code>` inside a statement
drops its background and border — five grey chips in one paragraph is noisier than the
monospace alone.

**The hint ladder** (`extra["hints"]`, 2–3 entries, hidden until tapped):

1. **注意什么** — point at the constraint or trap. Never name the pattern.
   *"数组含负数——滑动窗口为什么在这里失效？"*
2. **点名 pattern** — *"前缀和 + 哈希表。"*
3. **关键那一步** — the one detail that decides correctness, only when it earns its place.
   *"哈希表必须以 {0: 1} 起手，代表空前缀。"*

A hint that gives the whole answer is a wasted rung. If hint 1 already solves the problem,
rewrite it as an observation rather than an instruction.

Roughly 1 concept card per 2–3 problem cards. Every section with problem cards should have
at least one concept card, or the pattern has nowhere to be taught.

## Writing rules

**Concept-card front — lead, then hook.** (Problem-card fronts are the three-part
statement described under "Two kinds of card" — statement, example, fixed prompt.)

Every concept-card front has two parts, in this order:

1. **Lead** (`<span class='lead'>`) — one plain sentence naming the topic.
   "窗口 [l, r] 在数组上滑动，右指针扩张，左指针收缩。" It orients someone who picked the
   card up cold. Never ask anything here; never hint at the answer. One sentence, no bold.
2. **Hook** — the question itself.

- Ask a real question the reader can *attempt* before flipping. "Sliding window" is a label;
  "when do you shrink `left` — and which way does the rule flip for 最长 vs 最短?" is a hook.
- **Concept-card hooks ask for the rule, the invariant, or the decision** — "when do you
  shrink left?", "min-heap or max-heap?", "what must be true about the data?" Not "explain
  sliding window".
- Bold the 2–4 words that carry the question. The reader's eye lands there first.
- Prefer questions that expose the *counterintuitive* bit: "the answer feels backwards",
  "a stale value sounds like a bug — argue that it isn't", "which one leaves the answer
  correct but wrecks the runtime?"
- Use `<span class='sub'>` for a one-line nudge when the question alone is too bare.
- Never put the answer, or a giveaway keyword, on the front.

**Problem-card back — a fixed four-part solution.**

Free-form backs read as "solution 不全 而且奇怪": some cards opened with the insight, some
with code, some never said which pattern it was. Every problem card's back is now exactly
these four, in order, and the assembler discards whatever else was authored:

```python
PAT(why, "Hashmap as Memory"),   # ① 使用 pattern —— 名字 + 为什么是它，芯片可点到概念卡
IDEA([...]),                     # ② 思路分析 —— 2–4 步，讲为什么，不是复述代码
DIA("""..."""),                   # ②b 图解 —— 可选但尽量画
C(code),                         # ③ 完整代码实现 —— 能直接跑，不是骨架
KEYS([...]),                     # ④ 关键记忆点 —— 2–4 条，最后一条是复杂度
```

- **`IDEA` is reasoning, not narration.** The first step is usually *the rewrite* — the move
  that turns the original problem into an easier one ("把「找配对」变成「查记忆」"). The last
  is usually *why it can't miss*. "创建一个哈希表 seen" is narrating the code; delete it.
- **`DIA` must let you replay one execution of the algorithm.** Max 8 lines, max 52
  half-width columns (CJK counts as 2) — wider and it shrinks past legibility on a phone.
  Worth drawing for windows expanding/shrinking, pointers meeting, a stack's ins and outs,
  a grid being flooded, a DP table filling. If you can't get information into it, set it to
  `None`; a padded diagram is worse than none.
- **`C` is the whole function now, not the shape.** This reversed the old rule. It must run:
  real signature with LeetCode's method name, imports included, edge cases handled. Do not
  define `TreeNode`/`ListNode` — assume them. Type annotations are **stripped at build time**
  by `codefmt.strip_hints`, because `def twoSum(nums: list[int], target: int) -> list[int]:`
  wraps to three lines on a 393px card; author them if you like, they won't ship.
- **`KEYS` last item is always complexity** — the renderers rely on it, splitting it off into
  the dotted footer. Middle items are gotchas phrased as *the mistake actually made*:
  "坑：用双 map 特判 duplicate → [3,2,4], t=6 返回 (0,0)" beats "be careful with duplicates".
- Add a concrete counterexample wherever a claim is abstract — "贪心不行" is forgettable,
  "coins=[1,3,4], amount=6：贪心 3 枚，DP 2 枚" is not.

**Every code block is executed at build time.** `verify_sol.py` runs each solution against
the `输入 → 输出` example already on the card front. "完整代码实现" either survives execution
or it is a claim, not a fact. A solution without a passing `test`/`want` pair does not ship.

**The printed card cannot hold all four.** Measured: full four parts overflow 42 of 57
panels at 4×3in; dropping the diagram still overflows 18; dropping 思路 too still overflows 9.
The card stays palm-sized, so print carries only what you need *at the moment you flip it* —
pattern name, code, top two 记忆点, complexity — and 思路 + 图解 are app-only
(`PRINT_SKIP` in `render.py`). Code longer than `PRINT_CODE_MAX` lines is truncated with a
visible marker; an unmarked truncation would just be wrong code.

**Concept-card backs stay free-form** — open with `K(...)`, then the template, then `W(...)`
gotchas, then `CX(...)`. The four-part schema is a problem-card rule.

**Depth below `MORE()` — app only.**

The printed card is the core; the app scrolls, so it can carry more. Do not push a
*gotcha* below the marker — gotchas are core and belong on the printed card.

**Problem cards: 深入 is a fixed schema, not free text.** Free-form depth is what made the
old decks read 前言不搭后语 — each card wandered somewhere different. Every problem card's
深入 is exactly three blocks, in this order, answering four questions:

```python
MORE(),
PAT("配对问题 = 用哈希表把「见过的值」变成 O(1) 可查的记忆，"     # ① 这题是什么 pattern，为什么
    "暴力两重循环退化成一次遍历。",
    "Hashmap as Memory"),                                    # ② 对应哪张概念卡（必须是真实标题）
FQ([("数组已经有序呢？", "双指针从两端夹逼，<b>O(1) 空间</b>。面试官常用这句把你逼到双指针。"),
    ("能不能不用额外空间？", "不排序就不行——不排序时你必须记住见过什么。")]),   # ③ 面试会追问什么
VAR([("LC 167 Two Sum II", "输入<b>有序</b> → 双指针，O(1) 空间"),
     ("LC 15 3Sum",        "固定一个数 + 双指针，去重要做两处")]),              # ④ 还有什么变种
```

- `PAT(why, concept)` — one sentence on *why this problem is that pattern*, phrased as the
  recognition cue you'd want in an interview ("含负数 → 滑窗失效 → 前缀和 + 哈希表"). Not a
  restatement of the solution; the `K(...)` box above already did that. The second argument
  is the **exact title of a concept card in the same deck** — the app renders it as a
  tappable chip in the section color that jumps to that card. A dangling link is a build
  error, so the deck stays navigable.
- `FQ([(q, a)])` — 2–3 追问 an interviewer actually asks after a correct solution: the
  relaxed constraint (已排序? 有重复? 流式输入?), the "why this way" (为什么要带等号?), the
  cost trade (能不能省空间?). Answer in one or two sentences. Not quiz questions to yourself —
  questions someone else asks you.
- `VAR([(problem, diff)])` — 2–4 neighbours, each with the **one thing that changes**, not a
  description. "LC 525 Contiguous Array → 0 记成 -1，找前缀和相同的最远两点" is a variant;
  "另一道前缀和题" is noise. Write the problem name with its number (`LC 525 …`); a row that
  covers two problems can say `LC 159 / 340 …` and the build splits it into two.

**Variants do not become cards.** This is the rule that keeps a deck from rotting. Every
problem has three to five neighbours, so promoting them all would have tripled this deck
with thin, near-duplicate cards — and the whole point of a problem card is that recognising
its pattern is *hard*. A deck where five cards in a row are the same pattern trains nothing.

So the build sorts each `VAR` row into one of two buckets by its LC number:

- **already a card in this deck** → the row renders as a button that jumps to that card,
  same as the `PAT` chip. Nothing new is created.
- **not in the deck** → it is a *变种题*: it goes into `VARIANTS` (a separate table in the
  generated `cards.py`, `{lc: (official title, slug)}`) and shows up in two places only —
  a LeetCode link on the card, and a collapsible-by-section panel in the app's menu with
  one-tap 加入待练. It never enters the deck, never gets flipped, never counts toward
  "已记住 X/94".

Two details that matter when adding variants:

- The title in `VARIANTS` must be the **official LeetCode title**, because the slug is
  its kebab-case — `assemble.py` derives one from the other and a mismatch means a dead
  link. `01 Matrix → 01-matrix`, `All O\`one Data Structure → all-oone-data-structure`,
  `Longest Subarray of 1's… → longest-subarray-of-1s-…` (apostrophes vanish, not hyphenate).
- A problem must not list itself as its own variant; the build drops self-references.

Concept cards keep free-form depth below `MORE()` (alternate implementation, 面试话术,
complexity tables) — the schema is a problem-card rule.

**One card, one idea.**

- Split long topics by *question*, not by length: Dijkstra became "pick the algorithm" /
  "why pop = final" / "the 5 bugs". Each has its own hook and stands alone.
- If a back needs more than ~6 blocks, it's two cards.
- Pure API lookup tables make weak flashcards (nothing to recall). Convert them into a
  question with a wrong-but-tempting answer, or drop them.

**Language.** Default to the source notes' own wording — the user's 口诀 and phrasing are
their memory anchors, so preserve them verbatim. Front hooks may be normalized to English
(interviews are in English); backs keep the original mixed CN/EN.
