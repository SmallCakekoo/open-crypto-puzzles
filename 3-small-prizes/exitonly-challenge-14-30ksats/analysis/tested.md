# Negatives and findings ledger, Exitonly Bitcoin Challenge 14

Tracks work done against README.md's open lead #1: "solve episode #12 and compare its seed
to #13 to test for a weak or correlated random source." No candidate mnemonic has been
tested against Challenge 14's own escrow from this line of work; everything below is
information gathering about Challenges 12 and 13, both already spent.

## 2026-08-19: locating and auditing Challenge 12 and 13

| # | What was checked | Method | Result |
|---|---|---|---|
| 1 | Whether this repository holds Challenge 12/13 folders, solved seeds, or generator/RNG source code for this series | `grep`/`find` across the full repository tree and git log | none found; this repository only catalogs Challenge 14. No puzzle-generator or RNG source code exists anywhere in the repo (checked, matches expectation: this is a third-party catalog of someone else's puzzles, not the Exitonly creator's own repository) |
| 2 | Challenge 12 and 13 video descriptions, via the channel's public video pages | browser session against `youtube.com`, reading `ytInitialData`/`ytInitialPlayerResponse` for description text and publish date | Challenge 12: escrow `bc1qvlp4u2ak7sdz0hvg5vrq7gg739hccg0pfr3cvq`, 9 of 12 words stated as known (3 missing), published 2024-09-17. Challenge 13: escrow `bc1qc8lqxj02c0nq98zkysdvrjr5g3ngh8fh9pv9ly`, 8 of 12 words stated as known (4 missing), published 2024-10-01. Neither description lists the words themselves (same pattern as Challenge 14: words are only in the video's audio/on-screen captions) |
| 3 | Whether Challenge 12 and 13's escrows are actually spent (i.e. genuinely "solved") | `mempool.space` API, address and transaction lookups (read-only, no funds touched) | both confirmed fully spent: Ch12 `funded_txo_sum == spent_txo_sum == 30,000` sats (spent 2024-09-30); Ch13 `funded_txo_sum == spent_txo_sum == 40,000` sats (spent 2024-10-02) |
| 4 | Whether the winning 12-word mnemonics for Ch12/Ch13 are published anywhere reachable (video captions, auto-generated captions, comments) | checked video description text, attempted the YouTube auto-caption (`asr`) track for Ch12 (returned empty, no ASR transcript available for this video), attempted to load the comments section (did not render in this session) | not found. No source reachable in this session contains the actual word content, for either the known-words list or the words that completed the solve |

## Conclusion for this open lead, as of 2026-08-19

**The complete solved mnemonics for Challenge 12 and Challenge 13 are not available.** This
confirms, independently, what README.md's open lead #2 already stated ("the complete solved
seeds of episodes #11, #12, and #13 are not recorded anywhere I have access to"). A Bitcoin
transaction never contains the spending mnemonic (only a public key and a signature), so no
amount of further on-chain analysis can recover it; it would have to be published somewhere
by whoever solved it, and no such publication was found.

Entropy/checksum/pattern comparison between Challenge 12 and 13 (README.md steps 3-4) cannot
be performed without this missing input. `analyze_known_seeds.py` in this folder is built and
tested (against the public BIP39 test vectors, `--demo`) and ready to run the moment a
complete solved mnemonic for either challenge becomes available from a legitimate source.

## 2026-08-20: pipeline rehearsal against already-spent episodes (Challenge 1, Challenge 6)

Purpose: validate the checksum -> BIP84 derivation -> address-compare pipeline end to end
against a real, zero-risk target before ever pointing it at Challenge 14's live escrow.
Method: `analyze_known_seeds.py`'s sibling `practice_range.py`, which tries the single
missing word in all 12 possible slots (not just the slot implied by the source list),
keeping the given known words in their given relative order -- 24,576 raw candidates,
~1,536 checksum-valid, per episode.

| # | Target | Known words source | Candidates | Result |
|---|---|---|---|---|
| 1 | Challenge 1 escrow `bc1qnlj5s0ltkg4w3jr6f4jhd8yhr5hcpkat5fw33n` (spent 2024-09-02) | user-supplied transcription, missing-word count not officially confirmed by the video description (early template) | 1,530 checksum-valid | 0 matches |
| 2 | Challenge 6 escrow `bc1qcfwhwa20e4jl8dj3esl9egjpxrdaty96ac079y` (spent 2024-09-01) | user-supplied transcription; missing-word count of 1 IS officially confirmed by the video's own description ("11 out of the 12 words") | 1,535 checksum-valid | 0 matches |

Both runs completed in ~7.7s at ~3,190 candidates/sec, confirming the pipeline itself runs
correctly and fast at this scale. Neither reproduced the historical answer. Since Challenge
6's missing-word count is author-confirmed, the most likely explanations, in order, are: (a)
the user-supplied known-word transcription contains an error for one or more words, (b) the
known words' relative order is not actually preserved in the true mnemonic (a bigger,
792x-permutation search this session was not authorized to run), or (c) the escrow used a
non-canonical BIP84 account/address-index instead of `m/84'/0'/0'/0/0`. Not distinguished
between; needs either a verified re-transcription of the source video or explicit
authorization to widen the search before going further. This does not change anything about
Challenge 14 itself -- it is a methodology rehearsal, not a finding about the target puzzle.

## 2026-08-20: full-series destination clustering (who claims these prizes)

Extended the Ch12/Ch13 destination observation below to all 14 episodes. Located every
episode's escrow via the channel's video list, confirmed all of Challenges 1-13 are spent
on-chain, and read each spending transaction's destination address directly (raw API JSON,
not summarized) via `mempool.space`.

| Destination address | Episodes | Notes |
|---|---|---|
| `bc1q9sengmvxjqdkv3qyjrr4j0ewmq949yxp2kukud` | 1, 2, 5, 7, 8, 9, 10 | exactly 7 funding transactions on this address, matching all 7 episodes; fully drained onward since |
| `bc1qtx4fqx8nd5gqz9t83qftwqw55tmxaav7tz3xg0` | 11, 12, 13 | still holds all 97,525 sats unspent as of this check; the previously "not yet identified" third sweep in this address's history is Challenge 11's own escrow, `bc1qzlhrfaldw753q3e56edtdn048qa8gjm4pspg3s` |
| `bc1ql58295263dfnq307ml4x99tdwgxgpxsn7zys2f` | 3, 4 | this address has 28 unrelated funding transactions and 4.4M sats of lifetime volume, i.e. an actively used general wallet, not a single-purpose sweep address |
| `1NremNJ9zNHP4XzwHEF3BcVZuYoMnuzU3L` (legacy P2PKH) | 6 | the one episode whose proceeds did not go to a bech32 address |

A `WebSearch` for both cluster addresses by exact string returned no public writeup, tool,
or forum post naming either one. No identity or method was recoverable this way.

Conclusion: at most 3-4 distinct actors/wallets account for all 13 spent episodes, with one
wallet alone claiming 7 of the first 10. This is strong evidence the series has been resolved
by a small number of dedicated, fast actors rather than organically by many different
community members, and is relevant to how quickly a live episode should be expected to
disappear once its real search space becomes tractable. It says nothing about how the author
generates seeds and should not be read as evidence for or against the "shared generator"
hypothesis.
