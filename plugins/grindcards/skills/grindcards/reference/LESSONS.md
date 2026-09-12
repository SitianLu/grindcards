# Lessons — why the rules are what they are

Every rule in `SKILL.md` and `SOLUTION_SCHEMA.md` is here because something broke. Read
this before relaxing a check or "simplifying" the schema.

## Content

**Method labels made the reasoning worse, not better.** The first rewrite of `idea`
prefixed every bullet with the CtCI move it was making (*Brute force:*, *Bottleneck:*,
*Unused information:*). It read like a form. A person at a whiteboard doesn't say
"repeated work" — they say "I keep rescanning the same slice". The method has to live in
the sentence. Rule: no bold label at the start of an `idea` bullet, ever.

**The second rewrite was still written from the answer.** Steps that only make sense once
you already know the solution ("we maintain a monotonic stack") are a listing, not a
derivation. The fix was the voice: first person, present tense, and the dead-end kept in.
The test for a finished `idea`: could I walk an unseen problem with these steps?

**A card built from the editorial is forgotten; a card built from the user's failure
sticks.** Hence the three questions before any card is written. The user's broken input
goes into `test`; their own wrong turn goes into `idea`; their one line goes first in
`keys`.

**The front must not leak the pattern.** Early problem fronts asked a problem-specific
question ("which two pointers?"). The front now shows the statement plus a generic prompt;
pattern-naming moved into hint 2 of a tap-to-reveal ladder.

**LeetCode's sample I/O does not belong on the front.** Write your own example, and make
the front example, the first `test` case and the figure agree — otherwise the reader
re-derives the same problem three times with three sets of numbers.

**Variants never enter the deck.** Promoting them tripled the deck with near-duplicates
and put five same-pattern cards in a row. They live in the menu as links + a practice list.

## Verification

**Verify the data that ships, not an upstream of it.** The old verifier imported the
pre-rewrite source parts instead of the final `SOL`. A newly added problem's code was never
executed, and it stayed green. When that was fixed it exposed a test calling an import that
the card no longer had, and 27 code lines over the width limit. `grindcards verify` loads
the deck exactly the way `build` does.

**When the spec changes, change the check the same day.** `idea` was widened to 4–6
bullets in the spec but the verifier still said 2–4; fifty lines of false warnings buried
the one real failure. False positives are not free.

**Cross-language decks must produce the same card list, in the same order.** Progress
and the current position are stored by card title, and the in-app switch swaps the whole
deck in place. One extra card in one language shifts every index after it. `verify` diffs
the `(kind, section, title)` sequence across languages and refuses to build on mismatch.

**Code must be identical across languages, comments aside.** Otherwise "the same card in
Chinese" quietly becomes a different algorithm. The comparison strips comments and
docstrings and compares tokens.

## Engine

**Marker ids and other generated ids must be deterministic.** The SVG engine once used
`hash()` to name arrow markers; Python randomises string hashes per process, so every
build produced a different file and every diff was noise. Ids are numbered by insertion
order.

**SVG2 `context-stroke` is not available on older iOS Safari.** Arrowheads rendered black
regardless of line colour. One `<marker>` per colour, generated on demand.

**CJK glyphs take two monospace columns.** The app picks the code font size from the
widest line; `len()` under-counts wide characters and the block still wrapped. Width is
measured with `unicodedata.east_asian_width` at build time and stored on the `<pre>`.

**Never store progress by index.** Any new card shifts every index after it; progress
keyed by index is wiped by the next build. Keyed by title, merged per entry by timestamp.

**The sync key stays in the URL fragment on purpose.** iOS home-screen apps get an
isolated storage jar; if the key is scrubbed from the address bar before "Add to Home
Screen", the installed app starts empty and looks like lost progress. The manifest also
omits `start_url` for the same reason.

**Never replace local state with the server's response.** A blank response (function not
deployed, new site, missing body) once wiped a deck's progress on the next write. Merge
per entry by timestamp, both directions; local only ever moves forward.

**`sw.js` is network-first.** Cache-first pinned users to a stale deck after a deploy.

**Measure layout only after `document.fonts.ready`.** The PDF fitter measured before web
fonts applied; the same card overflowed in one run and not the next.

## Process

**Sources go in the repo; generated files are not a backup.** The original deck's source
files (`concepts.py`, `problems_b.py`) were never committed — only the generated
`cards.py` — and a reclaimed workspace took them. Concept cards could be recovered
byte-for-byte only because they pass through assembly unchanged; the problem sources could
not. "It can be reconstructed from the output" is luck, not design.

**Commit before you restructure.** While moving the starter deck into the package, a
`rm -rf` on a directory that had not been committed yet deleted an afternoon of content.
It was rebuilt from the scratch scripts, which was possible only because every hand edit
had been made through a script. Commit first; re-run scripts second; type edits by hand
never.

**Every hand edit to generated content should be a script.** Not for elegance — so it can
be replayed after the previous lesson.
