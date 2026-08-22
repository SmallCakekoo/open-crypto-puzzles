# Open leads, full notes

Ranked summary is in the README. This file has the reasoning behind the ranking.
The gate on this puzzle is entirely cultural (identifying films and an IMDb
field), not computational: once the 34 words and the intruder rule are both known,
checking a candidate is a single `tools/oracle.py` call, and searching every way to
drop 10 of 34 words is bounded (see the oracle's docstring for the timing).

All 34 panels are now identified (`data/films.csv`); the closed history for panels
11 and 34 is kept below for the record. A director/lead-actor intruder criterion
was found 2026-08-19 and the 792 candidates it implied were run in full with 0
matches (`analysis/tested.md`).

Update, 2026-08-19 (later the same day): panel 8 was re-checked against the actual
live still (not just trusted from an earlier "probable"-confidence pass) and was
wrong -- it is Shutter Island (2010), not The Goonies (`analysis/tested.md`, "Panel
8 re-identification"). This supplies a real, sourced word ("island") for one of the
3 gap panels, cutting the guessed-word gap to 2 (Sharknado, Raiders of the Lost
Ark), but it also breaks the director/lead-actor intruder criterion as previously
stated: Shutter Island's director (Martin Scorsese) also directs panel 13
(Goodfellas), and including that pair the same way McTiernan/Cruise/Gosling were
included pushes the flagged count to 12, not 10. Both consequences are now open
items (leads 1 and 2 below).

Update, 2026-08-19 (still later the same day): panel 11 was also corrected, from
Godzilla to Ace Ventura: When Nature Calls, this time on the user's own direct
identification of the still rather than something found in this session
(`analysis/tested.md`, "Panel 11 correction"). This does not change the
keeper/intruder split (Ace Ventura is not flagged by H1, same as Godzilla was not),
but it does add a 6th ambiguous keeper panel: the corrected title has 3 real
literal candidates ("when", "nature", "call"), none of them guessed. Every
candidate mnemonic checked against the escrow so far (both 792-candidate sweeps)
used Godzilla's "ill" at this panel's position and is invalidated by this
correction; see `analysis/tested.md` for the full invalidated-vs-still-valid
breakdown. Attempted independent verification of panel 11 (reverse-image search on
the actual still, and a search for a documented sand/tuna-can scene in the film)
was inconclusive/unsupportive: no film-specific match from the reverse-image
search, and no documented scene found matching the still's actual content (the
film's only "Bumblebee tuna" material is an unrelated spoken catchphrase). This
remains an open evidentiary tension, recorded transparently rather than resolved.

Update, 2026-08-19 (still later the same day): panel 8 was reverted from Shutter
Island back to The Goonies as the primary identification, per explicit user
instruction, with Shutter Island kept as a secondary probability rather than
discarded -- both "chunk" (Goonies) and "island" (Shutter Island) are carried as
live word options for this panel going forward. This removes the Scorsese-pair
complication in H1 entirely (it was specific to the Shutter Island hypothesis for
this panel): re-running `analysis/intruder_repeat_check.py` with Goonies restored
gives the clean original 10-panel flagged set again, {1, 2, 10, 14, 16, 17, 20, 22,
25, 33}. A full 4,752-candidate cross (7 ambiguous panels x Raiders' 11 guesses,
covering both panel 8 hypotheses and the corrected panel 11 together) was run
against the escrow: 0 matches (`analysis/tested.md`). Not reused from any prior
sweep, and not a kill of any single hypothesis inside it -- the 2 genuine gap
panels (Sharknado, Raiders of the Lost Ark) are still guessed within this space.

Update, 2026-08-19 (still later the same day): the user proposed 6 more candidate
words for Raiders (soft, rail, raise, risk, other, rather). Checked all 6 against
the full wordlist and the squashed title before adding any: only "soft" is a real
substring (via the same kind of boundary-crossing splice already flagged and
excluded for Barry Lyndon's "bar"); the other 5 have zero textual connection to the
title under any check. Added all 6 anyway (a MATCH would be its own proof), growing
Raiders' guess list to 17 and the total cross to **7,344 candidates**. Run against
the escrow: 0 matches (`analysis/tested.md`). This is now the most exhaustive
Raiders word-guess sweep run so far -- every candidate word proposed by any source
in this investigation has been tested, with none producing a match.

## 1. The title-to-word rule for titles with no literal BIP39 word

Update, 2026-08-19: panel 8 was re-identified from The Goonies to Shutter Island,
which does have a literal whole-word BIP39 candidate ("island"). Of the original 4
titles with no literal BIP39 substring, only 2 remain unexplained: Barry Lyndon
(already accounted for as an H1 intruder, so it never needs a word under that
hypothesis) and, still genuinely open, Sharknado and Raiders of the Lost Ark.

Four identified titles originally appeared to contain no English BIP39 word as a
literal substring: The Goonies, Barry Lyndon, Sharknado, and Raiders of the Lost
Ark (`analysis/tested.md`). If the rule is "the literal word in the title," these 4
titles have no answer, which means either the rule is not purely literal (a
synonym, a theme, or a different field of the title), or these 4 films are
themselves among the 10 intruders and never need a word at all.

What would confirm it: a title-to-word rule that produces exactly one BIP39 word
for every one of the 34 titles (or that explains why exactly these 4, or a
different set of 4, need none), checked against the escrow with
`tools/oracle.py` once the 24-word set is assembled.
What would kill it: this is not a bounded space to exhaust; it stays open until a
rule is proposed.
Cost: needs an insight; no compute action available today.

Update, 2026-08-19, after the intruder candidate in lead 2 was found: Barry Lyndon
is one of the 10 flagged intruders (shares director Stanley Kubrick with 4 other
panels), so under that hypothesis it never needs a word, which is exactly the
alternative floated above. That leaves 3 of the 24 keeper panels still needing a
word: The Goonies, Sharknado (both have an unverified single candidate below), and
Raiders of the Lost Ark (no candidate at all: a theme-word search found 11 loosely
plausible BIP39 words -- whip, snake, gold, hat, desert, skull, cave, stone, sand,
jungle, crystal -- with no basis to prefer one, so all 11 are listed as open
options rather than a guess). 5 further keeper panels remain ambiguous among 2-3
literal candidates each: Star Trek: The Motion Picture (motion/picture), Valerian
(city/planet/sand), Ordinary People (ordinary/people), Toy Story (story/toy), and
The Human Centipede (human/first/man). Combining every open choice
(2x3x2x2x3 ambiguous x 11 Raiders options, with Goonies and Sharknado fixed to
their single unverified candidate) gave 792 complete 24-word candidates.

**Result, 2026-08-19: all 792 checked against the escrow via
`analysis/build_candidates.py --run`, 0 matches** (`analysis/tested.md`). Since 16
of the 24 keeper words were held fixed at their single literal candidate, this
sweep did not test whether one of those 16 is actually wrong; it specifically
clears the 72 combinations of the 5 ambiguous panels crossed with "chunk" for
Goonies and "tornado" for Sharknado, for all 11 Raiders guesses. The most likely
next move is not to re-guess Raiders' word from theme association again (11
untargeted guesses already found nothing), but to find real information for it,
Goonies, and Sharknado the way panels 11 and 34 were actually resolved: someone
who knows the film, or a specific detail on its IMDb page, rather than more
pattern search from this end. This is now the highest-priority open lead.

**Update, 2026-08-19 (later the same day):** panel 8 was found to be misidentified
(The Goonies -> Shutter Island, `analysis/tested.md`, "Panel 8 re-identification").
Shutter Island supplies a real, sourced word ("island," a literal whole-word
match), removing the guessed "chunk" entirely. Re-ran the 792-candidate sweep with
"island" substituted in: still 0 matches (`analysis/tested.md`), which is expected
since Sharknado and Raiders of the Lost Ark are still guesses in that space. The
gap is now exactly 2 panels, not 3: Sharknado and Raiders of the Lost Ark, both
still with zero literal BIP39 candidate even after re-checking every word for
substring membership with word-boundary crossing allowed. This is now the
highest-priority open item, tied with lead 2's new complication below.

**Update, 2026-08-19 (still later the same day): panel 11 corrected, Godzilla ->
Ace Ventura: When Nature Calls** (`analysis/tested.md`, "Panel 11 correction," has
the full reasoning and source check). Recomputed from the actual wordlist, not
guessed: "when" and "nature" are literal whole-word BIP39 matches, "call" is a
literal match via the same plural-strip rule already used for "boy"/"boys" and
"river"/"rivers" elsewhere in this set. All 3 are real candidates, none guessed, so
this panel becomes a 6th ambiguous keeper (joining Star Trek, Valerian, Ordinary
People, Toy Story, and The Human Centipede) rather than a gap panel. The gap-panel
count itself is unchanged at 2 (Sharknado, Raiders of the Lost Ark): Godzilla was
never a gap panel (it had "ill"), and neither is Ace Ventura. The full open-choice
candidate space grows from 792 to 2,376 (6 ambiguous panels' product, 216, times
Raiders' 11 guessed options times Sharknado's 1 guessed option), counted directly
via `analysis/build_candidates.py` without `--run` -- not yet checked against the
escrow. Every previously-run candidate (both 792-candidate sweeps, including the
Shutter-Island-corrected one) fixed "ill" at this panel's position and is
invalidated for this reason; none of them tested "when," "nature," or "call" here.

Additional candidates found, 2026-08-19 (checked every BIP39 word for membership
via character-level substring against the squashed title, and by association rather
than literal substring): "chunk" is a valid BIP39 word and is the nickname of a
named character in The Goonies (Lawrence "Chunk" Cohen), a character-name match
rather than a title-substring match. "tornado" is a valid BIP39 word and is the
film's central subject (a tornado full of sharks), a theme match rather than a
title-substring match. Both are unverified hypotheses, not confirmations: neither
can be checked until the 24-word set and intruder rule are both settled, and both
would mean the "somehow" transform is not purely "literal substring of the title"
for every panel, which the existing base rate already suggested. Two much weaker
character-level matches were also found and are flagged as likely coincidental, not
proposed as candidates: "bar" appears in "Barry Lyndon" only by splicing across
"Bar-ry" without respecting the word's own boundaries, and "soft" appears in
"Raiders of the Lost Ark" only by splicing across the space between "...ers of
t..." ("raidersofthe" squashed). Neither respects a word boundary in the title the
way every other candidate in `data/films.csv` does, so both are recorded here for
completeness rather than promoted to `data/films.csv`.

## 2. The IMDb metadata field that splits 24 keepers from 10 intruders

The rules state plainly that "every information you need can be found on IMDb, on
each movie's page," which means the intruder criterion is a specific IMDb field,
not general knowledge about the films. About 25 to 30 binary criteria have been
tried and refuted (`analysis/tested.md`), including the 3 that looked correct
until the next film identification broke them.

**Candidate found, 2026-08-19** (`analysis/intruder_repeat_check.py`,
`analysis/tested.md`): "shares a director or lead actor with another panel in this
set" flags exactly 10 of 34 panels: {1, 2, 10, 14, 16, 17, 20, 22, 25, 33} (Die
Hard, Paths of Glory, the Tom Cruise / Brian De Palma title at panel 10, Eyes Wide
Shut, The 13th Warrior, A Clockwork Orange, First Man, Blade Runner 2049, Barry
Lyndon, The Shining), via Stanley Kubrick (5 films), John McTiernan (2), Tom Cruise
(2), and Ryan Gosling (2). This is the first criterion, out of roughly 30 tried, to
land on exactly
24-versus-10. It also happens to remove every ambiguous-word panel except 4 (Star
Trek, Valerian, Ordinary People, Toy Story), which is a second, independent
consistency check the earlier refuted criteria never had.

What would confirm it: a MATCH from `tools/oracle.py` on some complete, correctly
worded 24-candidate built under this split.
What would kill it: a MATCH under a different intruder split, found some other way.

**Result, 2026-08-19**: the 792-candidate space this criterion implied (see lead
1) was run in full, 0 matches. This is not a kill: 3 of the 24 keeper words in
that space were unverified guesses (see lead 1's update), so the negative result
is most naturally explained by one of those guesses being wrong, not by this
criterion being wrong. The criterion itself still stands on its own evidence (the
exact 24/10 fit and the ambiguous-word overlap in the paragraph above), unless and
until a real word for Raiders, Goonies, or Sharknado is found and still produces no
match.
Cost: the criterion itself cost an insight (found, and not yet falsified); a
retest costs assembling and running a new candidate set once better words for the
3 gap panels exist, on the order of seconds.

**Update, 2026-08-19 (later the same day): this criterion is now in question, not
just unconfirmed.** Correcting panel 8 to Shutter Island (see lead 1's update)
means its director, Martin Scorsese, also directs panel 13 (Goodfellas).
Re-running `analysis/intruder_repeat_check.py` with the corrected data flags 12
panels, not 10: the original 10 plus panels 8 and 13. Nothing in how H1 was
originally stated singles out McTiernan's, Cruise's, or Gosling's 2-film repeats as
valid while excluding Scorsese's 2-film repeat -- they are the same shape of
evidence. Two ways forward, neither resolved yet: (a) find a non-arbitrary
refinement of H1 that keeps the original 10 and excludes the Scorsese pair (for
example, a minimum-repeat-count or a "credited above a specific billing position"
rule that would need to be checked against all 34 panels for consistency, not just
fitted to this one case), or (b) treat this as real evidence against H1 and reopen
the search for a different criterion among the ~30 previously tried single-field
ideas, or a new one. Recorded here rather than silently patched, since fitting a
threshold specifically to exclude the one inconvenient case would be exactly the
kind of overfitting this file has flagged as a risk elsewhere.

Update, 2026-08-19 (panel 11 correction): re-checked with panel 11 corrected to Ace
Ventura: When Nature Calls (director Steve Oedekerk, lead actor Jim Carrey, neither
repeating elsewhere in the set). The flagged set is unchanged, still exactly the
same 12 panels as immediately above. This correction neither resolves nor worsens
the Scorsese-pair complication; the two corrections are independent of each other.

## Closed, then corrected: panel #11 identification (settled 2026-08-19, corrected 2026-08-19)

Panel #11 was unidentified as of 2026-08-16. The still shows what appear to be
"Bumble Bee" branded boxes partly buried in sand; a Nutrition Facts label visible
on the packaging dates the scene to sometime after about 1994.

First resolution (superseded, kept for the record): identified as Godzilla (1998).
Method: viewed the live still at bitcoinmovieenigma.com/blog/11 directly (hands
opening a "Bumble Bee White Tuna in Water" can among several more scattered in
sand), then found an independent plot summary describing the same scene: a beach
shipwreck in the film's Panama opening, where Matthew Broderick's character picks
up a Bumble Bee tuna can from the wreckage. Witness: the source describes the scene
without being prompted with the still itself, which is what makes this a real match
rather than a plausible-sounding guess.

**Correction, 2026-08-19 (later the same day): panel 11 is actually Ace Ventura:
When Nature Calls (1995), not Godzilla.** The user identified this from their own
direct viewing of the still, the same category of evidence (a human who has
watched the film recognizing it) this repository already treats as authoritative
for this kind of panel. I checked both identifications against independent
sources before accepting the change: Godzilla's tuna-can beach scene is
independently documented; the only tuna-related material found for Ace Ventura is
the character's spoken catchphrase ("Bumblebee tuna!"), not a documented visual
scene, so this correction is accepted as a first-hand identification, not as one
with its own independent written corroboration -- flagged as such rather than
overstated. Full reasoning, the recomputed literal BIP39 candidates ("when",
"nature", "call" -- all real, none guessed), the H1 re-check, and exactly what this
does and does not invalidate are in `analysis/tested.md`, "Panel 11 correction:
Godzilla was wrong, real film is Ace Ventura: When Nature Calls." `data/films.csv`
and `analysis/intruder_repeat_check.py` updated accordingly; confidence: confirmed
(identity), word choice: ambiguous among 3 literal candidates (see lead 1).

## Closed: panel #34 identification (settled 2026-08-19)

Two different identification sessions in earlier private research reached different
conclusions for panel #34: "Dead Ringers" (probable) and "The Human Centipede
(First Sequence)" (2009, reached at higher confidence in a later, independent
pass), not reconciled as of 2026-08-16.

An intermediate visual read on 2026-08-19 (before the resolution below) leaned
toward "Dead Ringers": the still shows a warm-lit, contemporary apartment living
room, a man seated on the edge of a couch and a woman reclining on it, 3 lit
candles on a table, and a large red/orange painting behind the couch whose subject
is two conjoined or merging figures. Reasoning at the time was that "Dead Ringers"
(twin gynecologists) fit a conjoined-figures painting thematically, and that "The
Human Centipede" was assumed to be shot in a uniformly drab, low-budget setting.
That assumption was wrong.

Resolution: identified as The Human Centipede (First Sequence). An independent
source on the film's production design states that Dr. Heiter's modernist villa has
"each modernly dressed room... punctuated by a brightly colored painting of
conjoined twins in various stages of surgery," painted by director Tom Six
specifically to foreshadow the plot. This matches the panel's painting exactly (not
just thematically, as a specific documented set-decoration detail) and explains the
"modernly dressed," non-drab room the earlier visual read had weighed against this
candidate: the whole house, not just the surgery room, uses this styling. The scene
is consistent with Heiter sitting beside a sedated victim before the operation.
Witness: the source describes the painting and its purpose without reference to
this specific still, independent confirmation rather than a fit found after the
fact. `data/films.csv` updated accordingly; confidence: confirmed.

Byproduct worth flagging: panel 20 ("First Man") and panel 34 both contain the
literal candidates "first" and "man"; if a well-formed answer does not reuse a word
across two different panels, that favors "human" for panel 34's word without
confirming it.

## Exhaustive literal-substring re-check, all 34 titles, 2026-08-20

Method: the literal-substring candidates in `data/films.csv` had accumulated by eye
over many separate passes, never re-checked mechanically end to end against the
full 2048-word BIP39 list. Ran that exhaustive check now (every BIP39 word, as a
substring within each single word of each of the 34 titles, no crossing spaces,
whole-word beats substring for the same title word per the established hierarchy).
Found several literal substrings earlier passes had missed; `data/films.csv`
updated. Full detail in `analysis/tested.md`. Most notably, **panel 9 (Spartacus)
now has a real literal candidate for the first time: "art" (sp-ART-acus)** -- it
had been "none" since the puzzle's very first pass.

## Non-literal candidates: spelled-out numerals and a portmanteau half, 2026-08-20

Two candidates proposed by the user, both real BIP39 words, neither a literal
substring of their title's actual characters (so kept here, not in
`data/films.csv`'s literal-only column):

- **"two"**, for the 3 panels whose title contains a bare numeral 2 (panel 27
  Terminator 2: Judgment Day, panel 28 Scream 2, panel 30 Toy Story 2) -- the
  digits "2" spelled out as the English word. Not literal (the letters t-w-o do
  not appear in any of these titles), but a very direct, low-ambiguity mapping
  (a numeral has exactly one spelled-out English word), arguably as trustworthy as
  a literal substring even though it fails the letter-for-letter test. Not yet
  tested against any intruder hypothesis.
- **"tornado"**, for panel 26 (Sharknado) -- not a substring of "Sharknado" (the
  letters don't line up: sh-A-R-K-N-A-D-O vs t-O-R-N-A-D-O, no unbroken match),
  but well documented as the second half of the film's own title portmanteau
  (Shark + tornado = Sharknado), independent of this puzzle. This exact word was
  already tried once before, under the old H1 intruder set, with 0 matches
  (`analysis/tested.md`); it has not yet been tried under any hypothesis where
  Sharknado is a keeper rather than an intruder (it currently sits as one of the
  10 dropped panels under the leading "single country + single language"
  hypothesis, so this word isn't needed there).

Still zero candidate of any kind (literal or otherwise sourced) for: panel 13
(Leon: The Professional, beyond "milk"/"gun" already added from IMDb
keywords/review text, see `analysis/tested.md`), panel 32 (Raiders of the Lost
Ark, beyond the pre-revision theme-word list and the IMDb-keyword words already
added), panel 33 (The Shining, beyond the IMDb-keyword words already added). Panel
8 (The Goonies) similarly has no literal candidate but does have IMDb-keyword and
character-name candidates already recorded (`analysis/tested.md`).

## Full IMDb keyword-page sweep for the same 5 zero-literal panels, 2026-08-20

Per the user's explicit priority ("find real words for the 5 zero-candidate
panels"), went back to all 5 zero-literal-substring panels and pulled each
film's *complete* IMDb `/keywords/` page (not just the top 5-6 already in the
field audit), keeping only tags that are themselves a whole BIP39 word. Full
method and per-panel diffs in `analysis/tested.md`, "Full IMDb keyword lists...
2026-08-20". Updated totals:

- **The Goonies** (panel 8): one, brand, chunk, gold, cave, gadget, beach,
  rescue, legend, chase, sword, coin, toilet, bicycle, tunnel, jewel, pizza,
  fire, sheriff, forest, skull, piano, child, trap, ship, pistol, arrest,
  organ, asthma, book, knife, escape, marble, camera, kiss, thunder, rain,
  wish, police, hidden, danger, humor.
- **Leon: The Professional** (panel 13): milk, gun, girl, police, elevator,
  crush, hotel, love, pistol, knife, weapon, shield.
- **Sharknado** (panel 26): tornado (now confirmed a real standalone keyword
  tag, not just the inferred portmanteau half), fish, dog, beach, gun, pistol,
  animal, vehicle, car, child.
- **Raiders of the Lost Ark** (panel 32): whip, snake, gold*, hat, horse, ship,
  knife (*"gold" is from the older props/scenes list, not this keyword page --
  not re-verified as a standalone tag here), truck, chase, jungle, torch,
  mirror, canyon, desert, fire, bar, love, ritual, lecture, dress, tent,
  island, wine, blood, warrior, escape, kiss, pistol, sword, rescue, spider,
  basket, soldier, spirit, alcohol, car, hero, magic, weapon, mechanic, faith,
  fiction.
- **The Shining** (panel 33): hotel, maze*, snow, ghost, mirror, blood (*"maze"
  itself isn't a standalone tag; the real tags are "labyrinth" and "hedge
  maze"), bar, chase, elevator, winter, marriage, kitchen, author, knife,
  doctor, window, door, toy, chef, escape, rescue, kiss, danger, night, gift,
  boy, airport. Plus a separate, weaker cluster of generic content-advisory
  words (cruel, fatal, shock, sadness, man, woman, vicious, tragic, sick,
  weird, suffer, limit, wrong, rare, fiction) that are literal BIP39 matches
  but read as severity/mood tagging rather than anything specific to this
  film -- kept distinct, not treated as equally trustworthy.

Not yet tested against any hypothesis or run through `oracle.py`. The combined
space across just these 5 panels is now large (39 x 12 x 10 x 42 x ~26-41) --
worth curating to a short list per panel (most iconic/distinctive word) before
any brute force, rather than testing the full cross exhaustively again.

## Curated top-5 per panel, 2026-08-20

The full expanded space (all keyword-tag words for the 4 zero-literal keeper
panels under the country+language-split hypothesis -- Sharknado is dropped
under that hypothesis so doesn't matter here) came to 4,389,396,480 candidates,
~113x the previous 38.9M run, an estimated ~26h to exhaust even at 12-worker
speed. Per the user's explicit choice, curated each of the 5 zero-literal
panels down to its **5 most iconic/distinctive words** -- character names,
signature props, or single-scene objects specific to that film, not generic
keyword-tag words shared by lots of films (e.g. "child", "police", "car").
This is a judgment call, not a mechanical filter; reasoning per panel below.
The excluded words are **not discarded** -- kept as a second/third-pass tier,
same convention as the "inferior substrings" column in
`analysis/imdb_field_audit.xlsx` (words that exist and are real BIP39 matches,
just not promoted to the primary candidate list for this pass).

- **Panel 8, The Goonies** -- top 5: **chunk** (Chunk's own nickname, the most
  specific possible identifier), **gold** (the treasure hunt's actual object),
  **cave** (the film's central setting), **piano** (the skeleton-organ booby
  trap, one of the film's most memorable scenes), **skull** (skeleton imagery
  throughout the cave sequence). Secondary tier (37): one, brand, gadget,
  beach, rescue, legend, chase, sword, coin, toilet, bicycle, tunnel, jewel,
  pizza, fire, sheriff, forest, child, trap, ship, pistol, arrest, organ,
  asthma, book, knife, escape, marble, camera, kiss, thunder, rain, wish,
  police, hidden, danger, humor.
- **Panel 13, Leon: The Professional** -- top 5: **milk** (Leon's own iconic
  habit, already the strongest candidate from the start), **gun** (the
  "child with a gun" image that defines Mathilda's arc), **shield** (Mathilda
  used as a human shield in the finale), **pistol** (Stansfield's signature
  pill-and-pistol ritual before a kill), **crush** (the age-difference
  relationship that is the film's central, controversial theme). Secondary
  tier (7): girl, police, elevator, hotel, love, knife, weapon.
- **Panel 26, Sharknado** -- top 5: **tornado** (half the title itself, and a
  real standalone IMDb keyword tag), **fish** (sharks classified as fish is
  literally the "sharksploitation" joke), **dog** (the widely-referenced
  "save the dog" beat), **beach** (the film's opening/central setting),
  **gun** (guns and improvised weapons used against the sharks throughout).
  Secondary tier (5): pistol, animal, vehicle, car, child. Note: under the
  currently-tested hypothesis Sharknado is a dropped intruder, so this
  panel's word doesn't affect the derivation -- curated anyway for
  completeness/future hypotheses.
- **Panel 32, Raiders of the Lost Ark** -- top 5: **whip** (Indy's single
  most iconic prop), **snake** ("why'd it have to be snakes," the snake pit
  scene), **hat** (Indy's fedora, iconic), **spider** (the giant tarantulas
  on the temple door in the opening sequence), **torch** (used throughout
  the opening cave sequence). Secondary tier (37): gold, horse, ship, knife,
  truck, chase, jungle, mirror, canyon, desert, fire, bar, love, ritual,
  lecture, dress, tent, island, wine, blood, warrior, escape, kiss, pistol,
  sword, rescue, basket, soldier, spirit, alcohol, car, hero, magic, weapon,
  mechanic, faith, fiction.
- **Panel 33, The Shining** -- top 5: **hotel** (the Overlook, the film's
  central setting), **mirror** (the REDRUM mirror-writing scene, one of the
  most famous shots in horror film history), **blood** (the elevator-of-blood
  image), **ghost** (the central haunting), **door** (the "Here's Johnny!"
  axe-through-the-door scene, the film's most quoted moment). Secondary tier
  (22): maze, snow, bar, chase, elevator, winter, marriage, kitchen, author,
  knife, doctor, window, toy, chef, escape, rescue, kiss, danger, night,
  gift, boy, airport.

New candidate space for the country+language-split derivation: 4,800,000
(down from 4,389,396,480), small enough to run in-process in minutes. See
`analysis/bruteforce_curated_top5.py` and `analysis/tested.md` for the run and
its result.

## Criterion sweep rebuilt programmatically, one field corrected, 2026-08-20

Per the user's request to focus on finding the real intruder criterion, the
whole 24-field sweep was rebuilt from scratch programmatically (not by hand)
from `analysis/imdb_field_audit.xlsx`, since the earlier session's exact
17-hit list was never saved to a file. This caught a real bug: the
single-writer-credit-block field was being computed by splitting on every
semicolon, which miscounts Scream 2's writers text ("Kevin Williamson
(characters; written by)" -- one person, two roles, semicolon inside the
parenthetical) as 2 writers instead of 1. Fixed, verified by hand against all
34 rows. **Corrected count: exactly 10**, not 9 -- this is now a genuinely
single-field intruder-criterion candidate (not an arbitrary two-field
AND/OR), dropping: Leon: The Professional, The Visitors, Star Wars: A New
Hope, Gravity, Sharknado, Terminator 2, Scream 2, The Matrix Reloaded,
Ghostbusters II, The Human Centipede. Tested end to end
(`analysis/tested.md`): **0 matches** across 480,000 candidates.

Full sweep re-run with the fix: 16 pairwise AND/OR hits (down from the
previously-recalled 17, consistent with the single-writer-block field's old
wrong count of 9 presumably producing one extra coincidental pairwise hit
that no longer appears) + 1 single-field hit = 17 total, matching what the
user recalled. Full list and every hit's exact dropped-panel set in
`analysis/tested.md`. All 15 not-yet-tested pairwise hits are queued for
end-to-end derivation via `analysis/bruteforce_all_criterion_hits.py`
(running in the background, ~2h, single-thread) -- see tested.md for results
once complete.

## Single definitive word per panel, all 34, 2026-08-20

Per the user's request, collapsed every panel's candidate list down to
exactly one word each (previously many panels carried 2-5 tied candidates),
so that any future intruder-hypothesis test becomes one instant check instead
of a combinatorial search. Rule applied: a literal whole title-word match
beats a mere substring/fragment; among multiple whole-word matches, the most
distinctive/iconic one for that film; for the 5 zero-literal panels, the
already-vetted single most iconic candidate. This is a judgment call on the
12 panels that had tied literal candidates, not a mechanical certainty --
full reasoning per panel in `analysis/SUMMARY_FOR_EXTERNAL_AI_2026-08-20.md`.

Final table (panel: word): 1 hard, 2 glory, 3 alien, 4 mad, 5 alien, 6 now,
7 escape, 8 chunk, 9 art, 10 possible, 11 ill, 12 life, 13 milk, 14 mask,
15 river, 16 visit, 17 orange, 18 hope, 19 gravity, 20 first, 21 solar,
22 blade, 23 galaxy, 24 close, 25 bar, 26 tornado, 27 day, 28 cream,
29 matrix, 30 toy, 31 ghost, 32 whip, 33 hotel, 34 human.

Only "alien" repeats (panels 3 and 5, unavoidable -- the films are literally
titled Aliens/Alien). Not yet run through the oracle as-is (34 words isn't a
valid mnemonic length until 10 are dropped) -- this table's purpose is to
make the next round of hypothesis testing trivial. Also written up in full,
alongside the whole investigation, in a standalone summary document prepared
for external review: `analysis/SUMMARY_FOR_EXTERNAL_AI_2026-08-20.md`.

## Splice check (full squashed title) + AKA titles for the 5 zero-literal panels, 2026-08-21

Per the user's concern that we've been brute-forcing intruder criteria without
first nailing down the words themselves, did two cheap/safe (no heavy compute)
checks instead:

1. **Squashed-title splice check**: concatenated each of the 5 zero-literal
   titles with no spaces (same method that found "soft" for Raiders earlier:
   panel-8 "thegoonies", panel-13 "leontheprofessional", panel-26
   "sharknado", panel-32 "raidersofthelostark", panel-33 "theshining") and
   checked every one of the 2048 BIP39 words as a substring, crossing word
   boundaries. **Result: only Raiders has any match ("soft", already known).
   Goonies, Leon, Sharknado, and Shining have zero literal BIP39 substring
   under any boundary-crossing, confirmed exhaustively, not just by the
   earlier single-word-boundary check.** This rules out an overlooked literal
   answer for these 4 -- if the transform really is "literal substring" for
   every title, these 4 films' true words (if the panels are correctly
   identified) must come from a different official title string entirely.

2. **AKA (official alternate title) check**, the puzzle rules' own title text
   doesn't specify *which* title string to use, so checked every official
   AKA IMDb lists for the 3 panels not yet checked this way (Raiders,
   Shining, Sharknado -- Goonies and Leon were already checked 2026-08-20,
   no new literal word found for either):
   - **Raiders**: English-language AKAs are "Raiders of the Lost Ark",
     "Indiana Jones and the Raiders of the Lost Ark", and working titles
     "Indiana Jones," "Raiders," "The Adventures of Indiana Smith." **"one"
     is a literal substring of "Jones"** (as in "Indiana Jones") -- clean,
     but "one" is already a Goonies candidate, so using it here too would
     duplicate a word across two panels, which this project has flagged
     before as a mark against a candidate, not for it. The working-title
     splices (sand, era, head, venture, find) are weaker still and rely on
     titles the film was never actually released under.
   - **Shining**: English AKAs are "The Shining," "Shining," and "Stanley
     Kubrick's 'The Shining'" (a real, distinct AKA entry on IMDb). **"brick"
     is a literal substring of "Kubrick"** -- real per IMDb's own AKA
     listing, but comes from the director's name, not the film's title
     proper, which feels like a stretch relative to every other panel's
     answer.
   - **Sharknado**: English AKAs are "Sharknado," "Sharknado 3D," and the
     working title "Dark Skies" (already flagged in
     `analysis/imdb_field_audit.xlsx` as an IMDb data quirk unrelated in
     content to this film, not a real alternate title). "Dark Skies" splices
     to "ski" (dark-SKI-es) -- weak, and builds on a title we already believe
     is a database error for this entry, not a genuine AKA.

None of these AKA-derived words are being promoted to the primary or
secondary candidate tier -- flagged here as found-but-weak, for the record,
not treated as better than the existing keyword-sourced candidates (chunk,
milk, tornado, whip, hotel and their secondary tiers). The exhaustive splice
check (item 1) is the more solid result: it closes off "we missed an obvious
literal match" as an explanation for these 4 panels' zero-literal status.

Still genuinely open: the puzzle's own rules text just says "transform
'somehow'" (the author's own quotation marks, see `clues/author-posts.md`)
with zero further detail -- there is no hidden precise rule being missed in
the author's own words, confirmed by re-reading the rules and about-page
quotes directly. Date: 2026-08-21.

## Panel 4 alternative identification considered and rejected: Going Places (1974), 2026-08-21

A third party's own candidate list (source unknown, passed to the user, not
the user's own visual identification) proposed panel 4 as **Going Places**
(1974, tt0072353, original title "Les Valseuses") instead of **Mad Max**
(1979). The user themselves was skeptical of this alternative but wanted it
checked in case Mad Max was the wrong call.

Checked what would follow if true, without being able to verify visually
(no access to the actual panel still): "Going Places" does have a clean
literal BIP39 word ("place," inside "Places," same plural-strip convention
used elsewhere in this project) -- stronger on its own than "mad." However,
**Going Places has zero IMDb Connections-tab links to any of the other 33
panels** (checked live: its only connections are to unrelated media --
Depardieu documentaries, podcasts, an unofficial remake, one spoof -- none
overlapping this puzzle's 34-film set). Mad Max, by contrast, already has a
real, verified connection to panel 17 (A Clockwork Orange). Swapping to
Going Places would turn panel 4 into an 11th zero-connection panel under the
Connections-based intruder hypothesis (the strongest hypothesis found so
far, see "NEW CRITERION FOUND" in tested.md), breaking its clean
"exactly 10" result.

**Conclusion: rejected.** No visual evidence supports the swap, the user's
own confidence in it was low, and the one concrete fact checkable without
the image (Connections-tab data) argues for Mad Max being the better fit,
not against it. Mad Max stays as the panel 4 identification. Flagging this
here so the same third-party suggestion isn't re-investigated from scratch
if it resurfaces. Date: 2026-08-21.

## Notes from community GitHub issue #9, for reconciliation, 2026-08-21

Full context and the three externally-tested criteria are in tested.md,
"Community cross-check: GitHub issue #9..." This entry is just the
open-questions/leads side of that same thread.

- **Alternate/regional title question, raised by "couldes"**: IMDb pages
  differ by region -- some show subtitles, some don't (e.g. "Star Wars:
  Episode IV - A New Hope" vs plain "Star Wars," or "Solaris" with/without a
  year disambiguator). Open question for the author: does the title-to-word
  transform apply to a specific canonical title string, or is any
  region/AKA variant fair game? This is directly relevant to our own
  AKA-title exploration (leads.md, "Splice check... + AKA titles,
  2026-08-21") -- we already tried this for the 5 zero-literal panels with
  weak results, but haven't tried it systematically across all 34 (e.g. a
  clean literal word hiding in a *different* region's title for an
  otherwise-solved panel, not just the problem ones).
- **Numeral-to-word readings, from "nosignme"**: their word list treats
  bare digits in titles as spelled-out numbers more aggressively than we
  have -- e.g. panel 22 (Blade Runner 2049) -> "two, zero" (from "2049"),
  panel 27/28/30/31 -> "two" (from "2"/"II"). We had already flagged "two"
  as a non-literal candidate for the bare-"2" titles (panels 27, 28, 30) but
  never extended this to multi-digit years like "2049," and never tried
  "zero" specifically. Not yet tested against any hypothesis.
- **Community consensus panel list** (floflo777's reconciliation, referencing
  a separate `data/films_community_issue9.csv` fork in that repo): confirms
  our own panel 4 (Mad Max) and panel 30 (Toy Story 2) calls, and
  independently surfaces the same ~9-panel identification-ambiguity cluster
  (3, 5, 9, 13, 14, 16, 23, 24, 27) our own 2026-08-20 major dataset
  revision already addressed from the user's own frame-by-frame review --
  worth a side-by-side diff against `data/films_community_issue9.csv` if
  that file becomes accessible, to see whether the community's frame reads
  agree with the user's for all 9, or whether any specific panel is still a
  live disagreement.
- **Three externally-run criteria now also ruled out** (not run by us, GPU
  compute reported by "timothy-barus," see tested.md for full detail):
  shared release year, year>=2000, ten-shortest-by-runtime. Do not
  re-attempt these -- if revisiting, the highest-value move would be
  independently reproducing just the checksum-valid count for one of the
  three as a spot-check of their methodology, not re-running the full
  sweep.
- **Our IMDb Connections hypothesis is not represented anywhere in that
  thread** -- worth posting there, since the thread's own current
  conclusion ("ideas on [Goonies/Leon/Sharknado's words] are worth more than
  compute") is exactly the kind of ask our Connections angle doesn't answer
  directly, but the *degree-0 panel list* it produces (a different 10-panel
  split than every criterion tried there so far) is new information for
  that effort regardless.
