# Open leads, full notes

Ranked summary is in the README. This file has the reasoning behind the
ranking. Block 76 was solved and swept by a reader on 2026-08-17 (solution
never disclosed); its leads (formerly ranked 4-5) are kept at the bottom for
historical record only and are no longer being pursued.

## 1. Identify which paragraphs of the "Second" chapter are hashed, and whether the case-flip transform applies at all

This is now the sole remaining unknown for Real Big Block. What is confirmed,
as of the 2026-08-22 investigation: the source (part 720888559 of the 34-part
"Second" Wattpad story, confirmed by the original announcement post's own
"Question: Final version of the second chapter of Wattpad story"); the
case-flip mechanism as a general technique (stated directly in the chapter's
own text, paragraph 227: "The letters I, T, A, S, and M as first letters of
each paragraph of this post" — not researcher-inferred); and both historical
paragraph separators (`\r\n` for the superseded escrow, `\r\n\r\n` for the
current one, both from direct, unambiguous author statements in the fully
recovered Real Big Block Discussion thread, `data/realbigblock_full_thread_recovered.md`).

What is not confirmed: which paragraphs of the 273-paragraph chapter actually
enter the hash, or whether the ITASM-style transform is reused at all for this
second stage (as opposed to being one of the "twists" the author says she
removed between the superseded and current versions — "I wanted to remove one
of the twists I had. The block is now slightly easier", `data/realbigblock_original_announcement.md`).

Exhaustively tested against both the current and superseded addresses, with
both confirmed separators, UTF-8 and ISO-8859-1 encoding, and 3 NBSP-handling
modes, all negative (see `analysis/tested.md` for exact candidate counts):

- Whole chapter and 12 precisely-bounded chapter sections, unmodified and with
  the ITASM case-flip rule (both literal-first-character and
  first-alphabetic-character variants).
- ITASM-only selection, non-ITASM-only selection (drop-not-flip, i.e. keep
  only the matching paragraphs and discard the rest, preserving order), both
  with and without also applying the case-flip to the kept paragraphs.
- Individual single-letter selectors (I-only, T-only, A-only, S-only,
  M-only), paragraphs containing the word "sign"/"signs", and selection
  restricted to the thematically closest section ("The Satoshi Code",
  paragraphs 174-245).
- Header/title-paragraph inclusion vs. exclusion, per-paragraph and
  whole-document trimming, crossed with the above.
- The reversed case-flip direction (ITASM-initial paragraphs flipped, others
  unchanged) against the real Stage One calibration text specifically, to
  settle an apparent contradiction with the author's own Grycoin Block 2
  worked example: the reversed direction does **not** reproduce the Stage One
  address; the original direction (ITASM unchanged, others flipped) does,
  exactly. Grycoin Block 2's prose is confirmed imprecise even about its own
  real text (it describes a real paragraph's transformation but gets the
  paragraph's actual last letter wrong), so it is treated as a loose teaching
  aid, not a literal spec, and ground truth is trusted over it.

A full byte-level forensic audit found the source text unusually clean:
exactly 6 non-breaking spaces (U+00A0) and no other non-ASCII content anywhere
in 273 paragraphs; no BOM; NFC/NFD/raw are byte-identical (nothing
decomposable exists in the text); the independently fetched rendered Wattpad
page and the API text agree exactly (0 differences) for their overlapping
paragraphs. This substantially narrows, without eliminating, "wrong bytes" as
an explanation for the negative results.

**Update 2026-08-22: all 33 parts of the "Second" Wattpad story have now been
read in full** (previously only 4 had been). No part states a Real Big Block
selection or transformation rule explicitly. One technique the author
demonstrates elsewhere in the story — "every 7th word, first letter" (part
18, "Quizchain as a Password Manager") — was translated to paragraph
granularity and tested as a positional selector (every Nth paragraph, N =
2/3/4/7, all offsets, with and without the case-flip transform): 0 match.
This closes the most textually-motivated remaining selection idea found in
the full book; no further selector candidate has primary-source support at
this time.

What would confirm this lead: a selector that is independently justified by a
specific sentence in a primary source (the chapter, the Reddit discussion, or
the two consolidated draft parts — see `data/wattpad_story_structure.md`),
not merely one that happens to produce the correct address, and that
reproduces either target address.
What would kill it, in the useful sense: nothing kills this lead outright, in
the same way lead 5 below never had a clean exhaustion condition — the
letter/selector space is large and only sparsely evidence-backed, so absence
of a hit does not prove absence of a valid rule.
Cost: open-ended; each individual evidence-backed selector is minutes to test
once defined, but defining a new one requires primary-source justification,
not brute force.

## 2. A bounded 2-character-edit sweep on the whole chapter under the two confirmed separators

The original single-character-edit sweep (266,038,400 candidates) was
UTF-8-only and used an unconfirmed separator assumption. **Fully redone
2026-08-22 with the confirmed separators, completing the edit-distance-1
family:**

- 1-character deletion: 182,888 candidates (every position, both
  separators, both addresses). 0 match.
- 1-character insertion: 1,097,352 candidates (space, NBSP, zero-width
  space, tab, CR, LF at every position, parallelized across 11 cores). 0
  match.
- 1-character substitution: 17,560,552 candidates (every position replaced
  with every printable ASCII character plus NBSP, 97 characters,
  parallelized across 7 cores, 9,450s runtime). 0 match.

All three against the whole chapter, unmodified and with the ITASM
transform, both confirmed separators, both target addresses. **This is a
genuinely exhaustive edit-distance-1 search under the confirmed formatting
— not a targeted sample — and it is negative.** A true 2-character sweep
(edit two positions simultaneously) remains unrun; even bounded to
NBSP/line-ending-adjacent positions it is estimated at roughly an hour on a
rented GPU, which was not available in this session (local throughput here:
~1,850 derivations/sec parallelized across 7 cores, vs. GPU rates on the
order of hundreds of thousands/sec cited elsewhere in this repository). An
unbounded 2-character sweep (every pair of positions x every pair of
characters) is not proposed; its cost is disproportionate without a
narrower reason to expect the answer lives there, now that edit-distance-1
has been exhausted.

What would confirm it: a match within a bounded 2-character space.
What would kill it: exhausting that bounded space with none.
Cost: a bounded 2-character sweep, on the order of an hour on a rented GPU;
not attempted locally given the throughput measured here.

## 3. Differential validation against the superseded address

Not yet applicable as an independent lead — it becomes actionable only once a
candidate transform reproduces either target address. At that point, the
same transform (or a small evidence-backed variant of it under the `\r\n`
separator instead of `\r\n\r\n`) should be checked against the superseded
address `1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC` as well. A transform that
explains both addresses, consistent with the author's own "removed one of the
twists" description of the difference between them, is far stronger evidence
than a single-address hit.

What would confirm it: the same transform family reproduces both addresses
under their respective confirmed separators.
What would kill it: not applicable until lead 1 produces a candidate to test.
Cost: minutes, contingent on lead 1.

---

## Historical: Block 76 leads (solved 2026-08-17, no longer pursued)

### Identify what "76" indexes for Block 76

A method confirmed on 3 other blocks in the same series (56, 57, 58) uses the
block's own number as a position index into a specific corpus (a numbered post
by Satoshi Nakamoto or Hal Finney on bitcointalk, read in a specific order).
The same method, tried against every corpus and ordering available, did not
produce a post containing "change" or "from" at position 76 before the block
was solved by another reader.

### A short, human-reasoned answer to "change to" / "from change to"

The author's own hint structure argued for a short, punchy answer rather than
a long dictionary phrase. Superseded by the block being solved; the solution
was never disclosed publicly, so this cannot be confirmed retrospectively.
