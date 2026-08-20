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

## Side observation (not evidence about seed generation, logged for context)

Both Challenge 12 and Challenge 13's spending transactions sent their proceeds to the same
address, `bc1qtx4fqx8nd5gqz9t83qftwqw55tmxaav7tz3xg0`. That address has received exactly 3
incoming transactions total: the Ch12 and Ch13 sweeps, plus a third 30,000-sat sweep from a
different address (`bc1qzlhrfaldw753q3e56edtdn048qa8gjm4pspg3s`, not yet identified) in the
same block as the Ch12 sweep. This says something about who claims prizes in this series (one
actor or bot appears to sweep multiple episodes in quick succession, sometimes batched in the
same block), not about how the author generates seeds; it does not bear on the "shared
generator" hypothesis and should not be read as evidence for or against it.
