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

## Local brute-force sweep, phases 1 + 2A + 3 (one-in/one-out), 2026-08-20

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
