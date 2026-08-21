"""
Exhaustive brute force over EVERY way to drop 10 of the 34 panels (keep the
other 24, in original panel order), using the single fixed word per panel
finalized 2026-08-20 (see analysis/leads.md, "Single definitive word per
panel, all 34, 2026-08-20" and analysis/SUMMARY_FOR_EXTERNAL_AI_2026-08-20.md).

This does NOT depend on guessing an intruder criterion at all -- it tries
every possible 10-panel drop, C(34,10) = 131,128,140 combinations, and checks
each resulting 24-word mnemonic against the escrow address via
tools/oracle.py. If the true answer is "drop exactly 10 of these 34 fixed
words, keep 24 in panel order," this run finds it for certain. The one thing
it depends on is that the single word chosen for each panel is actually
correct -- see the summary doc for the reasoning/judgment calls behind each
of the 34 picks, especially panels with a whole-word tie or no literal title
word at all (8, 13, 14, 20, 24, 26, 30, 32, 33, 34 and others).

Combinations are addressed directly by rank via the combinatorial number
system (unrank_combination), the same "compute the N-th combination directly,
no need to skip through the first N-1" trick the other bruteforce_*_mp.py
scripts use for Cartesian products, adapted here for combinations. This is
what makes chunking the work across workers cheap.

Usage (from repo root, with the project venv active):
    python analysis/bruteforce_all_10of34.py --workers 10

Prints progress periodically and stops immediately with the match printed if
one is found. Exits 0 on match, 1 on exhaustion with no match.
"""

from __future__ import annotations

import argparse
import multiprocessing as mp
import os
import sys
import time
from math import comb

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO_ROOT, "tools"))

# Single fixed word per panel, panel order 1..34 (index 0 = panel 1).
# See analysis/leads.md, "Single definitive word per panel, all 34, 2026-08-20".
WORDS: list[str] = [
    "hard", "glory", "alien", "mad", "alien", "now", "escape", "chunk", "art",
    "possible", "ill", "life", "milk", "mask", "river", "visit", "orange",
    "hope", "gravity", "first", "solar", "blade", "galaxy", "close", "bar",
    "tornado", "day", "cream", "matrix", "toy", "ghost", "whip", "hotel",
    "human",
]
assert len(WORDS) == 34

N = 34
K = 10  # number dropped; 24 kept
TOTAL = comb(N, K)


def unrank_combination(n: int, k: int, rank: int) -> list[int]:
    """Return the `rank`-th (0-indexed, lex order) k-combination of range(n)."""
    result = []
    element = 0
    for i in range(k):
        while True:
            c = comb(n - element - 1, k - i - 1)
            if rank < c:
                result.append(element)
                element += 1
                break
            rank -= c
            element += 1
    return result


def _worker_init() -> None:
    global oracle
    import oracle as _oracle  # noqa: PLC0415

    oracle = _oracle


def _check_rank_range(args: tuple[int, int]) -> tuple[str, str, str, tuple[int, ...]] | None:
    start, end = args
    for rank in range(start, end):
        drop = set(unrank_combination(N, K, rank))
        keep_words = [WORDS[i] for i in range(N) if i not in drop]
        mnemonic = " ".join(keep_words)
        matched, addr, path = oracle.check(mnemonic)
        if matched:
            dropped_panels = tuple(sorted(i + 1 for i in drop))
            return mnemonic, addr, path, dropped_panels
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=10)
    parser.add_argument("--chunk", type=int, default=100_000)
    args = parser.parse_args()

    print(f"Total combinations: C(34,10) = {TOTAL:,}", flush=True)
    print(f"Workers: {args.workers}, chunk size: {args.chunk:,}", flush=True)

    _worker_init()
    if not oracle.selftest():
        print("oracle selftest FAILED -- aborting", flush=True)
        return 2
    print("selftest OK", flush=True)

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
        for i, result in enumerate(pool.imap_unordered(_check_rank_range, ranges), start=1):
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
                    f"  ...~{min(checked, TOTAL):,}/{TOTAL:,} "
                    f"({elapsed:.0f}s elapsed, ~{rate:.0f}/s, ETA ~{eta:.0f}s)",
                    flush=True,
                )

    elapsed = time.time() - start_time
    print(f"Done in {elapsed:.1f}s", flush=True)
    if match:
        mnemonic, addr, path, dropped_panels = match
        print("MATCH FOUND!", flush=True)
        print("Mnemonic:", mnemonic, flush=True)
        print("Address:", addr, flush=True)
        print("Path:", path, flush=True)
        print("Dropped panels (intruders):", dropped_panels, flush=True)
        return 0
    print(f"NO MATCH across all {TOTAL:,} combinations.", flush=True)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
