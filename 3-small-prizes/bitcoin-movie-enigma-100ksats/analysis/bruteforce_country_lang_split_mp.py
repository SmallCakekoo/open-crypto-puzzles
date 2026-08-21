"""
Multiprocess brute-force of the "single country + single language" intruder-set
hypothesis (see analysis/tested.md, "First end-to-end derivation attempt against
the country+language-split hypothesis" and the widened-candidates follow-up entry,
both 2026-08-20).

Intruders (10, dropped): panels 4, 7, 9, 15, 18, 24, 26, 28, 30, 31.
Keepers (24, in panel order) and their candidate words below -- 15 fixed by a
single literal BIP39 substring from data/films.csv, 6 with multiple tied literal
substrings (all included), 4 with zero literal substring where non-literal
candidates were sourced from this film's own IMDb keywords/reviews already
collected in this session (never free-associated from memory alone). Total space:
~38.9 million candidates.

Usage (from repo root, with the project venv active):
    python analysis/bruteforce_country_lang_split_mp.py [--workers N]

Prints progress every ~2M candidates per worker-chunk boundary and stops
immediately with the match printed if one is found. Exits 0 on match, 1 on
exhaustion with no match (mirrors tools/oracle.py's convention).
"""

from __future__ import annotations

import argparse
import itertools
import multiprocessing as mp
import os
import sys
import time

# Make tools/oracle.py importable regardless of CWD.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO_ROOT, "tools"))

CANDIDATES: list[tuple[str, list[str]]] = [
    ("1 Die Hard", ["hard"]),
    ("2 Paths of Glory", ["glory", "path", "soldier", "battle", "general", "pistol"]),
    ("3 Aliens", ["alien"]),
    ("5 Alien", ["alien"]),
    ("6 Apocalypse Now", ["now"]),
    ("8 The Goonies", ["one", "brand", "chunk", "gold", "cave", "beach", "rescue"]),
    ("10 Mission: Impossible", ["miss", "possible", "train", "spy", "gadget", "escape", "bomb", "magic", "subway"]),
    ("11 Godzilla", ["ill"]),
    ("12 Life of Pi", ["life"]),
    ("13 Leon: The Professional", ["milk", "gun"]),
    ("14 The Man in the Iron Mask", ["man", "iron", "mask", "twin", "guard", "river", "horse"]),
    ("16 The Visitors", ["visit"]),
    ("17 A Clockwork Orange", ["clock", "orange", "range", "work", "chair"]),
    ("19 Gravity", ["gravity"]),
    ("20 First Man", ["first", "man", "moon", "rocket", "marriage"]),
    ("21 Solaris", ["solar"]),
    ("22 Blade Runner 2049", ["blade"]),
    ("23 Guardians of the Galaxy", ["galaxy"]),
    ("25 Barry Lyndon", ["bar"]),
    ("27 Terminator 2: Judgment Day", ["day"]),
    ("29 The Matrix Reloaded", ["matrix"]),
    ("32 Raiders of the Lost Ark", ["whip", "snake", "gold", "hat", "horse", "ship", "knife"]),
    ("33 The Shining", ["hotel", "maze", "snow", "ghost", "mirror", "blood"]),
    ("34 The Human Centipede (First Sequence)", ["human", "first", "man", "doctor", "mask", "illness", "cabin"]),
]

assert len(CANDIDATES) == 24, f"expected 24 keeper panels, got {len(CANDIDATES)}"

OPTION_LISTS = [opts for _name, opts in CANDIDATES]
TOTAL = 1
for _opts in OPTION_LISTS:
    TOTAL *= len(_opts)


def _worker_init() -> None:
    # Each process imports its own copy; bip_utils/oracle have no shared state.
    global oracle
    import oracle as _oracle  # noqa: PLC0415

    oracle = _oracle


def _check_index_range(args: tuple[int, int]) -> tuple[str, str, str] | None:
    """Check candidate indices [start, end) of the full Cartesian product.
    Returns (mnemonic, address, path) on a match, else None."""
    start, end = args
    # Recompute the mixed-radix digits for `start` directly (no need to skip
    # `start` items one at a time -- itertools.product has no seek, so we derive
    # the starting combination arithmetically from its flat index).
    sizes = [len(o) for o in OPTION_LISTS]
    idx = start
    digits = [0] * len(sizes)
    for i in range(len(sizes) - 1, -1, -1):
        digits[i] = idx % sizes[i]
        idx //= sizes[i]

    combo = [OPTION_LISTS[i][digits[i]] for i in range(len(sizes))]
    count = start
    while count < end:
        mnemonic = " ".join(combo)
        matched, addr, path = oracle.check(mnemonic)
        if matched:
            return mnemonic, addr, path
        count += 1
        # odometer increment (rightmost digit fastest, matches itertools.product order)
        for i in range(len(sizes) - 1, -1, -1):
            digits[i] += 1
            if digits[i] < sizes[i]:
                combo[i] = OPTION_LISTS[i][digits[i]]
                break
            digits[i] = 0
            combo[i] = OPTION_LISTS[i][0]
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=os.cpu_count() or 4)
    parser.add_argument("--chunk", type=int, default=200_000, help="candidates per task sent to a worker")
    args = parser.parse_args()

    print(f"Total combinations: {TOTAL:,}", flush=True)
    print(f"Workers: {args.workers}, chunk size: {args.chunk:,}", flush=True)

    # Selftest first, fail fast if the environment/oracle is broken.
    _worker_init()
    if not oracle.selftest():
        print("oracle selftest FAILED -- aborting", flush=True)
        return 2

    ranges = []
    pos = 0
    while pos < TOTAL:
        end = min(pos + args.chunk, TOTAL)
        ranges.append((pos, end))
        pos = end

    start_time = time.time()
    checked = 0
    match = None
    with mp.Pool(processes=args.workers, initializer=_worker_init) as pool:
        for i, result in enumerate(pool.imap_unordered(_check_index_range, ranges), start=1):
            checked += args.chunk
            if result is not None:
                match = result
                pool.terminate()
                break
            if i % 20 == 0:
                elapsed = time.time() - start_time
                rate = checked / elapsed if elapsed else 0
                eta = (TOTAL - checked) / rate if rate else float("inf")
                print(
                    f"  ...~{min(checked, TOTAL):,}/{TOTAL:,} chunks done "
                    f"({elapsed:.0f}s elapsed, ~{rate:.0f}/s, ETA ~{eta:.0f}s)",
                    flush=True,
                )

    elapsed = time.time() - start_time
    print(f"Done in {elapsed:.1f}s", flush=True)
    if match:
        mnemonic, addr, path = match
        print("MATCH FOUND!", flush=True)
        print("Mnemonic:", mnemonic, flush=True)
        print("Address:", addr, flush=True)
        print("Path:", path, flush=True)
        return 0
    print(f"NO MATCH across all {TOTAL:,} combinations.", flush=True)
    return 1


if __name__ == "__main__":
    # Required on Windows: multiprocessing uses spawn, which re-imports this
    # module in each child -- everything above this guard must be safe to
    # import without side effects, which it is (CANDIDATES etc. are just data).
    raise SystemExit(main())
