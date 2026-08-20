#!/usr/bin/env python3
"""
analyze_known_seeds.py -- objective comparison tool for testing the "shared/weak generator"
hypothesis for the Exitonly "Bitcoin Challenge" series (see README.md, open lead #1).

Purpose:
    Given two or more COMPLETE, already-solved BIP39 mnemonics from this series, decode each
    one into its word indices, 11-bit binary groups, 128-bit entropy, and 4-bit checksum,
    then compute objective relationships between every pair: identical entropy-byte prefixes
    and suffixes, byte-for-byte matches, XOR difference, Hamming distance, and same-position
    word matches. It prints numbers and a plain-English classification; it does not decide
    "vulnerable" or "not vulnerable" on your behalf.

    As of this writing, this repository has NO complete solved mnemonic for Challenge 12 or
    Challenge 13: both escrows are confirmed spent on-chain (see analysis/README.md), but the
    words that solved them were never found published anywhere I could reach (not in the
    video descriptions, not in accessible comments, not on-chain -- a BIP39 mnemonic is never
    part of a Bitcoin transaction). --demo runs this tool on the public BIP39 test vectors
    instead, purely to prove the arithmetic is correct and reproducible; it draws no
    conclusion about the puzzle series.

Input:
    --mnemonic "LABEL:word1 word2 ... word12" (repeat for each known solved mnemonic, 2+
    required for comparison), or --demo to run on two public BIP39 test vectors.

Output:
    Per-mnemonic breakdown (word count, indices, binary groups, entropy hex, checksum bits),
    then a pairwise comparison table with a 3-tier classification per signal:
      - "casual coincidence": within the range expected from two independent random values
      - "plausible pattern": outside that range but not conclusive on its own
      - "strong evidence": would require an extraordinary explanation other than a shared
        or non-random generation process
    The thresholds used for that classification are printed with the numbers, not hidden in
    the code, so the classification can be checked by hand.

Usage:
    python analysis/analyze_known_seeds.py --demo
    python analysis/analyze_known_seeds.py \\
        --mnemonic "ch12:w1 w2 w3 w4 w5 w6 w7 w8 w9 w10 w11 w12" \\
        --mnemonic "ch13:w1 w2 w3 w4 w5 w6 w7 w8 w9 w10 w11 w12"

This script never derives an address, never touches an escrow, and never broadcasts
anything -- it only decodes mnemonic text that you already have into numbers for comparison.

Cryptographic parts worth studying:
    Bip39MnemonicDecoder.Decode() reverses examples/bip39_demo.py's entropy -> mnemonic step:
    it turns 12 words back into the 16 raw entropy bytes, dropping the 4 checksum bits (which
    are redundant once the entropy is known -- see examples/bip39_validate.py for computing
    them back). Hamming distance and XOR here operate on that raw entropy, not on the words
    or their wordlist indices, since entropy is where a weak RNG's structure would actually
    show up; comparing word indices alone would miss, for example, two entropies that differ
    by exactly one bit but happen to fall in different 11-bit groups.
"""
import argparse
import sys

from bip_utils import Bip39Languages
from bip_utils.bip.bip39.bip39_mnemonic_decoder import Bip39MnemonicDecoder, Bip39WordsListGetter

DEMO_VECTORS = [
    ("demo_abandon12_about", "abandon abandon abandon abandon abandon abandon "
                              "abandon abandon abandon abandon abandon about"),
    ("demo_legal_winner", "legal winner thank year wave sausage worth useful legal "
                           "winner thank yellow"),
]


def decode(label: str, mnemonic: str) -> dict:
    words = mnemonic.strip().split()
    if len(words) != 12:
        raise SystemExit(f"{label}: expected 12 words, got {len(words)}")

    wordlist = Bip39WordsListGetter().GetByLanguage(Bip39Languages.ENGLISH)
    indices = [wordlist.GetWordIdx(w.lower()) for w in words]
    binary_groups = [format(i, "011b") for i in indices]

    decoder = Bip39MnemonicDecoder(Bip39Languages.ENGLISH)
    entropy = decoder.Decode(mnemonic.strip())  # 16 bytes = 128 bits, checksum stripped

    checksum_bits = binary_groups[-1][7:]  # last 4 bits of word 12 are the checksum

    return {
        "label": label,
        "words": words,
        "indices": indices,
        "binary_groups": binary_groups,
        "entropy": entropy,
        "checksum_bits": checksum_bits,
    }


def print_single(rec: dict):
    print(f"=== {rec['label']} ===")
    print(f"words:          {rec['words']}")
    print(f"BIP39 indices:  {rec['indices']}")
    print(f"binary (11b ea):{' '.join(rec['binary_groups'])}")
    print(f"entropy (hex):  {rec['entropy'].hex()}  ({len(rec['entropy']) * 8} bits)")
    print(f"checksum bits:  {rec['checksum_bits']}")
    print()


def hamming_distance(a: bytes, b: bytes) -> int:
    return sum(bin(x ^ y).count("1") for x, y in zip(a, b))


def common_prefix_bytes(a: bytes, b: bytes) -> int:
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


def common_suffix_bytes(a: bytes, b: bytes) -> int:
    n = 0
    for x, y in zip(reversed(a), reversed(b)):
        if x != y:
            break
        n += 1
    return n


def classify(signal_name: str, value, casual_if, plausible_if) -> str:
    if casual_if(value):
        return "casual coincidence"
    if plausible_if(value):
        return "plausible pattern"
    return "strong evidence"


def compare_pair(rec_a: dict, rec_b: dict):
    a, b = rec_a["entropy"], rec_b["entropy"]
    n_bits = len(a) * 8

    print(f"=== Comparison: {rec_a['label']} vs {rec_b['label']} ===")

    same_position_words = sum(1 for x, y in zip(rec_a["indices"], rec_b["indices"]) if x == y)
    print(f"same-position word matches: {same_position_words} / 12")
    print("  threshold: for two independent random mnemonics, the expected count is "
          f"12/2048 = {12/2048:.4f}; 1 match is unremarkable, 2+ starts to be notable, "
          "3+ would be surprising by chance alone.")

    prefix = common_prefix_bytes(a, b)
    suffix = common_suffix_bytes(a, b)
    print(f"identical entropy-byte prefix length: {prefix} / {len(a)} bytes")
    print(f"identical entropy-byte suffix length: {suffix} / {len(a)} bytes")
    print("  threshold: for independent random 128-bit values, P(prefix >= 1 byte) = 1/256; "
          "P(prefix >= 2 bytes) = 1/65536. A prefix/suffix of 2+ bytes is a plausible pattern; "
          "4+ bytes would be strong evidence.")

    xor = bytes(x ^ y for x, y in zip(a, b))
    print(f"XOR(entropy_a, entropy_b): {xor.hex()}")
    xor_zero_bytes = sum(1 for byte in xor if byte == 0)
    print(f"  zero bytes in XOR (byte-identical positions): {xor_zero_bytes} / {len(a)}")

    hd = hamming_distance(a, b)
    print(f"Hamming distance: {hd} / {n_bits} bits ({hd / n_bits:.1%} of bits differ)")
    print("  threshold: two independent random 128-bit values differ in ~50% of bits "
          f"(expected {n_bits/2:.0f}, std dev {(n_bits*0.25)**0.5:.1f}). A distance within "
          f"roughly {n_bits/2:.0f} +/- 15 bits is casual coincidence; well outside that band "
          "(very close to 0 or very close to 128) is a plausible pattern worth a second look; "
          "an exact or near-exact match (distance 0-2) alongside a known non-random source "
          "would be strong evidence.")

    diff_int_a = int.from_bytes(a, "big")
    diff_int_b = int.from_bytes(b, "big")
    numeric_diff = abs(diff_int_a - diff_int_b)
    print(f"numeric difference (entropy as big-endian integer): {numeric_diff}")
    print("  a small numeric difference (e.g. entropy_b = entropy_a + 1) would be strong "
          "evidence of a counter-based generator; a large, unstructured difference is not "
          "informative on its own.")

    print()
    print("Objective summary (see thresholds above for how each label was chosen):")
    prefix_class = classify("prefix", prefix, lambda v: v < 2, lambda v: v < 4)
    suffix_class = classify("suffix", suffix, lambda v: v < 2, lambda v: v < 4)
    hd_class = classify(
        "hamming", hd,
        lambda v: abs(v - n_bits / 2) <= 15,
        lambda v: abs(v - n_bits / 2) <= 40,
    )
    print(f"  entropy prefix match:  {prefix_class}")
    print(f"  entropy suffix match:  {suffix_class}")
    print(f"  Hamming distance:      {hd_class}")
    print()


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--mnemonic", action="append", default=None,
        help='"LABEL:w1 w2 ... w12", repeatable; needs 2+ to compare',
    )
    parser.add_argument("--demo", action="store_true", help="run on public BIP39 test vectors instead")
    args = parser.parse_args()

    if args.demo:
        pairs = DEMO_VECTORS
        print("Running in --demo mode: these are the PUBLIC BIP39 TEST VECTORS, not real "
              "Challenge 12/13/14 data. This only proves the arithmetic below is correct and "
              "reproducible.\n"
              "Note: both demo vectors are deliberately non-random spec edge cases (all-zero "
              "and all-0x7f entropy), chosen by the BIP39 authors to exercise the encoding, "
              "not to look like real random output. Expect their Hamming distance to land far "
              "from the ~50%% independent-random band below and be labeled 'strong evidence' "
              "as a result -- that reflects these two specific constants, not a real finding. "
              "Real solved mnemonics would not have this caveat.\n")
    elif args.mnemonic:
        pairs = []
        for entry in args.mnemonic:
            if ":" not in entry:
                parser.error('each --mnemonic must be "LABEL:w1 w2 ... w12"')
            label, mnemonic = entry.split(":", 1)
            pairs.append((label, mnemonic))
    else:
        print(
            "No input given. As of this writing, no complete solved mnemonic for Challenge "
            "12 or Challenge 13 is available from any source this tool can reach (see "
            "analysis/README.md for what was checked and what is missing). Provide "
            "--mnemonic entries once real solved words are found, or pass --demo to see this "
            "tool run on the public BIP39 test vectors.",
            file=sys.stderr,
        )
        sys.exit(2)

    if len(pairs) < 2:
        parser.error("need at least 2 mnemonics to compare")

    records = [decode(label, mnemonic) for label, mnemonic in pairs]
    for rec in records:
        print_single(rec)

    for i in range(len(records)):
        for j in range(i + 1, len(records)):
            compare_pair(records[i], records[j])


if __name__ == "__main__":
    main()
