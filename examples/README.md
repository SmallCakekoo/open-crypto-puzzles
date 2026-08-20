# BIP39 learning lab

Small, self-contained scripts to understand the BIP39 -> BIP32 -> BIP84 pipeline before
using it against any real puzzle. Nothing here touches funds, broadcasts anything, or reads
a real seed phrase. This folder is a companion to
[`3-small-prizes/exitonly-challenge-14-30ksats/`](../3-small-prizes/exitonly-challenge-14-30ksats/),
which has its own `analysis/search_space.py` and `tools/candidate_checker.py` for that
specific puzzle.

## Setup

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
```
macOS/Linux:
```bash
.venv/bin/python -m pip install -r requirements.txt
```

The dependency list is `tools/requirements.txt` at the repository root (this repo's shared
list); the root `requirements.txt` just points pip at it, so there is one file to update.

## Scripts

| Script | What it does |
|---|---|
| `bip39_demo.py` | Generates fresh random TEST entropy, walks it through mnemonic -> seed -> BIP84 derivation -> address, printing every intermediate value. |
| `bip39_validate.py` | Checks a phrase against the three BIP39 rules (word count, wordlist membership, checksum) and says which one failed. |
| `benchmark.py` | Times a small (default 2,000, capped at 20,000) batch of full BIP39-to-address derivations and projects how long larger hypothetical spaces would take at that rate. Does not run those larger spaces. |

Run them with:

```bash
python examples/bip39_demo.py
python examples/bip39_validate.py "your test phrase here"
python examples/benchmark.py
```

## How the BIP39 checksum works

A 12-word English mnemonic encodes 132 bits total:

1. **128 bits of entropy (ENT)**, normally random.
2. **4 bits of checksum (CS)**, computed as the first `ENT / 32 = 4` bits of
   `SHA-256(entropy)`.
3. Entropy and checksum are concatenated (`ENT || CS` = 132 bits) and split into 12 groups
   of 11 bits. Each 11-bit group is an index (0-2047) into the 2048-word English wordlist.

So words 1-11 carry the first 121 bits of entropy in full; word 12 carries the last 7 bits
of entropy plus the 4 checksum bits. This has a direct consequence for guessing: **if words
1-11 are fixed, only 1 in 16 of the 2048 possible word-12 choices will produce a matching
checksum** (4 checksum bits = 16 possible values, only one of which is correct for a given
entropy). `examples/bip39_validate.py` shows this rule failing explicitly when you flip the
last word of a valid phrase; `3-small-prizes/exitonly-challenge-14-30ksats/analysis/search_space.py`
uses this same fact (division by 16) to size that puzzle's real search space.

The general word count / entropy table:

| Words | Entropy bits (ENT) | Checksum bits (CS) | Total bits |
|---|---|---|---|
| 12 | 128 | 4 | 132 |
| 15 | 160 | 5 | 165 |
| 18 | 192 | 6 | 198 |
| 21 | 224 | 7 | 231 |
| 24 | 256 | 8 | 264 |

The checksum does **not** make brute-forcing a partial mnemonic hard by itself -- 1-in-16 is
a small filter. What makes it expensive is the sheer size of `2048^k` for `k` unknown words,
combined with the cost per candidate of PBKDF2-HMAC-SHA512 (mnemonic -> seed, 2048 rounds)
and the elliptic-curve work to go from seed to address.

## SECURITY

- Never enter a real seed phrase into any script in this repository, including these
  examples. They are for TEST data only (`os.urandom`, or a fixed `--entropy-hex` you chose
  for reproducibility).
- Never enter a real private key anywhere in this environment.
- Never save credentials, seed phrases, or private keys to disk, logs, or scrollback that
  might be shared or committed.
- Never run a script pulled from the internet without reading it first, especially anything
  claiming to "check" or "recover" a seed phrase.
- Never send funds, sign a transaction, or run a command that spends from any address while
  testing or learning.
- Never publish, paste, or commit a private key, even one found legitimately while solving a
  puzzle. Hand it to a human to sweep first.
- Never use a personal wallet's real seed as a test fixture, even temporarily.
- Keep all testing on data generated locally for that purpose; a matching candidate for a
  real puzzle should go through the puzzle's own `tools/oracle.py`, and any resulting key
  material stays local until a human decides what to do with it.
