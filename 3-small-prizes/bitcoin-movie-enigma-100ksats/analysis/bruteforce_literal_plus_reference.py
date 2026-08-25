"""
Bounded brute force under the IMDb Connections intruder hypothesis (see
tested.md, "NEW CRITERION FOUND..."), using a "literal word(s) + one sourced
reference word" candidate table per keeper panel instead of full keyword
lists. Per the user's request 2026-08-21: cap each panel at 2-4 candidates
(its literal title substring(s), plus one thematic "reference" word) rather
than the much larger full-keyword-list spaces already exhausted with 0
matches.

Intruders (10, dropped): panels 7, 10, 12, 14, 20, 21, 22, 25, 31, 34.

Sourcing status per panel's reference word, spelled out here since it
matters for how much weight a match (or lack of one) should carry:
- Panels 8, 13, 26, 32, 33: reference words are the same ones already
  sourced from real IMDb keywords/reviews/AKA titles earlier in this
  investigation (see leads.md).
- All other panels' reference words (tower, trial, marine, fuel, chest,
  jungle, arena, lizard, mountain, time, prison, force, orbit, raccoon,
  tower, metal, mask, machine, cowboy) are the user's/assistant's own
  thematic judgment calls, NOT yet verified against each film's actual IMDb
  keyword page. Flagged as such -- a match here would still need that
  verification before being trusted the way a literal-substring match would
  be trusted outright.

Total space: 286,654,464 candidates.

Usage (from repo root, with the project venv active):
    python analysis/bruteforce_literal_plus_reference.py --workers 6

Checkpointing: same mechanism as bruteforce_connections_criterion_full.py --
completed chunk-start indices are appended to a checkpoint file next to this
script; re-running with the same --chunk size resumes instead of restarting.
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
    ("4 Mad Max", ["mad", "fuel"]),
    ("5 Alien", ["alien", "chest"]),
    ("6 Apocalypse Now", ["now", "jungle"]),
    ("8 The Goonies", ["chunk", "gold"]),
    ("9 Spartacus", ["art", "arena"]),
    ("11 Godzilla", ["ill", "lizard"]),
    ("13 Leon: The Professional", ["milk", "gun"]),
    ("15 The Crimson Rivers", ["river", "mountain"]),
    ("16 The Visitors", ["visit", "time"]),
    ("17 A Clockwork Orange", ["orange", "work", "prison"]),
    ("18 Star Wars: A New Hope", ["hope", "force"]),
    ("19 Gravity", ["gravity", "orbit"]),
    ("23 Guardians of the Galaxy", ["galaxy", "guard", "raccoon"]),
    ("24 Close Encounters of the Third Kind", ["close", "kind", "tower"]),
    ("26 Sharknado", ["tornado", "ski"]),
    ("27 Terminator 2: Judgment Day", ["day", "term", "metal"]),
    ("28 Scream 2", ["cream", "mask"]),
    ("29 The Matrix Reloaded", ["matrix", "load", "machine"]),
    ("30 Toy Story 2", ["story", "toy", "cowboy"]),
    ("32 Raiders of the Lost Ark", ["whip", "snake"]),
    ("33 The Shining", ["hotel", "mirror"]),
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


_DEFAULT_CHECKPOINT = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".literal_plus_reference_checkpoint.txt")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=6)
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
