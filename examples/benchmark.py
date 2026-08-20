#!/usr/bin/env python3
"""
benchmark.py -- measure local BIP39-to-address throughput on a small, safe sample.

Purpose:
    Time how many full BIP39 candidates (checksum decode -> seed -> BIP84 derivation ->
    address) this machine can check per second, using a small number of candidates (a few
    thousand by default). This is a measurement tool, not a search tool: it never targets a
    real puzzle address and defaults to a size deliberately too small to matter.

Input:
    --count N (default 2000, capped at 20000 to keep this a "small benchmark" by
    construction), --path bip84|bip49|bip44.

Output:
    "Candidates tested / Time / Rate" summary, then a printed table projecting how long
    larger hypothetical search spaces would take at the measured rate -- arithmetic only,
    no actual search of those larger spaces.

Usage:
    python examples/benchmark.py
    python examples/benchmark.py --count 5000
    python examples/benchmark.py --project 2251799813685248   # e.g. Challenge 14's space

Why this measures the real cost:
    Each candidate here goes through the same steps a real solver's oracle would run:
    Bip39MnemonicGenerator.FromEntropy (always checksum-valid, so the checksum-decode cost
    is representative even though we skip re-deriving it), Bip39SeedGenerator (PBKDF2-HMAC-
    SHA512, 2048 rounds -- the dominant cost), and one BIP84 derivation down to an address.
    A real brute force would also try BIP49/BIP44 per candidate (see tools/oracle.py), which
    is roughly 3x slower; this benchmark measures one path only and says so in its output.

Study next: 3-small-prizes/exitonly-challenge-14-30ksats/analysis/search_space.py computes
the real N for that puzzle; this script gives you a real D (rate) to divide N by.
"""
import argparse
import os
import time

from bip_utils import (
    Bip39MnemonicGenerator,
    Bip39SeedGenerator,
    Bip39EntropyBitLen,
    Bip84,
    Bip84Coins,
    Bip44Changes,
)

MAX_COUNT = 20000  # keeps this a small benchmark by construction, not a search tool


def run(count: int) -> float:
    start = time.perf_counter()
    for _ in range(count):
        entropy = os.urandom(Bip39EntropyBitLen.BIT_LEN_128 // 8)
        mnemonic = Bip39MnemonicGenerator().FromEntropy(entropy)
        seed = Bip39SeedGenerator(mnemonic).Generate()
        Bip84.FromSeed(seed, Bip84Coins.BITCOIN).Purpose().Coin().Account(0) \
            .Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress()
    return time.perf_counter() - start


def project(rate: float, spaces: list):
    print("\nHypothetical time at this measured rate (arithmetic projection, not a run):")
    print(f"{'candidates':>24} | {'time':>20}")
    for n, label in spaces:
        seconds = n / rate if rate > 0 else float("inf")
        print(f"{n:>24,} | {fmt_duration(seconds):>20}   ({label})")


def fmt_duration(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.2f} s"
    minutes = seconds / 60
    if minutes < 60:
        return f"{minutes:.1f} min"
    hours = minutes / 60
    if hours < 24:
        return f"{hours:.1f} h"
    days = hours / 24
    if days < 365:
        return f"{days:.1f} days"
    years = days / 365.25
    return f"{years:,.0f} years"


def main():
    parser = argparse.ArgumentParser(description="Small local BIP39-to-address rate benchmark.")
    parser.add_argument("--count", type=int, default=2000, help=f"candidates to test (max {MAX_COUNT})")
    parser.add_argument(
        "--project", type=int, action="append", default=None,
        help="an additional candidate-space size to project time for (repeatable)",
    )
    args = parser.parse_args()

    if args.count > MAX_COUNT:
        raise SystemExit(f"--count is capped at {MAX_COUNT} in this script; this is a benchmark, not a search tool")
    if args.count < 1:
        raise SystemExit("--count must be positive")

    elapsed = run(args.count)
    rate = args.count / elapsed if elapsed > 0 else float("inf")

    print(f"Candidates tested: {args.count:,}")
    print(f"Time: {elapsed:.3f} seconds")
    print(f"Rate: {rate:,.1f} candidates/sec (single core, pure Python, BIP84 address only)")

    default_spaces = [
        (10_000, "same order as this benchmark, sanity check"),
        (2048 ** 4 * 128, "Challenge 14: 4 free words + checksum-constrained 5th, positions known"),
    ]
    extra_spaces = [(n, "user-supplied --project value") for n in (args.project or [])]
    project(rate, default_spaces + extra_spaces)


if __name__ == "__main__":
    main()
