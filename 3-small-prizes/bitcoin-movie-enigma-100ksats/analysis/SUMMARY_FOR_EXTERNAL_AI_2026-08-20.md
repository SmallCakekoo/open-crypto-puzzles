# Bitcoin Movie Enigma (100k sats) — full investigation summary, 2026-08-20

This is a self-contained summary of an ongoing puzzle-solving effort, written
to hand to a different AI for a fresh opinion / proposals. It assumes no
context beyond what's written here.

## The puzzle

An image (part of a larger "bounty puzzle" collection) shows **34 numbered
panels in fixed order**, each a still frame from a different movie. The
stated rule (from the puzzle author's own posts): transform each panel's film
title "somehow" into an **English BIP39 word** (the 2048-word list used for
Bitcoin/crypto wallet recovery phrases) — giving 34 candidate words in panel
order. Then **drop exactly 10 of them** ("intruders"), using some piece of
**information findable on that film's IMDb page**, leaving **24 words in
their original panel order**. Those 24 words, in order, are meant to be a
valid **BIP39 24-word mnemonic** that derives a Bitcoin wallet. The resulting
wallet's address must equal a specific escrow address:

```
bc1q94ecsn0qk8lap2gefrycnms3ruepy889z969a6
```

This address received exactly 100,000 sats in 2022 and the coins are still
unspent — i.e. this is a real, live bounty, not a hypothetical.

Two things are **not specified** by the puzzle and had to be reverse-engineered
by trial:
1. **The title→word transformation.** Working assumption (well-supported,
   see below): the BIP39 word is a literal English substring found inside one
   of the title's words (e.g. "hard" inside "Die **Hard**", "alien" inside
   "**Alien**s"). A handful of panels have no such literal substring and
   needed a differently-sourced (but still IMDb-grounded) word instead — see
   below.
2. **The intruder criterion** — what specific, checkable fact about a film,
   read off its own IMDb page, marks it as one of the 10 to drop. This is the
   main unsolved part of the puzzle right now.
3. **The BIP32 derivation path** from mnemonic → address is also not
   specified by the puzzle; a companion tool (`tools/oracle.py`) checks a
   film's candidate mnemonic against a reasonably broad but *not exhaustive*
   set of standard paths (BIP84, BIP49, BIP44, 2 accounts x 3 address
   indices, plus 3 other common raw paths). A checksum-valid 24-word mnemonic
   is *not* itself evidence of anything — only an actual address match against
   the escrow counts as a real result.

## The 34 panels (confirmed identities)

All 34 film identities are considered settled (either independently sourced
this investigation, or from the user's own frame-by-frame viewing of the
source video, cross-checked with other people — the latter panels are marked
"probable" rather than "confirmed" below, meaning: identity trusted, just not
independently re-verified by the AI assistant beyond the user's own claim).

| # | Title | Status |
|---|---|---|
| 1 | Die Hard | confirmed |
| 2 | Paths of Glory | confirmed |
| 3 | Aliens | probable |
| 4 | Mad Max | confirmed |
| 5 | Alien | probable |
| 6 | Apocalypse Now | confirmed |
| 7 | Escape from Alcatraz | confirmed |
| 8 | The Goonies | probable |
| 9 | Spartacus | probable |
| 10 | Mission: Impossible | confirmed |
| 11 | Godzilla (1998) | probable |
| 12 | Life of Pi | confirmed |
| 13 | Leon: The Professional | probable |
| 14 | The Man in the Iron Mask (1998) | probable |
| 15 | The Crimson Rivers | confirmed |
| 16 | The Visitors (Les Visiteurs) | probable |
| 17 | A Clockwork Orange | confirmed |
| 18 | Star Wars: A New Hope | confirmed |
| 19 | Gravity | confirmed |
| 20 | First Man | probable |
| 21 | Solaris (1972, Tarkovsky) | probable |
| 22 | Blade Runner 2049 | confirmed |
| 23 | Guardians of the Galaxy | probable |
| 24 | Close Encounters of the Third Kind | probable |
| 25 | Barry Lyndon | confirmed |
| 26 | Sharknado | probable |
| 27 | Terminator 2: Judgment Day | probable |
| 28 | Scream 2 | confirmed |
| 29 | The Matrix Reloaded | probable |
| 30 | Toy Story 2 | confirmed |
| 31 | Ghostbusters II | confirmed |
| 32 | Raiders of the Lost Ark | confirmed |
| 33 | The Shining | confirmed |
| 34 | The Human Centipede (First Sequence) | confirmed |

Notable identification history: panel 21 was double-checked as specifically
the **1972 Tarkovsky** Solaris (not the 2002 Soderbergh/Clooney remake — same
candidate word either way, "solar," so this doesn't change anything
downstream but was worth nailing down). Panel 30 was corrected mid-investigation
from "Toy Story" (1995) to **Toy Story 2** (1999) after closer inspection.
Panel 8 briefly flip-flopped to "Shutter Island" before being reverted to The
Goonies per the user's own direct research. These corrections are considered
closed, not open questions.

## Title → word: current candidate table

For 29 of the 34 panels, at least one literal English substring inside the
title is also a real BIP39 wordlist word. Several panels have more than one
such substring (ties). 5 panels have **no literal substring at all** in their
title and needed a differently-sourced candidate (character name, IMDb
keyword, or a well-documented portmanteau half) — flagged below.

**Just today**, per the user's explicit request, we collapsed every panel
down to a single "best" word (previously several panels carried 2-5 tied
candidates). The rule applied: a literal **whole title-word** match beats a
mere substring/fragment match; among multiple whole-word matches, pick the
most distinctive/iconic one for that specific film; for the 5 no-literal-word
panels, pick the single most iconic, already-vetted candidate (see next
section for how those were sourced). This table is a **judgment call**, not
mechanically certain — flagging every non-trivial pick:

| # | Title | Chosen word | Note |
|---|---|---|---|
| 1 | Die Hard | **hard** | only candidate |
| 2 | Paths of Glory | **glory** | whole word; "path" is a fragment of "Paths," not whole-word |
| 3 | Aliens | **alien** | only candidate (fragment of "Aliens") |
| 4 | Mad Max | **mad** | only candidate |
| 5 | Alien | **alien** | only candidate, whole word |
| 6 | Apocalypse Now | **now** | only candidate |
| 7 | Escape from Alcatraz | **escape** | whole word beats "cat" (buried fragment in "Alcatraz") |
| 8 | The Goonies | **chunk** | no literal word in title at all — character nickname, see below |
| 9 | Spartacus | **art** | only candidate (fragment, sp-ART-acus) |
| 10 | Mission: Impossible | **possible** | both candidates are fragments; "possible" (most of "Impossible") judged more recognizable than "miss" |
| 11 | Godzilla | **ill** | only candidate (fragment) |
| 12 | Life of Pi | **life** | only candidate |
| 13 | Leon: The Professional | **milk** | no literal word in title — Leon's own signature trait, see below |
| 14 | The Man in the Iron Mask | **mask** | 3-way tie of whole words (man/iron/mask); "mask" judged most distinctive to this specific film |
| 15 | The Crimson Rivers | **river** | only candidate (fragment of "Rivers") |
| 16 | The Visitors | **visit** | only candidate (fragment) |
| 17 | A Clockwork Orange | **orange** | only whole-word match; clock/lock/work/range are all fragments of "Clockwork" |
| 18 | Star Wars: A New Hope | **hope** | only candidate |
| 19 | Gravity | **gravity** | only candidate |
| 20 | First Man | **first** | 2-way tie of whole words (first/man); picked to avoid word reuse elsewhere in the table |
| 21 | Solaris | **solar** | only candidate |
| 22 | Blade Runner 2049 | **blade** | whole word beats "run" (fragment of "Runner") |
| 23 | Guardians of the Galaxy | **galaxy** | whole word beats "guard" (fragment of "Guardians") |
| 24 | Close Encounters of the Third Kind | **close** | 2-way tie of whole words (close/kind); "close" judged the more title-defining |
| 25 | Barry Lyndon | **bar** | only candidate (fragment of "Barry") |
| 26 | Sharknado | **tornado** | no literal word in title (letters don't line up) — portmanteau half AND a real IMDb keyword tag, see below |
| 27 | Terminator 2: Judgment Day | **day** | whole word beats "term" (fragment of "Terminator") |
| 28 | Scream 2 | **cream** | only candidate (fragment of "Scream") |
| 29 | The Matrix Reloaded | **matrix** | whole word beats "load" (fragment of "Reloaded") |
| 30 | Toy Story 2 | **toy** | 2-way tie of whole words (toy/story); "toy" judged more distinctive than the generic word "story" |
| 31 | Ghostbusters II | **ghost** | no whole-word match; "ghost" is the most recognizable of 3 fragments (ghost/host/bus) inside "Ghostbusters" |
| 32 | Raiders of the Lost Ark | **whip** | no literal word in title at all — Indy's signature prop, see below |
| 33 | The Shining | **hotel** | no literal word in title at all — the Overlook Hotel setting, see below |
| 34 | The Human Centipede (First Sequence) | **human** | 2-way tie of whole words (human/first); "human" is the primary title word, "first" is only in the subtitle |

Only 1 word repeats across the table ("alien," for the unavoidable reason
that panels 3 and 5 are literally titled Aliens/Alien). Every other word is
distinct across all 34 panels.

**This table has not yet been run through the oracle** — 34 words isn't a
valid BIP39 mnemonic length (valid lengths are 12/15/18/21/24) until 10 are
dropped. The point of finalizing it is to make testing *any* future
10-panel-drop hypothesis a single, instant check instead of a large
combinatorial search (previously, hypotheses with multiple tied/ambiguous
panels required testing thousands to billions of word combinations; with one
word fixed per panel, it's exactly one check per hypothesis).

### The 5 panels with no literal title substring

These needed non-literal but still IMDb-sourced candidates (never
free-associated from memory) — full sourcing history and secondary-tier
candidates for each are in `analysis/leads.md` and
`analysis/imdb_field_audit.xlsx`:

- **Panel 8, The Goonies → chunk**: the character Lawrence "Chunk" Cohen's
  own nickname. Secondary tier (37 more words, all real IMDb `/keywords/`
  page tags that are also literal BIP39 words): gold, cave, piano, skull,
  gadget, beach, rescue, legend, chase, sword, coin, toilet, bicycle, tunnel,
  jewel, pizza, fire, sheriff, forest, child, trap, ship, pistol, arrest,
  organ, asthma, book, knife, escape, marble, camera, kiss, thunder, rain,
  wish, police, hidden, danger, humor.
- **Panel 13, Leon: The Professional → milk**: Leon's own iconic
  milk-drinking habit (sourced from an IMDb review). Secondary tier (7 more):
  gun, shield, pistol, crush, girl, police, elevator, hotel, love, knife,
  weapon.
- **Panel 26, Sharknado → tornado**: not a literal substring (letters don't
  line up: sh-A-R-K-N-A-D-O vs t-O-R-N-A-D-O), but it's the second half of
  the title's own portmanteau (Shark + tornado) *and* a genuine standalone
  IMDb keyword tag for this film. Secondary tier (9 more): fish, dog, beach,
  gun, pistol, animal, vehicle, car, child.
- **Panel 32, Raiders of the Lost Ark → whip**: Indiana Jones's single most
  iconic prop. Secondary tier (41 more): snake, hat, spider, torch, gold,
  horse, ship, knife, truck, chase, jungle, mirror, canyon, desert, fire,
  bar, love, ritual, lecture, dress, tent, island, wine, blood, warrior,
  escape, kiss, pistol, sword, rescue, basket, soldier, spirit, alcohol, car,
  hero, magic, weapon, mechanic, faith, fiction.
- **Panel 33, The Shining → hotel**: the Overlook Hotel, the film's central
  setting. Secondary tier (26 more): mirror, blood, ghost, door, maze, snow,
  bar, chase, elevator, winter, marriage, kitchen, author, knife, doctor,
  window, toy, chef, escape, rescue, kiss, danger, night, gift, boy, airport.

## What has been tried and ruled out (with real derivation tests, not just plausibility)

House rule followed throughout: a criterion or word is never accepted just
because it "would be convenient." Every accepted word traces to either a
literal title substring or a specific, sourced piece of evidence (an IMDb
keyword/review/character name). A criterion hitting "exactly 10" by itself is
never treated as proof — only an actual derived-address match against the
escrow counts. All of the below were tested by literally constructing the
candidate mnemonic(s) and running them through `tools/oracle.py`, which
tries each candidate across BIP84/49/44 with 2 accounts x 3 address indices
plus 3 other common raw derivation paths, and checks for an exact address
match. `oracle.py --selftest` (verified against known public BIP39 test
vectors) passes before every run.

1. **H1: "shares a director or lead actor with another panel in the set."**
   Flags 14 of the 34 panels, not 10. **Falsified.**

2. **Single-field sweep, ~50 fields total across two passes** (country,
   language, certificate, color, genre [count/identity/first-listed],
   runtime, budget, gross, distributor, production-company count,
   writer-credit-block count, Oscar wins/nominations, sequel/reboot/franchise
   status, aspect ratio, IMDb "Franchise" keyword-category presence, rating
   score, vote count, decade, one-word-vs-multi-word title, and more).
   **No single field lands on exactly 10** with a natural reading, except
   IMDb vote count at one specific cutpoint — explicitly rejected on
   principle, since vote counts grow daily and the puzzle must be solvable
   the same way today as when the escrow was funded in 2022.

3. **Pairwise two-field AND/OR sweep**, 24 single-field boolean criteria x
   2 (AND/OR) x C(24,2) pairs = 600 tests. **16 combinations land on exactly
   10.** Only one has a clean single-concept reading rather than an arbitrary
   pairing of two unrelated facts: **"single country of origin AND single
   language"** (a purely domestic, monolingual production).

4. **A parsing bug was found and fixed** while re-verifying this sweep
   programmatically: the "single writer-credit-block" field was being
   computed by naively splitting on every semicolon in the writers text,
   which miscounts Scream 2's writers field ("Kevin Williamson (characters;
   written by)" — one person, two credited roles, semicolon *inside* the
   parenthetical) as 2 writers instead of 1. Corrected, this field now lands
   on **exactly 10** too — a genuinely single-field, single-concept
   criterion (drops: Leon, The Visitors, Star Wars ANH, Gravity, Sharknado,
   Terminator 2, Scream 2, The Matrix Reloaded, Ghostbusters II, The Human
   Centipede).

5. **All 17 of these exact-10 hits (the 16 pairwise + this 1 single-field
   one) have now been derivation-tested end to end** against the escrow
   address, using literal substrings plus (for whichever of the 5
   zero-literal panels each hypothesis's 24-panel keeper set includes) the
   top-5 curated words listed above for that panel. **Every single one: 0
   matches.** This is the strongest negative result so far — not "the
   leading hypothesis failed," but "every field-based criterion found by
   exhaustively sweeping ~25 IMDb metadata fields, singly or paired, fails."

6. **Word-property numerology** (a word's length or its alphabetical index
   in the BIP39 wordlist) was tried and explicitly rejected — not just
   because it didn't cleanly hit 10, but because a word's position in an
   arbitrary published list is not "information on the film's IMDb page,"
   which is what the puzzle's own rules require the criterion to use.

7. **A large brute-force word-search** (given the country+language-split
   hypothesis) was run at increasing scope: 6,912 candidates (literal words
   only) → 169,344 (adding sourced IMDb-keyword words for the 4
   then-zero-literal keeper panels) → 38,896,200 (also widening the 6
   tied-literal panels) → all **0 matches**. This tested only the "obvious"
   word space for that one specific 10-panel split, not any other.

## What has NOT been tried yet (open avenues)

- **Three-field (or more) combinations.** Only single fields and pairs have
  been swept. Multiple-comparisons risk gets worse with more fields, but
  it's unexplored territory.
- **Fields not in the current data template**: exact award category names
  (not just win/nomination counts), filming-location country vs. production
  country (these can differ), IMDbPro-only data, other numeric cutpoints
  besides the ones already tried, exact per-film IMDb keyword-category
  counts beyond the "Franchise" category already checked.
- **Auditing the other "near miss" field counts** (several fields landed on
  9, one off from 10) **for parsing bugs similar to the one just found and
  fixed** for the writer-credit-block field. This found a real hit once
  already; worth systematically re-checking the others by hand before
  assuming they're genuinely 9 and not 10.
- **The secondary-tier words** (listed above) for the 5 zero-literal panels
  have not been tested against any hypothesis — only each panel's top-5
  curated words have. The true word for one of these 5 panels could be in
  the secondary tier instead.
- **The full, uncurated word space** for the leading country+language-split
  hypothesis (4,389,396,480 candidates using every sourced IMDb-keyword word
  for the zero-literal panels, not just the curated top-5) has not been run
  to completion — only the curated 5-per-panel slice (4.8M) has.
- **A fundamentally different mechanism** — e.g. a positional rule instead
  of a shared-metadata-field rule, or something about the panel image itself
  rather than metadata — hasn't been seriously explored.

## Tooling notes (for reproducibility)

- `tools/oracle.py`: given a candidate 24-word string, checks BIP39 checksum
  validity, then derives addresses across BIP84 (native segwit)/BIP49
  (nested segwit)/BIP44 (legacy), 2 accounts x 3 address indices each, plus 3
  other common raw derivation paths, and compares against the escrow address.
  Has a `--selftest` mode against known public BIP39 test vectors.
- `analysis/imdb_field_audit.xlsx`: all 34 panels' full IMDb metadata
  (cast, countries, languages, exact release date, runtime, genres,
  certificate, color, aspect ratio, sound mix, budget, gross, production
  companies, distributor, awards, AKA titles, filming locations, keywords,
  sequel/franchise status, writers, notes), each row sourced from a live
  IMDb page (not guessed), plus the candidate-word columns described above.
- `analysis/tested.md`: a chronological, append-only negative-results ledger
  — read before proposing anything, to avoid re-testing something already
  ruled out.
- `analysis/leads.md`: open leads and non-literal candidate words, with
  sourcing.
- Several `analysis/bruteforce_*.py` scripts implement the various
  candidate-space searches described above, both single-threaded (safe to
  run unattended) and multiprocess (faster, but caused a real
  freeze/near-crash once on this machine when run at full core count
  concurrent with a video call — now always run with 1-2 cores of headroom).

## What we're specifically asking a second AI's opinion on

1. Any intruder criterion — field, combination, or something else entirely —
   that fits "information findable on a film's own IMDb page, naturally
   isolating exactly these 10 of these 34 specific films" that we haven't
   thought to check.
2. Whether the title→word transformation assumption (literal substring, or
   for 5 films a sourced non-literal word) seems right, or whether there's a
   cleaner unifying rule that would also resolve those 5 films' words
   non-arbitrarily.
3. Any reason to doubt the panel identifications marked "probable" above.
4. General sanity-check on whether "drop 10 by a shared property, keep 24 in
   order" is even the right mechanism, versus something else.
