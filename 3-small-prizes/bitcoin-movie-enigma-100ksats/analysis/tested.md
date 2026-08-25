# Tested hypotheses, full ledger

Summary table is in the README. This file has the full detail behind each row. All
counts below were re-read from my own private research notes before writing this
folder.

## Both published image sets are identical

The rules page mentions "an alternative release, as a single image." I compared
every one of the 34 individual panel images against the corresponding region of the
combined alternative-release image, byte for byte (MD5).

Result: 34 of 34 panels match exactly. This channel is closed: the alternative
release carries no additional or different information, it is the same 34 stills
republished as one file. Date: 2026-08-03.

## Intruder criterion: MPAA rating equals R

Hypothesis: the 10 "intruder" films are exactly the ones rated R by the MPAA, and
the IMDb page field the rules point to is the certificate rating.

Method: count the films confirmed R-rated as more panels were identified.

Result: this criterion looked correct early, when only a partial set of films was
identified (10 of 18 identified films rated R at one point). It broke as soon as 2
more films were confirmed: with panel #4 (Mad Max, R) and panel #34 (rated R under
either of its 2 disputed identifications) added, the R-rated count reached 16 to 18
out of the identified films, well past 10. Refuted. Witness: this is a direct count
over the film corpus, not a search that could produce a false negative; re-counting
is immediate from `data/films.csv`. Date: 2026-08-04.

## Intruder criterion: won at least one Oscar

Hypothesis: the 10 intruders are the films that won at least one Academy Award.

Method: same approach, counting Oscar-winning films as identifications accumulated.

Result: looked correct at 10 of 21 identified films early on, refuted once panel
#24 (Ordinary People, a 4-Oscar winner including Best Picture) was confirmed
through a route independent of the reverse-image search used for most other
panels, pushing the count to 11 of 34. Date: 2026-08-04.

## Intruder criterion: adapted from a novel

Hypothesis: the 10 intruders are the films adapted from a published novel.

Method: same approach.

Result: looked correct at 10 of 31 identified films, refuted at 12 of 34 once
further identifications landed. Date: 2026-08-04.

## About 25 further intruder criteria

Method: the same accumulate-and-recount approach applied to about 25 further
candidate IMDb fields and binary properties (examples: country of origin,
decade of release, director's other Bitcoin-relevant work, runtime bracket, color
versus black and white, single-word versus multi-word title).

Result: none produced an exact 24-versus-10 split against the identified film set,
either from the start or after refutation by a later identification. Witness: each
criterion is a direct count over the film corpus and is immediately re-checkable;
no witness protocol beyond re-counting applies here. Date: 2026-08-04.

## Panel 11 identification attempt, 2026-08-19

Method: viewed the live still at bitcoinmovieenigma.com/blog/11 directly (a pair of
hands opening a "Bumble Bee White Tuna in Water" can, several more Bumble Bee tuna
cans scattered in sand, a dark olive/green sleeve visible on the near arm). Ran
several web searches on the visible details (brand, setting, "buried in sand",
"stranded", "survival", combined with the post-1994 Nutrition-Facts-label date
constraint already on record). No reverse-image-search engine was reachable in this
session (Google Lens, TinEye and Bing visual search all refused to load under this
session's browsing policy), so this was a text-search-only attempt, not a true
reverse image search.

Result: no candidate film identified with any confidence. One search suggested a
film called "Cortes" involving a man buried in desert sand, but the search tool
itself could not confirm a tuna-can scene in it, so it is not recorded as a
candidate here. Refuted as a viable method, not as a lead: the panel itself is
unchanged and stays open. Witness: none available (no positive identification to
witness). Date: 2026-08-19.

## Panel 11 and panel 34 identified, 2026-08-19 (later the same day)

**Superseded, 2026-08-19 (still later the same day): the panel 11 result below
(Godzilla) was itself corrected to Ace Ventura: When Nature Calls; see "Panel 11
correction" further down this file for the full reasoning and evidence. Kept below
unedited for the record, not as a currently-valid identification.**

Method: a human researcher who had watched both films recognized panel 11 as
Godzilla (1998) and panel 34 as The Human Centipede (First Sequence), from the
still images. Both identifications were then checked against independent sources
before being accepted: for panel 11, a plot-summary source independently describes
the exact scene visible in the still (a Panama beach shipwreck with Bumble Bee tuna
cans); for panel 34, a production-design source independently describes Dr.
Heiter's house as decorated throughout with paintings of conjoined twins, matching
the painting visible in the still. Neither source was written with this puzzle or
this still in mind, which is what makes each a real corroboration rather than a
plausible-sounding coincidence.

Result: both confirmed. `data/films.csv`, `analysis/leads.md` and the README
updated accordingly. This is exactly the outcome the open-leads cost estimate
anticipated ("needs a person"): a computational or text-search-only method did not
crack either panel, a person's recognition did. Witness: yes, both against an
independent source (see analysis/leads.md for the exact sources). Date: 2026-08-19.

## Title-to-word rule: 2 new non-substring candidates found

Method: checked every BIP39 wordlist entry for character-level containment against
each of the 4 titles with no literal per-word substring match, allowing matches to
span the title's own word boundaries, and separately considered character-name and
theme associations for the same 4 titles.

Result: "chunk" (character name in The Goonies) and "tornado" (the film's subject,
in Sharknado) are valid BIP39 words associated with 2 of the 4 titles by a
non-literal rule (character name / theme, not substring). "bar" (Barry Lyndon) and
"soft" (Raiders of the Lost Ark) are technically containable in the squashed title
string but only by splicing across word boundaries the title itself does not have,
so they are recorded as likely coincidental, not proposed as candidates. None of
this is confirmed: it cannot be checked against the escrow until the 24-word set and
intruder rule are both settled (see analysis/leads.md, lead 1, for the full
reasoning). Date: 2026-08-19.

Methodological note, kept because it explains why no criterion is locked in below:
3 different criteria (MPAA=R, Oscar win, novel adaptation) each looked like the
answer while the film corpus was still incomplete, and each was broken by the very
next identification. With about 25 to 30 criteria tried against a set of only 34
films, landing on an exact 10-film split by chance is not strong evidence on its
own. My working rule is to not treat any criterion as confirmed before all 34
panels are identified with confidence.

## Title-to-word rule: base rate measurement

This is a measurement, not a hypothesis test with a pass or fail result: of the 33
titles identified as of 2026-08-04, 29 contain at least one English BIP39 word as a
literal substring of the title (for example, "Die Hard" contains "hard"; "A
Clockwork Orange" contains 4 candidates: "clock," "orange," "range," "work"). Four
titles contain none: The Goonies, Barry Lyndon, Sharknado, and Raiders of the Lost
Ark. The literal-substring rate across the 33 identified titles is about 14%,
counted per candidate word against the full BIP39 wordlist. This measurement rules
out "every title contains exactly one obvious word" as the full rule (4 titles have
none, several have more than one), but does not by itself say which of several
candidate words is the intended one, or what the rule is for the 4 titles with none.

Update, 2026-08-19: with panels 11 and 34 identified, the base rate is now 31 of 34
titles containing at least one literal BIP39 substring; the same 4 titles remain
the exception (both Godzilla and The Human Centipede (First Sequence) do have a
literal candidate). This does not change the measurement's conclusion above.

## Intruder criterion: shares a director or lead actor with another panel here

Hypothesis: an IMDb page lists a director and a top-billed cast; a film is an
"intruder" if its director or lead actor also directs/stars in another film among
these same 34 panels.

Method: compiled director and lead actor for all 34 panels from general film
knowledge, with a targeted web search to confirm each claim this session actually
relied on (`analysis/intruder_repeat_check.py` has the full table and sources for
the pairs below). Computed which panels share either field with another panel in
the set.

Result: exactly 10 panels are flagged, matching the puzzle's required count exactly
on the first attempt: Stanley Kubrick directs 5 of the 34 (panels 2, 14, 17, 25,
33: Paths of Glory, Eyes Wide Shut, A Clockwork Orange, Barry Lyndon, The Shining);
John McTiernan directs 2 (panels 1, 16: Die Hard, The 13th Warrior); Tom Cruise
leads 2 (panels 10, 14: panel 10's title and Eyes Wide Shut, panel 14 already
counted under Kubrick); Ryan Gosling leads 2 (panels 20, 22: First Man, Blade
Runner 2049). Union of flagged panels: {1, 2, 10, 14, 16, 17, 20, 22, 25, 33}, 10
distinct panels. This is the first criterion out of roughly 30 tried (here and
2026-08-04) to produce an exact 24-versus-10 split.

Cross-check: every panel whose literal candidate word was ambiguous (2 or more
BIP39 substrings, `data/films.csv`) except Star Trek: The Motion Picture,
Valerian, Ordinary People, and Toy Story falls inside this same 10-panel set
(Paths of Glory, panel 10, Eyes Wide Shut, A Clockwork Orange). If this
criterion is right, those 4 ambiguous panels get dropped as intruders and their
word ambiguity never had to be resolved, which is consistent with a real
underlying rule and not the kind of thing a spurious correlation tends to produce.

This is not yet run against the escrow: doing so needs a complete, ordered 24-word
candidate, and 3 of the 24 keeper panels (Goonies, Sharknado, Raiders of the Lost
Ark) still lack a settled word (`analysis/leads.md`), plus 5 keeper panels remain
ambiguous among their own literal candidates. Witness: both repeated-director and
repeated-actor claims trace to independent film-database sources listed in
`analysis/intruder_repeat_check.py`, not to a fit found after the fact. Date:
2026-08-19.

## Full 792-candidate sweep under the 2026-08-19 intruder + word findings

Method: `analysis/build_candidates.py --run` assembled every complete 24-word
mnemonic implied by the 24 keeper panels under the director/actor intruder
hypothesis above: 16 panels with a single literal BIP39 candidate held fixed, 5
ambiguous panels (Star Trek: The Motion Picture, Valerian, Ordinary People, Toy
Story, The Human Centipede) varied across their 2-3 literal candidates, and 3 gap
panels (The Goonies, Sharknado, Raiders of the Lost Ark) varied across their
non-literal or theme-word guesses (1, 1, and 11 options respectively). 792 total
candidates, each checked against the escrow via `tools/oracle.py --stdin`
(BIP84/49/44, 2 accounts x 3 indices, plus 3 raw paths).

Result: 0 matches. This is a certified negative for this specific bounded space
(the oracle's own `--selftest` passed immediately before this run, so a real match
would have been caught), not a refutation of the intruder criterion itself: the
weakest links in this candidate space are the 3 gap-panel guesses (Goonies
"chunk" and Sharknado "tornado" are association guesses, not literal matches;
Raiders' 11 options have no basis to prefer one over another) and, less likely,
one of the 16 "settled" single-literal-candidate words being the wrong reading.
Witness: `tools/oracle.py --selftest` passed before this run; the sweep is
reproducible by re-running `analysis/build_candidates.py --run`. Date: 2026-08-19.

## Focused word search for The Goonies, Sharknado, Raiders of the Lost Ark, 2026-08-19

Method: re-read the rules text closely ("transform each movie TITLE into a BIP39
word"), then searched specifically for evidence tied to each title rather than the
films generally: exact IMDb title strings, alternate/international titles (AKA),
working titles, official taglines, this site's own page source (checked for a
caption beyond the image, none found), archive.org snapshots of the rules page
(none exist), the author's Nostr profile and public notes (confirms the puzzle has
run "for two years," no mechanism detail beyond the rules page), a general web
search for outside community discussion of this specific puzzle (none found
indexed), and this repository's own git history for the folder (2 commits, nothing
beyond what is already in the files).

Result, per title:
- The Goonies: no literal BIP39 substring (already established). Alternate
  international titles exist (French "Les Goonies," German "Die Goonies," etc.)
  but are non-English and do not help, since the rule outputs an *English* BIP39
  word. Official tagline contains several BIP39 words ("secret," "hidden," "join,"
  "old," "call," "they") but these are common English function/filler words with
  no specific tie to this film over any other -- checking, they appear at similar
  rates in the other 2 films' taglines below, which is itself evidence that
  tagline text is too noisy a source to trust without a further rule to pick one
  word out of several.
- Sharknado: no literal BIP39 substring. Confirmed via an independent, sourced
  claim (Hollywood Reporter interview with cast member Cassie Scerbo) that the
  film's original working title was "Dark Skies," changed only to avoid clashing
  with an unrelated 2013 alien-abduction film of the same name. Neither "dark" nor
  "sky"/"skies" is a BIP39 word, so this real, verified fact does not yield a
  candidate. Tagline ("Enough said!") yields only "enough," a common word with no
  specific tie to the film.
- Raiders of the Lost Ark: no literal BIP39 substring in the theatrical title.
  The most-cited alternate title, "Indiana Jones and the Raiders of the Lost Ark"
  (home-video packaging only, never on screen), adds "Indiana" and "Jones," both
  checked and neither is a BIP39 word. Both official taglines checked; matches
  ("return," "great," "name," "must") are common words, same noise problem as
  above.

Conclusion: no solid, source-backed candidate word was found for any of the 3
films from title text, alternate titles, working titles, or taglines. Widening the
search past the literal title (to taglines) does not converge on an answer; it
multiplies false-positive hits from ordinary English words, which argues against
trying quotes or synopsis text next for the same reason. Refuted as a source, not
as a lead: the 3 panels stay open. Witness: the Sharknado working-title claim
traces to a named, quoted source (Cassie Scerbo, Hollywood Reporter); the "no
literal substring" claims are direct, reproducible checks against the full BIP39
wordlist. Date: 2026-08-19.

## Major dataset revision: 10 of 34 panels corrected from the user's own frame-by-frame research, 2026-08-20

Method: the user independently re-watched the actual films (including via
non-official streams) scene by scene, cross-checked identifications with other
people, and produced a revised 34-panel list. This is first-hand identification
work by the user, not something verified independently by me in this session
beyond panel 16 (which already had circumstantial support from an earlier
reverse-image/plot check, see above).

Panels changed from the prior dataset:

| # | Before | After |
|---|---|---|
| 3 | Alien (1979) | Aliens (1986) |
| 5 | Star Trek: The Motion Picture | Alien (1979) |
| 9 | Duel in the Sun | Spartacus (1960) |
| 11 | Ace Ventura: When Nature Calls | Godzilla (1998) (reverts to the original 2026-08-19 identification) |
| 13 | Goodfellas | Leon: The Professional |
| 14 | Eyes Wide Shut | The Man in the Iron Mask (1998) |
| 16 | The 13th Warrior | The Visitors (Les Visiteurs) -- confirms the disputed alternative from earlier in this file |
| 23 | Valerian and the City of a Thousand Planets | Guardians of the Galaxy |
| 24 | Ordinary People | Close Encounters of the Third Kind |
| 27 | The Lost Boys | Terminator 2: Judgment Day |

`data/films.csv` updated: these 10 panels recorded as "probable" (first-hand user
identification, not yet independently re-sourced by me for 9 of the 10). Also
corrected in the same pass, independent of this revision but discovered earlier in
this investigation and applied now: panel 25 (Barry Lyndon) "bar" is a real
substring, previously wrongly recorded as none; panel 31 (Ghostbusters II) gets 2
more valid substrings (host, bus) alongside the already-recorded "ghost"; panel 33
(The Shining) "shine" is corrected to none (verified not a literal substring of
"shining").

**Consequence for H1 (director/lead-actor repetition):** re-ran
`analysis/intruder_repeat_check.py` against the corrected list. Result: **14 of 34
panels flagged, not 10**: Stanley Kubrick x5 (Paths of Glory, Spartacus, A
Clockwork Orange, Barry Lyndon, The Shining), James Cameron x2 (Aliens, Terminator
2), Steven Spielberg x2 (Close Encounters, Raiders of the Lost Ark), Kirk Douglas
x2 (Paths of Glory, Spartacus, already counted under Kubrick), Sigourney Weaver x2
(Aliens, Alien), Jean Reno x2 (Leon: The Professional, The Crimson Rivers), Ryan
Gosling x2 (First Man, Blade Runner 2049). Union: {2, 3, 5, 9, 13, 15, 17, 20, 22,
24, 25, 27, 32, 33}, 14 panels. **H1 as previously stated no longer produces the
required 24-versus-10 split against the corrected dataset.** Checked whether a
simple sub-filter recovers exactly 10: "director-only" (drop the 3 actor-only
pairs) gives 9; "actor-only" (drop the 3 director clusters) gives 8; neither hits
10 either. No non-arbitrary refinement found yet.

**Consequence for the title-to-word literal check:** re-ran the same word-lookup
methodology (whole word > singular/plural > single-word substring) against the 9
changed titles. Aliens -> "alien" (singular/plural); Alien -> "alien" (whole word) 
-- these two would compete for the identical word if both were kept, which is
itself consistent with both being flagged by H1 above. Spartacus and Leon: The
Professional have zero literal candidates under any tier -- also both flagged by
H1, so neither needs a word if H1 (in whatever form) holds. The Man in the Iron
Mask has 3 whole-word candidates (man/iron/mask), a keeper under H1, unresolved.
Guardians of the Galaxy has one clean literal candidate, "galaxy" (whole word, no
competing candidate at any tier) -- a keeper under H1, and no longer ambiguous
unlike its predecessor Valerian. Close Encounters of the Third Kind has a 2-way
tie (close/kind) but is itself flagged by H1, so doesn't need resolving. Terminator
2: Judgment Day has one clean candidate, "day", but is also flagged by H1.

Status: dataset revision accepted and persisted; H1's specific 10-panel claim is
now falsified against this dataset (14, not 10); the search for the real intruder
criterion is reopened from scratch against the corrected 34-panel list, not
patched onto H1's specific membership. Date: 2026-08-20.

## Local brute-force sweep, phases 1 + 2A + 3 (one-in/one-out), 2026-08-20

**Superseded by the dataset revision above.** All 205,263,936 candidates checked in
this sweep used the pre-revision 34-panel list (panels 3, 5, 9, 11 [as Ace
Ventura], 13, 14, 16 [as 13th Warrior], 23, 24, 27 all since corrected). Kept below
for the historical record of what was actually run and when, not as a currently
applicable result to the corrected dataset.

Method: the user ran a local, resumable, multiprocess solver
(`analysis/bruteforce_solver.py`, `analysis/bruteforce_phase3_oneinoneout.py`,
`analysis/bruteforce_phase3_runall.py`) on their own machine, built and validated
in this session (self-test against `tools/oracle.py`, consistency check against
`oracle.check()`, dry runs, before any real sweep). Frozen inputs for this run,
none guessed beyond what was already backed by evidence: panel 16 = The 13th
Warrior (not changed to Les Visiteurs, per the unresolved visual comparison), H1
intruders = {1, 2, 10, 14, 16, 17, 20, 22, 25, 33}, the 24 keepers' candidate words
exactly as established earlier in this file and in `analysis/leads.md`, and
Raiders of the Lost Ark swept across the full, real 2048-word English BIP39 list
(no invented word) since it still has zero backed candidates.

Three phases run to completion, all on the same target address and the same
`tools/oracle.py` derivation paths (BIP84/49/44, 2 accounts x 3 indices, plus 3
raw paths), no shortcuts:

- **Phase 1**: 589,824 candidates (6 ambiguous keeper panels x Goonies'
  one/brand/chunk x Sharknado fixed at "april" x full Raiders sweep). 2,302
  checksum-valid. **0 matches.**
- **Phase 2A**: 1,179,648 candidates (same as phase 1, Sharknado also allows
  "tornado"). 4,589 checksum-valid. **0 matches.**
- **Phase 2B**: not run. Blocked by design: it would require Raiders to supply a
  fixed candidate list while Goonies took the 2048-word sweep, but Raiders still
  has none -- constructing this phase would mean inventing a word, which the user
  explicitly prohibited. Recorded as blocked, not silently skipped.
- **Phase 3 (one-in/one-out)**: every one of the 10 current H1 intruders swapped
  back in as a keeper, paired with every one of the 24 current keepers swapped out
  as the new intruder -- 240 possible pairs, 216 of them runnable (24 excluded
  because the incoming panel, The Shining, has no backed candidate word under the
  same whole-word/singular/substring hierarchy validated on the other 24 keepers:
  "shine" is not a literal substring of "shining"). All 216 runnable pairs run to
  completion: **203,494,464 candidates, 794,073 checksum-valid, 0 matches.**
  Cheapest pair: 288 candidates; most expensive: 2,949,120; total wall time
  1h45m17s at ~32,000 candidates/second (8 worker processes).

**Grand total across all three phases: 205,263,936 real candidates checked against
the live oracle, 0 matches.** `tools/oracle.py --selftest` passed before this work
began and the solver's own `check_candidate()` was verified to agree with
`oracle.check()` exactly (same function calls, not a reimplementation) before any
real sweep.

What this does and does not establish: this exhausts every word-cross combination
of the *currently backed* candidates under H1 exactly as stated, AND every single
one-panel swap of H1's own membership using only backed candidate words (not
guessed ones) for whichever panel gets swapped in. It does not test: two or more
simultaneous swaps to H1's membership; any word for Goonies, Sharknado, or Raiders
beyond what's listed above (Raiders' sweep was the full wordlist, so that panel
specifically is now exhausted for phase-1's other fixed assumptions, but not
combined with a different H1); a different order for the 24 words; a passphrase;
or a wrong identification among the 24 currently-"confirmed" keeper panels
(everything here assumed those 15 single-candidate answers and panel 34's
human/first pair are correct). Given the scale of this negative result, the most
likely remaining explanations are: (a) one of the 15 "settled" keeper words is
itself wrong, (b) the intruder criterion is not director/lead-actor repetition at
all (even with a single swap), or (c) a real, sourced word for Goonies, Sharknado,
or Raiders still doesn't exist among the options tried and needs actual new
evidence, not more search. Date: 2026-08-20.

## Panel 8 re-identification: The Goonies was wrong, real film is Shutter Island, 2026-08-19

Method: downloaded the actual still served at `bitcoinmovieenigma.com/blog/08`
(`https://bitcoinmovieenigma.com/user/pages/images/08_crop.png`) and looked at it
directly, rather than trusting the prior identification. The image shows 2 adult
men in matching tan trench coats and fedora/trilby hats, both holding black
umbrellas, standing at a white picket fence with a row of mailboxes, a dark 1970s-
80s American sedan, and a cargo ship on the water behind them. Nothing about this
(2 adult men in matching period coats, no children, no pirate-cove or treasure-map
elements) matches The Goonies. Ran this exact image through Bing Visual Search
(`bing.com/images/search` with `iss=sbiupload`, pasted image URL).

Result: Bing's own visual-match caption reads verbatim: "This still from the film
Shutter Island shows two men in trench coats and hats standing under umbrellas on a
rainy day near a waterfront." This matches the still exactly (matching coats, hats,
umbrellas, waterfront) and matches the film's real plot (2 US Marshals, played by
Leonardo DiCaprio and Mark Ruffalo, arrive by boat to a remote coastal
psychiatric-facility island in 1954). Re-identified panel 8 as **Shutter Island
(2010, dir. Martin Scorsese)**, confidence: confirmed. `data/films.csv` and
`analysis/intruder_repeat_check.py` updated accordingly.

Consequence for the word-gap problem: "Shutter Island" contains "island" as a
literal, whole-word BIP39 match (word 948 in the English list), the same
whole-word-preferred pattern as "orange," "wide," "glory," and "human" elsewhere in
this set. This removes The Goonies' guessed, unverified "chunk" from the candidate
space entirely and replaces it with a real, sourced word, cutting the number of
still-guessed gap panels from 3 to 2 (Sharknado, Raiders of the Lost Ark).

Consequence for the H1 intruder criterion (shares a director or lead actor with
another panel here): Shutter Island's director, Martin Scorsese, also directs panel
13 (Goodfellas). Re-running `analysis/intruder_repeat_check.py` with the corrected
panel 8 data flags **12** panels, not 10: the original 10 plus panels 8 and 13
(Scorsese pair). This is a real complication, not yet resolved: H1's own logic (a
director shared by exactly 2 panels here already counts McTiernan, Cruise, and
Gosling as valid 2-way triggers) gives no principled reason to exclude the Scorsese
pair, so H1 as previously stated no longer produces the required exact 24-versus-10
split against the corrected film list. Either H1 needs a different, non-arbitrary
refinement (for example, a repeat count threshold that would also have to exclude
McTiernan/Cruise/Gosling, which were part of H1's original supporting evidence), or
H1 is not the right criterion. This is now flagged as open, not silently patched.

Verified the other 3 lowest-confidence identifications the same way as a spot check
(downloaded the still, ran it through Bing Visual Search): panel 25 (Barry Lyndon)
and panel 26 (Sharknado) both returned a same-film match with a specific,
scene-accurate caption, so both stand confirmed as previously identified. Panel 27
(The Lost Boys, the single "uncertain"-confidence panel in the set) returned a weak,
generic, low-confidence guess ("Dredd") on a crop that is only a close-up of boots
on wet pavement at night with no faces or identifying detail, so this check was
inconclusive, neither confirming nor refuting the existing identification; not
changed. Date: 2026-08-19.

## Panel 11: reverse-image check attempted, inconclusive; no matching scene found in the film, 2026-08-19

Method: downloaded the actual panel 11 still (`bitcoinmovieenigma.com/user/pages/images/11_crop.png`, hands opening a "Bumble Bee White Tuna in Water" can among several more in sand) and ran it through Bing Visual Search, the same method that identified panel 8 as Shutter Island. Separately, searched for a documented scene in Ace Ventura: When Nature Calls (1995) matching physical tuna cans scattered in sand.

Result: the reverse-image search did not identify a specific film -- it only recognized the product ("Bumble Bee White Fish"), with no film association at all, because this crop has no faces or distinctive set design for the engine to match against. This neither confirms nor refutes either candidate. The scene search found that the film's actual opening is set at a Tibetan monastery, not a beach; the only documented "Bumblebee tuna" material in the film is a spoken catchphrase during an unrelated scene (emerging from a prop rhino), not a documented visual scene with cans in sand. No source describing a beach/sand/tuna-can scene in this film was found. Godzilla's independently-sourced beach-shipwreck scene (recorded in the entry below) remains the only identification with a documented match to the still's actual visual content. Reported to the user as an open evidentiary tension, not resolved by this check either way. Date: 2026-08-19.

## Panel 34: reverse-image check, weakly consistent with the existing identification, 2026-08-19

Method: same as above, applied to the panel 34 still, prompted by an external analysis (a ChatGPT session relayed by the user) that questioned whether Human Centipede or Dead Ringers was correct without having compared the actual frame.

Result: no specific-scene match returned, but "The Human Centipede" appears among the related-pages results and "Dead Ringers" does not appear at all. Weak, not a standalone confirmation, but consistent with (not contradicting) the existing sourced identification (the documented conjoined-twins-painting match to Dr. Heiter's house, `analysis/leads.md`, "Closed: panel #34 identification"). No change made. Date: 2026-08-19.

## Panel 8: reverted to The Goonies per user instruction, Shutter Island kept as a probability, 2026-08-19

The user reviewed the Shutter Island evidence (independent Bing Visual Search caption match) and the visual mismatch with The Goonies (2 adult men in trench coats/hats, no children, no pirate-cove or treasure-map content) presented in this session, and explicitly chose to keep The Goonies as the primary identification for panel 8, with Shutter Island retained as a secondary probability rather than discarded. No new evidence was presented for The Goonies beyond this direct instruction. `data/films.csv` reverted to `8,The Goonies,PG,probable,none`; `analysis/intruder_repeat_check.py` reverted to Richard Donner / Sean Astin for panel 8.

Consequence: re-running `analysis/intruder_repeat_check.py` with panel 8 back to The Goonies removes the Scorsese-pair complication entirely (Donner and Astin repeat nowhere else in the set), so H1 flags exactly the original 10 panels again: {1, 2, 10, 14, 16, 17, 20, 22, 25, 33}. This complication was specific to the Shutter Island hypothesis for panel 8 and does not apply while Goonies is the primary identification. Both words ("chunk" for Goonies, "island" for Shutter Island) were carried forward into the candidate-crossing run below rather than discarded, per "keep Shutter Island as a probability." Date: 2026-08-19.

## Panel 11 correction: Godzilla was wrong, real film is Ace Ventura: When Nature Calls, 2026-08-19

Method: the user, working from their own direct viewing of the still (not a search
or a plausibility read), stated that panel 11 is Ace Ventura: When Nature Calls
(1995), not Godzilla (1998), and that the Godzilla identification came from an
earlier, separate session's mistake. This is the same evidentiary category already
used to close panels 11 (previously) and 34 in this file: "a human researcher who
had watched [the] film[s] recognized" the panel. Before accepting it, I re-checked
the Godzilla identification's own supporting evidence and searched independently
for a matching scene in Ace Ventura: When Nature Calls.

What I found does not corroborate the swap on its own: an independent, unprompted
plot description of Godzilla (1998) describes Matthew Broderick's character
reaching a beach shipwreck in Panama that includes Bumblebee Tuna cans, which
matches the still (hands opening a "Bumble Bee White Tuna in Water" can among
several more in sand) at the level of a specific, documented scene. The only
Bumblebee-tuna-adjacent material I could find for Ace Ventura: When Nature Calls is
the character's own catchphrase line ("Bumblebee tuna!"), spoken while emerging
from a prop rhino -- a spoken joke, not a documented visual scene of tuna cans in
sand. I flagged this discrepancy to the user directly before making any change.

The user confirmed explicitly that their identification is a first-hand visual
comparison of the actual still against the actual film, not a word-association
guess from the "Bumblebee tuna" line, and asked for the correction to stand.
Applying this repository's own established standard for this exact class of
identification (a human who has watched the film recognizing the still, the same
method used to originally close panels 11 and 34), the correction is accepted:
**panel 11 is Ace Ventura: When Nature Calls (1995), dir. Steve Oedekerk, starring
Jim Carrey.** `data/films.csv` and `analysis/intruder_repeat_check.py` updated
accordingly.

This is recorded transparently as a first-hand identification that stands in
tension with an independent written source for the alternative it replaces, not as
an independent-source confirmation of its own (unlike the Shutter Island and Human
Centipede resolutions above, no third-party text describing this specific scene in
Ace Ventura: When Nature Calls was found in this session). If a documented source
describing a matching scene turns up later, record it here.

Recomputed from scratch, not reused from any prior candidate space:

1. **Literal BIP39 candidates for the corrected title**, checked against the full
   2048-word list, both per-title-word and across the squashed title (crossing
   word boundaries): "when" (whole word), "nature" (whole word), "call" (via the
   same plural-strip rule already used elsewhere in this set, e.g. boy/boys,
   river/rivers, applied to "calls"). 2 weaker, boundary-crossing-only substrings
   also exist ("hen" inside "when," "all" inside "calls") but are dominated by the
   whole-word matches already found, so they are not added to `data/films.csv`
   consistent with how this file has always ranked whole-word matches above
   partial substrings elsewhere in the set (see "Title-to-word rule: base rate
   measurement" above). "ace" and "ventura" have zero BIP39 substring matches.
   Result: panel 11 has 3 literal candidates, none guessed -- it moves from a
   single-fixed-word keeper to an ambiguous keeper, the same status as Star Trek:
   The Motion Picture, Valerian, Ordinary People, and Toy Story.
2. **H1 (director/lead-actor repeat) check for the corrected panel**: director
   Steve Oedekerk and lead actor Jim Carrey were checked against the director and
   lead-actor tables for all other 33 panels (`analysis/intruder_repeat_check.py`).
   Neither repeats anywhere else in the set. Result: panel 11 is NOT flagged by H1
   under the corrected data, exactly as it was not flagged under the (wrong)
   Godzilla data either -- Roland Emmerich and Matthew Broderick also did not
   repeat elsewhere. The keeper/intruder split itself (still {1, 2, 8, 10, 13, 14,
   16, 17, 20, 22, 25, 33} flagged, 12 of 34, under the Scorsese-complicated H1
   from the Shutter Island correction above) is unaffected by the panel 11
   correction: re-running `analysis/intruder_repeat_check.py` with both
   corrections applied together confirms the same 12 flagged panels and the same
   22 keepers, panel 11 among them either way.
3. **Does Godzilla appear anywhere else in the puzzle?** Checked: no. Godzilla
   (1998), Roland Emmerich, and Matthew Broderick do not appear anywhere else in
   `data/films.csv`, `analysis/intruder_repeat_check.py`, or any candidate word
   list for any other panel. Removing it breaks nothing else in the dataset by
   cross-reference; it was a leaf value used only at panel 11.
4. **Derived counts, recomputed**: the number of keeper panels with zero literal
   BIP39 candidate (the "gap panels" needing a guess, not just a choice) is
   unchanged at 2 (Sharknado, Raiders of the Lost Ark) -- panel 11 was never a gap
   panel under either identity, since both "ill" (Godzilla) and "when"/"nature"/
   "call" (Ace Ventura) are real literal candidates. The ambiguous-panel count
   rises from 5 to 6 (Star Trek, Valerian, Ordinary People, Toy Story, Human
   Centipede, and now Ace Ventura). The full candidate-space size (still-open
   choices only, gap panels' guesses included) rises from 792 to 2,376: 6
   ambiguous panels' product (2 x 3 x 2 x 2 x 3 x 3 = 216) times Raiders' 11 guessed
   options times Sharknado's 1 guessed option. Verified by direct enumeration,
   `analysis/build_candidates.py` (no `--run`, so nothing was checked against the
   escrow): "panels (keepers): 24" / "total candidates: 2376". Date: 2026-08-19.

**What this invalidates and what it does not**, stated explicitly per the user's
request:

- INVALIDATED: every one of the 792 candidate mnemonics checked against the escrow
  in both the original 2026-08-19 sweep and the Shutter-Island-corrected re-run
  above. All 792 used "ill" fixed at panel 11's position, which no longer applies
  once panel 11 is Ace Ventura, not Godzilla. The "0 matches" result from both
  sweeps says nothing about whether "when," "nature," or "call" is the right word
  for this panel -- that combination was never tested.
- INVALIDATED: the earlier claim that Godzilla (1998) is panel 11, and by
  extension the "Closed: panel #11 identification" entry in `analysis/leads.md` as
  a final answer (kept below for the record, not deleted, per this repository's
  practice of not erasing superseded findings).
- NOT INVALIDATED: the H1 director/lead-actor intruder criterion's specific
  flagged set ({1, 2, 8, 10, 13, 14, 16, 17, 20, 22, 25, 33}, 12 of 34) -- panel 11
  does not participate in any repeat under either identity, so this correction
  changes nothing about which panels H1 flags or about the still-open Scorsese-pair
  complication from the Shutter Island correction (that complication is
  independent of this one).
- NOT INVALIDATED: panel 8 (Shutter Island) and panel 34 (The Human Centipede
  (First Sequence)) identifications, the 2-gap-panel count (Sharknado, Raiders of
  the Lost Ark), and the general title-to-word and IMDb-field methodology
  described elsewhere in this file.
- STILL OPEN, UNCHANGED BY THIS CORRECTION: which of "when," "nature," or "call" is
  the intended word for panel 11 (an ambiguity, not a gap -- the same kind of
  open choice as the other 5 ambiguous panels); real words for the 2 true gap
  panels; and the Scorsese-pair complication in H1.

No brute-force run was performed as part of this correction, per instruction: the
2,376-candidate space above is reported as a count only, not tested against the
escrow. Date: 2026-08-19.

## 792-candidate sweep, re-run with the verified Shutter Island word, 2026-08-19

Note, added after the panel 11 correction above: this sweep (and the original
792-candidate sweep before it) is now superseded/invalidated for the reason stated
in the panel 11 correction entry -- both used "ill" (Godzilla) fixed at panel 11's
position, which is no longer valid. Kept below for the historical record of what
was actually run and when, not as a currently-valid result.

Method: `analysis/build_candidates.py --run`, same 24-keeper structure as the
2026-08-19 sweep above, with The Goonies' guessed "chunk" replaced by Shutter
Island's verified "island" (same slot, still a single fixed word, so the total
stays 792).

Result: 0 matches. Expected, not a new negative: the 2 remaining gap panels
(Sharknado, Raiders of the Lost Ark) are still guesses in this candidate set, so
this does not test whether the rest of the 24-word set is right. What it does
establish: the "island" substitution itself introduces no error, and the earlier
792-candidate negative result was not being caused by the "chunk" guess specifically
(a real word in that slot still gives 0 matches), which narrows the blame further
onto the 2 remaining gap panels, the 5 still-ambiguous panels, or the intruder
criterion itself (see the H1 complication above). Date: 2026-08-19.

## 4,752-candidate cross-sweep, panel 8 reverted to Goonies (with Shutter Island kept as a probability) and panel 11 corrected to Ace Ventura, 2026-08-19

Method: `analysis/build_candidates.py --run`, rebuilt candidate space (not reused
from any prior sweep) reflecting both dataset changes made this session: panel 8
back to The Goonies as primary with Shutter Island kept as a live alternative (both
words, "chunk" and "island", included as options for that panel's slot rather than
picking one), and panel 11 as Ace Ventura: When Nature Calls (3 literal candidates,
"when"/"nature"/"call"). Intruder split re-confirmed clean at exactly the original
10 panels ({1, 2, 10, 14, 16, 17, 20, 22, 25, 33}) once panel 8 reverted to Goonies
-- the Scorsese-pair complication was specific to the Shutter Island hypothesis for
panel 8 and does not apply here. 7 ambiguous panels (panel 8: 2 options, panel 11: 3
options, Star Trek: 2, Valerian: 3, Ordinary People: 2, Toy Story: 2, Human
Centipede: 3) times Raiders' 11 guessed options times Sharknado's 1 guessed option
= 2 x 3 x 2 x 3 x 2 x 2 x 3 x 11 x 1 = **4,752 candidates**, confirmed by direct
enumeration before running (`--preview`).

Result: **0 matches.** `tools/oracle.py --selftest` passed both before assembling
this space (via `analysis/intruder_repeat_check.py`'s own run) and immediately
after this sweep, confirming the oracle was not silently broken. This covers, for
the first time in one run, both live hypotheses for panel 8 (Goonies and Shutter
Island) crossed against every other still-open choice, including the corrected
panel 11. It does not test: any word for panel 8 or panel 11 other than the ones
listed (for example, "hen" or "all," the weaker boundary-crossing substrings noted
for panel 11 but not promoted to candidates); any Raiders or Sharknado word outside
the existing guessed lists; or any intruder split other than the original 10. Per
instruction, this negative result is reported as a candidate space cleared, not as
disproof of any single hypothesis inside it -- with 2 genuinely gap panels
(Sharknado, Raiders) still guessed inside this space, a wrong guess there remains
the most parsimonious explanation for 0 matches, same as every sweep before this
one. Date: 2026-08-19.

## 7,344-candidate cross, Raiders' guess list expanded per user suggestion, 2026-08-19

Method: the user proposed 6 additional candidate words for Raiders of the Lost Ark
(soft, rail, raise, risk, other, rather), relayed from an external analysis. Before
adding them, checked each against the full 2048-word BIP39 list and against the
squashed title "raidersofthelostark" (crossing word boundaries, the same check used
throughout this file): only **"soft"** is an actual substring, and even that only
by splicing across "raider**s**-**of**-**t**helostark" (the 's' ending "raiders",
then "of," then the 't' beginning "the"), the same kind of boundary-crossing
coincidence already flagged and excluded for "bar" in Barry Lyndon earlier in this
file. **"rail," "raise," "risk," "other," and "rather" do not appear anywhere in
the title, under any splicing** -- verified by exhaustive substring scan, not
found by eye. These 5 have no textual connection to the title at all, weaker even
than the original 11 theme/prop-word guesses (whip, snake, gold, etc., which are at
least drawn from the film's actual content). Flagged to the user as such before
proceeding.

Included anyway per instruction: a MATCH against the escrow would be its own proof
regardless of how the word was found, so excluding ungrounded candidates from a
cheap, bounded search would be overly conservative. Raiders' candidate list grew
from 11 to 17 (union of the original 11 + "soft" + the 5 new words, no
overlaps); `analysis/build_candidates.py` updated accordingly. New total: 7,344
candidates (same 7 ambiguous panels, product 432, times 17 Raiders options, times 1
Sharknado option), confirmed by direct enumeration before running.

Result: **0 matches.** `tools/oracle.py --selftest` passed immediately after this
run. Same caveat as every sweep in this file: this clears the space, it does not
individually clear "soft" or any of the 5 ungrounded words, and the 2 gap panels
remain the most likely source of the negative result -- though this run has now
tested every candidate word for Raiders that has been proposed by any source in
this investigation, real or speculative, with none producing a match. Date:
2026-08-19.

## IMDb field audit spreadsheet filled for all 34 panels, 2026-08-20

Method: per `analysis/HANDOFF_2026-08-20.md`, the systematic single-field IMDb
audit (started by the user to find a replacement intruder criterion after H1 was
falsified against the revised dataset -- see "Major dataset revision" above) needed
its yellow cells filled from real IMDb pages. I did this directly: resolved each of
the 34 films' current IMDb tt-IDs via web search, then pulled each film's IMDb
`/reference/` (genres, full credited stars, MPAA-equivalent rating), main title
page (Details/Box office/Tech-specs block: countries, languages, exact release
date, runtime, AKA titles, filming locations, production companies, budget, gross,
top cast, writers, awards), `/technical/` (sound mix, aspect ratio, color, when not
already on the main page), and `/keywords/` (top 5-6 Plot Details keywords, page
order) pages, using an interactive browser (not WebFetch -- IMDb returns HTTP 403
to it) with an `en_US`/`international-seo=us` cookie forced, since the default
session geo-localized to Mexico (Spanish UI, MX-specific release dates/ratings).
Cross-checked film identity via director/lead-actor already in the template plus
year, since several titles are ambiguous without it (Alien vs Aliens, Godzilla 1998
vs 2014, Solaris 1972 vs 2002, Spartacus 1960 film vs miniseries).

All 20 previously-empty columns (H through AB: extra cast, countries, languages,
exact release date, runtime, genres, color, aspect ratio, sound mix, budget, gross,
production companies, distributor, awards, AKA, filming locations, keywords,
sequel/franchise status, writers, notes) are now filled for all 34 rows, verified
programmatically (no empty cells H:AB across rows 4-37). This is raw data
collection, not analysis -- **no intruder criterion has been tested against it
yet**; that is the next step per the handoff, and per house rules no criterion
should be accepted without being defined first, giving exactly 10, and needing no
manual exceptions.

Notable things surfaced while pulling the data, flagged for whoever does the field
analysis next:
- **Panel 9 (Spartacus) certificate discrepancy**: `data/films.csv` and the
  spreadsheet's pre-filled green cell record "APPROVED", but IMDb's main page
  currently shows the certificate as **PG-13**. Not yet reconciled -- IMDb
  certificates can be re-rated/re-classified over time; needs a decision on which
  value to treat as authoritative before this field is used in any criterion test.
- **Panel 21 (Solaris)**: the template's pre-filled director cell already flagged
  "CONFIRM WHICH" (1972 Tarkovsky vs 2002 Soderbergh remake, same English word
  candidate "solar" either way). Filled this row as the **1972 Tarkovsky version**
  (tt0069293), matching the template's existing Year=1972 cell, and noted in the row
  that the 2002 remake is a separate IMDb title (tt0307479) in case the panel image
  is later confirmed to actually be the Clooney version instead.
- Several films' US theatrical release date on IMDb is a delayed US release, not
  the film's original home-country premiere (Mad Max: Australia 1979 vs IMDb's
  listed US 1980; The Crimson Rivers: France 2000 vs US 2001; The Visitors: France
  1993 vs US 1996, 3 years later after a rejected Mel Brooks English dub). Relevant
  if "exact release date" ends up being tested as a criterion field, since "the"
  release date is ambiguous for co-productions/imports.
- Sharknado (panel 26) is a **TV Movie**, not a theatrical release -- it has no
  MPAA rating (IMDb: "Not Rated"; films.csv records the actual US TV content rating
  "TV-14", a different rating system) and no theatrical box-office figures.
- Several older films' IMDb "Genres" pills (from `/reference/`) differ substantially
  from the newer "Related interests" tag cloud shown on the main page (e.g. Die
  Hard: reference-page genres "Action, Thriller" vs main-page interests "Dark
  Comedy, Disaster, One-Person Army Action, Action, Holiday, Thriller"). Recorded
  the reference-page 2-3-word genre list as the "Generos" column and the interest
  tags in "Notas", since it's unclear which one the puzzle means by "genres" --
  worth testing both if a genre-based criterion is attempted.
- Distributor was not always explicitly listed as a separate field from production
  companies on the main page; several rows note "no confirmado" and give a
  best-guess historical distributor instead of asserting one from memory.

Not done in this pass, left for the user or a follow-up session: actually testing
each single field against the 34-panel list for one that flags exactly 10 with no
exceptions (the stated next step in the handoff).

## Systematic single-field sweep against the newly-filled audit data, 2026-08-20

Method: loaded all 34 filled rows from `analysis/imdb_field_audit.xlsx` and tested
every natural binary/grouping split of every filled column against the "exactly 10,
no manual exceptions" bar, same discipline as the H1 search. Tested: country count
(single vs co-production: 20 vs 14), country = "United States" only (15 vs 19),
each individual country's film count (UK appears in 9, France in 4, etc.), language
count (single vs multi: 16 vs 18), certificate groups (R=14, PG=8, PG-13=8,
Approved=2, other=2), color (B&W-involved=3), runtime (no round-number threshold
lands on 10 in either direction), budget (no round threshold lands on 10), genre
count per film (2 genres=9, 3 genres=22, other=3), each individual genre word's
frequency (max Adventure=15, Action=14, Drama=14, ... none=10), first-listed genre
(Action=14, Adventure=6, Drama=5, ...), distributor grouped by studio (Warner
Bros.=6, Fox=4, Paramount=3, ...), production company count per film (1=4, 2=11,
3=19), writer-credit-block count (1=9, 2=17, 3=5, 4=2, 5=1), "based on a
novel/book" per writer field (16 adaptations vs 18 original screenplays, though
this one has false positives from "based on characters/comic" phrasing and needs
re-checking by hand before trusting the count), won-an-Oscar specifically (13),
nominated-for-an-Oscar (18), sequel/reboot/franchise-entry status as recorded in
the template (9: Aliens, Godzilla, Blade Runner 2049, Guardians of the Galaxy,
Terminator 2, Scream 2, The Matrix Reloaded, Ghostbusters II, The Human Centipede
-- note Guardians' "yes" here is a judgment call, since it's an original
screenplay that's merely part of a shared universe, not a literal sequel; dropping
it would make this 8), aspect-ratio family (2.39:1=18, 1.85:1=5, 2.35:1=4, ...),
distributor-unconfirmed-by-me count (5).

Result: **no single field, defined and read naturally, produces exactly 10** across
everything tested so far. Closest near-misses, none exact: sequel/franchise status
(9, and ambiguous for at least one panel), single-writer-credit (9), 2-genre films
(9), UK country involvement (9), won-an-Oscar (13).

Known gaps in the sweep, not yet closed:
- Star Wars: A New Hope's `/keywords/` page was never fetched (only its
  `/reference/` and main-page "Related interests" were used for genre/notes), so
  its IMDb Franchise-keyword-category status and full Plot Details keyword list are
  unverified relative to the other 33 panels.
- Only the top 5-6 keywords per film were recorded, not the full keyword list or
  each film's Subgenres/Franchise IMDb keyword categories as a whole -- a
  keyword-category-based criterion (e.g. "IMDb tags this with a Franchise
  keyword") could not be fully tested from the recorded data; from what was
  observed in passing while collecting keywords, Aliens, Alien, Mission:
  Impossible, Godzilla, Raiders, Terminator 2, Scream 2, The Matrix Reloaded, Toy
  Story, Guardians of the Galaxy, and Blade Runner 2049 all showed a "Franchise
  (1)" category on their keyword pages (11 films, Star Wars unchecked) -- close to
  10 but unconfirmed and likely 11 or 12, not exact.
- Numeric fields (budget, gross, runtime) were only checked for round-number
  thresholds; an exhaustive "does *some* cutpoint produce exactly 10" scan (any of
  the 34 sorted values as a boundary) was not run, since without a principled
  reason to pick one specific cutpoint over the adjacent ones this reduces to
  overfitting -- flagging as future work only if a natural boundary is proposed
  first (e.g. "$50M+", "over 2.5 hours"), not by search.

This clears the fields and splits actually tested; it does not prove no
single-field criterion exists (untested: exact keyword-category counts per film,
combinations of two weak fields, and any field not present in the template at
all). Date: 2026-08-20.

## Gaps closed: Star Wars keywords + IMDb "Franchise" keyword-category count, 2026-08-20

Context: the user restructured `imdb_field_audit.xlsx` themselves after the initial
fill -- removed the legend row and the "EJEMPLO" Die Hard row (35 rows now: 1
header + 34 data, was 37), and added a real source URL to every row's confidence
column (upgrading all 34 from "probable"/bare "confirmed" to "confirmed <url>").
**Also corrected panel 30's title from "Toy Story" to "Toy Story 2"** -- the H:AB
data I had filled for that row was still the 1995 film's; re-pulled and replaced
with the actual Toy Story 2 (1999, tt0120363) data (director team Lasseter/
Brannon/Unkrich, Nov 24 1999, 92 min, $90M budget, $497M worldwide, etc.).

While re-checking whether this changed the sequel/reboot/spin-off count from the
prior sweep (9), caught and fixed two of my own miscodings that had been
inconsistent with the field's actual question ("is this film itself a sequel/
reboot/spin-off", not "did it spawn sequels"): The Human Centipede (First
Sequence) and Guardians of the Galaxy were both wrongly marked "Si" (Human
Centipede is the *original* film in its trilogy; Guardians is an original
screenplay merely set in the shared MCU, not a sequel/reboot of anything). Both
corrected to "No" with an explanation in the cell. **Recomputed strict
sequel/reboot/spin-off count with Toy Story 2 included and the two errors
removed: 8** (Aliens, Godzilla, Blade Runner 2049, Terminator 2, Scream 2, The
Matrix Reloaded, Toy Story 2, Ghostbusters II) -- not 9, and not 10. Re-ran every
other field split from the prior sweep against the corrected data too (country,
language, genre count, certificate, Oscar wins, writer-block count, UK
co-production); none of them depend on the Toy Story identity or the sequel-flag
column, so none of their counts changed.

Then closed the two gaps flagged at the end of the prior sweep entry:

1. **Star Wars: A New Hope's `/keywords/` page**, never fetched before, now
   pulled. It does carry a "Franchise (1)" keyword category ("star wars"). Real
   top-5 Plot Details keywords by the page's relevance order: rebellion, princess,
   space opera, good versus evil, jedi -- replacing the placeholder "not captured"
   text that was in the template's Keywords/Notas cells for this row.

2. **Full "Franchise" keyword-category check across all 34 panels**, re-verified
   one by one directly from each film's live `/keywords/` "Jump to" summary line
   (not from memory this time). Films whose keyword page carries a Franchise
   category: **Aliens, Alien, Mission: Impossible, Godzilla, Star Wars: A New
   Hope, Blade Runner 2049, Guardians of the Galaxy, Terminator 2: Judgment Day,
   Scream 2, The Matrix Reloaded, Toy Story 2, Raiders of the Lost Ark = 12
   films, not 10.** Notably Ghostbusters II -- a numbered direct sequel -- does
   *not* carry a Franchise keyword category on IMDb, confirming this is an
   IMDb-editorial-curation quirk and not a reliable proxy for "is a sequel."

Result: **both gaps are now closed with verified (not recalled) data, and neither
resolves to exactly 10.** The corrected sequel/reboot/spin-off field (8) and the
verified Franchise-keyword-category field (12) both join the earlier near-misses
as clean negatives, not hits. No single IMDb field tested across this session (see
prior sweep entry for the full list) produces exactly 10 with a natural reading
and no manual exceptions. Untested still: combinations of two fields, and any
field not represented in the current template. Date: 2026-08-20.

## Pairwise two-field combination sweep, 2026-08-20

Method: built 24 natural single-field boolean criteria from the filled audit data
(is-sequel/reboot, won-an-Oscar, nominated-for-Oscar, single-writer-credit-block,
exactly-2-genres, exactly-3-genres, UK-co-production, single-country,
single-language, certificate=R/PG-13/PG, involves-black-and-white,
first-genre=Action, genre-contains-Sci-Fi/Thriller/Horror, distributor=Warner
Bros., aspect-ratio=2.39:1, runtime>140min, runtime<100min, budget>=$100M,
budget<$10M, >=3 production companies, has-IMDb-Franchise-keyword-category), then
computed AND and OR for every pair (300 pairs x 2 = 600 tests) looking for exactly
10.

Result: **17 of the 600 combinations land on exactly 10.** Flagged to the user as
almost certainly multiple-comparisons noise (with 600 near-independent trials over
34 items, several coincidental exact-10 hits are expected by chance alone, the
same caveat this file has applied to checksum-valid mnemonics throughout). Full
list of the 17 hits is in the chat transcript, not reproduced here since none of
them were treated as validated. Only one had a genuinely single-concept natural
reading rather than an arbitrary AND/OR of two unrelated facts: **single country
of origin AND single language** (i.e. "a purely domestic, monolingual
production," as opposed to an international co-production or multi-language
film) -- gives exactly these 10: Close Encounters of the Third Kind, Escape from
Alcatraz, Ghostbusters II, Mad Max, Scream 2, Sharknado, Spartacus, Star Wars: A
New Hope, The Crimson Rivers, Toy Story 2.

## First end-to-end derivation attempt against the country+language-split hypothesis, 2026-08-20

Per house rule, a split landing on 10 is not evidence by itself -- only a derived
address match is. Built the full 24-word candidate space for the "single country +
single language" intruder set above (panels 4, 7, 9, 15, 18, 24, 26, 28, 30, 31
dropped; the other 24 kept, in panel order) and ran it through `tools/oracle.py`'s
`check()` function directly (imported in-process, not via subprocess, for speed).

Word candidates used per keeper panel:
- 15 panels have exactly one literal-substring candidate from `data/films.csv`
  (unchanged): hard, alien (x2, panels 3 and 5), now, ill, life, visit, gravity,
  solar, blade, galaxy, bar, day, matrix.
- 6 panels have multiple tied literal candidates, all included: Paths of Glory
  (glory/path), Mission: Impossible (miss/possible), The Man in the Iron Mask
  (man/iron/mask), A Clockwork Orange (clock/orange/range/work), First Man
  (first/man), The Human Centipede (human/first/man).
- 3 panels have **zero literal candidate** and needed non-literal, sourced
  guesses to be testable at all: The Goonies (one/brand/chunk -- character names,
  carried over from pre-revision research, see "leads.md" history above), Léon:
  The Professional (milk -- Léon's iconic milk-drinking habit, sourced from an
  IMDb user review already fetched during the field-audit pass, not asserted from
  memory alone), The Shining (hotel/maze -- both literal IMDb keywords already
  recorded for this panel: "haunted hotel", "hedge maze"). Raiders of the Lost
  Ark (whip/snake/gold/hat -- iconic props/scenes, carried over from pre-revision
  leads.md research, previously tested only against the old H1 intruder set, not
  this one). **These 4 panels' words are guesses, explicitly weaker than the
  literal-substring candidates, and not independently re-verified beyond what is
  noted above -- flagged as such, not asserted as fact.**

Total candidate space: 2 x 2 x 3 x 4 x 2 x 3 (six tied panels) x 3 (Goonies) x 1
(Leon) x 4 (Raiders) x 2 (Shining) = 6,912 candidates, generated by direct
product and checked in-process (0.6s total, ~11,400/s).

Result: **0 matches.** `tools/oracle.py --selftest` passed before this run. This
clears the specific 6,912-candidate space tested; it does **not** disprove the
country+language-split hypothesis itself, since 3 of the 24 keeper panels
(Goonies, Leon, Raiders, Shining minus Shining has 2 tried) had no literal word at
all and were filled with guesses that may simply be wrong. A negative result here
is much weaker evidence against the hypothesis than the earlier H1 sweeps were
against H1, precisely because of this gap -- unlike H1's exhaustive coverage, this
run leaves real word-choice uncertainty unresolved for those 3-4 panels. Date:
2026-08-20.

## Widened non-literal candidate lists for the 4 zero-literal-word panels, re-run, 2026-08-20

Method: rather than free-associating from memory, cross-referenced the *actual*
IMDb `/keywords/` lists already fetched and recorded during the field-audit pass
for the 4 zero-literal-candidate keeper panels (Goonies, Leon, Raiders, Shining)
against the real 2048-word BIP39 list, keeping only words that are both (a) BIP39
words and (b) a genuine keyword/plot element IMDb itself lists for that film (not
just superficially plausible). This is the same discipline used for "chunk"
(Goonies) earlier, extended to the other 3 panels and widened for Goonies/Raiders
too. Result, replacing the single-guess lists from the previous entry:

- **The Goonies**: one, brand, chunk (character names, from pre-revision
  research) + gold, cave, beach, rescue (all literal IMDb Plot Details keywords
  for this panel) = 7 candidates, up from 3.
- **Leon: The Professional**: milk (from IMDb review text) + gun (from the IMDb
  keyword "child with a gun") = 2 candidates, up from 1.
- **Raiders of the Lost Ark**: whip, snake, gold, hat (pre-revision leads.md) +
  horse, ship, knife (all literal IMDb Plot Details keywords) = 7 candidates, up
  from 4.
- **The Shining**: hotel, maze (IMDb keywords "haunted hotel", "hedge maze") +
  snow, ghost, mirror, blood (all also literal IMDb Plot Details keywords for
  this panel) = 6 candidates, up from 2.

Words considered but rejected as not in the real BIP39 list despite being
genuine keywords: map, attic, skeleton, dungeon, outlaw, waterfall (Goonies);
plant, apartment, grenade, eyeglass(es) (Leon); ark, nazi (Raiders); labyrinth,
tricycle, typewriter, axe, elevator (Shining).

New total candidate space: same 288-way product across the 6 tied-literal panels
x 7 (Goonies) x 2 (Leon) x 7 (Raiders) x 6 (Shining) = **169,344 candidates**,
checked in-process against `tools/oracle.py`'s `check()` in 15.3s (~11,100/s).

Result: **0 matches**, `--selftest` passed beforehand. This is a substantially
more thorough negative than the previous 6,912-candidate run (24.5x the coverage
on the 4 previously weakest panels, still grounded entirely in either literal
substrings or IMDb's own listed keywords/reviews, no free-associated guesses).
Still does not prove the country+language-split hypothesis wrong -- the true word
for any of these 4 panels could be something IMDb's top keywords don't surface,
or a character name not covered here, or the hypothesis itself could simply be
wrong -- but it meaningfully narrows the space where it could still be hiding.
Date: 2026-08-20.

## Full 38.9M-candidate run, also widening the 6 tied-literal-substring panels, 2026-08-20

Method: extended the same non-invented, keyword-sourced discipline to the 6
panels that already had multiple *tied literal* BIP39 substrings (kept those,
added more IMDb-keyword-grounded non-literal words on top, same filter as
before: must be both a real BIP39 word and an actual IMDb-listed keyword/plot
element for that specific film): Paths of Glory (+ soldier, battle, general,
pistol), Mission: Impossible (+ train, spy, gadget, escape, bomb, magic,
subway), The Man in the Iron Mask (+ twin, guard, river, horse), A Clockwork
Orange (+ chair -- most candidate keywords for this one, e.g. gang/thug/
robbery/suicide/violence, are not actual BIP39 words), First Man (+ moon,
rocket, marriage), The Human Centipede (+ doctor, mask, illness, cabin). Full
per-panel candidate lists and the words checked-and-rejected as non-BIP39 are in
`analysis/bruteforce_country_lang_split_mp.py`.

New total: 38,896,200 candidates (verified by direct `itertools.product` count
match and by two independent spot-checks of the script's mixed-radix
index-to-combination arithmetic before running, both exact). Given the size, this
run was handed to the user to execute locally with a multiprocess version of the
same `oracle.check()` logic (`analysis/bruteforce_country_lang_split_mp.py`,
12 workers, 200k-candidate chunks) rather than run single-process in this
session. `--selftest` passed at the start of their run.

**Result reported by the user: 0 matches across the full 38,896,200-candidate
space**, at ~46,000/candidates-sec sustained across 12 cores (~14 minutes total).
This is the most thorough test yet of the country+language-split hypothesis --
every literal substring candidate for every keeper panel, plus every
IMDb-keyword-grounded non-literal candidate found so far for the 6 tied and 4
zero-literal panels, crossed exhaustively. Still not a disproof of the hypothesis
itself (a word IMDb's own keyword lists don't surface, for any of these 10
under-determined panels, would not have been covered), but the space of "the
right word was somewhere fairly obvious in IMDb's keyword list" is now
exhausted for this specific intruder set.

Operational note: the user's machine had what sounded like a serious freeze/hard
reboot partway through this run (unresponsive to input, stuck cursor) while also
on a video call -- 12 processes at full CPU for ~14 minutes concurrent with video
call load is a plausible thermal/stability trigger on laptop hardware. Worth
reserving 1-2 cores headroom (`--workers <cpu_count-2>`) for any future run of
this kind, especially if the machine will be used for anything else at the same
time. Date: 2026-08-20.

## Full IMDb keyword lists (not just top 5-6) for the 5 zero-literal-word panels, 2026-08-20

Method: the field-audit spreadsheet only recorded each panel's top 5-6 IMDb
keywords by relevance. For the 5 panels with zero literal title-substring
(Goonies, Leon, Sharknado, Raiders, Shining), fetched each film's full
`/keywords/` page in the browser (cookies set for `en_US` locale first, per the
operational note above), expanded all "N more" / "See all" sections via a JS
click on the actual DOM buttons (not just scrolling), and extracted every
keyword tag via `document.querySelectorAll('a[href*="/search/title/?keywords="]')`.
This is IMDb's own full keyword corpus for each film, not a partial or
by-relevance-truncated sample. Kept only keyword tags that are themselves a
single word matching the real BIP39 English wordlist exactly (not a fragment of
a multi-word tag like "one" from "one night timespan" -- that would be noise;
the tag itself has to be the BIP39 word), same "genuine listed keyword, not
free-associated" discipline as the earlier keyword pass. Full keyword lists
saved to the session scratchpad, not committed to the repo (large, purely
intermediate).

Results (chase panel counts: Goonies 343 keyword tags total, Leon 318,
Sharknado 119, Raiders 328, Shining 415 -- Shining's total includes a large
generic "content advisory" tag cluster, e.g. "brutal", "shocking", "morbid",
"viewer discretion is advised", that reads as auto-generated severity tagging
rather than plot-specific keywords; flagged separately below, not treated as
equally strong as plot/prop/setting words):

- **The Goonies** (was: one, brand, chunk, gold, cave, beach, rescue -- 7):
  +32 new: gadget, legend, chase, sword, coin, toilet, bicycle, tunnel, jewel,
  pizza, fire, sheriff, forest, skull, piano, child, trap, ship, pistol, arrest,
  organ, asthma, book, knife, escape, marble, camera, kiss, thunder, rain,
  wish, police, hidden, danger, humor. **39 total now.**
- **Leon: The Professional** (was: milk, gun -- 2; "gun" itself is not a
  standalone tag on this page, only inside multi-word tags like "child with a
  gun", kept from the earlier review-text/keyword-phrase pass): +9 new: girl,
  police, elevator, crush, hotel, love, pistol, knife, weapon, shield. **11
  total now** (10 standalone-tag + milk from review text).
- **Sharknado** (was: tornado only, non-literal portmanteau -- 1; **"tornado"
  is also a genuine standalone IMDb keyword tag for this film**, upgrading it
  from portmanteau-inference to directly-sourced): +9 new: fish, dog, beach,
  gun, pistol, animal, vehicle, car, child. **10 total now**, the biggest
  relative gain of the 5 panels (this panel is a TV movie with a much shorter
  page, so the earlier top-5-6 pass barely scratched it).
- **Raiders of the Lost Ark** (was: whip, snake, gold, hat, horse, ship, knife
  -- 7, from a pre-revision props/scenes list, not this keyword page -- "gold"
  specifically is not a keyword tag on the current page, kept as-is from that
  older source): +35 new from the keyword page: truck, chase, jungle, torch,
  mirror, canyon, desert, fire, bar, love, ritual, lecture, dress, tent,
  island, wine, blood, warrior, escape, kiss, pistol, sword, rescue, spider,
  basket, soldier, spirit, alcohol, car, hero, magic, weapon, mechanic, faith,
  fiction. **42 total now**, the single largest expansion of the 5 panels.
- **The Shining** (was: hotel, maze, snow, ghost, mirror, blood -- 6): +19 new
  plot/prop/setting words: bar, chase, elevator, winter, marriage, kitchen,
  author, knife, doctor, window, door, toy, chef, escape, rescue, kiss, danger,
  night, gift, boy, airport ("maze" itself is not a standalone tag -- the real
  tags are "labyrinth" and "hedge maze"; "maze" was presumably kept from
  earlier as a paraphrase, not re-verified here). **Separately, +15 generic
  content-advisory words** that are also literal BIP39 matches but read as
  severity/mood tagging rather than plot-specific (cruel, fatal, shock,
  sadness, man, woman, vicious, tragic, sick, weird, suffer, limit, wrong,
  rare, fiction) -- flagged as weak, not promoted to the same tier as the 25
  plot/prop words without the user's call.

This is a large expansion of the sourced (not free-associated) candidate space
for exactly the 5 panels the user asked to prioritize. Not yet run against any
intruder hypothesis or through `oracle.py` -- the combined candidate space
across all 5 panels (39 x 11 x 10 x 42 x ~25-40) is large enough that testing it
naively would need curation first (top few per panel) or a lot more compute
than the 38.9M run above, and per the user's stated priority the criterion
search still comes before more word brute-forcing. Date: 2026-08-20.

## Curated top-5-per-panel run against the country+language-split hypothesis, 2026-08-20

Computed the exact size of testing the full widened keyword lists above against
the leading (noise-suspected) country+language-split hypothesis: **4,389,396,480
candidates** (~113x the 38.9M run, ~26h even at the previous 12-worker ~46,000/s
rate) -- too large to run without checking in, given the freeze/reboot the
38.9M run already caused. Presented the size and two options to the user
(run the full 4.39B overnight, or curate down first); user chose to curate:
5 most iconic/distinctive words per zero-literal panel, rest kept as a documented
secondary tier (not discarded) -- see `analysis/leads.md`, "Curated top-5 per
panel, 2026-08-20" for the exact picks and reasoning per panel.

Curated space: **4,800,000 candidates** (24 keeper panels, same panels/order as
the original 38.9M run, `analysis/bruteforce_curated_top5.py`). Ran in-process,
single-thread (small enough not to need multiprocessing): `--selftest` passed,
~13,000/s sustained, 373s total.

**Result: NO MATCH across all 4,800,000 combinations.** This does not disprove
the country+language-split hypothesis (only the 5-word-per-panel curated slice
was tested, not the full 4.39B expanded space, and curation is a judgment call
that could exclude the true word), but it does rule out every combination of
each zero-literal panel's single most iconic/obvious word alongside all the
literal-substring and tied-literal candidates elsewhere. If this hypothesis is
still considered live, the next step would be either the full 4.39B run
(overnight, with CPU headroom, not on a video call) or curating a second tier
(the "5 most iconic" words swapped for the next-best 5) rather than assuming
the hypothesis is dead. Date: 2026-08-20.

## Full programmatic re-derivation of the criterion sweep, catches a parsing bug, 2026-08-20

The user asked to focus specifically on finding the real intruder criterion,
and pointed out uncertainty about whether the earlier "17 combinations" (see
"Pairwise two-field combination sweep" above) had actually been tested end to
end. They hadn't -- only the country+language-split hit had a derivation
attempt; the other 16 were never checked against `oracle.py` at all. Since the
exact 17-hit list from that session was never saved to a file (only in that
session's chat transcript), rebuilt the whole sweep from scratch,
programmatically, from `analysis/imdb_field_audit.xlsx`'s raw columns (country,
language, genres, certificate, color, aspect ratio, runtime, budget,
production-company count, writer credits, awards text, sequel status), rather
than by hand, to remove any manual-counting risk.

**Caught a real bug while doing this**: the original "single-writer-credit-block"
field (documented as landing on 9, a near-miss) was being computed by naively
splitting each film's writers-column text on every semicolon. Panel 28 (Scream
2)'s writers field is `"Kevin Williamson (characters; written by)"` -- one
person, credited for two roles, with the semicolon *inside* the parenthetical
describing his roles, not separating two different writers. A naive split
miscounts this as 2 writer blocks. Re-parsed with a proper "split on `;` only
outside parentheses" routine and verified the fix by hand against all 34 rows'
writers text: **single-writer-credit-block now correctly comes out to exactly
10** (Leon: The Professional, The Visitors, Star Wars: A New Hope, Gravity,
Sharknado, Terminator 2, Scream 2, The Matrix Reloaded, Ghostbusters II, The
Human Centipede) -- not 9. This is a genuinely single-field, single-concept
criterion (not an arbitrary two-field AND/OR), so tested it first and
separately, ahead of the pairwise re-sweep.

Built the 24-word candidate space for this hypothesis (panels 1,2,3,4,5,6,7,8,
9,10,11,12,14,15,17,20,21,22,23,24,25,30,32,33 kept, in order) using literal
substrings from `data/films.csv` plus the curated top-5 words for the
zero-literal panels in the keeper set (8 Goonies, 32 Raiders, 33 Shining --
Leon and Sharknado are dropped intruders under this specific hypothesis, so
their words don't matter here). Space: 480,000 candidates, ran in-process in
39.7s at ~12,000/s. **Result: NO MATCH.** `--selftest` passed. Script not
separately committed (one-off, folded into the batch runner below).

Re-ran the full 24-field x 600-pair sweep programmatically with the corrected
data (24 fields: is-sequel [corrected count 8, unchanged], won-Oscar [13],
nominated-or-won-Oscar [17], single-writer-block [10, corrected from 9],
exactly-2-genres [9], exactly-3-genres [22], UK-co-production [9],
single-country [20], single-language [16], certificate=R/PG-13/PG [14/8/8],
involves-black-and-white [3], first-genre=Action [14], genre-contains-
Sci-Fi/Thriller/Horror [8/5/5], distributor=Warner Bros. [7], aspect-ratio=
2.39:1 [19], runtime>140min [7], runtime<100min [6], budget>=$100M [7],
budget<$10M [5], >=3 production companies [19], has-Franchise-keyword [12,
using the already-verified list from the "Gaps closed" entry above]). Full
script: see the batch runner referenced below.

**Result: 16 of the 600 pairwise AND/OR tests land on exactly 10** (one fewer
than the previously-recalled 17, consistent with the single-writer-block fix:
that field's old wrong count of 9 was presumably producing one extra
coincidental pairwise hit that the corrected count of 10 no longer produces).
Combined with the single-field hit above, **17 total exact-10 criteria**,
matching what the user recalled. Full list of the 16 pairwise hits and their
exact dropped-panel sets (all newly computed, not from memory) -- most are
arbitrary-looking AND/OR pairs of unrelated facts, flagged as multiple-
comparisons noise same as before; only "single_country AND single_language"
(already tested, see above, 0 match on the curated slice) has a clean
single-concept reading:

1. nominated-or-won-Oscar AND >=3 production companies -> drops [1,5,12,17,19,20,22,23,25,27]
2. exactly-2-genres OR involves-B&W -> drops [1,2,5,16,17,21,24,28,29,33]
3. exactly-3-genres AND single-language -> drops [4,7,15,18,20,22,23,26,30,31]
4. single-language AND >=3 production companies -> drops [4,5,15,17,20,22,23,26,28,33]
5. certificate=PG-13 OR involves-B&W -> drops [2,10,11,14,16,17,19,20,21,23]
6. certificate=PG-13 OR genre-has-Thriller -> drops [1,10,11,14,15,16,19,20,21,23]
7. involves-B&W OR genre-has-Sci-Fi -> drops [2,4,5,11,17,19,21,24,27,29]
8. involves-B&W OR budget>=$100M -> drops [2,11,12,17,19,21,22,23,27,29]
9. first-genre=Action AND aspect-ratio=2.39:1 -> drops [1,4,10,11,13,22,23,27,29,31]
10. genre-has-Thriller OR genre-has-Horror -> drops [1,3,5,10,11,15,19,28,33,34]
11. genre-has-Thriller OR runtime<100min -> drops [1,2,4,10,11,15,19,26,30,34]
12. genre-has-Thriller OR budget>=$100M -> drops [1,10,11,12,15,19,22,23,27,29]
13. genre-has-Thriller OR budget<$10M -> drops [1,2,4,7,10,11,15,17,19,26]
14. genre-has-Horror OR runtime<100min -> drops [2,3,4,5,19,26,28,30,33,34]
15. genre-has-Horror OR budget<$10M -> drops [2,3,4,5,7,17,26,28,33,34]

(16 listed as 1-15 above since "single_country AND single_language" is the
16th and already covered separately.)

Rather than pre-judge which of these are "real" vs noise by eyeballing them,
built candidate word spaces for all 15 not-yet-tested hits (literal substrings
+ curated top-5 for whichever zero-literal panels each hits' keeper set
includes) and ran every one through `oracle.py`'s `check()`, in-process,
single-thread (deliberately not multiprocess/12-core, to avoid repeating the
freeze incident, since this is a background/unattended run). Combined space
across all 15: 90,864,000 candidates, individual hypothesis spaces ranging
288,000 to 24,000,000. At ~13,000/s single-thread this is roughly 2 hours;
launched as a background process rather than run synchronously. Script:
`analysis/bruteforce_all_criterion_hits.py`. See the next entry for the
result once it completes.

## All 17 exact-10 criterion hits derivation-tested: 0 matches, 2026-08-20

The single-thread background run (previous entry) completed 9 of 15
hypotheses cleanly (all no match) before the user, present and not on a call,
offered to switch to multiprocessing since the single-thread pace was slow.
Killed the single-thread job (PIDs 31512/35424) and restarted the 6 remaining
hypotheses -- including "thriller OR horror," which was mid-run and had to be
redone from scratch -- with a 10-worker multiprocess version (same mixed-radix
chunked approach as `bruteforce_country_lang_split_mp.py`, 10 of 12 cores, 2
held back as headroom per the earlier freeze-incident lesson; safe to use more
workers here since it's evening, no video call, user actively present and
monitoring).

Result: **~65,000-68,000/s sustained across 10 workers, all 6 remaining
hypotheses done in ~10 minutes total (vs. an estimated ~70 more minutes
single-thread) -- 0 matches on every one:**

- thriller OR horror (14.4M): no match (222s)
- thriller OR runtime<100min (3.6M): no match (55s)
- thriller OR budget>=$100M (18M): no match (266s)
- thriller OR budget<$10M (2.88M): no match (53s)
- horror OR runtime<100min (1.44M): no match (26s)
- horror OR budget<$10M (288K): no match (18s)

**Combined with everything already tested, all 17 of the 17 exact-10
criterion hits from the reconstructed 24-field sweep have now been
end-to-end derivation-tested against the escrow address, using literal
substrings plus the curated top-5 words for whichever zero-literal panels
(Goonies, Leon, Sharknado, Raiders, Shining) each hypothesis's keeper set
includes: 0 matches, across every single one.** This is a substantially
stronger negative than anything before it in this investigation -- it's not
"one leading hypothesis failed," it's "every field-based criterion (single or
paired) found by exhaustively sweeping ~25 IMDb metadata fields across all 34
panels fails," at least within the curated top-5-per-panel word space.

What this does *not* rule out, to be explicit:
- A field not represented in `imdb_field_audit.xlsx` at all (exact award
  category names, filming-location country vs. production country,
  IMDbPro-only data, a three-field combination, a numeric cutpoint other than
  the ones tested).
- The true word for a curated panel not being in that panel's top-5 (curation
  was a judgment call, not exhaustive -- the secondary tier in
  `analysis/imdb_field_audit.xlsx` and `leads.md` has 37, 7, 5, 37, and 22
  more words respectively for Goonies/Leon/Sharknado/Raiders/Shining that
  were not part of this run).
- The mechanism itself being something other than "drop 10 by one shared
  metadata property, keep 24 in panel order."

Scripts: `analysis/bruteforce_all_criterion_hits.py` (single-thread version,
covers the same 15 hypotheses) plus the ad hoc 10-worker rerun (not
separately committed, logic identical to `bruteforce_country_lang_split_mp.py`
generalized to loop over multiple hypotheses). Date: 2026-08-20.

## Exhaustive C(34,10) sweep against the single fixed-word table: 0 matches, 2026-08-21

Per the user's request, tested literally every possible way to drop 10 of the
34 panels (keep the other 24, in panel order), using the single definitive
word per panel finalized 2026-08-20 (see leads.md, "Single definitive word
per panel, all 34, 2026-08-20"). This does not depend on any intruder
criterion at all -- it is the complete space of "drop exactly 10 of these 34
fixed words," C(34,10) = 131,128,140 combinations, addressed directly via
combination unranking (the combinatorial number system) so the work could be
chunked across workers without generating all prior combinations first.
`analysis/bruteforce_all_10of34.py`, 10-worker multiprocess.

The run was interrupted once at ~14M/131M (14M lost to opening a VS Code
window, which closed the terminal it was running in) and restarted from
scratch under Claude's own background process instead, to avoid depending on
a terminal window staying open.

**Full run completed this time: 131,128,140/131,128,140 combinations checked,
~70,800/s sustained across 10 workers, 1847.4s (~30.8 minutes) total.
`--selftest` passed beforehand. Result: NO MATCH.**

This is the strongest possible negative result for this specific hypothesis
space: it is not "one criterion failed" or "one curated word list failed,"
it is "every single one of the 131 million ways to pick which 10 of the 34
panels are intruders fails," conditional entirely on the 34-word table being
correct. Since this is now a *certainty* within that word table (not a
probabilistic/sampled result), the only ways forward from here are:

1. **One or more of the 34 single-word picks is wrong.** The most suspect
   ones are the judgment calls (12 panels that had a tied literal
   candidate -- see the table in `analysis/SUMMARY_FOR_EXTERNAL_AI_2026-08-20.md`
   for exactly which -- and especially the 5 panels with no literal word at
   all: Goonies/chunk, Leon/milk, Sharknado/tornado, Raiders/whip,
   Shining/hotel, each of which has a substantial secondary-tier word list
   not tried here).
2. **The mechanism itself is not "drop exactly 10, keep 24 in panel order."**
   Worth re-examining the puzzle's own rules text for anything that
   contradicts this assumption.
3. Some panel's **film identification** is wrong (see the "probable" vs
   "confirmed" panels list).

Since finalizing one word per panel makes each individual hypothesis test
instant, the natural next step if a specific panel's word is suspected wrong
is to swap in that panel's next-best candidate and re-run this same C(34,10)
sweep (still ~131M combinations, ~31 minutes) -- much cheaper than the
various targeted-hypothesis approaches used earlier, since it no longer
requires guessing *which* 10 to drop, only *which single word* is right for
the suspect panel(s). Date: 2026-08-21.

## NEW CRITERION FOUND: IMDb Connections self-reference among the 34 panels, 2026-08-21

Per an external-AI-assisted research plan the user brought back, checked IMDb's
"Connections" tab (References/Referenced in/Follows/Spoofed in/etc.) for all
34 panels, specifically looking for cross-references *between the 34 films
themselves* (not references to outside media). Fetched every film's
`/movieconnections/` page live (cookies set for en_US locale), expanded all
"See all" sections via JS click + a 500ms render wait, then grepped each
page's text for all 33 other panel titles (exact "Title (Year)" patterns to
avoid false positives from generic title mentions in unrelated TV episode
titles -- e.g. "Blade Runner (1982)" mentions on other pages do NOT count for
panel 22, which is specifically Blade Runner 2049; verified this distinction
carefully throughout).

Found a real, documented web of 30 cross-references among the 34 films (full
edge list below). Counting each panel's degree (how many *other panels in
this specific 34-film set* it has a documented Connections-tab link to, in
either direction):

**Exactly 10 panels have zero connections to any other panel in the set:**
Escape from Alcatraz (7), Mission: Impossible (10), Life of Pi (12), The Man
in the Iron Mask (14), First Man (20), Solaris (21), Blade Runner 2049 (22),
Barry Lyndon (25), Ghostbusters II (31), The Human Centipede (34).

This is a genuinely single-concept, non-arbitrary, self-referential criterion
-- "does this film have an IMDb-documented Connections-tab link to another
film in this exact set of 34" -- and it lands on exactly 10 without any
manual adjustment, unlike every field tried so far. It's also structurally
different from every prior hypothesis: those were all properties of a single
film's own metadata (country, language, awards, etc.); this one depends on
the *set itself*, which fits a puzzle deliberately built around a specific
set of 34 films far better than a coincidental metadata split would.

Full edge list (panel-panel, both directions imply a link either way):
8-32, 13-16, 13-17, 26-32, 32-18, 32-30, 33-3, 33-15, 33-27, 33-28, 3-5,
3-24, 2-9, 2-17, 4-17, 1-17, 1-30, 11-3, 19-5, 19-18, 23-27, 23-32, 24-18,
28-3, 28-5, 28-18, 28-27, 29-3, 29-6, 29-27.

**Caveat, disclosed not hidden**: 3 of the 34 pages (A Clockwork Orange,
Star Wars: A New Hope, Toy Story 2) have very large "Referenced in" counts
(870, unknown-but-large, and moderate respectively) that did not fully
render as text even after clicking "See all" -- likely IMDb's virtualized
list rendering only materializing visible DOM nodes. Real connections to/from
these 3 films were still caught via the *reciprocal* check (searching for
their titles on every other film's own, fully-rendered page), so the graph
above is very likely complete or near-complete, but this is not a
mathematical guarantee the same way the field-audit-derived counts were.

**First derivation test**: built the 24-word mnemonic using the single fixed
word per panel (see leads.md) for the 24 keeper panels under this hypothesis
-- `hard glory alien mad alien now chunk art ill milk river visit orange hope
gravity galaxy close tornado day cream matrix toy whip hotel` -- checked via
`tools/oracle.py`: **NO MATCH**.

**Second derivation test, widened to top-5 curated words for all 5
zero-literal panels** (Goonies, Leon, Sharknado, Raiders, Shining are all
*kept* panels under this hypothesis, unlike the country+language split where
Sharknado was dropped) -- 1,000,000 candidates, ran in-process in 72.4s.
`--selftest` passed. **Result: NO MATCH.**

Not yet tried: the full secondary-tier word lists for these 5 panels
(1,698,278,400 combined candidates, ~7.2h at 10-worker multiprocess speed) --
flagged to the user given the size, per the established practice of not
launching a many-hour job without checking in first. Given how much stronger
this criterion is than anything found before it, this is considered the
current best lead in the whole investigation, worth the larger run if the
user wants to pursue it. Date: 2026-08-21.

## Full-word-space run against the Connections-criterion hypothesis: complete, 0 matches, 2026-08-21

Ran `analysis/bruteforce_connections_criterion_full.py` (8 workers, after
starting at 10 and stepping down to 8 via 6 once the user flagged fan noise
as a thermal-risk signal -- see chat; checkpointing added before the final
launch so a restart would resume instead of losing progress, verified
working with a real interrupt-and-resume smoke test first).

**Completed in full: all 1,828,915,200 candidates checked, 25,641.3s (~7.1h),
~71,300/s sustained the entire run, no crashes/interruptions. `--selftest`
passed at start. Result: NO MATCH.**

This exhausts the complete word space for the Connections-based intruder
criterion (panels 7, 10, 12, 14, 20, 21, 22, 25, 31, 34 dropped -- the 10
films with zero IMDb Connections-tab links to any other film in this
34-panel set) -- every literal title-substring candidate (including full
ties) for the 19 straightforward keeper panels, crossed with *every* sourced
word (top-5 curated plus the full secondary tier) for the 5 zero-literal
keeper panels (Goonies, Leon, Sharknado, Raiders, Shining). Not a sample, not
a curated slice -- the entire space as currently sourced.

This is the most thorough single-hypothesis test in the whole investigation.
It does not disprove the Connections criterion itself (the true word for one
of the 5 tricky panels could still be something not on either page's
keyword/character-name list, or the 3 hub-page virtualization gaps flagged
when this criterion was found could hide an additional edge that would
change which 10 panels are dropped), but the "obvious, sourced" word space
for this specific 24-panel split is now fully exhausted with a clean
negative. Date: 2026-08-21.

## BIP39 passphrase test against a curated guess list, 2026-08-21

Per the user's request, tested whether a BIP39 passphrase (the optional
"25th word" -- a separate string combined with the mnemonic via PBKDF2-HMAC-
SHA512 to derive the seed, giving a completely different wallet per
passphrase) could explain the negative results so far. Not an exhaustive
search -- a passphrase can be any string, unlike the 24 words (a closed
2048-word list) or the intruder criterion (a bounded set of IMDb fields) --
only a curated list of 28 plausible guesses was tested (author handle/npub,
phrases from the rules text including the author's own "IMBD" misspelling,
the puzzle's name/domain, known dates, empty string).

The single fixed-word table (24 words, one per panel, under the Connections
hypothesis) fails the BIP39 checksum on its own -- checksum depends only on
the 24 words, not the passphrase, so no passphrase can rescue a
checksum-invalid combination. Widened to the 1,000,000-candidate top-5
word space instead: scanned for checksum-valid mnemonics first (3,782 found,
close to the expected ~1/256 of 1,000,000), then crossed each against all 28
passphrase candidates -- 105,896 total (mnemonic, passphrase) pairs, each
requiring a full PBKDF2 seed derivation (inherently slow by design, unlike
plain word-checking). Ran multiprocess, 8 workers
(`analysis/try_passphrases.py --workers 8`). `--selftest` passed. **Result:
NO MATCH across all 105,896 combinations.**

This only clears these 28 specific passphrase guesses against the top-5
Connections-hypothesis word space -- it does not rule out a passphrase in
general (unbounded space), a passphrase combined with the full secondary-tier
word space, or a passphrase combined with a different intruder hypothesis
entirely. Date: 2026-08-21.

## Community cross-check: GitHub issue #9, three more criteria tested externally, 2026-08-21

A public GitHub issue (#9) on the puzzle's community/upstream repo has an
independent effort running in parallel, with several contributors
(deviceio121, floflo777 [repo owner], SmallCakekoo [this user's own GitHub
handle -- they already posted there independently, see below], couldes,
timothy-barus, nosignme). Pasted into this session by the user 2026-08-21;
not re-verified by fetching the issue directly, recorded as reported.

**Panel identification convergence** (cross-checks our own data, not
duplicated work):
- Panel 4 = Mad Max: the user (as "SmallCakekoo") independently caught and
  posted the same "Going Places" red herring raised earlier in this session
  (see leads.md, "Panel 4 alternative identification considered and
  rejected") and reached the same conclusion externally, citing an IMDb
  media-viewer URL as proof. Cross-confirms our own rejection of that swap.
- Panel 30 = Toy Story 2 (not Toy Story): independently caught by "couldes"
  in the community thread too, same correction already applied on our side
  2026-08-20 ("Gaps closed" entry above).
- Community consensus (floflo777's summary): panels 3, 5, 9, 13, 14, 16, 23,
  24, 27 remain genuinely unreconciled between different contributors' frame
  identifications -- this overlaps exactly with our own "major dataset
  revision" panel list (2026-08-20), meaning the same identification
  ambiguity independently surfaced in two separate efforts.

**Three new intruder-criterion hypotheses, tested externally with GPU
compute** (by "timothy-barus," not run by us -- recorded as their reported
result, not independently reproduced):
1. "Shares a release year with another film in the set" -> drops
   {4,5,6,7,11,14,18,19,24,26}. 96,636,764,160 raw candidates,
   377,480,432 checksum-valid, **0 matches**.
2. "Released 2000 or later" -> drops {12,15,19,20,21,22,23,26,29,34}.
   72,477,573,120 raw, 283,125,641 checksum-valid, **0 matches**.
3. "The ten shortest films by runtime" (a rank-based selection, not a fixed
   threshold -- structurally different from every criterion we tried, since
   a top-N-by-rank rule always yields exactly N by construction rather than
   landing on 10 by coincidence) -> drops {2,4,15,16,19,21,26,30,31,34}.
   144,955,146,240 raw, 566,220,239 checksum-valid, **0 matches**.
   Total across the three: 1,226,826,312 checksum-valid seeds tested, 0
   matches. Reported methodology: BIP84 `m/84'/0'/0'/0/{0,1,2}` only (not
   the wider BIP49/44 + raw-path sweep `tools/oracle.py` covers), ~130,000
   seeds/s on a rented GPU, gated by reproducing a CPU reference byte for
   byte, recovering 3 planted witness mnemonics, and checking the
   checksum-valid rate landed within 0.6 sigma of the expected 1/256 -- a
   real validation methodology, given credibility here though not
   independently reproduced by us. Two further candidate rules ("pre-1980,
   the ten longest" and one other) were identified but not run: they leave
   Sharknado wordless too (3 unknowns instead of 2), and a 3-wildcard sweep
   at 2048^3 is out of reach even on their hardware.

**Word-table discrepancy worth flagging back to the thread**: timothy-barus's
table lists **"shine"** as panel 33's (The Shining) BIP39 word. This
contradicts our own explicit, already-documented finding (2026-08-20 dataset
revision entry above): "shine" is **not** a literal substring of "shining"
(s-h-i-n-**i**-n-g vs s-h-i-n-**e** -- the 5th letter differs, no valid
match under simple substring or plural/suffix-strip rules). Likely an error
in their table, not a rule we're missing. Their own conclusion text ("The
Goonies, Leon and Sharknado give nothing") is consistent with treating
Shining as solved via "shine," so this may be silently propping up their
"only 3 unknowns" framing.

**Independent corroboration of our own AKA-title finding**: contributor
"nosignme" proposes "ski" for panel 26 (Sharknado), via the film's "Dark
Skies" alternate title -- the exact same find this session made independently
2026-08-21 (see leads.md, "Splice check... + AKA titles," which also flagged
it as weak since "Dark Skies" is itself a known IMDb-database quirk, not a
real alternate title for this film). Two independent efforts landing on the
same word via the same path is worth noting either way.

**Not mentioned anywhere in the community thread**: the IMDb Connections
self-reference criterion (this session's strongest hypothesis, "NEW
CRITERION FOUND" entry above). Appears to be a genuinely novel contribution
relative to the public effort. Date: 2026-08-21.

## Literal + one sourced reference word per panel, under the Connections hypothesis: 0 matches, 2026-08-21

Per the user's request, built a bounded candidate table for the 24 keeper
panels under the Connections intruder hypothesis (dropped: 7, 10, 12, 14,
20, 21, 22, 25, 31, 34): each panel's literal title substring(s) plus one
additional "reference" word meant to capture what the film is actually
about (prompted directly by a community-issue critique -- see "Community
cross-check: GitHub issue #9" above -- arguing thematic words like "lizard"
for Godzilla deserve consideration alongside literal ones like "ill").

Sourcing status, stated plainly: the reference words for panels 8, 13, 26,
32, 33 are the same ones already sourced from real IMDb keywords/reviews/AKA
titles earlier in this investigation. The reference words for the other 19
panels (tower, trial, marine, fuel, chest, jungle, arena, lizard, mountain,
time, prison, force, orbit, raccoon, tower again, metal, mask, machine,
cowboy) are the assistant's own thematic judgment calls, checked only for
BIP39 wordlist membership, NOT verified against each film's actual IMDb
keyword page the way the established 5 were. Flagged as weaker evidence
throughout.

Full table and per-panel candidate counts in chat (2026-08-21). Total space:
286,654,464 candidates. Ran multiprocess, 6 workers (user was concurrently
using the machine for Photoshop and video, so kept to 6 instead of 8-10 for
headroom; 6 workers still reached ~68,000-72,000/s, close to the 8-10-worker
rate seen in earlier runs, suggesting the bottleneck isn't purely
core-bound). Checkpointing enabled (`analysis/bruteforce_literal_plus_reference.py`,
same mechanism as the Connections full-space run) though not needed this
time -- ran start to finish without interruption.

**Result: NO MATCH across all 286,654,464 combinations.** `--selftest`
passed, 4184.5s (~1h10m) total. This clears the specific "literal + one
thematic reference word" table as drafted -- it does not clear thematic
words in general (only the ones on that specific list), and 19 of the 24
panels' reference words are still IMDb-keyword-unverified, so a genuine
miss there remains a live possibility distinct from "thematic words don't
work." Date: 2026-08-21.

## Literal + reference word, single-writer-credit hypothesis: 0 matches, 2026-08-24

Same "literal title substring(s) + one thematic reference word" approach as
the Connections-hypothesis run above, applied to the other hypothesis the
user picked: single-writer-credit-block (dropped: 13, 16, 18, 19, 26, 27,
28, 29, 31, 34). Candidate table and sourcing-confidence caveats (5 panels'
words independently IMDb-sourced; the rest are thematic judgment calls,
BIP39-checked but not IMDb-keyword-verified) match the Connections run;
full table in `analysis/bruteforce_writer_literal_plus_reference.py`.

Total space: 1,289,945,088 candidates. Ran multiprocess, 10 workers,
checkpointing enabled. `--selftest` passed.

Operational note: the machine went to sleep for an extended period (multiple
days) partway through this run despite being plugged in -- Windows sleep
was not disabled beforehand. The background process was suspended, not
killed, and resumed correctly on wake with no lost progress (checkpoint
mechanism wasn't even needed here, the process itself survived the sleep).
Real throughput before and after the sleep gap was consistent
(~85,000-92,000/s); only the script's own cumulative-average-since-start
rate readout was skewed by the wall-clock gap, recovering over the
following ~30-40 minutes of real runtime as the average caught up. Power
settings were changed afterward (`powercfg /change standby-timeout-ac 0`)
to prevent recurrence on future long runs.

**Result: NO MATCH across all 1,289,945,088 combinations**, 33,528.7s of
actual runtime (~9.3h, spread over a longer wall-clock window due to the
sleep interruption). Same caveat as the Connections-hypothesis run: this
clears the specific candidate table as drafted, not thematic words in
general -- most of the 24 panels' reference words are still
IMDb-keyword-unverified. Date: 2026-08-24.

## Literal + reference word, single-country+single-language hypothesis: 0 matches, 2026-08-24

Third and final planned run of the "literal title substring(s) + one
thematic reference word" approach, this time against the original leading
hypothesis (single country of origin AND single language; dropped: 4, 7, 9,
15, 18, 24, 26, 28, 30, 31). Candidate table in
`analysis/bruteforce_country_lang_literal_plus_reference.py`, same
sourcing-confidence split as the other two runs (panels 8, 13, 32, 33
IMDb-sourced; the rest thematic judgment calls checked only for BIP39
membership).

Total space: 2,149,908,480 candidates. Ran multiprocess, 10 workers,
checkpointing enabled (not needed this run -- machine stayed awake
throughout after `powercfg /change standby-timeout-ac 0` was applied
following the previous run's sleep interruption). `--selftest` passed.
Sustained ~82,700/s the entire run, no interruptions.

**Result: NO MATCH across all 2,149,908,480 combinations**, 25,978.0s
(~7.2h). Same caveat as the other two literal-plus-reference runs: clears
this specific candidate table, not thematic words in general.

**This closes out all three hypotheses the user chose to test with the
literal+reference approach** (Connections, single-writer-credit,
country+language) -- combined with everything else in this file, every
promising intruder criterion identified so far has now been tested with
both the narrow (literal-only / top-5-keyword) and the widened
(literal+thematic-reference) word spaces, all with 0 matches. Date:
2026-08-24.

## Word-table audit: no errors found, 2026-08-24

Per the user's request to sanity-check the shared 34-word candidate table
before trusting further billions of candidates against it, independently
re-derived every literal substring for all 34 titles from scratch (not by
eye, programmatically against the real 2048-word BIP39 list) and cross-checked
three things: (1) every word recorded in `data/films.csv` is a real BIP39
word, (2) every one of those words genuinely appears as a substring of some
title-word (not a transcription error), (3) the single-fixed-word table
reused across every large brute-force script in this session matches either
`data/films.csv` (for the 29 literal panels) or a properly-sourced non-literal
word (for the 5 zero-literal panels), never anything invented mid-script.

**Result: no errors.** One informational, already-known non-issue: "ask" is
a real extra substring inside panel 14's "Mask" not recorded in films.csv,
correctly excluded per this project's established whole-word-beats-substring
hierarchy (already documented). This rules out "a silent typo in the shared
word table" as an explanation for the long string of 0-match results across
this investigation's several-billion-candidate history. Date: 2026-08-24.

## Oracle derivation path coverage widened, re-running the Connections literal+reference space, 2026-08-24

The one assumption never questioned across ~6 billion tested candidates:
`tools/oracle.py` only checked 2 accounts x 3 address indices (external
chain only) for each of BIP84/49/44, plus 3 raw paths -- 21 addresses per
candidate. If the real wallet uses a different account or a higher address
index, no amount of correct words or correct intruder criterion would ever
have found it.

**Widened `tools/oracle.py` itself** (the canonical, documented tool, not a
one-off fork) to 5 accounts x 10 indices x both external and internal/change
chains per BIP84/49/44 -- 303 addresses per candidate now, ~14.4x more.
`--selftest` re-verified passing after the change (key format for the
addresses dict changed to include the chain label, e.g. "bip84 account 0 ext
index 0"; selftest's lookups updated to match). README.md's documented
derivation-coverage claim updated to match.

Measured impact on throughput: a realistic mixed sample (mostly
checksum-invalid candidates, as any real sweep is) drops from ~12,000/s to
**~7,900/s single-threaded** -- much less than the naive 14.4x, because
`check()` rejects checksum-invalid candidates (the vast majority, 255/256)
before ever calling the now-more-expensive `addresses()`. Only the
checksum-valid ~1/256 pays the full new cost.

Re-running the Connections-hypothesis literal+reference space (286,654,464
candidates, previously 0 matches under the narrower oracle -- see "Literal +
one sourced reference word per panel... 2026-08-21") against the widened
oracle, 10 workers. In progress; result to follow. Date: 2026-08-24.
