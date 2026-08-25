#!/usr/bin/env python3
"""
bench_scale.py -- measure this machine's real parallel throughput before
committing to a multi-hour sweep.

Why: the sweep's cost is dominated by PBKDF2-HMAC-SHA512 (2048 iterations,
BIP39's seed step), which is pure CPU and does not vectorise. Per-core rate
varies by several times across machines, and parallel scaling is often far
worse than the core count suggests -- a development laptop measured here hit
only 3.3x with 8 workers (4 physical cores plus hyperthreading, plus thermal
throttling). Do not size a run from a core count. Measure.

Usage:
    python3 tools/bench_scale.py
    python3 tools/bench_scale.py --max-workers 24 --seconds 6

Read the output as: pick the worker count where throughput stops improving,
then divide the candidate counts in tools/README-sweep.md by that rate.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import time
from multiprocessing import Pool

import fastderive as fd


def _job(args):
    start, count = args
    for i in range(start, start + count):
        fd.derive_hash160s(hashlib.md5(str(i).encode()).digest(), 6)
    return count


def measure(workers: int, batch: int, batches_per_worker: int = 4) -> float:
    tasks = [(w * batch, batch) for w in range(workers * batches_per_worker)]
    t0 = time.perf_counter()
    with Pool(workers) as pool:
        n = sum(pool.map(_job, tasks, chunksize=1))
    return n / (time.perf_counter() - t0)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-workers", type=int, default=os.cpu_count())
    ap.add_argument("--seconds", type=float, default=4.0,
                    help="rough target duration per measurement")
    args = ap.parse_args()

    print(f"logical cores reported: {os.cpu_count()}")

    t0 = time.perf_counter()
    for i in range(40):
        fd.derive_hash160s(hashlib.md5(str(i).encode()).digest(), 6)
    single = 40 / (time.perf_counter() - t0)
    print(f"single-core baseline:   {single:,.0f} candidates/sec\n")

    batch = max(10, int(single * args.seconds / 4))

    counts = []
    w = 1
    while w < args.max_workers:
        counts.append(w)
        w *= 2
    counts.append(args.max_workers)

    best = (0, 0.0)
    print(f"{'workers':>8s} {'cand/s':>12s} {'speedup':>9s} {'efficiency':>11s}")
    for w in counts:
        rate = measure(w, batch)
        if rate > best[1]:
            best = (w, rate)
        print(f"{w:8d} {rate:12,.0f} {rate/single:8.1f}x {100*rate/(single*w):10.0f}%")

    print(f"\nbest: {best[0]} workers at {best[1]:,.0f} candidates/sec")
    print("\nestimated wall time for the large sweeps at that rate:")
    for name, n in (("ranges --profile full", 43_085_952), ("edit2", 37_503_424)):
        print(f"  {name:24s} {n:12,d} candidates -> {n/best[1]/3600:6.2f} h")
    print("\nSmaller sweeps (transpose, ranges core, appbytes) are minutes or less.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
