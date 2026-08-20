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
