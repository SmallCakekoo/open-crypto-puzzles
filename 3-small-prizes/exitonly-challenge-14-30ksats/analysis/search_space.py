#!/usr/bin/env python3
"""
search_space.py -- combinatorics for Challenge 14, computed only, nothing searched.

Purpose:
    Print the size of the candidate space implied by the puzzle's known facts (7 of 12
    BIP39 words given, 5 missing) under each assumption a solver might make, and explain
    where each factor in the arithmetic comes from. This script performs no search and
    checks no candidate; see tools/candidate_checker.py for that, and run it deliberately.

Input:
    None (the 7 known words and totals are the published facts, hardcoded below and
    matched against README.md at the "known words in order" line).

Output:
    A breakdown of the search space under two position assumptions, printed to stdout.

Usage:
    python analysis/search_space.py

The arithmetic, spelled out:
    - 12 words total, 7 known, 5 unknown.
    - A BIP39 12-word mnemonic carries 132 bits: 128 bits of entropy (words 1-11 in full,
      plus the first 7 bits of word 12) and a 4-bit checksum (the last 4 bits of word 12,
      = the first 4 bits of SHA-256(entropy)).
    - Case A -- positions of the 5 unknown words are known, and one of them is word 12
      (the checksum word): the other 4 unknown words are fully free (2048 choices each),
      and word 12 is constrained by the checksum to 1 of every 16 possibilities among its
      2048 (2048 / 16 = 128 valid words once the other 11 are fixed).
        space_A = 2048^4 x 128
    - Case B -- the positions of the 5 unknown words among the 12 slots are ALSO unknown
      (only that 7 specific words appear somewhere, 5 gaps somewhere else, both groups in
      their given relative order): multiply by the number of ways to choose which 5 of the
      12 slots are the gaps, C(12, 5).
        space_B = space_A x C(12, 5)
    This reproduces the two numbers in README.md's "Established facts" section; run this
    script to see the arithmetic rather than trusting the prose.
"""
from itertools import combinations

KNOWN_WORDS = ["dad", "butter", "wink", "follow", "trophy", "mixed", "erosion"]
TOTAL_WORDS = 12
UNKNOWN_COUNT = TOTAL_WORDS - len(KNOWN_WORDS)
WORDLIST_SIZE = 2048
CHECKSUM_DIVISOR = 16  # 4 checksum bits -> 1 of every 16 words at the checksum-bearing slot


def n_choose_k(n: int, k: int) -> int:
    from math import comb
    return comb(n, k)


def main():
    print("=== Challenge 14: known facts ===")
    print(f"total words:            {TOTAL_WORDS}")
    print(f"known words (in order): {KNOWN_WORDS}  ({len(KNOWN_WORDS)} words)")
    print(f"unknown words:          {UNKNOWN_COUNT}")
    print(f"wordlist size:          {WORDLIST_SIZE} (2^11, since each word encodes 11 bits)")

    print("\n=== Case A: positions of the 5 unknown words are known ===")
    print("assumption: one of the 5 unknown words is word 12 (the checksum-bearing word)")
    free_words = UNKNOWN_COUNT - 1
    checksum_word_choices = WORDLIST_SIZE // CHECKSUM_DIVISOR
    space_a = (WORDLIST_SIZE ** free_words) * checksum_word_choices
    print(f"  {free_words} fully free words: {WORDLIST_SIZE}^{free_words} = {WORDLIST_SIZE ** free_words:,}")
    print(f"  1 checksum-constrained word: {WORDLIST_SIZE} / {CHECKSUM_DIVISOR} = {checksum_word_choices}")
    print(f"  space_A = {WORDLIST_SIZE}^{free_words} x {checksum_word_choices} = {space_a:,}")

    print("\n=== Case B: positions of the 5 unknown words are ALSO unknown ===")
    position_choices = n_choose_k(TOTAL_WORDS, UNKNOWN_COUNT)
    space_b = space_a * position_choices
    print(f"  ways to choose which {UNKNOWN_COUNT} of {TOTAL_WORDS} slots are the gaps: "
          f"C({TOTAL_WORDS},{UNKNOWN_COUNT}) = {position_choices}")
    print(f"  space_B = space_A x {position_choices} = {space_b:,}")

    print("\n=== Effect of the checksum, isolated ===")
    print(f"  without any checksum constraint, 5 fully free words would be "
          f"{WORDLIST_SIZE}^{UNKNOWN_COUNT} = {WORDLIST_SIZE ** UNKNOWN_COUNT:,} candidates")
    print(f"  the checksum shrinks that by a factor of {CHECKSUM_DIVISOR} "
          f"(only when the checksum word is among the unknowns): "
          f"{WORDLIST_SIZE ** UNKNOWN_COUNT:,} / {CHECKSUM_DIVISOR} = {space_a:,}")

    print(
        "\nNo search is performed by this script. To measure how long these spaces would "
        "take at a real local rate, run examples/benchmark.py; to test one specific "
        "candidate, run tools/candidate_checker.py."
    )


if __name__ == "__main__":
    main()
