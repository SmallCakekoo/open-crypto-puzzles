#!/usr/bin/env python3
"""
benchmark_parallel.py -- small, capped multi-process throughput measurement.

Purpose:
    examples/benchmark.py measures single-core throughput (~360-480 candidates/sec on this
    machine; profiling showed PBKDF2-HMAC-SHA512 seed generation, at 2048 rounds by design,
    is ~75%% of that cost, with BIP32/84 derivation the other ~25%%; bip_utils already calls
    the C-accelerated hashlib.pbkdf2_hmac, so there is no faster single-call implementation
    to switch to here). Since each candidate's PBKDF2 call is independent, the only real
    lever left is spreading candidates across CPU cores. This script measures that, still on
    a small, safe candidate count -- it is a rate measurement, not a search tool.

    Worker count is capped at 6 (physical cores on this machine, not the 12 logical/
    hyperthreaded count os.cpu_count() reports) at the user's explicit instruction, to leave
    headroom on the machine rather than saturate every logical thread.

Input:
    --count N (default 6000, same MAX_COUNT cap as benchmark.py), --workers N (default 6,
    hard-capped at 6 in this script).

Output:
    Candidates tested, wall-clock time, aggregate rate, and the same "hypothetical time at
    this rate" projection as benchmark.py, so the two are directly comparable.

Usage:
    python examples/benchmark_parallel.py
    python examples/benchmark_parallel.py --count 6000 --workers 6

This still never targets a real puzzle address and is capped well below anything that would
constitute a real search.
"""
import argparse
import multiprocessing as mp
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

MAX_COUNT = 20000
MAX_WORKERS = 6  # capped at physical cores, not os.cpu_count()'s 12 logical threads, per instruction


def derive_one(_):
    entropy = os.urandom(Bip39EntropyBitLen.BIT_LEN_128 // 8)
    mnemonic = Bip39MnemonicGenerator().FromEntropy(entropy)
    seed = Bip39SeedGenerator(mnemonic).Generate()
    return (
        Bip84.FromSeed(seed, Bip84Coins.BITCOIN).Purpose().Coin().Account(0)
        .Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress()
    )


def fmt_duration(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.2f} s"
    m = seconds / 60
    if m < 60:
        return f"{m:.1f} min"
    h = m / 60
    if h < 24:
        return f"{h:.1f} h"
    d = h / 24
    if d < 365:
        return f"{d:.1f} days"
    y = d / 365.25
    return f"{y:,.0f} years"


def main():
    parser = argparse.ArgumentParser(description="Small multi-process BIP39-to-address rate benchmark.")
    parser.add_argument("--count", type=int, default=6000, help=f"candidates to test (max {MAX_COUNT})")
    parser.add_argument("--workers", type=int, default=MAX_WORKERS, help=f"worker processes (hard-capped at {MAX_WORKERS})")
    args = parser.parse_args()

    if args.count > MAX_COUNT:
        raise SystemExit(f"--count is capped at {MAX_COUNT}; this is a benchmark, not a search tool")
    workers = min(args.workers, MAX_WORKERS)

    print(f"logical CPUs reported by the OS: {os.cpu_count()} (not used as the cap)")
    print(f"worker processes for this run: {workers} (capped at physical cores, per instruction)\n")

    start = time.perf_counter()
    with mp.Pool(processes=workers) as pool:
        pool.map(derive_one, range(args.count), chunksize=max(1, args.count // (workers * 8)))
    elapsed = time.perf_counter() - start
    rate = args.count / elapsed if elapsed > 0 else float("inf")

    print(f"Candidates tested: {args.count:,}")
    print(f"Time: {elapsed:.3f} seconds")
    print(f"Rate: {rate:,.1f} candidates/sec across {workers} processes "
          f"({rate/workers:,.1f}/sec/process)")

    spaces = [
        (61_312_204_800, "Ch1-10 style: 1 missing word, order of known words also unknown (12!/1!)"),
        (2048 ** 4 * 128, "Challenge 14: 4 free words + checksum-constrained 5th, positions known"),
    ]
    print("\nHypothetical time at this measured rate (arithmetic projection, not a run):")
    for n, label in spaces:
        print(f"{n:>24,} | {fmt_duration(n / rate):>20}   ({label})")


if __name__ == "__main__":
    main()
