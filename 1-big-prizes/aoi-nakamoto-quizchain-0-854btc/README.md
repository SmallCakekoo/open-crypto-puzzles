# Aoi Nakamoto Quizchain (0.777 BTC, [OPEN])

AoiNakamoto, a pseudonymous Reddit user, ran a series of roughly 90 self-funded
Bitcoin puzzle blocks from April to October 2019 on r/bitcoinpuzzles and her own
r/Grycoin, each with its own escrow address, question, and prize. She stopped
posting in October 2019 without ever reclaiming her own puzzle funds. Every
block was solved and swept by readers except the last two she published: the
second and final stage of "Real Big Block" (0.777 BTC) and "Quizchain2 Block
76" (0.077 BTC). Block 76 was solved and swept by a reader on 2026-08-17 (tx
`2e271ac2f63f488cd14112bceeed56f159ecd98cb3ce753f08e2d94bb62714a3`); the
solution was never disclosed publicly. Only Real Big Block, 0.777 BTC, remains
open. The MD5-to-BIP39 derivation mechanism is confirmed exactly, including a
case-flip rule that the puzzle's own source text explicitly states (not just a
researcher-inferred fit), and the exact paragraph-separator bytes for both the
original and rehashed versions of Real Big Block are confirmed from the
author's own words. What remains unresolved is which paragraphs of the
confirmed source chapter are actually hashed, and whether the case-flip rule
is reused at all for this second stage.

## At a glance

| | |
|---|---|
| Author | AoiNakamoto (pseudonymous), [r/Grycoin](https://www.reddit.com/r/Grycoin/) |
| Published | 2019-04 to 2019-07-31, rolling releases on r/bitcoinpuzzles and r/Grycoin |
| Prize | 0.777 BTC open (Real Big Block); Block 76's 0.077 BTC was solved and swept by a reader 2026-08-17 |
| Chain | bitcoin |
| Escrow | `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W` (Real Big Block, current, [explorer](https://mempool.space/address/14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W)); `1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC` (Real Big Block, superseded pre-rehash address, funded 2019-07-24, swept back by the author herself before the rehash, not part of the live prize); `13Cv6SXUnzGDT8JHqzzJ8xMPtsSdhJA4wd` (Block 76, solved and swept 2026-08-17, [explorer](https://mempool.space/address/13Cv6SXUnzGDT8JHqzzJ8xMPtsSdhJA4wd)) |
| Last on-chain check | 2026-08-22: Real Big Block funded and unspent (0.777 BTC); Block 76 swept 2026-08-17 |
| Status | OPEN |
| Puzzle type | bip39-seed, word-selection |
| Target format | source text (candidate answer), MD5 to 128-bit entropy, BIP39 mnemonic, BIP44 `m/44'/0'/0'/0/i` for i = 0 to 5, P2PKH address |
| Certified oracle | yes: `tools/oracle.py --selftest` (certified against the author's own published entropy-to-WIF vector; see "Certified against") |
| What remains | Real Big Block: which paragraphs of the confirmed "Second" Wattpad chapter are hashed, and whether the case-flip transform is reused at all. The paragraph-separator bytes for both historical versions are confirmed (see "What is understood"); the source itself is confirmed; selection is not |
| Series | this folder covers Real Big Block, the last open lot of the approximately 90-block Quizchain series; the rest, including Block 76 (August 2026), were solved by other readers |

## The puzzle as published

Real Big Block stage 1, 2019-07-07
([reddit.com/r/Grycoin/comments/ca6jxv](https://www.reddit.com/r/Grycoin/comments/ca6jxv/77_mbtc_quizchain2_block_77_stage_one/)):
"I do disclose that this one has no TOMI field, but that is all. You are on your
own completely." Its question links to Hal Finney's "Bitcoin and me" post on
bitcointalk (topic 155054). She adds: "I will publish the complete solution as
the Second stage of this block. This solution will in turn be the question for
the Second stage, which will have the final 777 mbtc prize." This stage's
escrow, `19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN`, was solved and swept on
2019-08-03; it is not part of the live prize and is used in this folder only to
certify the case-flip rule.

Real Big Block stage 2 ("this Second stage" from the quote above) is Real Big
Block itself — the same puzzle, not a separate one. Its question, per the
original announcement post (`cgkpbb`, r/bitcoinpuzzles/Grycoin, 2019-07-22/24):
"Question: Final version of the second chapter of Wattpad story", published as
a chapter titled "Second" on the author's own Wattpad account
([wattpad.com/720888559-second](https://www.wattpad.com/720888559-second)),
which is part 2 of a 33-part Wattpad story also titled "Second"
(story id 184148284). The same announcement post also states: "I wanted to
remove one of the twists I had. The block is now slightly easier... hashed
with two line breaks between paragraphs now" — the rehash from the superseded
address to the current one.

In the "Real Big Block Discussion" thread
([reddit.com/r/Grycoin/comments/chn8un](https://www.reddit.com/r/Grycoin/comments/chn8un/real_big_block_discussion/),
fully recovered, 33 comments, exact UTC timestamps, via the Arctic Shift Reddit
archive — reddit.com itself is not fetchable by this repository's tooling):

- 2019-07-25: "When I posted the real big block at the Wattpad site, I added
  extra line breaks between paragraphs. This information is needed to solve
  the block."
- 2019-07-28: "The solution you need to hash with has only one line break
  between paragraphs, which is one 13 and one 10" — i.e. the **superseded**
  address's separator is a single `\r\n` (2 bytes).
- 2019-07-30: "Once someone figures out the format for the first stage, they
  will also have a big hint for the format of this second stage."
- 2019-07-31, after moving the funds to the current escrow: "I took back the
  prize for a moment and sent it again to a new address, hashing with a
  slightly different solution [...] It has multiple paragraphs and two line
  breaks between each of them."
- 2019-08-01, disambiguating an exact reader question ("hit enter once or
  twice?"): "I mean the second one. Hit enter twice. This displays in Ascii as
  13 10 13 10" — i.e. the **current** address's separator is `\r\n\r\n` (4
  bytes).

![Quizchain series structure: both rounds solved and claimed except the 1 open gate](images/02-structure-blocks.svg)
*Figure 2. The Quizchain series, colored by claim status (source: data/blocks-structure.json, script tools/fig_blocks.py).*

## What is understood

### Mechanism

Every block in the series follows the same transform: MD5 the exact bytes of a
source text to get 128 bits of entropy, generate a BIP39 mnemonic from that
entropy, derive BIP44 path `m/44'/0'/0'/0/i` (the author confirms taking a low
index, typically the first), and compare the resulting P2PKH address to the
block's escrow.

![Source text to P2PKH address, five stages linked by MD5, BIP39 and BIP44](images/01-pipeline-derivation.svg)
*Figure 1. The MD5-to-address derivation pipeline (source: data/pipeline-stages.json, script tools/fig_pipeline.py).*

**The case-flip rule is not just a researcher fit to Stage One's calibration
address — the puzzle's own confirmed source text states it directly.** The
"Second" Wattpad chapter (Real Big Block's confirmed source) contains, in its
own narrative, a full walkthrough of the Stage One mechanism, and states
verbatim: "The letters I, T, A, S, and M as first letters of each paragraph of
this post," followed by "the only ones where we don't recognize the signs"
describing the 4 exception paragraphs (2 starting with F, 2 with W). Applied to
Hal Finney's real bitcointalk post (fetched and reconstructed directly, raw
HTML, `<br /><br />` as paragraph separator, a single trailing `<br />` kept as
an internal newline, entities decoded — all confirmed against GitHub issue #1
on the upstream repository), this reproduces `19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN`
exactly at BIP44 index 0: MD5 `9dd2efb9bc976c2095bd534d7b8d431c`. The Stage One
source text is pure ASCII, so UTF-8/ISO-8859-1/cp1252 are byte-identical for
it and the encoding question cannot be resolved from this calibration alone.

A brute-force check of all 512 subsets (sizes 0-9) of the 9 distinct letters in
"SATOSHI NAKAMOTO" confirms `ITASM` is the unique size-5 subset from that pool
that reproduces the address — but only 5 of the 26 alphabet letters (I, T, A,
S, M, plus F and W as confirmed exceptions) are actually exercised by any
paragraph in the Finney post; the other 19 letters are unconstrained by this
one calibration point. This does not weaken the rule's validity — it is
confirmed by the source text directly — but it does mean the rule cannot, by
itself, tell us how paragraphs starting with other letters should be treated
in a different source text.

**For Real Big Block, the source chapter is confirmed, the two historical
paragraph-separator byte sequences are confirmed, and reproducibility of the
full pipeline is confirmed — but which paragraphs of that chapter are hashed,
and whether the case-flip rule applies at all, is not.** Extensive testing
(see "What has been tested") of the whole chapter, its major sections, every
ITASM/non-ITASM selection and complement, individual-letter selectors,
header-inclusion variants, per-paragraph and whole-document trimming, and
every combination of the two confirmed separators with UTF-8/ISO-8859-1
encoding, against both the current and superseded escrow addresses, has found
zero matches. A full byte-level forensic audit (invisible characters, NBSP
positions, Unicode normalization, BOM, repeated whitespace) found the source
text unusually clean: exactly 6 non-breaking spaces and nothing else
non-ASCII in the entire 273-paragraph chapter, no BOM, and NFC/NFD/raw are
byte-identical (nothing decomposable exists in the text). The independently
fetched rendered Wattpad page and the API text agree exactly (0 differences)
for their overlapping paragraphs, ruling out "wrong access method" as an
explanation.

The chapter is part 2 of a larger, previously unexamined 33-part Wattpad
story (also titled "Second"). Two earlier draft parts ("THOMAS and SATOSHI",
"The Satoshi Code") were consolidated into the final chapter before its last
edit; diffing a draft against the corresponding final section shows real
editorial changes (a heading added, two paragraphs merged via an internal
newline, one word changed, one NBSP inserted) — confirming the chapter
fetched today is the post-edit, final version the announcement post refers to,
not stale draft content. A later part, "Starting Up" (the story's true last
edit, 12 minutes after the chapter itself, right before the initial funding),
contains no further mechanism information — just a "no more hints" statement.

### Derivation and oracle

```
python3 tools/oracle.py --selftest
python3 tools/oracle.py "<candidate text>"
python3 tools/oracle.py --stdin
python3 tools/oracle.py --flip-case "<one paragraph>"
```

Given a candidate text, the oracle MD5s its UTF-8 bytes, derives BIP44 indices 0
through 5, and compares each resulting address against the open escrow (and,
for historical/calibration purposes, the superseded and Stage One addresses).
`--flip-case` applies the confirmed Stage One rule to one paragraph you supply.
This script ships no source text of its own: Real Big Block's source (a Wattpad
chapter) and the Stage One certification text (a bitcointalk post by Hal
Finney) are both excluded, the first as bulk chapter content and the second as
third-party historical material neither the puzzle's author nor this repository
holds the rights to. Supply your own candidate text to test it. Block 76's
`--block76-filter` mode has been removed now that the block is solved and no
longer part of the live prize; see git history if you need it for reference.

### Certified against

`tools/oracle.py --selftest` reproduces the author's own published calibration
vector, given in the round-1 corpus: entropy `2941774a2abec9f30c7d6777d1d53d91`,
at BIP44 index 1 ("my 2nd private key"), derives WIF
`L5Z66qPmUkTAsWQywjRNHDxHrX6J1X1SQedp6V8QsbaXR7rGd6ex` exactly, and that WIF
appears at no other index. This certifies the MD5-to-address transform itself,
without needing any third-party text. The selftest also checks the
`--flip-case` helper against a synthetic (non-puzzle) example sentence.

This does not, by itself, reproduce Block 77 Stage One end to end, since that
needs Hal Finney's bitcointalk post text, which this repository does not ship.
Anyone who supplies that text (freely readable at bitcointalk topic 155054) can
reproduce it themselves with `apply_stage_one_rule()` in `tools/oracle.py`;
this was done during research and reproduces `19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN`
exactly, MD5 `9dd2efb9bc976c2095bd534d7b8d431c`, independently cross-confirmed
against GitHub issue #1 on the upstream repository and against the author's
own "9dd (copypasted)" celebration comment in the Block 77 Reddit thread.

Reproduced 2026-08-22.

### Established facts

1. Real Big Block's escrow is funded and unspent as of 2026-08-22:
   `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W` holds 0.777 BTC (funded 2019-07-30,
   block 587833), checked via [mempool.space](https://mempool.space).
2. Block 76's escrow (`13Cv6SXUnzGDT8JHqzzJ8xMPtsSdhJA4wd`) was solved and
   swept by a reader on 2026-08-17 (tx
   `2e271ac2f63f488cd14112bceeed56f159ecd98cb3ce753f08e2d94bb62714a3`, to
   `bc1qaxm5p35r3yl25rdh5ex0j6wx33peht9r735x90`); the solution was never
   disclosed publicly by the solver or by AoiNakamoto.
3. The MD5-to-BIP39-to-BIP44 transform is confirmed exactly against the
   author's own published calibration vector.
4. The case-flip rule is confirmed exactly against the solved sibling lot
   Block 77 Stage One, reproducing its escrow address byte for byte, **and**
   is stated directly in the confirmed Real Big Block source text itself
   (paragraph 227 of the "Second" chapter), not merely inferred from the
   address match.
5. Real Big Block's paragraph separator is confirmed as exactly `\r\n` (2
   bytes, ASCII 13 10) for the superseded pre-rehash address
   (`1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC`, funded 2019-07-24) and exactly
   `\r\n\r\n` (4 bytes, ASCII 13 10 13 10) for the current address, both from
   direct, unambiguous author statements in the fully-recovered Real Big
   Block Discussion thread.
6. The "Second" chapter's Wattpad `modifyDate` (2019-07-23T23:12:04Z) predates
   both the superseded (2019-07-24) and current (2019-07-30) fundings, and has
   not changed since, confirmed via the Wattpad API — the underlying prose did
   not change between the two hash attempts; whatever "the twist" that was
   removed was, it was not an edit to the chapter's own wording.
7. The chapter's non-ASCII content is exactly 6 non-breaking-space characters
   (U+00A0) and nothing else — no curly quotes, dashes, ellipses, or HTML
   entities anywhere in its 273 paragraphs, confirmed by a full character-level
   audit; NFC/NFD/raw are byte-identical (nothing in the text is decomposable).
8. No archived capture of the "Second" Wattpad chapter, or of the bare
   `wattpad.com` domain, exists on the Wayback Machine (checked via the direct
   `wayback/available` API on both URLs); archive.today is rate-limited (HTTP
   429) on every attempt, consistent across two independent research sessions;
   whether this reflects a platform-level exclusion is unconfirmed.
9. MD5 is positively confirmed as Real Big Block's hash algorithm, not merely
   assumed: in "Mistakes" (Wattpad part 14, 2019-04-25) the author describes
   accidentally hashing two early blocks with MD5 after her tablet's hashing
   tool reverted to its default, and states she then standardised every hash
   on MD5 to prevent recurrence — three months before Real Big Block. The same
   passage establishes that she hashed by pasting text into a GUI app on a
   tablet, not through a script (see lead 5).
10. AoiNakamoto's complete Reddit post history (100 submissions, confirmed
   complete via pagination) contains no solution disclosure at any point after
   2019-08-04, including no post around the two expiry conditions she set for
   disclosure (Mayer Multiple hitting $100/mbtc, or Tanabata 2022, both since
   passed) — consistent with the escrow still being funded today.

## What has been tested

Full ledger in [analysis/tested.md](analysis/tested.md). Summary:

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| RBB: chapter unmodified or with the certified rule on a small set of candidate paragraph groups (original private research) | approximately 350,000 | MD5 to BIP39 to address compare | 0 match | yes: oracle certified against Stage One | 2026-08-15 |
| RBB: every subset of 17 candidate paragraphs, 18 serializations (original private research) | 2,360,000 | same | 0 match | yes | 2026-08-15 |
| RBB: every single-character edit across 40 base texts (original private research, UTF-8 only) | 266,038,400 | same | 0 match | yes: 3 planted witnesses per base plus the real Stage One text, all recovered | 2026-08-15 |
| RBB: name/word paragraph selectors, browser-copy simulation, invisible characters, alternate encodings (original private research) | approximately 1,830,000 | same | 0 match | yes | 2026-08-15 |
| RBB: whole chapter and 12 precise chapter sections, 3 case-rule variants, both confirmed separators plus `\n`/`\n\n`, 3 NBSP-handling modes, UTF-8/ISO-8859-1, both addresses | 1,437 | same | 0 match | yes, real fetched source | 2026-08-22 |
| RBB: ITASM-only, non-ITASM-only, and complement selection (drop-not-flip), with and without the Phase-1 transform, both confirmed separators, both addresses | 288 | same | 0 match | yes | 2026-08-22 |
| RBB: individual single-sign selectors (I-only, T-only, A-only, S-only, M-only), "sign(s)"-containing paragraphs, Satoshi-Code-section-restricted selection | 192 | same | 0 match | yes | 2026-08-22 |
| RBB: header-inclusion/exclusion x per-paragraph/whole-document trim x transform x both separators x both addresses (byte-level forensic audit) | 192 | same | 0 match | yes | 2026-08-22 |
| RBB: reversed case-flip direction (ITASM flipped, others unchanged) against the real Stage One calibration text | 1 | same | 0 match (confirms the original direction is correct) | yes | 2026-08-22 |
| RBB: positional paragraph selection (every Nth paragraph, N=2/3/4/7, all offsets), read from the author's own "every 7th word" technique in the Wattpad story | 384 | same | 0 match | yes | 2026-08-22 |
| RBB: full edit-distance-1 sweep (deletion, insertion, substitution) on the whole chapter, both confirmed separators, unmodified and ITASM bases, both addresses, parallelized 7-11 cores | 18,840,792 | same | 0 match | yes, first exhaustive edit-distance-1 sweep under the confirmed separators | 2026-08-22 |
| RBB: **every contiguous paragraph range of the chapter** (all 37,401), both confirmed separators, 3 case-rule variants | 224,406 | same | 0 match | yes, planted witness recovered | 2026-08-25 |
| RBB: transposition (reversed, halves swapped, interleaved, evens/odds), each across the full serialization matrix | 6,912 | same | 0 match | yes, planted witness recovered | 2026-08-25 |

Cumulative: approximately 272 million candidates tested against Real Big Block
by the original private research, plus approximately 18.8 million additional,
encoding- and separator-aware candidates tested against real fetched source
data in the 2026-08-22 session, plus 231,318 witness-verified candidates in the
2026-08-25 session (approximately 291.2 million total), all negative. The
2026-08-25 rows are small in count but close two structural gaps: **all 37,401
contiguous paragraph ranges** (prior work tested 12 hand-picked sections) and
order-changing transforms (never tested before). Full scope notes, including
which rows are complete sweeps versus targeted tests, are in
`analysis/tested.md`.

## Open leads, ranked

1. **Identify which paragraphs of the "Second" chapter are hashed, and
   whether the case-flip transform applies at all** (open-ended). This is now
   the sole remaining unknown — source, both historical separators, and the
   general mechanism family are all confirmed; selection is not. No primary
   source (the chapter, its two draft predecessors, the "Starting Up" part, or
   the complete Reddit history) states it explicitly, unlike Stage One.
   Confirmed by any selector that is independently justified by a specific
   sentence in a primary source (not merely by producing the correct address)
   and reproduces either target; this lead has no clean exhaustion condition,
   since the letter-selector space is large and only sparsely evidence-backed.
2. **A bounded 2-character-edit sweep on the whole chapter under the two
   confirmed separators** (hours on a rented GPU). The original 1-character
   sweep (266M) was UTF-8-only and used a different, unconfirmed separator
   assumption; redoing a 2-character-edit sweep specifically under `\r\n` and
   `\r\n\r\n` has not been done. Confirmed by a match; killed by exhausting it
   with none.
3. **Compare the superseded and current addresses as a differential
   constraint, if a working transform for either is ever found.** Not yet
   applicable, since neither address has been reproduced from any tested
   candidate; recorded as a method to apply once one hit is found, to
   independently validate it against the "twist removed" description.

4. **The "-gry" wordplay behind the r/Grycoin name** (speculative, low
   priority). The author named her subreddit Grycoin and wrote "I hope you are
   not anGRY any more"; "-gry" is a well-known answerless English word riddle
   whose trick is its phrasing, matching her Atbash/ITASM style. Weakened by
   the finding that "gry" appears nowhere in the confirmed source chapter, and
   that the "GRYcoin project" in the same thread is a commenter's climate-coin
   proposal, not hers. Cheap to close out; not worth compute beyond that.
5. **Identify the tablet hashing app she actually used** (strongest of the new
   leads). "Mistakes" (Wattpad part 14) confirms she pasted strings into a GUI
   hashing app on a tablet whose default was MD5 — which positively confirms
   MD5 for Real Big Block, and opens the possibility that the unexplained
   byte-level mismatch comes from that app's silent text handling (trailing
   newline, CRLF-to-LF normalisation, BOM, whitespace trim) rather than from
   paragraph selection. Her asciivalue.com checks prove what the clipboard
   held, not what the app did with it.
6. **Transposition transforms** (structural gap). Every test to date preserves
   paragraph order; order-changing transforms have never been tried.

Full notes, including a triage of which cryptographic techniques can and
cannot attach to this puzzle at all: [analysis/leads.md](analysis/leads.md).

## Files in this folder

| Path | What it is |
|---|---|
| `clues/author-posts.md` | short, dated quotes from the author's own Reddit posts, with links |
| `data/pipeline-stages.json` | the 6-stage label list for the derivation pipeline figure |
| `data/blocks-structure.json` | the series structure and the 1 open gate, for the structure figure |
| `data/realbigblock_reddit_foros.md` | a partial local capture of the Real Big Block Discussion thread |
| `data/realbigblock_full_thread_recovered.md` | the complete 33-comment Real Big Block Discussion thread with exact UTC timestamps, recovered via the Arctic Shift Reddit archive |
| `data/realbigblock_original_announcement.md` | the original Real Big Block announcement post (`cgkpbb`), never previously captured in this repository |
| `data/wattpad_story_structure.md` | the full 33-part structure of the "Second" Wattpad story, with the "Starting Up" part's full text |
| `data/quizchain2block76_reddit_foros.md` | local capture of the (now solved) Block 76 thread, kept for historical reference |
| `data/quizchain2block77_reddit_foros.md` | local capture of the Block 77 Stage One thread |
| `analysis/tested.md` | the complete negatives ledger |
| `analysis/leads.md` | full notes behind the ranked leads |
| `images/01-pipeline-derivation.svg` | the MD5-to-address derivation pipeline diagram |
| `images/02-structure-blocks.svg` | the Quizchain series structure, colored by claim status |
| `tools/oracle.py` | candidate checker, certified against the author's own vector; includes the Stage One case-flip helper |
| `tools/fastderive.py` | fast reimplementation of the same transform (hashlib + coincurve, no bip_utils) for large sweeps; self-tests against the same published vector and cross-checks against `oracle.py`'s library when available |
| `tools/bip39-english.txt` | the standard BIP39 English wordlist (public domain, sha256 `2f5eed53...`), so `fastderive.py` needs no wordlist dependency |
| `tools/secp256k1_pure.py` | stdlib-only secp256k1, used automatically when coincurve is unavailable (a locked-down machine); verified against coincurve on random keys, 11x slower |
| `tools/ripemd160_pure.py` | stdlib-only RIPEMD-160, used automatically when hashlib lacks it (OpenSSL 3 legacy-provider builds); passes the official test vectors |
| `tools/bench_scale.py` | measures this machine's real parallel throughput and converts it into wall times, since PBKDF2 scaling is much worse than core count suggests |
| `tools/fetch_source.py` | fetches the Wattpad source chapter into a local, gitignored cache, refusing to write it unless the 273-paragraph / 6-NBSP forensic audit still holds |
| `tools/sweep.py` | parallel sweep engine: contiguous-range, app-byte-matrix, bounded 2-edit, and transposition modes, each witness-verified |
| `tools/README-sweep.md` | what a compute machine needs and the order to run the sweeps in |
| `tools/fig_pipeline.py` | generates images/01-pipeline-derivation.svg from data/pipeline-stages.json |
| `tools/fig_blocks.py` | generates images/02-structure-blocks.svg from data/blocks-structure.json |

## Sources

- Real Big Block stage 1, Reddit, 2019-07-07: https://www.reddit.com/r/Grycoin/comments/ca6jxv/77_mbtc_quizchain2_block_77_stage_one/
- Real Big Block original announcement ("Quizchain last block"), Reddit, 2019-07-22: https://www.reddit.com/r/Grycoin/comments/cgkpbb/
- Real Big Block Discussion (fully recovered), Reddit, 2019-07-25 to 2019-08-03: https://www.reddit.com/r/Grycoin/comments/chn8un/real_big_block_discussion/
- Grycoin Block 2 (the author's own worked example for "the format used in both phases of block 77"), Reddit: https://www.reddit.com/r/Grycoin/comments/cleczc/
- Quizchain Introduction (general rules, MD5/BIP39/TOMI mechanics), Reddit: https://www.reddit.com/r/Grycoin/comments/bry4fw/
- "Second", Wattpad chapter by AoiNakamoto (part 2 of 34): https://www.wattpad.com/720888559-second
- "Starting Up", Wattpad part (the story's true last edit): part id 762380140, same story (184148284)
- GitHub issue #1 on the upstream repository (Stage One MD5 and reimplementation gotchas): https://github.com/floflo777/open-crypto-puzzles/issues/1
- Real Big Block escrow funding transaction (current), mempool.space, 2019-07-30: https://mempool.space/tx/a1916e7ed9eac3fcc56a55056328cb09d06925e2694f2e6720de12b228514d1f
- Real Big Block escrow funding transaction (superseded), mempool.space, 2019-07-24: https://mempool.space/tx/499bcd420c7f662d2513b440aedd29c4fa829d6c9edb90dfc545e9305466d49f
- Block 76 solving transaction, mempool.space, 2026-08-17: https://mempool.space/tx/2e271ac2f63f488cd14112bceeed56f159ecd98cb3ce753f08e2d94bb62714a3
- Block 77 Stage One escrow (certification reference, solved and swept 2019-08-03), mempool.space: https://mempool.space/address/19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN
- Hal Finney, "Bitcoin and me", bitcointalk topic 155054 (source text for the Stage One certification reference, not reproduced here): https://bitcointalk.org/index.php?topic=155054.0
