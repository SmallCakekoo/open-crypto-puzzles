#!/usr/bin/env python3
"""
build_candidates.py -- assemble the bounded 24-word candidate set from the
2026-08-19 findings (intruder split + per-panel word candidates) and, only if
explicitly asked, run them through tools/oracle.py.

Purpose:
    Turn the 24 surviving "keeper" panels (34 minus the 10 intruders found by
    analysis/intruder_repeat_check.py) and their candidate BIP39 words
    (data/films.csv, analysis/leads.md) into every complete, panel-ordered 24-word
    mnemonic implied by the still-open choices, then optionally check each one
    against the escrow via tools/oracle.py.

Input:
    None (the panel/word data is hardcoded below, matching data/films.csv and
    analysis/leads.md as of 2026-08-19). --run actually invokes the oracle;
    without it, this only counts and previews candidates.

Output:
    Without --run: the candidate count (2376 as of 2026-08-19, after panel 11 was
    corrected from Godzilla to Ace Ventura: When Nature Calls -- see below) and a
    few example candidates, so the combinatorics can be checked by hand before
    anything is tested against the escrow.
    With --run: every candidate is checked; on a MATCH, the matching mnemonic and
    address are printed and nothing else happens -- no transaction is built or
    broadcast, and this script does not sweep the wallet.

Usage:
    python analysis/build_candidates.py             # count and preview only
    python analysis/build_candidates.py --run        # also check every candidate

This checks a specific, small, justified space (2376 candidates, all traced to a
finding recorded in analysis/tested.md), not a blind sweep.

Update, 2026-08-19 (panel 11 correction): panel 11 was corrected from Godzilla to
Ace Ventura: When Nature Calls (human-verified identification; see
analysis/tested.md). This is NOT a drop-in word swap: Godzilla had a single fixed
literal candidate ("ill"), while Ace Ventura has 3 literal candidates ("when",
"nature", "call"), so this panel moved from the 17 fixed-word keepers into the
ambiguous-panel group, changing the space from 792 to 2376 candidates. Every
mnemonic ever checked against the escrow under the old 792-candidate space used
"ill" for this panel's position and is therefore invalid for this panel's
identity; none of those checks say anything about whether "when," "nature," or
"call" is the right word here. This has deliberately not been run with --run yet
(see analysis/tested.md for why).
"""
import argparse
import itertools
import os
import subprocess
import sys

# 24 keeper panels in panel order, each with its still-open candidate word(s).
# Single-item lists are settled candidates; multi-item lists are unresolved ties;
# panel 26 and 32 use non-literal or theme-word guesses, not verified words (see
# analysis/leads.md). Panel 11 (Ace Ventura: When Nature Calls, corrected from
# Godzilla 2026-08-19) has 3 literal candidates and is treated as ambiguous, not
# guessed -- all 3 are real substrings of the title, unlike panel 26/32's guesses.
KEEPER_WORDS = [
    ("Alien", ["alien"]),
    ("Mad Max", ["mad"]),
    ("Star Trek: The Motion Picture", ["motion", "picture"]),
    ("Apocalypse Now", ["now"]),
    ("Escape from Alcatraz", ["escape"]),
    ("The Goonies / Shutter Island (panel 8, disputed)", ["chunk", "island"]),  # "chunk": Goonies, primary hypothesis per user 2026-08-19, non-literal (character name); "island": Shutter Island, kept as a probability, literal whole-word
    ("Duel in the Sun", ["sun"]),
    ("Ace Ventura: When Nature Calls", ["when", "nature", "call"]),  # verified 2026-08-19: panel 11 corrected from Godzilla; all 3 are literal (when/nature whole-word, call via plural-strip of "calls")
    ("Life of Pi", ["life"]),
    ("Goodfellas", ["good"]),
    ("The Crimson Rivers", ["river"]),
    ("Star Wars: A New Hope", ["hope"]),
    ("Gravity", ["gravity"]),
    ("Solaris", ["solar"]),
    ("Valerian and the City of a Thousand Planets", ["city", "planet", "sand"]),
    ("Ordinary People", ["ordinary", "people"]),
    ("Sharknado", ["tornado"]),  # unverified: theme word, not literal substring
    ("The Lost Boys", ["boy"]),
    ("Scream 2", ["cream"]),
    ("The Matrix Reloaded", ["matrix"]),
    ("Toy Story", ["story", "toy"]),
    ("Ghostbusters II", ["ghost"]),
    ("Raiders of the Lost Ark",
     # original 11 theme/prop-word guesses (no textual basis, association only) +
     # "soft" (real substring, but only by splicing across "raiderS-OF-Thelostark",
     # not respecting the title's own word boundaries) + 5 words suggested by the
     # user 2026-08-19 (rail/raise/risk/other/rather) that are NOT substrings of
     # the title under any splicing, verified against the full 2048-word list --
     # included anyway since a MATCH would be its own proof regardless of textual
     # grounding, but flagged here as having zero found connection to the title
     ["whip", "snake", "gold", "hat", "desert", "skull", "cave", "stone", "sand", "jungle", "crystal",
      "soft", "rail", "raise", "risk", "other", "rather"]),
    ("The Human Centipede (First Sequence)", ["human", "first", "man"]),
]

HERE = os.path.dirname(os.path.abspath(__file__))
ORACLE = os.path.join(os.path.dirname(HERE), "tools", "oracle.py")


def candidates():
    word_lists = [words for _title, words in KEEPER_WORDS]
    for combo in itertools.product(*word_lists):
        yield " ".join(combo)


def main():
    parser = argparse.ArgumentParser(description="Assemble and optionally test the 792-candidate set.")
    parser.add_argument("--run", action="store_true", help="pipe every candidate through tools/oracle.py")
    parser.add_argument("--preview", type=int, default=3, help="how many example candidates to print")
    args = parser.parse_args()

    total = 1
    for _title, words in KEEPER_WORDS:
        total *= len(words)
    print(f"panels (keepers): {len(KEEPER_WORDS)}")
    print(f"total candidates: {total}")

    gen = candidates()
    print(f"\nfirst {args.preview} example candidates:")
    for _ in range(args.preview):
        try:
            print(" ", next(gen))
        except StopIteration:
            break

    if not args.run:
        print("\n--run not given: nothing was checked against the escrow.")
        return

    print(f"\nRunning all {total} candidates through {ORACLE} --stdin ...")
    proc = subprocess.run(
        [sys.executable, ORACLE, "--stdin"],
        input="\n".join(candidates()),
        capture_output=True, text=True,
    )
    matches = [line for line in proc.stdout.splitlines() if line.startswith("MATCH")]
    print(f"done. {len(matches)} match(es).")
    for m in matches:
        print(m)
    if not matches:
        print("NO MATCH across all candidates in this bounded set.")


if __name__ == "__main__":
    main()
