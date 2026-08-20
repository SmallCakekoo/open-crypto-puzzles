#!/usr/bin/env python3
"""
bruteforce_recheck_paths.py -- re-derives addresses for the checksum-valid
mnemonics ALREADY saved in bruteforce_checksumvalid_*.jsonl, across a WIDER path
space than tools/oracle.py checks, without regenerating or re-validating any of
the 205,263,936 candidates from scratch. Checksum validity does not depend on
derivation path, so this is safe: the saved mnemonics are exactly the same set a
full re-run would find valid.

Why this exists (2026-08-20 audit): tools/oracle.py checks BIP84, BIP49 and BIP44
(2 accounts x 3 indices, receive/external chain only) plus 3 raw paths. Verified
empirically: BIP49 addresses always start with "3..." and BIP44 always with
"1...", so neither can EVER equal the target bc1q... address -- checking them was
harmless but added no real coverage for this specific target. Only BIP84 and the
3 raw P2WPKH paths could ever match. Two real gaps in what was actually tested:
  - the internal/change chain (Bip44Changes.CHAIN_INT) was never tried, only
    external/receive;
  - only accounts 0-1 and indices 0-2 were tried.

This script re-derives, for every already-saved checksum-valid mnemonic, BIP84
addresses across a much wider account/index range and BOTH chains, still using
the exact same bip_utils calls tools/oracle.py uses (imported, not reimplemented).

Usage:
  python analysis/bruteforce_recheck_paths.py --phase phase1 --accounts 5 --indices 20
  python analysis/bruteforce_recheck_paths.py --phase phase2a --accounts 5 --indices 20
  python analysis/bruteforce_recheck_paths.py --all-phase3 --accounts 3 --indices 10
"""

from __future__ import annotations

import argparse
import glob
import json
import multiprocessing as mp
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PUZZLE_ROOT = HERE.parent
sys.path.insert(0, str(PUZZLE_ROOT / "tools"))

from bip_utils import Bip84, Bip84Coins, Bip39SeedGenerator, Bip44Changes  # noqa: E402
import oracle  # noqa: E402  (for TARGET_ADDRESS only)

DEFAULT_OUTDIR = Path("Z:/bitcoin-movie-enigma-bruteforce")
CHUNK_SIZE = 200  # lines per worker task


def wide_addresses(mnemonic: str, accounts: int, indices: int) -> dict[str, str]:
    """BIP84 only (the one path family that can structurally produce a bc1q
    address), swept across a wider account/index range AND both chains
    (external/receive and internal/change) than tools/oracle.py tries."""
    seed = Bip39SeedGenerator(mnemonic).Generate("")
    ctx = Bip84.FromSeed(seed, Bip84Coins.BITCOIN)
    out = {}
    for acct in range(accounts):
        for change in (Bip44Changes.CHAIN_EXT, Bip44Changes.CHAIN_INT):
            change_name = "receive" if change == Bip44Changes.CHAIN_EXT else "change"
            for i in range(indices):
                node = ctx.Purpose().Coin().Account(acct).Change(change).AddressIndex(i)
                addr = node.PublicKey().ToAddress()
                out[f"bip84 account {acct} {change_name} index {i}"] = addr
    return out


def _worker_recheck_chunk(args: tuple[list[dict], int, int, str]) -> tuple[int, list[dict]]:
    records, accounts, indices, source_file = args
    n = 0
    matches = []
    for rec in records:
        mnemonic = rec["mnemonic"]
        n += 1
        for path_name, addr in wide_addresses(mnemonic, accounts, indices).items():
            if addr == oracle.TARGET_ADDRESS:
                matches.append({
                    "candidate_index": rec.get("candidate_index"),
                    "mnemonic": mnemonic,
                    "address": addr,
                    "path": path_name,
                    "source_file": source_file,
                })
    return n, matches


def _read_records(path: Path) -> list[dict]:
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def build_chunks(files: list[Path], accounts: int, indices: int) -> tuple[list[tuple], int]:
    """One flat list of (records_chunk, accounts, indices, source_file) tuples
    spanning ALL files, so a single Pool can be used for the whole run instead of
    spawning a fresh set of worker processes per file (the actual cause of the
    slowdown: on Windows, each mp.Pool(...) spawns new interpreter processes,
    and most of the 216 phase-3 files have far too few records for that spawn
    cost to be worth paying per file)."""
    chunks = []
    total_records = 0
    for path in files:
        records = _read_records(path)
        total_records += len(records)
        for i in range(0, len(records), CHUNK_SIZE):
            chunks.append((records[i:i + CHUNK_SIZE], accounts, indices, str(path)))
    return chunks, total_records


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--outdir", default=str(DEFAULT_OUTDIR))
    ap.add_argument("--phase")
    ap.add_argument("--all-phase3", action="store_true")
    ap.add_argument("--accounts", type=int, default=5, help="BIP84 accounts 0..N-1 (oracle.py only tries 2)")
    ap.add_argument("--indices", type=int, default=20, help="address indices 0..N-1 per (account,chain) (oracle.py only tries 3, receive only)")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    outdir = Path(args.outdir)
    if args.all_phase3:
        files = sorted(Path(p) for p in glob.glob(str(outdir / "bruteforce_checksumvalid_phase3_*.jsonl")))
    elif args.phase:
        files = [outdir / f"bruteforce_checksumvalid_{args.phase}.jsonl"]
    else:
        ap.error("pass --phase phase1|phase2a or --all-phase3")
        return 1

    files = [f for f in files if f.exists()]
    if not files:
        print(f"no checksum-valid files found under {outdir}")
        return 1

    print(f"reading {len(files)} file(s)...")
    chunks, total_records = build_chunks(files, args.accounts, args.indices)
    print(f"re-checking {total_records:,} mnemonics across {len(files)} file(s) in {len(chunks)} "
          f"chunk(s) of up to {CHUNK_SIZE}, BIP84 accounts=0..{args.accounts-1}, "
          f"indices=0..{args.indices-1}, both receive and change chains "
          f"({args.accounts * args.indices * 2} addresses per mnemonic, vs oracle.py's 6 receive-only), "
          f"workers={args.workers} (ONE pool for the whole run, not per file)", flush=True)

    t0 = time.time()
    total_mnemonics = 0
    all_matches = []
    last_print = t0

    def _process(n, matches):
        nonlocal total_mnemonics, last_print
        total_mnemonics += n
        all_matches.extend(matches)
        if matches:
            print(f"!!! MATCH: {matches}", flush=True)
        now = time.time()
        if now - last_print >= 5.0:
            elapsed = now - t0
            rate = total_mnemonics / elapsed if elapsed > 0 else 0.0
            remaining = total_records - total_mnemonics
            eta = remaining / rate if rate > 0 else float("inf")
            eta_str = "unknown" if eta == float("inf") else f"{eta:.0f}s"
            print(f"  {total_mnemonics:,}/{total_records:,} "
                  f"({100*total_mnemonics/total_records:.1f}%) | {rate:,.1f}/s | "
                  f"matches={len(all_matches)} | elapsed={elapsed:.0f}s | ETA={eta_str}", flush=True)
            last_print = now

    if args.workers <= 1 or len(chunks) <= 1:
        for chunk in chunks:
            n, matches = _worker_recheck_chunk(chunk)
            _process(n, matches)
    else:
        with mp.Pool(processes=args.workers) as pool:
            for n, matches in pool.imap_unordered(_worker_recheck_chunk, chunks, chunksize=1):
                _process(n, matches)

    dt = time.time() - t0
    print(f"\ndone: {total_mnemonics} already-checksum-valid mnemonics re-derived across a wider "
          f"BIP84 path space in {dt:.1f}s ({total_mnemonics/dt:,.1f}/s), {len(all_matches)} match(es).")
    if all_matches:
        out = outdir / "bruteforce_widepath_matches.json"
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(all_matches, fh, indent=2)
        print(f"matches written to {out}")
    else:
        print("0 matches. This does not re-test word choices -- only widens which BIP84 "
              "account/index/chain combinations were tried for the SAME already-checksum-valid "
              "mnemonics found earlier.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
