#!/usr/bin/env python3
"""
practice_range.py -- safe rehearsal of the full solving pipeline against an ALREADY
SPENT episode of this series, to validate methodology before touching Challenge 14.

Purpose:
    Challenges 1-13 of the Exitonly "Bitcoin Challenge" series are all already spent
    (confirmed on-chain, see analysis/tested.md); their escrows cannot be claimed by
    anyone anymore. That makes them a zero-risk practice range: brute-forcing one small,
    already-dead episode end-to-end (checksum -> BIP84 derivation -> address compare)
    proves the pipeline is correct on a target where nothing can be won or lost, using
    the exact same code that would eventually run against Challenge 14's live escrow.

    This script only rehearses episodes where the missing-word count is small enough
    that even the "position unknown" case (see README.md's search_space.py) stays in
    the low thousands of candidates -- still not a mass brute force.

Input:
    --known "w1 w2 ... w11" (the words the video gives, in the order given -- NOT
    assumed to be their final position in the 12-word mnemonic), --target <address>
    (the episode's own escrow, for the record), --episode <n> (label only).

Output:
    Tries the missing word in every one of the 12 possible slots (not just the slot the
    source material implied), keeping the known words in their given relative order in
    the remaining 11 slots -- this is exactly README.md's "Case B" (positions unknown).
    Every checksum-valid combination is derived under BIP84 and compared to --target.
    Prints the match if found, plus candidate/time counts. Never touches funds; there is
    nothing to touch, the target address is historical.

Usage (Challenge 1 example, run 2026-08-20):
    python analysis/practice_range.py \\
        --known "trouble battle idle skirt farm office emotion grow raise mother cable" \\
        --target bc1qnlj5s0ltkg4w3jr6f4jhd8yhr5hcpkat5fw33n --episode 1

Cryptographic parts worth studying:
    This is the same Bip39MnemonicValidator + Bip84.FromSeed(...).Purpose().Coin()
    .Account(0).Change(CHAIN_EXT).AddressIndex(0) pipeline as
    ../tools/candidate_checker.py, just wrapped in a loop over every (slot, word) pair
    instead of checking one candidate at a time. Study the two nested loops in
    search(): the outer one is README.md's Case B position multiplier (C(12,1)=12 here),
    the inner one is the 2048-word wordlist; the checksum filter inside
    Bip39MnemonicValidator is what silently discards ~15 of every 16 raw candidates
    before a single BIP84 derivation is even attempted, which is most of why this stays
    fast even without any real optimization.
"""
import argparse
import time

from bip_utils import (
    Bip39MnemonicValidator, Bip39SeedGenerator,
    Bip84, Bip84Coins, Bip44Changes,
)
from bip_utils.bip.bip39.bip39_mnemonic_decoder import Bip39WordsListGetter
from bip_utils import Bip39Languages

MAX_KNOWN_MISSING = 1  # keeps the position-unknown space at 12 x 2048 = 24,576 raw
                        # candidates (~1,536 checksum-valid) -- a rehearsal, not a search


def derive_bip84_address(mnemonic: str) -> str:
    seed = Bip39SeedGenerator(mnemonic).Generate()
    return (
        Bip84.FromSeed(seed, Bip84Coins.BITCOIN).Purpose().Coin().Account(0)
        .Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        .PublicKey().ToAddress()
    )


def search(known_words: list, target: str):
    n_total = len(known_words) + 1
    wordlist = Bip39WordsListGetter().GetByLanguage(Bip39Languages.ENGLISH)
    all_words = [wordlist.GetWordAtIdx(i) for i in range(2048)]

    validator = Bip39MnemonicValidator()
    tried = 0
    checksum_valid = 0
    start = time.perf_counter()
    found = None

    for slot in range(n_total):
        for candidate_word in all_words:
            mnemonic_words = known_words[:slot] + [candidate_word] + known_words[slot:]
            mnemonic = " ".join(mnemonic_words)
            tried += 1
            if not validator.IsValid(mnemonic):
                continue
            checksum_valid += 1
            address = derive_bip84_address(mnemonic)
            if address == target:
                found = (mnemonic, address, slot)
                break
        if found:
            break

    elapsed = time.perf_counter() - start
    return found, tried, checksum_valid, elapsed


def main():
    parser = argparse.ArgumentParser(description="Rehearse the pipeline on an already-spent episode.")
    parser.add_argument("--known", required=True, help="space-separated known words, in given order")
    parser.add_argument("--target", required=True, help="that episode's escrow address")
    parser.add_argument("--episode", default="?", help="episode number, for the printed label only")
    args = parser.parse_args()

    known_words = args.known.split()
    missing = 12 - len(known_words)
    if missing != MAX_KNOWN_MISSING:
        raise SystemExit(
            f"this script is a rehearsal tool capped at {MAX_KNOWN_MISSING} missing word "
            f"(12 x 2048 candidates); episode {args.episode} needs {missing} missing words, "
            f"which is out of scope here"
        )

    print(f"=== Practice range: Challenge {args.episode} (already spent, historical target) ===")
    print(f"known words ({len(known_words)}): {known_words}")
    print(f"target (dead escrow, for the record only): {args.target}")
    print(f"position of the missing word: NOT assumed -- trying all {len(known_words)+1} slots\n")

    found, tried, checksum_valid, elapsed = search(known_words, args.target)

    print(f"raw candidates tried: {tried:,}")
    print(f"checksum-valid candidates: {checksum_valid:,}")
    print(f"time: {elapsed:.2f}s ({tried/elapsed:.0f} candidates/sec)\n")

    if found:
        mnemonic, address, slot = found
        print("MATCH")
        print(f"  mnemonic: {mnemonic}")
        print(f"  missing word was at slot {slot + 1} of 12: '{mnemonic.split()[slot]}'")
        print(f"  address: {address}")
        print(
            "\nThis reconstructs a historical answer to an ALREADY SPENT puzzle. It proves "
            "nothing about Challenge 14 except that this exact pipeline is correct; the "
            "escrow above cannot be claimed by anyone, the funds moved years ago."
        )
    else:
        print("NO MATCH across all 1,536 checksum-valid candidates and all 12 positions.")
        print(
            "This would mean either the known words are not all correct/in the assumed "
            "relative order, or the puzzle used a derivation path other than BIP84 -- "
            "worth rechecking against BIP49/BIP44 before concluding anything."
        )


if __name__ == "__main__":
    main()
