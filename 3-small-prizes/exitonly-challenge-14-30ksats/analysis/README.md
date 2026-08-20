# Local analysis tools for Challenge 14

This folder holds local, non-published tooling built on top of the puzzle's own
[`README.md`](../README.md) and [`tools/oracle.py`](../tools/oracle.py). It does not change
the puzzle's official facts, and no search has been run from here.

| File | What it does | What it does not do |
|---|---|---|
| `search_space.py` | Computes the size of the candidate space from the known facts (7/12 words given) under two position assumptions, and shows the arithmetic behind each factor. | Does not generate or test a single candidate. |
| [`../tools/candidate_checker.py`](../tools/candidate_checker.py) | Given one full 12-word candidate, prints CHECKSUM / DERIVATION PATH / ADDRESS / TARGET / MATCH, reusing the same bip_utils calls as `tools/oracle.py`. | Does not loop over candidates, does not touch funds, does not broadcast anything. |
| `analyze_known_seeds.py` | Decodes two or more complete, already-solved mnemonics into indices/binary/entropy/checksum and computes objective pairwise comparisons (prefix/suffix match, XOR, Hamming distance) with stated thresholds, for the "shared generator" hypothesis (README.md open lead #1). `--demo` runs it on the public BIP39 test vectors. | Cannot run against Challenge 12/13 yet: no complete solved mnemonic for either is available from any source reached so far. See `tested.md`. |

See [`tested.md`](tested.md) for what has actually been checked against this open lead, with
dates and methods.

Run:

```bash
python 3-small-prizes/exitonly-challenge-14-30ksats/analysis/search_space.py
python 3-small-prizes/exitonly-challenge-14-30ksats/tools/candidate_checker.py --selftest
python 3-small-prizes/exitonly-challenge-14-30ksats/tools/candidate_checker.py "w1 w2 ... w12"
```

Per [AGENTS.md](../../../AGENTS.md), before any real search: write down N (space size, from
`search_space.py`), D (measured rate, from `examples/benchmark.py`), and t = N / D. The
puzzle's own README already estimates this space as economically out of reach of the prize
(see its "Established facts" section); nothing here changes that conclusion, it only makes
the arithmetic runnable and the single-candidate check auditable step by step.
