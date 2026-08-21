"""
Curated-candidates brute-force of the "single country + single language" intruder-set
hypothesis (see analysis/tested.md and analysis/leads.md, 2026-08-20 entries).

Follow-up to bruteforce_country_lang_split_mp.py's 38.9M-candidate run. That run's
4 zero-literal-substring keeper panels (Goonies, Leon, Raiders, Shining) had their
IMDb-keyword candidate lists massively widened afterwards (full /keywords/ page,
not just top 5-6) -- see "Full IMDb keyword lists... 2026-08-20" in tested.md. Using
every one of those words directly would make the space ~4.39 billion candidates
(~113x bigger, ~26h to exhaust even at 12-worker speed) -- too large and too risky
for the machine (see the freeze/reboot note on the 38.9M run) to run without
checking in. Per the user's explicit choice, curated each of the 4 expanded panels
down to its 5 most iconic/distinctive words (character names, signature props,
famous single-scene objects -- not generic keyword-tag words shared by lots of
films); the excluded words are NOT discarded, just demoted to a second/third-pass
tier, same convention as the "inferior substrings" column in
analysis/imdb_field_audit.xlsx. Full excluded-word lists per panel are in
leads.md, "Curated top-5..." entry.

Intruders (10, dropped): panels 4, 7, 9, 15, 18, 24, 26, 28, 30, 31 (unchanged
from the original hypothesis -- Sharknado, panel 26, is dropped here, so its
candidate word doesn't matter for this specific run).

Total space: 4,800,000 candidates -- small enough to run in-process, single-thread,
no multiprocessing needed (~6 minutes at ~13,000/s on this machine).

Usage (from repo root, with the project venv active):
    python analysis/bruteforce_curated_top5.py

Result of the 2026-08-20 run: NO MATCH across all 4,800,000 combinations.
Selftest passed beforehand.
"""

from __future__ import annotations

import itertools
import os
import sys
import time

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO_ROOT, "tools"))
import oracle  # noqa: E402

CANDIDATES: list[tuple[str, list[str]]] = [
    ("1 Die Hard", ["hard"]),
    ("2 Paths of Glory", ["glory", "path"]),
    ("3 Aliens", ["alien"]),
    ("5 Alien", ["alien"]),
    ("6 Apocalypse Now", ["now"]),
    ("8 The Goonies", ["chunk", "gold", "cave", "piano", "skull"]),
    ("10 Mission: Impossible", ["miss", "possible"]),
    ("11 Godzilla", ["ill"]),
    ("12 Life of Pi", ["life"]),
    ("13 Leon: The Professional", ["milk", "gun", "shield", "pistol", "crush"]),
    ("14 The Man in the Iron Mask", ["man", "iron", "mask"]),
    ("16 The Visitors", ["visit"]),
    ("17 A Clockwork Orange", ["clock", "lock", "orange", "range", "work"]),
    ("19 Gravity", ["gravity"]),
    ("20 First Man", ["first", "man"]),
    ("21 Solaris", ["solar"]),
    ("22 Blade Runner 2049", ["blade", "run"]),
    ("23 Guardians of the Galaxy", ["galaxy", "guard"]),
    ("25 Barry Lyndon", ["bar"]),
    ("27 Terminator 2: Judgment Day", ["day", "term"]),
    ("29 The Matrix Reloaded", ["matrix", "load"]),
    ("32 Raiders of the Lost Ark", ["whip", "snake", "hat", "spider", "torch"]),
    ("33 The Shining", ["hotel", "mirror", "blood", "ghost", "door"]),
    ("34 The Human Centipede (First Sequence)", ["human", "first", "man", "tip"]),
]

assert len(CANDIDATES) == 24, f"expected 24 keeper panels, got {len(CANDIDATES)}"

OPTION_LISTS = [opts for _name, opts in CANDIDATES]
TOTAL = 1
for _opts in OPTION_LISTS:
    TOTAL *= len(_opts)


def main() -> int:
    print(f"Total candidates: {TOTAL:,}", flush=True)
    if not oracle.selftest():
        print("SELFTEST FAILED -- aborting", flush=True)
        return 2
    print("selftest OK", flush=True)

    t0 = time.time()
    checked = 0
    match = None
    for combo in itertools.product(*OPTION_LISTS):
        mnemonic = " ".join(combo)
        matched, addr, path = oracle.check(mnemonic)
        checked += 1
        if matched:
            match = (mnemonic, addr, path)
            break
        if checked % 200_000 == 0:
            elapsed = time.time() - t0
            rate = checked / elapsed
            eta = (TOTAL - checked) / rate
            print(f"  ...{checked:,}/{TOTAL:,} ({elapsed:.0f}s, {rate:.0f}/s, ETA {eta:.0f}s)", flush=True)

    elapsed = time.time() - t0
    print(f"Done in {elapsed:.1f}s, checked {checked:,}", flush=True)
    if match:
        mnemonic, addr, path = match
        print("MATCH FOUND!")
        print("Mnemonic:", mnemonic)
        print("Address:", addr)
        print("Path:", path)
        return 0
    print(f"NO MATCH across all {TOTAL:,} combinations.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
