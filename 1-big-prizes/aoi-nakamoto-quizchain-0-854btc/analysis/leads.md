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

## 4. Speculative: the "-gry" wordplay behind the r/Grycoin name

**Status: speculative, no primary-source support, and partly contradicted by
the source text itself. Recorded for completeness, not recommended for
compute.**

Observation: the author named her own subreddit **r/Grycoin**, and in the Real
Big Block Discussion thread she wrote "I hope you are not anGRY any more"
(`data/realbigblock_full_thread_recovered.md:121`), capitalising G-R-Y inside
"angry" in a way that is hard to read as a typo. "-gry" is a well-known English
word riddle ("angry and hungry end in -gry; name the third such word"), famous
precisely for having no agreed answer — the trick lives in how the question is
worded, not in the vocabulary. That shape (a question whose real content is its
phrasing) matches this author's demonstrated style: she uses Atbash in the
series' introduction post, and the confirmed Stage One rule is itself a
first-letter wordplay (ITASM).

Evidence against, found while investigating it:

- The substring "gry" does **not** appear anywhere in the confirmed Real Big
  Block source chapter (part 720888559), in any case, including inside
  "angry"/"hungry". A selector or transform keyed on it has nothing to bind to.
- The "GRYcoin project" discussed at length in the same thread is a
  climate/carbon-credit coin proposal raised by a *commenter*
  (`data/realbigblock_full_thread_recovered.md:103`), not by the author; her
  "anGRY" line is a reply to that commenter's criticism, so the capitalisation
  reads at least as plausibly as a pun on their topic as on a cipher.
- "Grycoin" was already tested as a paragraph-selector word
  (`analysis/tested.md:21`), 0 match.
- No post in the 33-part Wattpad story or the recovered Reddit history
  explains the name "Grycoin" at all.

What would confirm it: a primary source in which the author connects "gry" to
the puzzle mechanism rather than to the coin proposal or to the joke.
What would kill it: nothing cleanly; it is already weak enough that absence of
further evidence is the expected outcome.
Cost: near zero to test the riddle's stock answers ("language", "say",
"agree") as selector words or TOMI strings, if only to close it out. Not worth
more than that.

## 5. Forensic: identify the hashing tool the author actually used

**This is a stronger lead than 4 and is newly opened.** Part 14 of the Wattpad
story ("Mistakes", part id 724275249, 2019-04-25) states verbatim: "The next
trap was unintended change of hashing algo to MD5. That happened because I
restarted my tablet and the hashing tool I use switched back to the default
(MD5)", and then: "I avoid this by the simple strategy of changing all hashes
to MD5, the default of the hashing tool."

Two things follow, one reassuring and one actionable:

- **MD5 is positively confirmed for Real Big Block**, not merely assumed. She
  standardised on MD5 in April 2019 precisely to eliminate algorithm drift;
  Real Big Block is July 2019, well after. This closes "maybe it was SHA-256"
  as a branch without needing to test it.
- **She hashed by pasting a string into a GUI hashing app on a tablet**, not
  via a scripted pipeline. That is the single most likely origin of the
  byte-level mismatch that has defeated approximately 291 million candidates
  so far. Mobile hashing apps differ in ways that are invisible to the user
  and fatal to a hash: some append a trailing newline to a multi-line text
  field, some normalise pasted CRLF to LF regardless of what the clipboard
  held, some hash the field as UTF-8 with BOM, some trim leading/trailing
  whitespace silently. Her asciivalue.com checks
  (`data/realbigblock_full_thread_recovered.md:168`) prove what the *clipboard*
  contained; they prove nothing about what the *hashing app* did with it
  afterwards.

This reframes the problem usefully: the remaining unknown may not be "which
paragraphs" (lead 1) at all, but "what did her app silently do to the bytes",
which is a much smaller and more structured space than a free selector search.

What would confirm it: identifying a 2019-era tablet hashing app with MD5 as
its default algorithm whose text-field handling, applied to the whole chapter
under `\r\n\r\n`, reproduces either target address.
What would kill it: exhausting the plausible app-behaviour transforms (trailing
newline, LF normalisation, BOM, whitespace trim, and their pairwise
combinations) against the whole chapter and the major sections with no match.
Note that several of these individually are already covered by the
edit-distance-1 sweep in lead 2; the untested part is their **combinations**,
which is also exactly the bounded 2-character space lead 2 proposes.
Cost: hours. The transform set is small and enumerable, unlike lead 1.

## 6. Untested transform family: transposition

Every test recorded in `analysis/tested.md` preserves the chapter's paragraph
order, selecting or transforming paragraphs in place. Order-changing transforms
(reversed paragraph order, section reordering, interleaving two halves) have
never been tried. This has no primary-source support and is listed only because
it is a genuine structural gap in the tested space rather than a new idea about
the author's intent — the same standard under which lead 4 is marked
speculative. Cheap to add to any existing sweep.

## Cryptographic techniques triaged against this puzzle

Recorded so future work does not re-derive it. Real Big Block is a
**single-preimage search**: find the exact byte string whose MD5 seeds a BIP39
mnemonic deriving a known P2PKH address. There is no protocol, no key exchange,
no ciphertext under an unknown key, and no signature to verify, so most of the
standard cryptography curriculum has no attachment point here.

Applicable, and either already used or worth using:

- **Substitution ciphers.** Confirmed in-universe: the author solves her own
  introduction block with Atbash ("apply the well known Atbash method",
  r/Grycoin `bry4fw`). Atbash/ROT-n over selector words is cheap and untried.
- **Transposition.** See lead 6 above.
- **Hash functions.** MD5 confirmed (lead 5). The 128-bit output matching BIP39
  128-bit entropy exactly is why the series uses it.
- **Brute force and dictionary attacks.** Already the main instrument;
  approximately 291 million candidates, all negative.
- **Side-channel attack, in the broad sense.** The productive work in the last
  two sessions has been exactly this: attacking the author's operational
  environment (Wattpad metadata, `modifyDate`, draft parts, her tablet's
  hashing app) rather than the hash. Lead 5 is a side-channel lead.

Not applicable, with the reason:

- **DES/3DES, AES, block-cipher modes (CBC/CTR/GCM), key management** — nothing
  in the puzzle is encrypted under a key; there is no ciphertext.
- **RSA, Diffie-Hellman, ECC as attack surfaces** — no key exchange occurs.
  secp256k1 is the substrate BIP44 derives over, not a target.
- **Digital signatures, certificates, PKI, certificate authorities** — nothing
  is signed or attested.
- **HMAC, password storage, nonces** — HMAC-SHA512 appears inside BIP32 key
  derivation, but as a fixed, already-certified step, not an attackable one.
- **HTTPS/TLS, SSH, VPN, web application cryptography, secure key exchange** —
  no live protocol is involved; the puzzle is static text and a static address.
- **Replay and man-in-the-middle attacks** — no session or channel exists.
- **Hash collisions** — a collision needs a known target digest to collide
  with. The target digest here is unknown (only the resulting *address* is
  known), so collision techniques cannot be pointed at anything. A preimage is
  required, and MD5 has no practical preimage break.
- **Post-quantum cryptography** — worth stating precisely, because it is the
  one branch people assume is a backdoor: `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W`
  is an **unspent P2PKH** address, so it publishes only HASH160 of the public
  key, never the public key itself. Shor's algorithm attacks a public key, so
  even a working quantum computer has nothing to attack until the address is
  spent. This branch is closed by construction, not by difficulty.
- **Zero-knowledge proofs** — a tool for proving knowledge without revealing
  it; it cannot produce knowledge nobody has.

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
