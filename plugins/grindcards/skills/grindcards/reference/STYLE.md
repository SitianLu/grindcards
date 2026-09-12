# Flashcard style spec

The layout is settled. What decides whether a deck is good is the *writing*. Read the
writing rules before authoring a deck.

## Physical format (`grindcards pdf`)

- **US Letter**, margins `0.42in 0.25in 0.30in 0.25in`. Content width 8.0in.
- Each card is one **8.0 × 3.0 in strip**, split into two 4.0in panels: left = front, right = back.
- **3 strips per page**, 0.085in gap. Thin solid border = cut line. Dashed center line = fold line.
- Fold the right panel *behind* the left. Flipping the finished card around its vertical
  spine shows the back upright — this is why no panel is ever rotated 180°.
- Print **single-sided**. Never duplex: registration drift ruins the alignment.
- Finished card: 4 × 3 in — palm-sized, pocketable, still fits ~20 lines of code.

## Typography

- Sans: `Noto Sans CJK SC, Noto Sans, DejaVu Sans`. Mono: `DejaVu Sans Mono, Noto Sans Mono CJK SC`.
- On paper, the front hook starts at 14pt and auto-shrinks (min 6.5pt). The back body
  starts at 8.0pt (min 4.3pt). Everything inside the back is sized in `em` so it scales
  with the body — **never give `pre`, `table`, or `.cx` an absolute pt size**, or shrinking
  silently stops working on code-heavy cards.
- The fitter checks vertical overflow **and** horizontal overflow of `pre` (code never
  wraps, so a long line would otherwise be clipped without warning).
- Code is syntax-highlighted by `grindcards.highlight` — a deliberately small Python
  tokenizer. Anything it can't classify stays plain text, so a mis-tokenised line degrades
  to unstyled rather than to broken markup. Both outputs use it; the PDF gets the light
  palette, the app switches palettes with the system theme.

## Color

One accent color per section, used on the front section label, the front rule, and the
back's dot. Muted 700-level tones so they survive grayscale printing. `sections.py` at the
deck root is the table — the starter deck's:

```
ARRAYS & HASHING #1d4ed8   TWO POINTERS  #0369a1   SLIDING WINDOW #047857
PREFIX SUM       #0e7490   BINARY SEARCH #c2410c   STACK          #9f1239
TREES            #15803d   GRAPHS        #7e22ce   DYNAMIC PROG.  #a16207
```

Add sections in the same register (`HEAP #6d28d9`, `INTERVALS #b45309`, `LINKED LIST
#4338ca`, `GREEDY #65a30d`, `DESIGN #b91c1c` have all worked). Dict order = app order.

Problem-card **fronts** ignore this table and use `var(--mute)` gray. Only backs are colored.

Semantic boxes are fixed regardless of section: **green = insight** (`K`), **amber =
gotcha** (`W`), **gray = code** (`C`). Consistency here is what makes a card scannable in
one second.

## Two kinds of card

A deck mixes two kinds, and they are written differently because they train different recall.

| | **Concept card** (`concepts.py`) | **Problem card** (`problems.py` + the five per-language files) |
|---|---|---|
| Trains | see the pattern → recall the template, invariant, complexity | see the problem → recall **which pattern** + the solution |
| Title | the pattern's name (`Monotonic Stack`) | `LC 1249 · Minimum Remove to Make Valid Parens`, built from `lc` + `title` |
| Front label | the section name, in the section color | the word **Problem**, in neutral gray |
| Front accent | section color | gray |
| Back header | the card title | **the pattern name, in the section color** |
| Front body | small lead + the big question, centred at 24px | **full problem statement + one example line**, top-aligned at 18px, then a fixed prompt |
| Hints | none | three hidden hints from `hints.py`, revealed one tap at a time |
| Extras | none | LeetCode slug → link + one-tap "add to practice list" |

The colour rule is the whole point of the split: **a problem card's front must not leak
which pattern it is** — identifying the pattern is exactly what you're recalling. So the
front is colourless and the back reveals both the pattern name and its colour. A concept
card has nothing to hide, so it shows its pattern up front.

The same logic governs the **front text**. A problem card's front is a mock-interview
prompt, and it has exactly three parts in this order:

1. **The statement** (`STMT[lc][0]`) — what the interviewer would actually say out loud.
   Given what → return what → which boundaries are settled. Name the real parameters
   (`nums`, `s`, `t`, `k`, `root`, `grid`) so the example below lines up with the prose.
   Two to four sentences; a one-line paraphrase is not enough to attempt the problem cold.
2. **One example** (`STMT[lc][1]`) — a single mono line, `input → output`, that you wrote
   yourself (never LeetCode's sample I/O). This is the highest-value line on the card: it
   makes the problem concrete in about a second and leaks nothing. Design problems get a
   short call trace instead (`cap=2: put(1,1) put(2,2) get(1)→1 put(3,3) get(2)→-1`).
   Omit it only when you truly can't write one — never pad it.
3. **The fixed prompt** — `Pattern?　Key insight?　Complexity?`. The engine adds it, in the
   card's language, to every problem card; you never type it.

Constraints belong in the statement **only when the interviewer would state them**: sorted,
contains negatives, all distinct, exactly one answer guaranteed, may be empty. Those are
given information. Anything that points at the approach ("can you do it in O(1) space?",
"note the window isn't monotonic") is a hint and belongs in the ladder. Grep a finished
deck's `statements.py` for hash map / two pointers / sliding window / prefix sum / monotonic
stack / binary search / backtracking / topological — none of them may appear in a statement.

A fuller statement changes the type scale: the front is now a paragraph, not a headline.
Problem-card hooks start at **18px** (min 13.5) and are **top-aligned** so every card's
first line lands in the same place; concept cards keep 24px (min 15) and stay vertically
centred, because their one-sentence question earns the big type. Inline `<code>` inside a
statement drops its background and border — five grey chips in one paragraph is noisier
than the monospace alone.

**The hint ladder** (`HINTS[lc] = [h1, h2, h3]` in `hints.py`, hidden until tapped):

1. **Notice something** — point at the constraint or trap. Never name the pattern.
   *"The array contains negatives — why does a sliding window break down here?"*
2. **Name the pattern** — *"Prefix sums + hash map."*
3. **The key step** — the one detail that decides correctness, only when it earns its place.
   *"The map must start as {0: 1}, standing for the empty prefix."*

A hint that gives the whole answer is a wasted rung. If hint 1 already solves the problem,
rewrite it as an observation rather than an instruction.

Roughly 1 concept card per 2–3 problem cards. Every section with problem cards should have
at least one concept card, or the pattern has nowhere to be taught — and nowhere for the
problem's `pat` to point, which is a build error.

## Writing rules

**Concept-card front — lead, then hook.** (Problem-card fronts are the three-part
statement described under "Two kinds of card" — statement, example, fixed prompt.)

Every concept-card front has two parts, in this order:

1. **Lead** (`LEAD("...")`) — one plain sentence naming the topic.
   "A window [l, r] slides over the array: the right pointer expands, the left pointer
   shrinks." It orients someone who picked the card up cold. Never ask anything here; never
   hint at the answer. One sentence, no bold. The assembler rejects a front without one.
2. **Hook** — the question itself, concatenated after the lead.

- Ask a real question the reader can *attempt* before flipping. "Sliding window" is a label;
  "when do you shrink `left` — and which way does the rule flip for longest vs shortest?"
  is a hook.
- **Concept-card hooks ask for the rule, the invariant, or the decision** — "when do you
  shrink left?", "min-heap or max-heap?", "what must be true about the data?" Not "explain
  sliding window".
- Bold the 2–4 words that carry the question. The reader's eye lands there first.
- Prefer questions that expose the *counterintuitive* bit: "the answer feels backwards",
  "a stale value sounds like a bug — argue that it isn't", "which one leaves the answer
  correct but wrecks the runtime?"
- Use `<span class='sub'>` for a one-line nudge when the question alone is too bare.
- Never put the answer, or a giveaway keyword, on the front.

**Concept-card back — built from the block helpers.**

`from grindcards.helpers import *` gives you one-letter helpers, so a back reads like an
outline rather than markup. These are the ones you write by hand:

| helper | renders as | use it for |
|---|---|---|
| `K(text)` | green box | the one insight worth memorising — open with it |
| `C(code)` | gray code block, never wraps | the template; ≤64 chars per line, same as solutions |
| `W(text)` | amber box | the gotcha, phrased as the mistake actually made |
| `T(head, rows)` | table | a decision matrix (goal → rule → bookkeeping) |
| `P(text)` | paragraph | prose that doesn't fit the boxes |
| `L(*items)` | bullet list | short enumerations |
| `CX(text)` | dotted footer | complexity |
| `MORE()` | fold marker | everything after it is app-only depth |

`PAT`, `IDEA`, `FIG`, `DIA`, `KEYS`, `FQ` and `VAR` also exist in `helpers.py`, but they
are **produced by the engine** from `deep.py`, `solutions.py` and `figures.py` when it
assembles a problem card. Never write them by hand. The usual concept shape: `K(...)`,
`C(...)` the template, `W(...)` gotchas, `CX(...)`, then `MORE()` and whatever depth helps
(alternate implementation, what to say out loud, a variant table). Concept backs stay
free-form; the four-part schema below is a problem-card rule.

**Problem-card back — a fixed four-part solution.**

Free-form backs read as "the solution is incomplete, and odd": some cards opened with the
insight, some with code, some never said which pattern it was. Every problem card's back is
now exactly these four, in order, and the assembler builds them itself — nothing you write
elsewhere in the entry gets in:

```
① Pattern              PAT(why, concept)   ← deep.py   pat=(why, "Hashmap as Memory")
② Reasoning            IDEA([...])         ← solutions.py idea
   (+ figure)          FIG(svg) / DIA(txt) ← figures.py, else solutions.py dia
③ Full implementation  C(code)             ← solutions.py code, annotations stripped
④ Remember             KEYS([...])         ← solutions.py keys, last item = complexity
── MORE() ──
   Follow-ups          FQ([(q, a)])        ← deep.py fq
   Variants            VAR([(name, diff)]) ← deep.py var
```

- **Reasoning is derivation, not narration.** The first step is usually *the rewrite* — the
  move that turns the original problem into an easier one ("turn 'find the pair' into 'look
  it up in memory'"). The last is usually *why it can't miss*. "Create a hash map seen" is
  narrating the code; delete it. Full spec in `SOLUTION_SCHEMA.md`.
- **The diagram must let you replay one execution of the algorithm.** ASCII: max 8 lines,
  max 52 half-width columns (CJK counts as 2) — wider and it shrinks past legibility on a
  phone. If you can't get information into it, set it to `None`; a padded diagram is worse
  than none. An SVG in `figures.py` replaces it.
- **The code is the whole function now, not the shape.** This reversed the old rule. It must
  run: real signature with LeetCode's method name, imports included, edge cases handled. Do
  not define `TreeNode`/`ListNode` — assume them. Type annotations are **stripped at build
  time** by `codefmt.strip_hints`, because `def twoSum(nums: list[int], target: int) ->
  list[int]:` wraps to three lines on a 393px card; author them if you like, they won't ship.
- **The last key is always complexity** — the renderers rely on it, splitting it off into
  the dotted footer. Middle items are gotchas phrased as *the mistake actually made*:
  "Mistake: two maps plus a duplicate special-case → [3,2,4], t=6 returned (0,0)" beats
  "be careful with duplicates".
- Add a concrete counterexample wherever a claim is abstract — "greedy fails" is
  forgettable, "coins=[1,3,4], amount=6: greedy takes 3 coins, DP takes 2" is not.

**Every code block is executed at build time.** `grindcards verify` (and `build`, which runs
it first) executes each solution — the stripped bytes that ship — against its own
`test`/`want` pair, in every language. "Full implementation" either survives execution or it
is a claim, not a fact. A solution without a passing test does not ship.

**The printed card cannot hold all four.** Measured on a 57-card deck: the full four parts
overflowed 42 panels at 4×3in; dropping the diagram still overflowed 18; dropping the
reasoning too still overflowed 9. The card stays palm-sized, so print carries only what you
need *at the moment you flip it* — pattern name, code, top two keys, complexity — and
reasoning + figure are app-only (`PRINT_SKIP` in `render_pdf.py`). Code longer than
`PRINT_CODE_MAX` (24) lines is truncated with a visible marker; an unmarked truncation
would just be wrong code. `grindcards pdf` lists any panel that still overflows.

**Depth below `MORE()` — app only.**

The printed card is the core; the app scrolls, so it can carry more. Do not push a
*gotcha* below the marker — gotchas are core and belong on the printed card.

**Problem cards: depth is a fixed schema, not free text.** Free-form depth is what made the
old decks read as if each card had wandered off somewhere different. Every problem card's
depth is one `deep.py` entry answering four questions:

```python
1: dict(
    pat=('A pairing problem = a hash map turns "values I have seen" into an O(1) memory, '
         'so the brute-force double loop collapses into one pass.',     # ① which pattern, and why
         'Hashmap as Memory'),                                          # ② which concept card (a real title)
    fq=[
        ('What if the array is already sorted?',                        # ③ what the interviewer asks next
         'Two pointers squeezing in from both ends, <b>O(1) space</b>, no hash map. '
         'Interviewers use this line to push you toward two pointers.'),
    ],
    var=[
        ('LC 167 Two Sum II', 'input is <b>sorted</b> → two pointers, O(1) space'),   # ④ neighbours
        ('LC 15 3Sum', 'fix one number + two pointers; dedupe in two places'),
    ],
),
```

- `pat=(why, concept)` — one sentence on *why this problem is that pattern*, phrased as the
  recognition cue you'd want in an interview ("contains negatives → window fails → prefix
  sum + hash map"). Not a restatement of the solution; the reasoning section does that. The
  second element is the **exact title of a concept card in the same deck** — the app renders
  it as a tappable chip in the section color that jumps to that card. A dangling link is a
  build error, so the deck stays navigable. This one renders at the top of the back as ①.
- `fq=[(q, a)]` — 2–3 follow-ups an interviewer actually asks after a correct solution: the
  relaxed constraint (sorted? duplicates? streaming input?), the "why this way" (why the
  `<=`?), the cost trade (can you save space?). Answer in one or two sentences. Not quiz
  questions to yourself — questions someone else asks you.
- `var=[(problem, diff)]` — 2–4 neighbours, each with the **one thing that changes**, not a
  description. "LC 525 Contiguous Array → treat 0 as −1, find the farthest two equal prefix
  sums" is a variant; "another prefix-sum problem" is noise. Write the problem name with its
  number (`LC 525 …`); a row that covers two problems can say `LC 159 / 340 …` and the build
  splits it into two. A row with no number at all is kept as plain text.

**Variants do not become cards.** This is the rule that keeps a deck from rotting. Every
problem has three to five neighbours, so promoting them all would have tripled the original
deck with thin, near-duplicate cards — and the whole point of a problem card is that
recognising its pattern is *hard*. A deck where five cards in a row are the same pattern
trains nothing.

So the build sorts each `var` row into one of two buckets by its LC number:

- **already a card in this deck** → the row renders as a button that jumps to that card,
  same as the `pat` chip. Nothing new is created.
- **not in the deck** → it is a *variant*: it must have an entry in `variants.py` at the
  deck root (`{lc: (official title, slug)}`) and shows up in two places only — a LeetCode
  link on the card, and a collapsible-by-section panel in the app's menu with one-tap "add
  to practice list". It never enters the deck, never gets flipped, never counts toward
  "remembered X/N".

Two details that matter when adding variants:

- The slug in `variants.py` must be the **real LeetCode URL slug**, because the app links to
  `https://leetcode.com/problems/<slug>/`. It is usually the kebab-case title, but not always:
  `01 Matrix → 01-matrix`, `All O\`one Data Structure → all-oone-data-structure`,
  `Longest Subarray of 1's… → longest-subarray-of-1s-…` (apostrophes vanish, not hyphenate).
  Copy it from the URL.
- A problem must not list itself as its own variant; the build drops self-references. A
  number that is neither in the deck nor in `variants.py` is a build error.

**One card, one idea.**

- Split long topics by *question*, not by length: Dijkstra became "pick the algorithm" /
  "why pop = final" / "the 5 bugs". Each has its own hook and stands alone.
- If a concept back needs more than ~6 blocks before `MORE()`, it's two cards.
- Pure API lookup tables make weak flashcards (nothing to recall). Convert them into a
  question with a wrong-but-tempting answer, or drop them.

**Language.** Default to the user's own wording — their mnemonics and phrasing are their
memory anchors, so preserve them verbatim. In a multi-language deck everything a reader reads
is rewritten per language, not machine-translated; titles, `lc` numbers, `code` (comments
aside) and `test`/`want` are identical everywhere, and `verify` checks that.
