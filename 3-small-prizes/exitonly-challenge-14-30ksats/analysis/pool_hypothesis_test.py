#!/usr/bin/env python3
"""
pool_hypothesis_test.py -- test whether Challenge 14's 5 missing words come from a small,
explicit pool of words already seen elsewhere in the series, instead of the full 2048-word
BIP39 list.

Purpose:
    Fills Challenge 14's 5 unknown word slots only from a small candidate pool, tried in
    every one of the C(12,5)=792 possible slot arrangements (positions are NOT assumed, per
    this puzzle's own open question). Every checksum-valid combination is derived under
    BIP84 and compared to the live escrow. This is a real, live attempt (unlike
    practice_range.py's rehearsals against dead escrows), kept small specifically because
    the pool is small, not because the puzzle itself is small.

    Default pool (10 words): the 3 words that repeat across two different episodes anywhere
    in Challenges 1-14 (adult, army, expire -- see tested.md's word-reuse statistics: this
    is NOT more repetition than pure chance predicts, ~3 observed vs ~4.5 expected, so this
    pool has no real statistical support) plus Challenge 14's own 7 known words (BIP39
    allows a word to repeat within one mnemonic, so re-using an already-known word in an
    unknown slot is a legal, if low-prior, guess).

    Defaults to a single process. --workers N > 1 splits the 792 slot arrangements across N
    worker processes instead. That multiprocessing path is UNTESTED END TO END in the
    sandbox this script was built in: a real run there failed immediately with WinError 5
    ("Acceso denegado") duplicating the spawn pipe handle between processes -- confirmed with
    a small 2-worker reproduction, logged in tested.md, and it is an OS/sandbox-level
    restriction on spawning child processes, not a bug in the candidate-checking logic
    itself (that logic is covered by a separate planted-match self-test, also in tested.md).
    It may well work fine in a normal local terminal outside that sandbox; there is just no
    confirmed successful run of --workers to point to yet. If it fails for you the same way,
    fall back to the single-process default -- slower (~35-40 min for the checksum-filter
    pass over all 79.2M raw candidates, ~1 hour more for the ~4.95M BIP84 derivations the
    filter leaves) but with nothing OS-specific to go wrong.

Input:
    --pool "w1 w2 ..." (default: the 10-word set above), --target (default: Challenge 14's
    own escrow), --workers (default 1; try a small number like 4-6 if you want to test
    multiprocessing on your own machine), --progress-every (default 2,000,000; how often to
    print a progress line in single-process mode).

Output:
    Total raw and checksum-valid candidate counts before any derivation runs, then periodic
    progress lines, then MATCH (with the full mnemonic and address) or a final NO MATCH
    summary. Never broadcasts or constructs a transaction; a MATCH only prints the mnemonic
    and address, it does not spend anything.

Usage:
    python analysis/pool_hypothesis_test.py

Cryptographic parts worth studying:
    Same BIP39 checksum + BIP84 derivation as candidate_checker.py. The structural
    difference is the two nested loops: the outer one is itertools.combinations(range(12),5)
    -- README.md's "Case B" position multiplier, C(12,5)=792 -- and the inner one is
    itertools.product(pool, repeat=5) -- every ordered way to fill those 5 chosen slots from
    the pool, with repetition allowed. The known 7 words fill the remaining 7 slots in the
    order given in clues/author-posts.md, per position within itertools.combinations'
    complement.
"""
import argparse
import itertools
import multiprocessing as mp
import sys
import time

from bip_utils import (
    Bip39MnemonicValidator, Bip39SeedGenerator,
    Bip84, Bip84Coins, Bip44Changes,
)

KNOWN_WORDS = ["dad", "butter", "wink", "follow", "trophy", "mixed", "erosion"]
TARGET = "bc1q5rjy2cdfy4n4dkk4r6pxtwqlm8tgjcc2dj0ee9"
DEFAULT_POOL = ["adult", "army", "expire"] + KNOWN_WORDS


def derive_bip84_address(mnemonic: str) -> str:
    seed = Bip39SeedGenerator(mnemonic).Generate()
    return (
        Bip84.FromSeed(seed, Bip84Coins.BITCOIN).Purpose().Coin().Account(0)
        .Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        .PublicKey().ToAddress()
    )


def build_mnemonic(slots: tuple, fillers: tuple) -> str:
    words = [None] * 12
    for slot, word in zip(slots, fillers):
        words[slot] = word
    known_iter = iter(KNOWN_WORDS)
    for i in range(12):
        if words[i] is None:
            words[i] = next(known_iter)
    return " ".join(words)


def run_single(slot_combos, pool, target, k, progress_every):
    raw_total = len(slot_combos) * (len(pool) ** k)
    validator = Bip39MnemonicValidator()
    tried = 0
    checksum_valid = 0
    start = time.perf_counter()
    found = None

    for slots in slot_combos:
        for fillers in itertools.product(pool, repeat=k):
            mnemonic = build_mnemonic(slots, fillers)
            tried += 1
            if tried % progress_every == 0:
                elapsed = time.perf_counter() - start
                rate = tried / elapsed
                remaining = (raw_total - tried) / rate if rate > 0 else float("inf")
                print(f"  ... {tried:,}/{raw_total:,} raw checked, {checksum_valid:,} checksum-valid so far, "
                      f"{rate:,.0f}/s, ~{remaining/60:,.1f} min remaining", flush=True)
            if not validator.IsValid(mnemonic):
                continue
            checksum_valid += 1
            address = derive_bip84_address(mnemonic)
            if address == target:
                found = (mnemonic, address)
                break
        if found:
            break

    elapsed = time.perf_counter() - start
    return found, tried, checksum_valid, elapsed


def _worker(task):
    worker_id, slot_combos_chunk, pool, target, k = task
    validator = Bip39MnemonicValidator()
    tried = 0
    checksum_valid = 0
    for slots in slot_combos_chunk:
        for fillers in itertools.product(pool, repeat=k):
            mnemonic = build_mnemonic(slots, fillers)
            tried += 1
            if not validator.IsValid(mnemonic):
                continue
            checksum_valid += 1
            address = derive_bip84_address(mnemonic)
            if address == target:
                return {"worker": worker_id, "tried": tried, "checksum_valid": checksum_valid,
                        "match": (mnemonic, address)}
    return {"worker": worker_id, "tried": tried, "checksum_valid": checksum_valid, "match": None}


def _chunk(lst, n):
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]


def run_parallel(slot_combos, pool, target, k, workers):
    chunks = [c for c in _chunk(slot_combos, workers) if c]
    tasks = [(i, c, pool, target, k) for i, c in enumerate(chunks)]

    start = time.perf_counter()
    tried = 0
    checksum_valid = 0
    found = None
    with mp.Pool(processes=len(tasks)) as p:
        for result in p.imap_unordered(_worker, tasks):
            tried += result["tried"]
            checksum_valid += result["checksum_valid"]
            elapsed = time.perf_counter() - start
            print(f"  worker {result['worker']} done: {result['tried']:,} tried, "
                  f"{result['checksum_valid']:,} checksum-valid, elapsed {elapsed:.0f}s", flush=True)
            if result["match"]:
                found = result["match"]

    elapsed = time.perf_counter() - start
    return found, tried, checksum_valid, elapsed


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--pool", default=" ".join(DEFAULT_POOL), help="space-separated candidate pool")
    parser.add_argument("--target", default=TARGET, help="escrow address to compare against")
    parser.add_argument("--workers", type=int, default=1,
                         help="worker processes; 1 (default) = single process, known to work. "
                              ">1 uses multiprocessing, UNTESTED end to end in this sandbox (see module docstring)")
    parser.add_argument("--progress-every", type=int, default=2_000_000,
                         help="print a progress line every N raw candidates (single-process mode only)")
    args = parser.parse_args()

    pool = args.pool.split()
    k = 5
    slot_combos = list(itertools.combinations(range(12), k))
    raw_total = len(slot_combos) * (len(pool) ** k)

    print(f"pool ({len(pool)} words): {pool}", flush=True)
    print(f"known words (fill the other 7 slots, in this order): {KNOWN_WORDS}", flush=True)
    print(f"target: {args.target}", flush=True)
    mode = "single process" if args.workers <= 1 else f"{args.workers} worker processes (untested here, see docstring)"
    print(f"slot arrangements: {len(slot_combos)} (C(12,5)), {mode}", flush=True)
    print(f"raw candidates: {raw_total:,}", flush=True)
    print(f"expected checksum-valid (full BIP84 derivation needed): ~{raw_total // 16:,}\n", flush=True)

    if args.workers <= 1:
        found, tried, checksum_valid, elapsed = run_single(slot_combos, pool, args.target, k, args.progress_every)
    else:
        found, tried, checksum_valid, elapsed = run_parallel(slot_combos, pool, args.target, k, args.workers)

    print(f"\ntotal raw candidates tried: {tried:,}")
    print(f"total checksum-valid candidates: {checksum_valid:,}")
    print(f"total time: {elapsed:.1f}s ({tried/elapsed:,.0f}/s)\n")

    if found:
        mnemonic, address = found
        print("MATCH")
        print(f"  mnemonic: {mnemonic}")
        print(f"  address: {address}")
        print("\nThis is a live escrow. Do not broadcast anything from this script -- it only")
        print("checks candidates. Stop here and hand the mnemonic to a human before any spend.")
    else:
        print("NO MATCH. The pool-reuse hypothesis (with this specific 10-word pool) is refuted"
              " for Challenge 14 across all 792 position arrangements.")
        sys.exit(1)


if __name__ == "__main__":
    main()
