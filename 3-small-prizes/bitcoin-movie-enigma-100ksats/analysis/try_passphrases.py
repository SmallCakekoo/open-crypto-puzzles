"""
Tests a curated list of plausible BIP39 passphrases ("25th word") against
every checksum-valid 24-word candidate in the top-5-curated word space for
the IMDb Connections-self-reference intruder hypothesis (see
analysis/tested.md, "NEW CRITERION FOUND..." and "Full-word-space run
against the Connections-criterion hypothesis" for why this is the leading
hypothesis). The single fixed-word table alone fails the BIP39 checksum
outright (checksum depends only on the 24 words, not the passphrase, so no
passphrase can rescue a checksum-invalid combination) -- this widens to the
1,000,000-candidate top-5 space instead, filters to the ~1/256 of those that
pass checksum (a few thousand), and crosses each with every passphrase
candidate.

This is NOT an exhaustive search over passphrases -- a passphrase can be any
string, so there is no bounded space to exhaust the way there was for the
24-word candidates (a fixed 2048-word list) or the intruder criterion (a
bounded set of IMDb fields). This only tests a hand-picked list of
passphrases plausible given what's publicly known about the puzzle and its
author (see clues/author-posts.md): the author's handle/npub, phrases from
the rules text, the puzzle's own name/domain, and known dates. A negative
result here does not rule out a passphrase in general, only these specific
guesses, crossed with only the top-5-curated words (not the full secondary
tier) for the 5 zero-literal panels.

Usage:
    python analysis/try_passphrases.py
"""

from __future__ import annotations

import argparse
import itertools
import multiprocessing as mp
import os
import sys

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO_ROOT, "tools"))
import oracle  # noqa: E402
from bip_utils import Bip39MnemonicValidator  # noqa: E402

# Top-5 curated candidates per keeper panel under the Connections hypothesis
# (dropped: 7, 10, 12, 14, 20, 21, 22, 25, 31, 34), in panel order.
CANDIDATES: list[tuple[str, list[str]]] = [
    ("1 Die Hard", ["hard"]),
    ("2 Paths of Glory", ["glory", "path"]),
    ("3 Aliens", ["alien"]),
    ("4 Mad Max", ["mad"]),
    ("5 Alien", ["alien"]),
    ("6 Apocalypse Now", ["now"]),
    ("8 The Goonies", ["chunk", "gold", "cave", "piano", "skull"]),
    ("9 Spartacus", ["art"]),
    ("11 Godzilla", ["ill"]),
    ("13 Leon: The Professional", ["milk", "gun", "shield", "pistol", "crush"]),
    ("15 The Crimson Rivers", ["river"]),
    ("16 The Visitors", ["visit"]),
    ("17 A Clockwork Orange", ["clock", "lock", "orange", "range", "work"]),
    ("18 Star Wars: A New Hope", ["hope"]),
    ("19 Gravity", ["gravity"]),
    ("23 Guardians of the Galaxy", ["galaxy", "guard"]),
    ("24 Close Encounters of the Third Kind", ["close", "kind"]),
    ("26 Sharknado", ["tornado", "fish", "dog", "beach", "gun"]),
    ("27 Terminator 2: Judgment Day", ["day", "term"]),
    ("28 Scream 2", ["cream"]),
    ("29 The Matrix Reloaded", ["matrix", "load"]),
    ("30 Toy Story 2", ["story", "toy"]),
    ("32 Raiders of the Lost Ark", ["whip", "snake", "hat", "spider", "torch"]),
    ("33 The Shining", ["hotel", "mirror", "blood", "ghost", "door"]),
]
assert len(CANDIDATES) == 24
OPTION_LISTS = [opts for _name, opts in CANDIDATES]

PASSPHRASES = [
    "",  # baseline, already implicitly tested throughout -- confirms no passphrase changes this specific mnemonic's result
    "klems",
    "Klems",
    "KLEMS",
    "somehow",
    "Somehow",
    "enigma",
    "Enigma",
    "movie enigma",
    "Movie Enigma",
    "bitcoin movie enigma",
    "Bitcoin Movie Enigma",
    "bitcoinmovieenigma",
    "bitcoinmovieenigma.com",
    "npub10q5dpm5p05a0g3vtgcl76wv0pc4t820f5fj8qmpfaa4umv6404xqvwzvp0",
    "34",
    "intruders",
    "intruder",
    "somehow somehow",
    "giga brain",
    "gigabrain",
    "2022-04-08",
    "04/08/2022",
    "2024-01-03",
    "100000",
    "IMDB",
    "imdb",
    "IMBD",  # the author's own (mis-)spelling, quoted verbatim in the rules
]


def _worker_init() -> None:
    global oracle
    import oracle as _oracle  # noqa: PLC0415

    oracle = _oracle


def _check_one(args: tuple[str, str]) -> tuple[str, str, str] | None:
    mnemonic, pp = args
    addrs = oracle.addresses(mnemonic, pp)
    for path, addr in addrs.items():
        if addr == oracle.TARGET_ADDRESS:
            return mnemonic, pp, f"{path} | {addr}"
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    _worker_init()
    if not oracle.selftest():
        print("selftest FAILED", flush=True)
        return 2
    print("selftest OK", flush=True)

    total = 1
    for o in OPTION_LISTS:
        total *= len(o)
    print(f"Scanning {total:,} candidates for checksum-valid mnemonics...", flush=True)

    validator = Bip39MnemonicValidator()
    valid_mnemonics = []
    for combo in itertools.product(*OPTION_LISTS):
        mnemonic = " ".join(combo)
        if validator.IsValid(mnemonic):
            valid_mnemonics.append(mnemonic)
    print(f"Found {len(valid_mnemonics):,} checksum-valid mnemonics "
          f"(~1/256 expected: {total // 256:,})", flush=True)

    print(f"Testing {len(PASSPHRASES)} candidate passphrases against each, "
          f"{args.workers} workers...", flush=True)
    jobs = [(m, pp) for m in valid_mnemonics for pp in PASSPHRASES]
    total_checks = len(jobs)
    print(f"Total checks: {total_checks:,}", flush=True)

    checked = 0
    with mp.Pool(processes=args.workers, initializer=_worker_init) as pool:
        for i, result in enumerate(pool.imap_unordered(_check_one, jobs, chunksize=200), start=1):
            checked += 1
            if result is not None:
                mnemonic, pp, detail = result
                pool.terminate()
                print("\n*** FOUND IT ***")
                print("Mnemonic:", mnemonic)
                print("Passphrase:", repr(pp))
                print("Path | Address:", detail)
                return 0
            if checked % 5000 == 0:
                print(f"  ...{checked:,}/{total_checks:,} checked", flush=True)

    print(f"\nNo match across all {total_checks:,} (mnemonic, passphrase) combinations.", flush=True)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
