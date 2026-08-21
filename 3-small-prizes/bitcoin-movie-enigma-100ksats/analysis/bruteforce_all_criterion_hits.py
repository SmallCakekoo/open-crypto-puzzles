"""
Derivation test for every exact-10 criterion hit from the reconstructed
24-field x 600-pair sweep (see analysis/tested.md, "Full programmatic
re-derivation of the criterion sweep... 2026-08-20").

The user asked to focus on finding the real intruder criterion and pointed out
that the earlier session's "17 combinations" were flagged as likely noise but
never actually derivation-tested (except the single leading one, single_country
AND single_language). This script closes that gap: rebuilds the 24-word
candidate space for each of the 15 not-yet-tested exact-10 hits (the 16th,
single_country AND single_language, was already tested separately with the
curated top-5 words -- see bruteforce_curated_top5.py) and runs every one
through oracle.check(), so that "probably noise" is backed by an actual
negative result instead of a prior.

Word candidates: literal substrings from data/films.csv for panels that have
one, the curated top-5 most iconic/distinctive words (chosen 2026-08-20, see
leads.md "Curated top-5 per panel") for the 5 zero-literal panels (8 Goonies,
13 Leon, 26 Sharknado, 32 Raiders, 33 Shining) whenever a given hypothesis
keeps that panel.

Runs single-thread, in-process, deliberately not multiprocess -- this is meant
to run unattended in the background (see the freeze/reboot note on the earlier
12-worker 38.9M run) at a gentler, single-core pace. ~90.9M candidates combined
across all 15 hypotheses, ~2h at ~13,000/s.

Usage (from repo root, with the project venv active):
    python analysis/bruteforce_all_criterion_hits.py

Stops immediately and prints the match if any hypothesis's full space contains
one; otherwise runs all 15 to exhaustion and prints a summary.
"""

from __future__ import annotations

import itertools
import os
import sys
import time

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO_ROOT, "tools"))
import oracle  # noqa: E402

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


# Every exact-10 hit from the reconstructed sweep, except single_country AND
# single_language (already tested separately) and single_writer_block (already
# tested separately, the single-field hit found by the parsing-bug fix).
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

ALL34 = set(range(1, 35))


def main() -> int:
    if not oracle.selftest():
        print("SELFTEST FAILED -- aborting", flush=True)
        return 2
    print("selftest OK", flush=True)
    print(f"Testing {len(HYPOTHESES)} hypotheses, total ~90.9M candidates combined", flush=True)

    overall_t0 = time.time()
    any_match = False
    for hname, dropped in HYPOTHESES.items():
        dropped_set = set(dropped)
        keep = sorted(ALL34 - dropped_set)
        option_lists = [candidates(p) for p in keep]
        total = 1
        for o in option_lists:
            total *= len(o)
        print(f"\n=== {hname} | dropped={sorted(dropped_set)} | space={total:,} ===", flush=True)

        t0 = time.time()
        checked = 0
        match = None
        for combo in itertools.product(*option_lists):
            mnemonic = " ".join(combo)
            matched, addr, path = oracle.check(mnemonic)
            checked += 1
            if matched:
                match = (mnemonic, addr, path)
                break
            if checked % 1_000_000 == 0:
                elapsed = time.time() - t0
                print(f"  ...{checked:,}/{total:,} ({elapsed:.0f}s)", flush=True)
        elapsed = time.time() - t0
        if match:
            mnemonic, addr, path = match
            print(f"  *** MATCH FOUND for '{hname}' ***", flush=True)
            print("  Mnemonic:", mnemonic, flush=True)
            print("  Address:", addr, flush=True)
            print("  Path:", path, flush=True)
            any_match = True
            break
        print(f"  no match ({elapsed:.0f}s, {checked:,} checked)", flush=True)

    total_elapsed = time.time() - overall_t0
    print(f"\nAll done in {total_elapsed:.0f}s. any_match={any_match}", flush=True)
    return 0 if any_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
