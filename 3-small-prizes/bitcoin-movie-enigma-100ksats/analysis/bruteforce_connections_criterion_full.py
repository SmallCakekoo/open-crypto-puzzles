"""
Full-word-space multiprocess derivation test for the strongest intruder
criterion found so far: "this film has zero IMDb Connections-tab links
(References/Referenced in/Follows/Spoofed in/etc.) to any other film in this
specific 34-panel set." See analysis/tested.md, "NEW CRITERION FOUND: IMDb
Connections self-reference among the 34 panels, 2026-08-21" for the full
edge list and methodology, and analysis/SUMMARY_FOR_EXTERNAL_AI_2026-08-20.md
for background on the puzzle itself.

Intruders (10, dropped): panels 7, 10, 12, 14, 20, 21, 22, 25, 31, 34
(Escape from Alcatraz, Mission: Impossible, Life of Pi, The Man in the Iron
Mask, First Man, Solaris, Blade Runner 2049, Barry Lyndon, Ghostbusters II,
The Human Centipede).

Two smaller derivation passes already ran against this hypothesis with 0
matches: the single fixed-word table (1 candidate), and the top-5 curated
words for the 5 zero-literal keeper panels (1,000,000 candidates, 72s). This
script widens those same 5 panels (Goonies, Leon, Sharknado, Raiders,
Shining) to their FULL word lists -- top-5 plus every secondary-tier word
sourced from each film's real IMDb `/keywords/` page (see
analysis/leads.md, "Curated top-5 per panel, 2026-08-20" for the split and
analysis/imdb_field_audit.xlsx for the source data). All other 19 keeper
panels use their literal title-substring candidates (including full ties
where more than one exists).

Total space: 1,828,915,200 candidates (corrected from an earlier estimate of
1,698,278,400 -- panel 8's full word count is 42, not 39, see chat). At the
~70,800/s sustained rate measured on this machine with 10 workers, this is
roughly 7.2 hours.

Usage (from repo root, with the project venv active):
    python analysis/bruteforce_connections_criterion_full.py --workers 10

Prints progress periodically and stops immediately with the match printed if
one is found. Exits 0 on match, 1 on exhaustion with no match.

Checkpointing: completed chunk-start indices are appended, one per line, to
a checkpoint file (default analysis/.bruteforce_connections_checkpoint.txt,
next to this script, git-ignored) as each chunk finishes. If the process is
interrupted (power loss, crash, manual stop) and restarted with the same
--chunk size, it reads that file first and skips every chunk already marked
done, so a restart resumes instead of starting over. Delete the checkpoint
file to force a full restart from zero.
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

CANDIDATES: list[tuple[str, list[str]]] = [
    ("1 Die Hard", ["hard"]),
    ("2 Paths of Glory", ["glory", "path"]),
    ("3 Aliens", ["alien"]),
    ("4 Mad Max", ["mad"]),
    ("5 Alien", ["alien"]),
    ("6 Apocalypse Now", ["now"]),
    ("8 The Goonies", [
        "one", "brand", "chunk", "gold", "cave", "gadget", "beach", "rescue",
        "legend", "chase", "sword", "coin", "toilet", "bicycle", "tunnel",
        "jewel", "pizza", "fire", "sheriff", "forest", "skull", "piano",
        "child", "trap", "ship", "pistol", "arrest", "organ", "asthma",
        "book", "knife", "escape", "marble", "camera", "kiss", "thunder",
        "rain", "wish", "police", "hidden", "danger", "humor",
    ]),
    ("9 Spartacus", ["art"]),
    ("11 Godzilla", ["ill"]),
    ("13 Leon: The Professional", [
        "milk", "gun", "shield", "pistol", "crush", "girl", "police",
        "elevator", "hotel", "love", "knife", "weapon",
    ]),
    ("15 The Crimson Rivers", ["river"]),
    ("16 The Visitors", ["visit"]),
    ("17 A Clockwork Orange", ["clock", "lock", "orange", "range", "work"]),
    ("18 Star Wars: A New Hope", ["hope"]),
    ("19 Gravity", ["gravity"]),
    ("23 Guardians of the Galaxy", ["galaxy", "guard"]),
    ("24 Close Encounters of the Third Kind", ["close", "kind"]),
    ("26 Sharknado", [
        "tornado", "fish", "dog", "beach", "gun", "pistol", "animal",
        "vehicle", "car", "child",
    ]),
    ("27 Terminator 2: Judgment Day", ["day", "term"]),
    ("28 Scream 2", ["cream"]),
    ("29 The Matrix Reloaded", ["matrix", "load"]),
    ("30 Toy Story 2", ["story", "toy"]),
    ("32 Raiders of the Lost Ark", [
        "whip", "snake", "hat", "spider", "torch", "gold", "horse", "ship",
        "knife", "truck", "chase", "jungle", "mirror", "canyon", "desert",
        "fire", "bar", "love", "ritual", "lecture", "dress", "tent",
        "island", "wine", "blood", "warrior", "escape", "kiss", "pistol",
        "sword", "rescue", "basket", "soldier", "spirit", "alcohol", "car",
        "hero", "magic", "weapon", "mechanic", "faith", "fiction",
    ]),
    ("33 The Shining", [
        "hotel", "mirror", "blood", "ghost", "door", "maze", "snow", "bar",
        "chase", "elevator", "winter", "marriage", "kitchen", "author",
        "knife", "doctor", "window", "toy", "chef", "escape", "rescue",
        "kiss", "danger", "night", "gift", "boy", "airport",
    ]),
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


_DEFAULT_CHECKPOINT = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".bruteforce_connections_checkpoint.txt")


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
