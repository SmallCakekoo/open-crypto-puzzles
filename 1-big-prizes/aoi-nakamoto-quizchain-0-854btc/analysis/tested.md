# Tested hypotheses, full ledger

Summary table is in the README. This file has the full detail behind each row.
All figures are re-read from the private research's own dated result logs before
being written here.

## Real Big Block (0.777 BTC)

The mechanism is certified (the case-flip rule reproduces the solved sibling lot
Block 77 Stage One exactly). What is not established is exactly which paragraphs
of the "Second" chapter the author modified on 2019-07-30, and the precise text
she copied. Every row below tests a specific hypothesis about that, against both
the current escrow (`14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W`) and its superseded
predecessor (`1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC`).

| Hypothesis family | Candidates | Result |
|---|---|---|
| Chapter unmodified, every plausible serialization (line-break style, encoding) | approximately 150,000 | 0 match |
| Certified case-flip rule applied to the 3 planted paragraph groups plus the Finney quote, 16 combinations, both letter-position modes | approximately 200,000 | 0 match |
| Every subset of the 17 candidate paragraphs (2^17), 18 serialization variants | 2,360,000 | 0 match |
| Paragraphs selected by a name or word ("Satoshi", "Aoi Nakamoto", "Hal Finney", "Grycoin", and 7 more), by first letter or first character | approximately 10,000 | 0 match |
| Every paragraph starting with F or W (and F, W, H) | approximately 1,000 | 0 match |
| The certified groups plus one arbitrary extra paragraph | 13,000 | 0 match |
| The certified groups plus two arbitrary extra paragraphs | approximately 600,000 | 0 match |
| The single-word planted correction from block 29 ("voice" to "vOIce"), alone and combined with the groups | 6,000 | 0 match |
| Block-29-style link suffixes appended to the text | 8,000 | 0 match |
| Chapter subsections read alone | 3,000 | 0 match |
| Page-level prefixes (duplicated title, author byline) | 2,000 | 0 match |
| A simulated Chromium browser copy (selection/innerText rendering rules) | 1,000 | 0 match |
| Alternate text encodings (Latin-1, UTF-16, cp1252, NBSP normalization) | 3,000 | 0 match |
| Simulated-browser-copy base combined with the name/word selectors, then with all 2^17 paragraph subsets | approximately 800,000 | 0 match |
| A single invisible character (BOM, zero-width space, tab, and 6 more) inserted at the start or end | 5,000 | 0 match |
| Paragraphs selected by the letters of "Satoshi Nakamoto" specifically (a refinement of the name-selector row above, after finding the Finney post has a paragraph starting with M) | 60 | 0 match |
| Last-letter-only or first-letter-only variants of the case-flip rule, on the certified groups | 456 texts (2,736 address checks across derivation indices) | 0 match |
| All of the above serialization families repeated under CRLF line endings | 2,448 texts (14,688 address checks) | 0 match |
| 1 to 3 single-letter case toggles across all sign positions, and 1 to 2 across all paragraph boundaries | 1,450,000 | 0 match |
| Every single-character edit (insert, delete, replace, case toggle) at every position, across 40 base texts (5 paragraph-set choices x 2 NBSP conventions x 2 line-ending conventions x 2 separator conventions) | 266,038,400 | 0 match |

Witness status: every row above used the oracle certified against Block 77 Stage
One (see README, "Certified against"); the single-character-edit row additionally
planted 3 synthetic witnesses per base text (head, middle, tail) and recovered
all of them on all 40 bases, plus recovered the real Stage One text and address
when run as a 41st base. Dates: all rows 2026-08-15.

Cumulative for the original private research: approximately 272 million
candidates tested, 0 match. The single-character-edit sweep accounts for the
large majority of this total and is the only row certified as a complete sweep
of its stated space (all 40 bases, every single edit) — **under UTF-8 only**;
this should not be read as an unconditional exhaustive search, since the two
paragraph separators actually used by the author (`\r\n` and `\r\n\r\n`,
confirmed 2026-08-22, see below) were not known or tested at the time it ran,
and were different from the `\n\n`/`\n` assumptions the private research used.
Every other row is a targeted, not exhaustive, test of one specific hypothesis
about which paragraphs were modified.

### 2026-08-22 session: real fetched source, confirmed separators, encoding-aware

Conducted after recovering the exact separator specification directly from the
author (Real Big Block Discussion thread, fully recovered via the Arctic Shift
Reddit archive — see `data/realbigblock_full_thread_recovered.md`) and after
fetching the actual 273-paragraph chapter text via the Wattpad API (not
previously done against real data in earlier ledger rows; the 2019
private-research base texts are not available in this repository). All rows
below tested against **both** target addresses
(`14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W` current, `1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC`
superseded), each with its own confirmed separator (`\r\n\r\n` current, `\r\n`
superseded), all 6 BIP44 indices, using `oracle.py`'s certified transform.

| Hypothesis family | Candidates | Result |
|---|---|---|
| Whole chapter and 12 precisely-bounded chapter sections, 3 case-rule variants (unmodified, ITASM-literal-first-char, ITASM-first-alphabetic-char), separator variants (`\r\n`, `\r\n\r\n`, `\n`, `\n\n`), 3 NBSP-handling modes, UTF-8/ISO-8859-1 | 1,437 | 0 match |
| ITASM-only and non-ITASM-only selection (drop-not-flip: keep only matching paragraphs, discard the rest, preserve order), with and without also applying the case-flip to the kept paragraphs | 96 | 0 match |
| Individual single-sign selectors (I-only, T-only, A-only, S-only, M-only paragraphs), paragraphs containing "sign"/"signs", selection restricted to the "Satoshi Code" section (ITASM-initial and non-ITASM-initial subsets within it) | 192 | 0 match |
| Header/title-paragraph inclusion vs. exclusion x per-paragraph/whole-document trim x transform x both separators x both encodings (byte-level forensic-audit follow-up) | 192 + 192 | 0 match |
| Reversed case-flip direction (ITASM-initial paragraphs flipped, non-ITASM unchanged) against the real Stage One calibration text | 1 | 0 match (confirms the original, already-certified direction is the correct one — resolves an apparent contradiction with Grycoin Block 2's imprecise worked example) |
| First-letter and last-letter streams of the whole chapter, and restricted to ITASM-only / non-ITASM-only characters, visually inspected for readable structure | 4 streams | no recognizable word or phrase found |
| Stage One calibration under UTF-8, ISO-8859-1, and cp1252 (the real bitcointalk post text, fetched fresh and reconstructed per GitHub issue #1's `<br><br>` rule) | 3 | all 3 reproduce the calibration address identically — the source is pure ASCII, so this confirms the pipeline but cannot discriminate encodings |
| ITASM uniqueness: all 512 subsets (sizes 0-9) of the 9 distinct letters in "SATOSHI NAKAMOTO", against the real Stage One text | 512 | 16 subsets reproduce the address; all are supersets of the minimal 5-letter set `{A,I,M,S,T}` plus any combination of the 4 letters that never appear as a first letter in the Finney post (`O,H,N,K`) — confirms ITASM is the unique minimal representative, not a coincidence, and is independently corroborated by the chapter's own explicit statement of it |

### 2026-08-22 session, continued: full book read, positional selection, edit-distance sweeps with confirmed separators

Read all 33 parts of the "Second" Wattpad story in full (previously only 4
had been read). No part states a Real Big Block selection or transformation
rule. One reusable technique found: "Quizchain as a Password Manager" (part
18) demonstrates the author's own "every 7th word, first letter" extraction
method; translated to paragraph granularity and tested as a positional
selector, also negative (see below).

| Hypothesis family | Candidates | Result |
|---|---|---|
| Positional paragraph selection: every Nth paragraph (N = 2, 3, 4, 7) at every possible offset, kept and joined in order, with and without the case-flip transform, both confirmed separators, 3 NBSP modes, 2 encodings, both addresses | 384 | 0 match |
| Full 1-character-deletion sweep: every position of the whole chapter deleted, one at a time, both confirmed separators, unmodified and ITASM variants, both addresses (UTF-8) — the first exhaustive edit-distance-1 sweep run against the confirmed separator bytes; the original 266M sweep used unconfirmed `\n`/`\n\n` | 182,888 | 0 match |
| Full 1-character-insertion sweep: 6 candidate characters (space, NBSP, zero-width space, tab, CR, LF) inserted at every position of the whole chapter, same base/separator/address matrix, parallelized across 11 cores | 1,097,352 | 0 match |
| Full 1-character-substitution sweep: every position of the whole chapter replaced with every printable ASCII character plus NBSP (97 characters), same base/separator/address matrix, parallelized across 7 cores, 9,450s (2.6h) runtime | 17,560,552 | 0 match |

This completes the edit-distance-1 family (deletion, insertion, and
substitution, each independently exhaustive) against the whole chapter under
both confirmed separators and both the unmodified and ITASM-transformed
bases, on both target addresses. Cumulative for the 2026-08-22 session:
approximately 18.8 million candidates from the edit-distance sweeps, plus
roughly 2,100 from the earlier selection/boundary/encoding testing the same
day, all real fetched data, all negative on both addresses.

### 2026-08-22, continued: br-stripped internal-`<br>` corpus variant

An independent third party (via the user) reported a corpus reconstruction
with a different byte length (45,990 vs. this repository's 46,000) for the
same 273 paragraphs under `\r\n\r\n`. Verified directly: the difference is
exactly the 10 internal `<br>` tags (mid-paragraph line breaks, not paragraph
boundaries) — this repository's `load_paragraphs()` converts them to `\n`
(1 byte each); the third party's pipeline strips them to nothing (0 bytes).
With that one change, this repository independently reproduces their exact
claimed byte count (45,990) and MD5 (`f74e8e0122e114fe13c89a3bba25294a`) for
the unmodified whole chapter. Their 13 trailing-space paragraph indices were
also independently reproduced exactly by this repository's own byte audit
before this cross-check, confirming their corpus derives from genuine,
correctly-extracted source data, not a fabrication. This is a real,
previously untested base-text variant, distinct from every candidate in the
rows above.

| Hypothesis family | Candidates | Result |
|---|---|---|
| br-stripped variant: whole chapter unmodified and ITASM, both separators, 3 NBSP modes, 2 encodings, both addresses | 24 | 0 match |
| br-stripped variant: full 1-character-deletion and 1-character-insertion sweep, both separators, both bases, both addresses, parallelized 7 cores | 1,279,960 | 0 match |
| br-stripped variant: full 1-character-substitution sweep, 97 characters, both separators, both bases, both addresses, parallelized 7 cores, 8,209s runtime | 17,556,672 | 0 match |

This completes the edit-distance-1 family under **both** corpus conventions
now identified (internal `<br>` as `\n`, and internal `<br>` stripped to
nothing) — 18,836,632 candidates for the br-stripped variant alone, all
negative on both addresses.

Note: a third-party claim of having independently reproduced Grycoin Block
2's solution oracle (author-published MD5 prefix `3c6`) was checked directly
against the real Block 2 post text (exact substring the author specifies,
"I thought..." through "...thinking only method.", 10 paragraphs, initials
`IAFFIOWWIA`). This repository independently reproduced the separate,
already-known RAW oracle (`7759227d7406d8230d7e3a8f7b9846d7`, unmodified
text + `\n\n`) exactly, corroborating that the third party's methodology is
sound for that fact. However, none of the natural extensions tested here —
unmodified, ITASM-original-direction, ITASM-reversed-direction, each under
`\r\n\r\n`/`\n\n`/`\r\n` (9 combinations) — reproduce the `3c6` prefix. The
third party's specific `3c6`-producing candidate has not been shared or
independently verified; treat that particular claim as unconfirmed pending
the exact text/transformation they used.

### 2026-08-22, continued: reverse paragraph order (Block 10 "twist" precedent)

The author's only other calibrated meaning of "twist" (Block 10: "not taking
the obvious choice... but the third word from the end of the list") was
tested as a full-document reordering: all 273 paragraphs in reverse order,
both corpus conventions (`<br>` as `\n` and `<br>` stripped), unmodified and
ITASM-transformed (both applying the case-flip before and after reversal,
since order could plausibly affect which paragraphs count as "first"/"last"
for the transform), both confirmed separators, 3 NBSP modes, 2 encodings,
both addresses.

| Hypothesis family | Candidates | Result |
|---|---|---|
| Full-document reverse paragraph order, both corpus conventions, with/without ITASM | 72 | 0 match |

### 2026-08-22, continued: zoned internal 1/2-character case-toggle sweep

A third party's independent investigation (via the user) reported the same
repeated structural pattern this repository's original README already noted
("the same paragraph-initial pattern 3 times... plus a quotation from the
Finney post") but with specific paragraph ranges. Independently verified
against the real fetched chapter: three 5-paragraph groups, each opening a
major section (paragraphs 3-7 "Second Coming", 91-95 "Purpose of Grycoin",
166-170 "My Identity"), each with first-letter sequence I-F-F-W-W — the exact
Stage One exception pattern — plus the literal quoted Finney paragraphs
(230-234) and all 12 paragraphs containing the exact phrase "recognize the
signs" (verified: 13 occurrences, 12 distinct paragraphs, matching the third
party's claim exactly).

Rather than testing these paragraphs as a *selection* (already done, see
above, 0 match) or as *boundary* toggles only (already done, boundary2-style,
0 match on the whole document), this sweep toggles the case of every ASCII
letter *within* these specific paragraphs (not just first/last letters),
one and two positions at a time, while leaving the rest of the 273-paragraph
chapter untouched — a genuinely new dimension, bounded to evidence-backed
zones rather than the full document (which would be computationally
infeasible: ~35,825 letters, C(35825,2) ≈ 641M pairs for the whole document,
not attempted).

| Hypothesis family | Candidates | Result |
|---|---|---|
| Internal 1-and-2-letter case toggles restricted to signs+U1+U2+U3+U4 zones (4,635 ASCII-alpha positions), both corpus conventions, both separators/addresses, parallelized 7 cores | 42,975,720 | in progress, started 2026-08-22, ~6h estimated |

Total across all research phases: approximately 310 million candidates
against Real Big Block confirmed negative, plus this zoned internal sweep in
progress.

### 2026-08-25 session: contiguous-range and transposition sweeps (tools/sweep.py)

First runs of `tools/sweep.py`, a new parallel engine built on
`tools/fastderive.py` (the same transform as `oracle.py`, reimplemented on
hashlib + coincurve and self-certified against the author's own published
vector). Source text fetched fresh by `tools/fetch_source.py`, which
re-validated the forensic audit on the spot: exactly 273 paragraphs and exactly
6 U+00A0, no other non-ASCII.

Both runs are **witness-verified**: a candidate drawn from the sweep's own
enumeration had its HASH160 planted in the target set before the run, and both
runs recovered it. A run that fails to recover its witness exits non-zero and
its negative is discarded rather than recorded.

| Hypothesis family | Candidates | Result |
|---|---|---|
| **Every contiguous paragraph range of the chapter** (all 37,401 of them, i.e. every `paragraphs[s:e]`), x both confirmed separators x 3 case-rule variants (none, ITASM, flip-all), UTF-8, NBSP kept, no trailing bytes | 224,406 | 0 match, witness recovered |
| Transposition: reversed order, reversed-within-halves, halves swapped, interleaved halves, evens-then-odds, odds-then-evens; each x the full serialization matrix (4 separators x 3 transforms x 3 NBSP modes x 4 trailing-byte variants x BOM/no-BOM x per-paragraph rstrip x UTF-8/ISO-8859-1) | 6,912 | 0 match, witness recovered |

The contiguous-range row closes what had been the largest coverage gap in this
ledger: prior work tested **12 hand-picked sections**, and this tests **all
37,401 contiguous ranges** under the confirmed formatting. Any hypothesis of
the form "she hashed some contiguous stretch of the chapter, unmodified or
under the ITASM rule, with a confirmed separator" is now exhausted for UTF-8
with clean bytes. What remains open within that shape is the cross product with
the app-behaviour matrix (`--mode ranges --profile full`, 43,085,952
candidates) and non-contiguous selections.

The transposition row closes lead 6 in `analysis/leads.md` at full serialization
depth; order-changing transforms had never been tested at all before.

Running total: approximately 291.2 million candidates against Real Big Block,
all negative.

## Quizchain2 Block 76 (0.077 BTC) — solved and swept by a reader 2026-08-17

Kept for historical reference; no longer part of the live prize. The solution
was never disclosed publicly by the solver or by AoiNakamoto, so the negative
results below cannot be retrospectively explained.

The chain a community player found in 2019 (`solution = "format"`,
`TOMI = "before TOMI"`) satisfies both of the author's published MD5-prefix
hints, but no standard BIP44/49/84 derivation, derivation path, or passphrase
variant of it produces the escrow address. Two later calibration checks (blocks
73 and 74, both already solved and swept, not part of the live prize) confirm
the derivation code itself is correct, and a later cross-check on 2019-07-29
comment timing suggests the "format" chain was itself a false positive found by
searching for strings that pass the 2 published prefixes, rather than the
author's real answer, since the author never corrected the block after seeing it
posted publicly (see README).

Standard-derivation sweep on the `format`/`before TOMI` chain:

| Hypothesis family | Candidates | Result |
|---|---|---|
| BIP44, BIP49, BIP84, accounts 0 to 4, external and internal chains, index 0 to 199 (BIP44 external: 0 to 1999) | standard derivation space | 0 match |
| Non-standard derivation paths (Coleman-style m/0'/0/i, m/0/i, m/0', root key) | small, enumerated | 0 match |
| Passphrase variants ("TOMI", "format", "before TOMI", bracket and whitespace forms) | small, enumerated | 0 match |
| Alternate entropy functions (SHA-256 as a 24-word mnemonic, SHA-1, RIPEMD-160, truncated SHA-512, double MD5) | small, enumerated | 0 match |
| Off-by-one word at BIP39 import (12 positions x 2,047 alternate words each) | 24,564 | 0 match |
| Word order reversed | 1 | 0 match |

Word-transform "salves" on the question "change to" / "from change to" (each
family's candidate solution strings tested through the same 2 MD5-prefix filters
before any derivation; only pairs passing both filters were derivation-tested):

| Salve | Candidate solutions | Passed prefix 1d | Passed both filters (derivation-tested) |
|---|---|---|---|
| Single-letter edits, anagrams, Atbash/ROT/foldover, translations of "change" | 7,730 | 32 | 3,506 TOMI pairs, 0 match |
| WordNet synsets and hyper/hyponyms of change/alter | 20,199 | 74 | 8,806 TOMI pairs, 0 match |
| Wikipedia article titles containing "change" | 14,666 | 44 | 4,949 TOMI pairs, 0 match |
| Sentences from Satoshi/Hal Finney bitcointalk posts and emails containing "change to" | 46 | 0 | n/a |
| Sentences from bitcointalk posts numbered 60 to 94 (2 orderings) | 1,992 | 11 (noise) | n/a |
| Strings built from the number 76 (years, technical constants, ordinals) | 3,779 | 23 (noise) | n/a |
| Encodings of "change" (hex, base64, NATO alphabet, Morse, keyboard shift) | approximately 130 | 1 (noise) | n/a |
| "changeto" (no space) combined with TOMI variants | 1 | 1 | 1,701 TOMI pairs, 0 match |
| Every address and txid from the author's 158 other funding transactions | approximately 1,500 | 4 (case noise) | n/a |
| Renaming candidates ("wealth", "legacy", and similar) | 45 | 0 | n/a |
| An Easter/resurrection word family, echoing the same block number in round 1 | 2,752 | 17 (noise) | 5,857 TOMI pairs, 0 match |
| Halving-related terms | 45 | 1 (noise) | n/a |
| Grycoin/burn-address/second-layer terms from the chapter | 60 | 0 | n/a |
| Literal strings and typos from the block's own post | 45 | 0 | n/a |

A separate "post-number-as-index" method, confirmed on 3 other blocks in the
series (numbers 56, 57 and 58 each index a specific post or tweet by Satoshi or
Hal Finney, by position), does not carry over to block 76: post number 76 in
every corpus and ordering tried (Satoshi's bitcointalk posts newest-first and
chronological, Hal Finney's posts, Hal Finney's tweets) contains neither "change"
nor "from".

A large dictionary-times-corpus sweep tested every 1-to-4-word phrase built from
the author's own writing (Reddit posts, comments, and Wattpad chapters) as a
candidate TOMI value, against a dictionary-and-WordNet-derived candidate solution
list: 189,565 candidate solutions passing the first filter, times 656,845 to
1,250,000 candidate TOMI phrases depending on the pass, for a combined total of
approximately 3.2x10^11 MD5 computations and approximately 78 million full
address derivations on the pairs that passed both filters. 0 match. The
derivation code was re-confirmed correct on both calibration blocks (73 and 74)
at the head, middle and tail of this run.

Cumulative for Block 76: approximately 78 million address derivations from the
scripted dictionary sweep, plus approximately 53,000 smaller thematic candidates
across the 14 salves above, plus the full standard-derivation sweep on the one
chain found by search. 0 match anywhere. This is reported as a targeted, not
exhaustive, negative: the true solution may use vocabulary outside the corpora
swept (the author's own writing and 2 general-purpose dictionaries), and the
block may simply be misconfigured (see README).
