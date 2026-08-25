#!/usr/bin/env python3
"""
oracle.py -- candidate checker for the Aoi Nakamoto Quizchain puzzle.

Purpose:
    Given a candidate text, reproduce the puzzle's confirmed transform: MD5 the
    bytes of the text (encoding selectable, see --encoding) to get 128 bits of
    entropy, turn that entropy into a BIP39 mnemonic, derive BIP44 path
    m/44'/0'/0'/0/i for i = 0 to 5, and compare each resulting P2PKH address
    against Real Big Block's current and superseded escrows (and, for
    calibration, the solved Block 77 Stage One escrow). A helper function
    reproduces the case-flip rule the puzzle's own source text states
    directly (see "Certified against" in the README), for use on a candidate
    text you supply yourself.

    Quizchain2 Block 76 was solved and swept by a reader on 2026-08-17; its
    MD5-prefix filter mode has been removed from this tool. See git history
    (analysis/tested.md, clues/author-posts.md) for reference.

    This script does not embed the text of Block 77 Stage One's source (Hal
    Finney's bitcointalk post) or of the Real Big Block's source (a Wattpad
    chapter): both are third-party or bulk material this repository does not
    redistribute. --selftest certifies the transform against the author's own
    published calibration vector instead, which needs no such text (see
    "Certified against" in the README for what this does and does not prove).

Usage:
    python3 tools/oracle.py --selftest                          # see README
    python3 tools/oracle.py "<candidate text>"                   # MD5 -> BIP39 -> derive
    python3 tools/oracle.py "<candidate text>" --encoding iso-8859-1
    python3 tools/oracle.py --stdin                              # one candidate per line
    python3 tools/oracle.py --flip-case "<paragraph>"            # apply the Stage One rule to one paragraph

Input:
    A candidate text string (the exact bytes to MD5), or, for --flip-case,
    one paragraph.

Output:
    "MATCH <label> <address> index=<i>" on a hit, "NO MATCH" otherwise.
    Exit 0 on any match, 1 if none.

Dependencies: stdlib, bip_utils.
"""

from __future__ import annotations

import argparse
import hashlib
import sys

from bip_utils import (
    Bip39MnemonicGenerator,
    Bip39SeedGenerator,
    Bip44,
    Bip44Coins,
    Bip44Changes,
)

TARGETS = {
    "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W": "Real Big Block, current (block 77 stage 2, 0.777 BTC, OPEN)",
    "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC": "Real Big Block, superseded pre-rehash address (funded 2019-07-24, swept back by the author before the rehash, not part of the live prize)",
    "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN": "Block 77 Stage One (solved 2019-08-03, calibration reference only)",
}

# Certification vector: published by the author in the round-1 corpus. This
# entropy, at BIP44 index 1 ("my 2nd private key"), must produce this WIF.
# Self-contained: needs no third-party text.
VECTOR_ENTROPY = "2941774a2abec9f30c7d6777d1d53d91"
VECTOR_WIF_INDEX1 = "L5Z66qPmUkTAsWQywjRNHDxHrX6J1X1SQedp6V8QsbaXR7rGd6ex"

# Initials rule: of a text's paragraphs, the ones whose first letter is NOT
# one of these get the case-flip rule applied (see flip_case). Confirmed two
# independent ways for Block 77 Stage One: (1) applying it to Hal Finney's
# real bitcointalk post reproduces the escrow address exactly; (2) the
# "Second" Wattpad chapter (Real Big Block's own confirmed source) states it
# directly in its own narrative -- "The letters I, T, A, S, and M as first
# letters of each paragraph of this post" -- so this is not a fit to the
# address, it is the puzzle's own stated rule. A brute-force check of all 512
# subsets (sizes 0-9) of the 9 distinct letters in "SATOSHI NAKAMOTO" against
# the real Finney text confirms ITASM is the unique minimal (size-5) subset
# that reproduces the address; the other 4 letters in that pool (O, H, N, K)
# never appear as a paragraph-initial letter in that text and are therefore
# unconstrained by the calibration, not "also correct."
STAGE_ONE_NO_FLIP_INITIALS = set("ITASM")

# Real Big Block's confirmed paragraph separators, from direct author
# statements in the fully-recovered Real Big Block Discussion thread (see
# data/realbigblock_full_thread_recovered.md). Different from Stage One's own
# separator (a blank line, ASCII 10 10, from the bitcointalk source's
# <br><br> convention) -- "the format" the author says is shared between the
# two stages is the general case-flip technique, not an identical byte-level
# recipe; the separator is independently re-specified per block.
REAL_BIG_BLOCK_SEPARATOR_CURRENT = "\r\n\r\n"       # ASCII 13 10 13 10, "hit enter twice"
REAL_BIG_BLOCK_SEPARATOR_SUPERSEDED = "\r\n"        # ASCII 13 10, "only one line break"
STAGE_ONE_SEPARATOR = "\n\n"                        # blank line, confirmed by reproduction


def md5_entropy(text: str, encoding: str = "utf-8") -> bytes:
    return hashlib.md5(text.encode(encoding)).digest()


def derive_addresses(entropy: bytes, n: int = 6) -> list[str]:
    """entropy (16 raw bytes) -> BIP39 -> m/44'/0'/0'/0/i for i in 0..n-1."""
    mnemonic = Bip39MnemonicGenerator().FromEntropy(entropy)
    seed = Bip39SeedGenerator(mnemonic).Generate()
    account = (
        Bip44.FromSeed(seed, Bip44Coins.BITCOIN)
        .Purpose()
        .Coin()
        .Account(0)
        .Change(Bip44Changes.CHAIN_EXT)
    )
    return [account.AddressIndex(i).PublicKey().ToAddress() for i in range(n)]


def derive_wif(entropy: bytes, index: int) -> str:
    mnemonic = Bip39MnemonicGenerator().FromEntropy(entropy)
    seed = Bip39SeedGenerator(mnemonic).Generate()
    account = (
        Bip44.FromSeed(seed, Bip44Coins.BITCOIN)
        .Purpose()
        .Coin()
        .Account(0)
        .Change(Bip44Changes.CHAIN_EXT)
    )
    return account.AddressIndex(index).PrivateKey().ToWif()


def flip_case(paragraph: str) -> str:
    """First letter to lowercase, last letter to uppercase (non-letters
    untouched). This is the rule confirmed on Block 77 Stage One, and stated
    directly in the Real Big Block source chapter's own text: apply it to
    each paragraph of a candidate text whose first letter is not in
    STAGE_ONE_NO_FLIP_INITIALS, then join and run it through attempt()
    below. Note: which paragraphs of Real Big Block's source this rule
    should even be applied to -- or whether it is reused for that block at
    all -- remains unconfirmed; see analysis/leads.md."""
    chars = list(paragraph)
    letters = [i for i, c in enumerate(chars) if c.isalpha()]
    if not letters:
        return paragraph
    first, last = letters[0], letters[-1]
    chars[first] = chars[first].lower()
    chars[last] = chars[last].upper()
    return "".join(chars)


def apply_stage_one_rule(paragraphs: list[str], separator: str = STAGE_ONE_SEPARATOR) -> str:
    """Apply the confirmed rule to a list of paragraphs you supply yourself
    (this script ships no paragraph text of its own) and join with
    `separator` (defaults to Stage One's own confirmed blank-line separator;
    pass REAL_BIG_BLOCK_SEPARATOR_CURRENT or _SUPERSEDED for Real Big Block
    candidates)."""
    modified = [
        p if p and p[0] in STAGE_ONE_NO_FLIP_INITIALS else flip_case(p)
        for p in paragraphs
    ]
    return separator.join(modified)


def attempt(candidate: str, encoding: str = "utf-8") -> tuple[bool, dict]:
    entropy = md5_entropy(candidate, encoding)
    addresses = derive_addresses(entropy, n=6)
    for i, addr in enumerate(addresses):
        if addr in TARGETS:
            return True, {"address": addr, "label": TARGETS[addr], "index": i}
    return False, {}


def selftest() -> bool:
    ok = True

    # Part 1: the core transform (MD5 -> BIP39 -> BIP44 -> address), certified
    # against the author's own published calibration vector. Self-contained.
    entropy = bytes.fromhex(VECTOR_ENTROPY)
    wif1 = derive_wif(entropy, 1)
    part1 = wif1 == VECTOR_WIF_INDEX1
    print(f"author's own vector: entropy {VECTOR_ENTROPY[:8]}... index 1 WIF -> {'OK' if part1 else 'FAIL'}")
    ok = ok and part1

    others = [derive_wif(entropy, i) for i in range(6) if i != 1]
    part1b = wif1 not in others
    print(f"that WIF appears at no other index (no collision): {'OK' if part1b else 'FAIL'}")
    ok = ok and part1b

    # Part 2: the flip_case rule, tested on a synthetic (non-puzzle) example,
    # since this script ships no copyrighted source text.
    example = "When the wind blows across the plain"
    flipped = flip_case(example)
    expected = "when the wind blows across the plaiN"
    part2 = flipped == expected
    print(f"flip_case on a synthetic example matches the expected first/last-letter swap: {'OK' if part2 else 'FAIL'}")
    ok = ok and part2

    if ok:
        print("SELFTEST OK")
        print(
            "Note: this certifies the MD5-to-address transform and the "
            "flip_case helper. It does NOT reproduce Block 77 Stage One end "
            "to end, since that needs Hal Finney's bitcointalk post text, "
            "which this repository does not ship (third-party copyrighted "
            "content). Feed that text yourself to apply_stage_one_rule() to "
            "reproduce it -- it should join with STAGE_ONE_SEPARATOR (a "
            "blank line) and reproduce 19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN "
            "exactly at index 0, MD5 9dd2efb9bc976c2095bd534d7b8d431c."
        )
    return ok


def _print_result(candidate: str, encoding: str) -> bool:
    matched, info = attempt(candidate, encoding)
    if matched:
        print(f"MATCH {info['label']} {info['address']} index={info['index']}")
    else:
        print("NO MATCH")
    return matched


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", nargs="?", help="candidate text (MD5'd as-is)")
    parser.add_argument("--stdin", action="store_true", help="read candidates, one per line")
    parser.add_argument("--selftest", action="store_true", help="run the certification checks")
    parser.add_argument(
        "--encoding",
        default="utf-8",
        choices=["utf-8", "iso-8859-1", "cp1252"],
        help="byte encoding for the MD5 input (default utf-8); only matters for candidates with non-ASCII characters",
    )
    parser.add_argument(
        "--flip-case",
        metavar="PARAGRAPH",
        help="apply the Stage One case-flip rule to one paragraph and print it",
    )
    args = parser.parse_args()

    if args.selftest:
        return 0 if selftest() else 1

    if args.flip_case is not None:
        print(flip_case(args.flip_case))
        return 0

    if args.stdin:
        any_hit = False
        for line in sys.stdin:
            line = line.rstrip("\n")
            if not line:
                continue
            any_hit = _print_result(line, args.encoding) or any_hit
        return 0 if any_hit else 1

    if not args.candidate:
        parser.print_help()
        return 0

    return 0 if _print_result(args.candidate, args.encoding) else 1


if __name__ == "__main__":
    sys.exit(main())
