"""
10-worker multiprocess companion to bruteforce_all_criterion_hits.py.

Same 15 exact-10 criterion hits, same word candidates (literal substrings +
curated top-5 for the zero-literal panels), same mixed-radix chunked worker
approach as bruteforce_country_lang_split_mp.py, generalized to loop over
multiple hypotheses in one run. Used to finish the last 6 of the 15
hypotheses after the single-thread run (see analysis/tested.md, "All 17
exact-10 criterion hits derivation-tested... 2026-08-20") was interrupted
partway through by the user, who was free and offered more CPU -- 10 of 12
cores, 2 held back as headroom (see the freeze-incident note on the original
38.9M run; only safe to use more workers when the machine isn't also under
video-call load).

Result of the 2026-08-20 run (all 15 hypotheses, combining the single-thread
run's first 9 with this script's remaining 6): 0 matches across every one.

Usage (from repo root, with the project venv active):
    python analysis/bruteforce_all_criterion_hits_mp.py [--workers N]
"""

from __future__ import annotations

import argparse
import itertools
import multiprocessing as mp
import os
import sys
import time

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO_ROOT, "tools"))

LITERAL: dict[int, list[str] | None] = {
    1: ["hard"], 2: ["glory", "path"], 3: ["alien"], 4: ["mad"], 5: ["alien"],
    6: ["now"], 7: ["escape", "cat"], 8: None, 9: ["art"],
    10: ["miss", "possible"], 11: ["ill"], 12: ["life"], 13: None,
    14: ["man", "iron", "mask"], 15: ["river"], 16: ["visit"],
    17: ["clock", "lock", "orange", "range", "work"], 18: ["hope"],
    19: ["gravity"], 20: ["first", "man"], 21: ["solar"], 22: ["blade", "run"],
    23: ["galaxy", "guard"], 24: ["close", "kind"], 25: ["bar"], 26: None,
    27: ["day", "term"], 28: ["cream"], 29: ["matrix", "load"],
    30: ["story", "toy"], 31: ["ghost", "host", "bus"], 32: None, 33: None,
    34: ["human", "first", "man", "tip"],
}
TOP5: dict[int, list[str]] = {
    8: ["chunk", "gold", "cave", "piano", "skull"],
    13: ["milk", "gun", "shield", "pistol", "crush"],
    26: ["tornado", "fish", "dog", "beach", "gun"],
    32: ["whip", "snake", "hat", "spider", "torch"],
    33: ["hotel", "mirror", "blood", "ghost", "door"],
}


def candidates(panel: int) -> list[str]:
    return LITERAL[panel] if LITERAL[panel] is not None else TOP5[panel]


ALL34 = set(range(1, 35))

HYPOTHESES: dict[str, list[int]] = {
    "nom_or_won_oscar AND prodco>=3": [1, 5, 12, 17, 19, 20, 22, 23, 25, 27],
    "genres==2 OR bw": [1, 2, 5, 16, 17, 21, 24, 28, 29, 33],
    "genres==3 AND single_lang": [4, 7, 15, 18, 20, 22, 23, 26, 30, 31],
    "single_lang AND prodco>=3": [4, 5, 15, 17, 20, 22, 23, 26, 28, 33],
    "certPG13 OR bw": [2, 10, 11, 14, 16, 17, 19, 20, 21, 23],
    "certPG13 OR thriller": [1, 10, 11, 14, 15, 16, 19, 20, 21, 23],
    "bw OR scifi": [2, 4, 5, 11, 17, 19, 21, 24, 27, 29],
    "bw OR budget>=100M": [2, 11, 12, 17, 19, 21, 22, 23, 27, 29],
    "action1st AND aspect239": [1, 4, 10, 11, 13, 22, 23, 27, 29, 31],
    "thriller OR horror": [1, 3, 5, 10, 11, 15, 19, 28, 33, 34],
    "thriller OR runtime<100": [1, 2, 4, 10, 11, 15, 19, 26, 30, 34],
    "thriller OR budget>=100M": [1, 10, 11, 12, 15, 19, 22, 23, 27, 29],
    "thriller OR budget<10M": [1, 2, 4, 7, 10, 11, 15, 17, 19, 26],
    "horror OR runtime<100": [2, 3, 4, 5, 19, 26, 28, 30, 33, 34],
    "horror OR budget<10M": [2, 3, 4, 5, 7, 17, 26, 28, 33, 34],
}


def _worker_init() -> None:
    global oracle
    import oracle as _oracle  # noqa: PLC0415

    oracle = _oracle


def _check_range(args: tuple[list[list[str]], int, int]) -> tuple[str, str, str] | None:
    option_lists, start, end = args
    sizes = [len(o) for o in option_lists]
    idx = start
    digits = [0] * len(sizes)
    for i in range(len(sizes) - 1, -1, -1):
        digits[i] = idx % sizes[i]
        idx //= sizes[i]
    combo = [option_lists[i][digits[i]] for i in range(len(sizes))]
    count = start
    while count < end:
        mnemonic = " ".join(combo)
        matched, addr, path = oracle.check(mnemonic)
        if matched:
            return mnemonic, addr, path
        count += 1
        for i in range(len(sizes) - 1, -1, -1):
            digits[i] += 1
            if digits[i] < sizes[i]:
                combo[i] = option_lists[i][digits[i]]
                break
            digits[i] = 0
            combo[i] = option_lists[i][0]
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=max((os.cpu_count() or 4) - 2, 1))
    parser.add_argument("--chunk", type=int, default=200_000)
    args = parser.parse_args()

    _worker_init()
    if not oracle.selftest():
        print("SELFTEST FAILED -- aborting", flush=True)
        return 2
    print(f"selftest OK, workers={args.workers}", flush=True)

    for hname, dropped in HYPOTHESES.items():
        keep = sorted(ALL34 - set(dropped))
        option_lists = [candidates(p) for p in keep]
        total = 1
        for o in option_lists:
            total *= len(o)
        print(f"\n=== {hname} | dropped={sorted(dropped)} | space={total:,} ===", flush=True)

        ranges = []
        pos = 0
        while pos < total:
            end = min(pos + args.chunk, total)
            ranges.append((option_lists, pos, end))
            pos = end

        t0 = time.time()
        checked = 0
        match = None
        with mp.Pool(processes=args.workers, initializer=_worker_init) as pool:
            for i, result in enumerate(pool.imap_unordered(_check_range, ranges), start=1):
                checked += args.chunk
                if result is not None:
                    match = result
                    pool.terminate()
                    break
                if i % 10 == 0:
                    elapsed = time.time() - t0
                    rate = checked / elapsed if elapsed else 0
                    print(f"  ...~{min(checked, total):,}/{total:,} ({elapsed:.0f}s, ~{rate:.0f}/s)", flush=True)
        elapsed = time.time() - t0
        if match:
            mnemonic, addr, path = match
            print(f"  *** MATCH FOUND for '{hname}' ***", flush=True)
            print("  Mnemonic:", mnemonic, flush=True)
            print("  Address:", addr, flush=True)
            print("  Path:", path, flush=True)
            return 0
        print(f"  no match ({elapsed:.0f}s)", flush=True)

    print("\nAll hypotheses done, no match.", flush=True)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
