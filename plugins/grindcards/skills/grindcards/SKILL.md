---
name: grindcards
description: Turn a coding-interview problem the user just failed (LeetCode or otherwise) into a flashcard in their GrindCards deck — pattern, first-person reasoning with the user's own dead-end, executable code, memory keys — then verify and rebuild the offline app. Use whenever the user says they got a problem wrong, wants to "add a card", asks to review a deck, or mentions grindcards.
---

# GrindCards

A deck is a directory (`deck.toml`, `problems.py`, `sections.py`, `variants.py`, one
folder per language). The `grindcards` CLI verifies it — **every card's code is executed
against its own test** — and builds a single-file offline app. You write the cards.

```
grindcards init mydeck --starter     # 20-card bilingual example deck to copy from
grindcards verify [deck]             # run all code, check structure, both languages
grindcards build  [deck]             # verify → deck/build/index.html (+ PWA files)
grindcards serve  [deck]             # build and open in a browser
```

If `grindcards` is missing: `pip install grindcards` (PDF needs `grindcards[render]`).

## The protocol: failed problem → three questions → card

A card that only restates the editorial is a card the user will forget. The value is in
**their** wrong turn and **their** memory hook, so never write a card straight from the
problem number. Do this, in order:

1. **Anchor the failure.** Find the deck (`deck.toml` in cwd or the path the user gives)
   and the problem (LC number, or the statement if it isn't LeetCode). Read
   `<lang>/solutions.py` to learn the deck's voice before writing anything.
2. **Ask three questions — one message, then wait.**
   - *Where did it break?* What approach did you try, and at what point did it stop
     working (TLE, wrong answer on which input, couldn't get started)?
   - *What did the working solution see that you didn't?* In your own words, not the
     editorial's.
   - *What's the one line you want to remember next time?*
   If the user answers "just make the card", proceed with your best guess and say so.
3. **Build the card** in the deck's schema (below). The user's dead-end becomes the wrong
   turn inside `idea`; their one line becomes the first item of `keys`; the input that
   broke them becomes a case in `test`.
4. **Verify, build, report.** `grindcards build` must pass. Show the user the `idea`
   bullets and `keys` as plain text so they can push back on the wording — that is the
   review that matters, not the HTML.

## What a problem card is

Every problem is spread over the language folder's five files, keyed by `lc`:

| file | entry | what it holds |
|---|---|---|
| `statements.py` | `STMT[lc] = (statement_html, example)` | the problem in your words + one self-authored example line |
| `hints.py` | `HINTS[lc] = [h1, h2, h3]` | notice something → name the pattern → the key step |
| `deep.py` | `DEEP[lc] = dict(pat=(why, concept_title), fq=[(q, a)], var=[(name, diff)])` | which concept card and why; follow-ups; neighbouring problems |
| `solutions.py` | `SOL[lc] = dict(idea, code, keys, test, want)` | the card back |
| `figures.py` | `FIG[lc] = f.done()` (optional) | an SVG drawn with `grindcards.svgdia` |

plus one line in `problems.py`: `dict(lc=, title=, section=, slug=)`. The back always
renders as ① pattern → ② reasoning (+ figure) → ③ code → ④ keys → follow-ups → variants;
you never lay it out by hand.

### `idea` — 3–6 bullets, ≤110 visible characters each

First person, present tense, thinking aloud at a whiteboard. Start with the obvious
approach and why it fails; give yourself a target complexity; use the constraint the
problem hands you; walk into the dead-end and out again; then the move. **No bold labels
at the start of a bullet** ("**Brute force:**") — the method lives in the sentences, not in
category names. Don't narrate the code ("create a hash map") — say why you'd think of it.
The user's own dead-end from question 1 goes here, phrased as *I tried … and it broke on …*.

### `code` — runs as-is, ≤64 characters per line

LeetCode's method name, imports at the top, no `TreeNode`/`ListNode` definitions (the
verifier provides them, plus `build_tree`, `build_list`, `to_list`). Readable over short:
named variables, branches spelled out, comments that say *why*. The 64-column limit is hard —
the card sizes its font from the widest line.

### `keys` — 2–6 items, last one is the complexity

First item: the one thing to walk away with, as a positive statement. Middle items: mistakes
phrased as mistakes actually made, with the input that exposes them (`"[3,3], t=6 pairs an
index with itself"`), not advice ("handle duplicates"). Last: `"O(n) time · O(n) space"`.

### `test` / `want`

A Python expression evaluated after `code`; must equal `want`. Normalise unordered output
inside `test` (`sorted(...)`). Include the front example, the user's failing input, and
the empty/degenerate case.

### Example line and hints

Write your own example (never LeetCode's sample I/O). The example on the front, the first
case of `test`, and any numbers in the figure should agree. Hints never name the pattern
before hint 2.

## Concept cards

`("C", section, title, LEAD("one line of context") + "a question that forces recall",
[blocks])` in `concepts.py`, built from `K` (the insight), `C` (the template), `W` (the
gotcha), `T` (decision table), `L`, `P`, `CX` (complexity), `MORE()` (everything after is
app-only). Add one when a new problem doesn't fit any existing `pat` target — and link the
problem to it. Titles are language-neutral; write them once, identically, in every language.

## Multiple languages

`deck.toml` lists languages; each has an identical set of files. Card titles, sections,
`lc` numbers, `code` (comments aside), `test`/`want`, variant names and concept titles must
match across languages — `verify` checks all of it. Everything a reader reads is rewritten
per language, not machine-translated; the reasoning should sound native in each.

## Figures

Only when the step is easier drawn than said (the wrong-but-natural move next to the right
one is the usual shape). `from grindcards.svgdia import Fig, AC, GOOD, BAD, MUTE, INK`;
primitives `row`/`span`/`ptr`, `tree`, `chain`/`hop`, `bars`, `graph`, `grid`, `bands`,
`stack`, `caption`, `title`; canvas is 340px wide, keep captions under ~52 characters, and
`gap()` before anything drawn *above* the current line. Colours are CSS variables, so dark
mode is free. See `reference/SOLUTION_SCHEMA.md` for the full primitive table.

## Reference

- `reference/SOLUTION_SCHEMA.md` — the full spec of the card back, with a complete example.
- `reference/STYLE.md` — how the two card kinds differ, what belongs on a front, why
  variants never enter the deck.
- `reference/LESSONS.md` — the pitfall log: every rule above that exists because it was
  broken once. Read it before changing the engine or the schema.
