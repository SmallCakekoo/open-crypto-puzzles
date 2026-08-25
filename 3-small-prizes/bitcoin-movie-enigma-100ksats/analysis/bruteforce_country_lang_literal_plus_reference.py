"""
Bounded brute force under the "single country of origin AND single language"
intruder hypothesis (the original leading hypothesis, see tested.md,
"Pairwise two-field combination sweep"), using the same "literal title
substring(s) + one thematic reference word" candidate table approach as the
Connections and single-writer-credit runs above (both 0 matches).

Intruders (10, dropped): panels 4, 7, 9, 15, 18, 24, 26, 28, 30, 31 (Mad Max,
Escape from Alcatraz, Spartacus, The Crimson Rivers, Star Wars: A New Hope,
Close Encounters of the Third Kind, Sharknado, Scream 2, Toy Story 2,
Ghostbusters II).

Sourcing status per panel's reference word: same caveats as the other two
literal-plus-reference runs -- panels 8, 13, 32, 33 (26/Sharknado is dropped
here, so its word doesn't matter) use IMDb-sourced reference words; the rest
are thematic judgment calls, BIP39-checked but not IMDb-keyword-verified.

Total space: 2,149,908,480 candidates.

Usage (from repo root, with the project venv active):
    python analysis/bruteforce_country_lang_literal_plus_reference.py --workers 10

Checkpointing: same mechanism as the other bruteforce_*.py scripts in this
directory.
"""

from __future__ import annotations

import argparse
import multiprocessing as mp
import os
import sys
import time

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO_ROOT, "tools"))

CANDIDATES: list[tuple[str, list[str]]] = [
    ("1 Die Hard", ["hard", "tower"]),
    ("2 Paths of Glory", ["glory", "path", "trial"]),
    ("3 Aliens", ["alien", "marine"]),
    ("5 Alien", ["alien", "chest"]),
    ("6 Apocalypse Now", ["now", "jungle"]),
    ("8 The Goonies", ["chunk", "gold"]),
    ("10 Mission: Impossible", ["miss", "possible", "agent"]),
    ("11 Godzilla", ["ill", "lizard"]),
    ("12 Life of Pi", ["life", "tiger"]),
    ("13 Leon: The Professional", ["milk", "gun"]),
    ("14 The Man in the Iron Mask", ["man", "iron", "mask", "twin"]),
    ("16 The Visitors", ["visit", "time"]),
    ("17 A Clockwork Orange", ["orange", "work", "prison"]),
    ("19 Gravity", ["gravity", "orbit"]),
    ("20 First Man", ["first", "man", "moon"]),
    ("21 Solaris", ["solar", "ocean"]),
    ("22 Blade Runner 2049", ["blade", "run", "robot"]),
    ("23 Guardians of the Galaxy", ["galaxy", "guard", "raccoon"]),
    ("25 Barry Lyndon", ["bar", "fortune"]),
    ("27 Terminator 2: Judgment Day", ["day", "term", "metal"]),
    ("29 The Matrix Reloaded", ["matrix", "load", "machine"]),
    ("32 Raiders of the Lost Ark", ["whip", "snake"]),
    ("33 The Shining", ["hotel", "mirror"]),
    ("34 The Human Centipede (First Sequence)", ["human", "first", "man", "tip", "doctor"]),
]

assert len(CANDIDATES) == 24, f"expected 24 keeper panels, got {len(CANDIDATES)}"

OPTION_LISTS = [opts for _name, opts in CANDIDATES]
TOTAL = 1
for _opts in OPTION_LISTS:
    TOTAL *= len(_opts)


def _worker_init() -> None:
    global oracle
    import oracle as _oracle  # noqa: PLC0415

    oracle = _oracle


def _check_index_range(args: tuple[int, int]) -> tuple[int, tuple[str, str, str] | None]:
    start, end = args
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
            return start, (mnemonic, addr, path)
        count += 1
        for i in range(len(sizes) - 1, -1, -1):
            digits[i] += 1
            if digits[i] < sizes[i]:
                combo[i] = OPTION_LISTS[i][digits[i]]
                break
            digits[i] = 0
            combo[i] = OPTION_LISTS[i][0]
    return start, None


_DEFAULT_CHECKPOINT = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".country_lang_literal_plus_reference_checkpoint.txt")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=10)
    parser.add_argument("--chunk", type=int, default=200_000)
    parser.add_argument("--checkpoint", type=str, default=_DEFAULT_CHECKPOINT)
    args = parser.parse_args()

    print(f"Total combinations: {TOTAL:,}", flush=True)
    print(f"Workers: {args.workers}, chunk size: {args.chunk:,}", flush=True)
    print(f"Checkpoint file: {args.checkpoint}", flush=True)

    _worker_init()
    if not oracle.selftest():
        print("oracle selftest FAILED -- aborting", flush=True)
        return 2
    print("selftest OK", flush=True)

    done_starts: set[int] = set()
    if os.path.exists(args.checkpoint):
        with open(args.checkpoint, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    done_starts.add(int(line))
        print(f"Resuming: {len(done_starts):,} chunks already done per checkpoint file", flush=True)

    all_ranges = []
    pos = 0
    while pos < TOTAL:
        end = min(pos + args.chunk, TOTAL)
        all_ranges.append((pos, end))
        pos = end

    ranges = [r for r in all_ranges if r[0] not in done_starts]
    already_checked = (len(all_ranges) - len(ranges)) * args.chunk
    print(f"{len(ranges):,}/{len(all_ranges):,} chunks remaining to check", flush=True)

    start_time = time.time()
    checked = already_checked
    match = None
    checkpoint_f = open(args.checkpoint, "a", buffering=1)
    try:
        with mp.Pool(processes=args.workers, initializer=_worker_init) as pool:
            for i, (start, result) in enumerate(pool.imap_unordered(_check_index_range, ranges), start=1):
                checked += args.chunk
                if result is not None:
                    match = result
                    pool.terminate()
                    break
                checkpoint_f.write(f"{start}\n")
                if i % 20 == 0:
                    elapsed = time.time() - start_time
                    rate = (checked - already_checked) / elapsed if elapsed else 0
                    remaining = TOTAL - checked
                    eta = remaining / rate if rate else float("inf")
                    print(
                        f"  ...~{min(checked, TOTAL):,}/{TOTAL:,} chunks done "
                        f"({elapsed:.0f}s elapsed this run, ~{rate:.0f}/s, ETA ~{eta:.0f}s)",
                        flush=True,
                    )
    finally:
        checkpoint_f.close()

    elapsed = time.time() - start_time
    print(f"Done in {elapsed:.1f}s (this run)", flush=True)
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
    raise SystemExit(main())
