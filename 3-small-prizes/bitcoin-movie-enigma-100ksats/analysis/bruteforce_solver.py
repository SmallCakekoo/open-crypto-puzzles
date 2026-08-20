#!/usr/bin/env python3
"""
bruteforce_solver.py -- local, resumable, multiprocess brute-force search for the
Bitcoin Movie Enigma, over the exact 24-keeper / word-candidate space frozen by the
user on 2026-08-20 (see bruteforce_config.json). Meant to run on the user's own
machine overnight, not inside a Claude Code turn.

What this does NOT do:
  - It does not invent words. Raiders of the Lost Ark ("__WORDLIST__" in the
    config) is swept across the full, real 2048-word English BIP39 list because
    no candidate for it has been derived from real evidence yet -- that is
    exactly the question phase 1 asks the target address.
  - It does not modify data/films.csv, tools/oracle.py, or any canonical file.
  - It does not change the derivation paths: every candidate is checked with the
    SAME oracle.check()/oracle.addresses() functions already in tools/oracle.py
    (BIP84, BIP49, BIP44, 2 accounts x 3 indices each, plus the 3 raw paths). This
    script imports that module directly; it does not reimplement any crypto.

Word order used: ascending panel number among the 24 keepers. This is the order
already used throughout this repo (analysis/build_candidates.py's KEEPER_WORDS is
listed in panel order) and is what README.md states: "leaving the real 24-word
mnemonic in panel order." See bruteforce_config.json's keeper_order.

Phases:
  phase1  -- 589,824 candidates (6 ambiguous panels x Goonies x full Raiders sweep;
             Sharknado fixed at "april").
  phase2a -- 1,179,648 candidates (same as phase1, Sharknado also allows "tornado").
             Only meaningful if phase1 finds 0 matches.
  phase2b -- not run: Raiders has no backed candidate to swap the sweep target to
             without inventing one. `--phase 2b` just prints why.
  phase3  -- one-in/one-out on H1 (separate script: bruteforce_phase3_oneinoneout.py).

Usage:
  python analysis/bruteforce_solver.py --selftest
  python analysis/bruteforce_solver.py --dry-run 100 --phase 1
  python analysis/bruteforce_solver.py --run --phase 1 --workers 8
  python analysis/bruteforce_solver.py --resume --phase 1 --workers 8
  python analysis/bruteforce_solver.py --status --phase 1
  python analysis/bruteforce_solver.py --phase 2b
  python analysis/bruteforce_solver.py --auto --workers 8   # phase1, then phase2a if phase1=0, then reports 2b/3

All progress/results/log files default to Z:\\bitcoin-movie-enigma-bruteforce\\
(override with --outdir). bruteforce_config.json stays in this analysis/ folder.
"""

from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PUZZLE_ROOT = HERE.parent
DEFAULT_CONFIG_PATH = HERE / "bruteforce_config.json"
DEFAULT_OUTDIR = Path("Z:/bitcoin-movie-enigma-bruteforce")

sys.path.insert(0, str(PUZZLE_ROOT / "tools"))
import oracle  # noqa: E402  (tools/oracle.py, imported unmodified)
from bip_utils import Bip39MnemonicValidator  # noqa: E402  (same import oracle.py uses)

BLOCK_SIZE = 10_000


# --------------------------------------------------------------------------- #
# Config / wordlist loading
# --------------------------------------------------------------------------- #

def load_config(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_bip39_wordlist(path: str) -> list[str]:
    words = Path(path).read_text(encoding="utf-8").split()
    if len(words) != 2048:
        raise RuntimeError(f"expected 2048 BIP39 words at {path}, got {len(words)}")
    return words


def resolve_word_lists(cfg: dict, phase: str, wordlist_2048: list[str]) -> tuple[list[int], list[list[str]]]:
    """Return (keeper_order, list-of-word-lists) for the given phase, in panel order."""
    key = {"phase1": "phase1_words", "phase2a": "phase2a_words"}[phase]
    words_by_panel = cfg[key]
    order = cfg["keeper_order"]
    lists = []
    for panel in order:
        entry = words_by_panel[str(panel)]
        if entry == "__WORDLIST__":
            lists.append(wordlist_2048)
        else:
            lists.append(entry)
    return order, lists


# --------------------------------------------------------------------------- #
# Mixed-radix enumeration: map a flat integer index <-> one word per keeper panel
# --------------------------------------------------------------------------- #

def total_count(word_lists: list[list[str]]) -> int:
    total = 1
    for wl in word_lists:
        total *= len(wl)
    return total


def index_to_words(idx: int, word_lists: list[list[str]]) -> list[str]:
    sizes = [len(wl) for wl in word_lists]
    digits = []
    for size in reversed(sizes):
        idx, r = divmod(idx, size)
        digits.append(r)
    digits.reverse()
    return [word_lists[i][d] for i, d in enumerate(digits)]


def words_to_mnemonic(words: list[str]) -> str:
    return " ".join(words)


# --------------------------------------------------------------------------- #
# Per-candidate check -- uses tools/oracle.py's own functions, unmodified
# --------------------------------------------------------------------------- #

def check_candidate(mnemonic: str) -> tuple[bool, bool, str | None, str | None]:
    """Return (checksum_valid, matched, address, path). Mirrors oracle.check()
    exactly (same Bip39MnemonicValidator, same oracle.addresses()), decomposed
    only so the caller can also count checksum-valid candidates for stats."""
    valid = Bip39MnemonicValidator().IsValid(mnemonic)
    if not valid:
        return False, False, None, None
    for path, addr in oracle.addresses(mnemonic).items():
        if addr == oracle.TARGET_ADDRESS:
            return True, True, addr, path
    return True, False, None, None


# --------------------------------------------------------------------------- #
# Worker (multiprocessing) -- processes one block of consecutive indices
# --------------------------------------------------------------------------- #

_WORKER_WORD_LISTS: list[list[str]] | None = None
_WORKER_KEEPER_ORDER: list[int] | None = None


def _worker_init(word_lists: list[list[str]], keeper_order: list[int]) -> None:
    global _WORKER_WORD_LISTS, _WORKER_KEEPER_ORDER
    _WORKER_WORD_LISTS = word_lists
    _WORKER_KEEPER_ORDER = keeper_order


def _worker_process_block(args: tuple[int, int, int]) -> dict:
    block_id, start, size = args
    word_lists = _WORKER_WORD_LISTS
    keeper_order = _WORKER_KEEPER_ORDER
    checksum_valid_records = []
    matches = []
    end = start + size
    for idx in range(start, end):
        words = index_to_words(idx, word_lists)
        mnemonic = words_to_mnemonic(words)
        valid, matched, addr, path = check_candidate(mnemonic)
        if valid:
            # Every checksum-valid candidate is kept, not just a running count:
            # candidate_index, mnemonic, and checksum_valid=true at minimum, plus
            # the panel/word breakdown for traceability.
            checksum_valid_records.append({
                "candidate_index": idx,
                "mnemonic": mnemonic,
                "checksum_valid": True,
                "block_id": block_id,
                "panel_words": {str(p): w for p, w in zip(keeper_order, words)},
            })
        if matched:
            matches.append({
                "index": idx,
                "block_id": block_id,
                "panel_words": {str(p): w for p, w in zip(keeper_order, words)},
                "mnemonic": mnemonic,
                "address": addr,
                "path": path,
            })
    return {
        "block_id": block_id,
        "processed": end - start,
        "checksum_valid": len(checksum_valid_records),
        "checksum_valid_records": checksum_valid_records,
        "matches": matches,
    }


# --------------------------------------------------------------------------- #
# Progress / results / log I/O
# --------------------------------------------------------------------------- #

def progress_path(outdir: Path, phase: str) -> Path:
    return outdir / f"bruteforce_progress_{phase}.json"


def results_path(outdir: Path, phase: str) -> Path:
    return outdir / f"bruteforce_results_{phase}.json"


def checksumvalid_path(outdir: Path, phase: str) -> Path:
    """JSON Lines (one record per line, append-only) so this scales to tens of
    thousands of checksum-valid records per phase without rewriting the whole
    file on every block, unlike results_path()'s plain-JSON list."""
    return outdir / f"bruteforce_checksumvalid_{phase}.jsonl"


def append_checksum_valid(outdir: Path, phase: str, records: list[dict]) -> None:
    if not records:
        return
    outdir.mkdir(parents=True, exist_ok=True)
    with open(checksumvalid_path(outdir, phase), "a", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")


def log_path(outdir: Path) -> Path:
    return outdir / "bruteforce.log"


def log(outdir: Path, msg: str) -> None:
    line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line)
    outdir.mkdir(parents=True, exist_ok=True)
    with open(log_path(outdir), "a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_progress(outdir: Path, phase: str, total: int) -> dict:
    p = progress_path(outdir, phase)
    if p.exists():
        with open(p, encoding="utf-8") as f:
            data = json.load(f)
        if data.get("total_candidates") == total:
            return data
        log(outdir, f"WARNING: existing progress file total ({data.get('total_candidates')}) "
                     f"!= expected ({total}); starting fresh for phase {phase}.")
    return {
        "phase": phase,
        "total_candidates": total,
        "block_size": BLOCK_SIZE,
        "completed_blocks": [],
        "processed_count": 0,
        "checksum_valid_count": 0,
        "matches_count": 0,
        "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "last_updated": None,
        "elapsed_seconds": 0.0,
    }


def save_progress(outdir: Path, phase: str, progress: dict) -> None:
    progress["last_updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    outdir.mkdir(parents=True, exist_ok=True)
    tmp = progress_path(outdir, phase).with_suffix(".json.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2)
    tmp.replace(progress_path(outdir, phase))


def append_results(outdir: Path, phase: str, new_matches: list[dict]) -> None:
    if not new_matches:
        return
    p = results_path(outdir, phase)
    existing = []
    if p.exists():
        with open(p, encoding="utf-8") as f:
            existing = json.load(f)
    existing.extend(new_matches)
    outdir.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(existing, f, indent=2)


# --------------------------------------------------------------------------- #
# Phase runner
# --------------------------------------------------------------------------- #

def run_phase(cfg: dict, phase: str, outdir: Path, workers: int, resume: bool) -> int:
    """Returns total matches found (cumulative, across this and prior runs)."""
    wordlist_2048 = load_bip39_wordlist(cfg["bip39_wordlist_path"])
    keeper_order, word_lists = resolve_word_lists(cfg, phase, wordlist_2048)
    total = total_count(word_lists)
    expected = cfg[f"{phase}_expected_total"]
    if total != expected:
        raise RuntimeError(
            f"{phase}: computed total {total} != expected {expected} from config. "
            "Refusing to run until this is reconciled (do not silently proceed)."
        )

    progress = load_progress(outdir, phase, total) if resume else {
        "phase": phase, "total_candidates": total, "block_size": BLOCK_SIZE,
        "completed_blocks": [], "processed_count": 0, "checksum_valid_count": 0,
        "matches_count": 0, "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "last_updated": None, "elapsed_seconds": 0.0,
    }
    if not resume and progress_path(outdir, phase).exists():
        log(outdir, f"{phase}: --run without --resume, but a progress file already exists. "
                     f"Starting a FRESH run overwrites it. Use --resume to continue instead.")
        cv_path = checksumvalid_path(outdir, phase)
        if cv_path.exists():
            cv_path.unlink()

    completed = set(progress["completed_blocks"])
    all_block_ids = list(range(0, total, BLOCK_SIZE))
    remaining = [(bid // BLOCK_SIZE, bid, min(BLOCK_SIZE, total - bid))
                 for bid in all_block_ids if (bid // BLOCK_SIZE) not in completed]

    log(outdir, f"=== {phase} === total={total:,} block_size={BLOCK_SIZE:,} "
                f"blocks_total={len(all_block_ids)} blocks_remaining={len(remaining)} "
                f"workers={workers}")

    if not remaining:
        log(outdir, f"{phase}: already complete ({progress['processed_count']:,}/{total:,}). "
                     f"matches so far: {progress['matches_count']}")
        return progress["matches_count"]

    run_start = time.time()
    processed_this_run = 0

    with mp.Pool(processes=workers, initializer=_worker_init, initargs=(word_lists, keeper_order)) as pool:
        for result in pool.imap_unordered(_worker_process_block, remaining, chunksize=1):
            bid = result["block_id"]
            completed.add(bid)
            progress["completed_blocks"] = sorted(completed)
            progress["processed_count"] += result["processed"]
            progress["checksum_valid_count"] += result["checksum_valid"]
            processed_this_run += result["processed"]

            append_checksum_valid(outdir, phase, result.get("checksum_valid_records", []))

            if result["matches"]:
                progress["matches_count"] += len(result["matches"])
                append_results(outdir, phase, result["matches"])
                for m in result["matches"]:
                    log(outdir, f"!!! MATCH !!! index={m['index']} path={m['path']} "
                                f"address={m['address']} mnemonic={m['mnemonic']}")

            elapsed_run = time.time() - run_start
            progress["elapsed_seconds"] = progress.get("elapsed_seconds", 0.0) + 0.0
            rate = processed_this_run / elapsed_run if elapsed_run > 0 else 0.0
            remaining_count = total - progress["processed_count"]
            eta_s = remaining_count / rate if rate > 0 else float("inf")
            pct = 100.0 * progress["processed_count"] / total

            save_progress(outdir, phase, progress)
            log(outdir, f"{phase}: block {bid} done | "
                        f"{progress['processed_count']:,}/{total:,} ({pct:.2f}%) | "
                        f"checksum_valid={progress['checksum_valid_count']} | "
                        f"matches={progress['matches_count']} | "
                        f"rate={rate:,.1f}/s | ETA={_fmt_eta(eta_s)}")

    total_elapsed = progress.get("elapsed_seconds", 0.0) + (time.time() - run_start)
    progress["elapsed_seconds"] = total_elapsed
    save_progress(outdir, phase, progress)
    log(outdir, f"=== {phase} COMPLETE === processed={progress['processed_count']:,}/{total:,} "
                f"checksum_valid={progress['checksum_valid_count']} matches={progress['matches_count']} "
                f"total_elapsed={_fmt_eta(total_elapsed)}")
    return progress["matches_count"]


def _fmt_eta(seconds: float) -> str:
    if seconds == float("inf") or seconds != seconds:  # inf or nan
        return "unknown"
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}h{m:02d}m{s:02d}s"


def print_status(outdir: Path, phase: str) -> None:
    p = progress_path(outdir, phase)
    if not p.exists():
        print(f"{phase}: no progress file yet at {p}")
        return
    with open(p, encoding="utf-8") as f:
        progress = json.load(f)
    total = progress["total_candidates"]
    pct = 100.0 * progress["processed_count"] / total if total else 0.0
    print(f"phase: {progress['phase']}")
    print(f"processed: {progress['processed_count']:,} / {total:,} ({pct:.2f}%)")
    print(f"checksum_valid: {progress['checksum_valid_count']}")
    print(f"matches: {progress['matches_count']}")
    print(f"started_at: {progress['started_at']}")
    print(f"last_updated: {progress['last_updated']}")
    print(f"elapsed: {_fmt_eta(progress.get('elapsed_seconds', 0.0))}")
    cv = checksumvalid_path(outdir, phase)
    if cv.exists():
        with open(cv, encoding="utf-8") as f:
            n = sum(1 for _ in f)
        print(f"checksum-valid records file: {cv} ({n} record(s), one JSON object per line)")
    rp = results_path(outdir, phase)
    if rp.exists():
        with open(rp, encoding="utf-8") as f:
            n = len(json.load(f))
        print(f"results file: {rp} ({n} match record(s))")


# --------------------------------------------------------------------------- #
# Selftest / dry-run
# --------------------------------------------------------------------------- #

def run_selftest(cfg: dict) -> bool:
    print("--- step 1: tools/oracle.py --selftest ---")
    ok = oracle.selftest()
    if not ok:
        print("oracle selftest FAILED -- stopping, will not proceed to brute force.")
        return False

    print("\n--- step 2: solver check_candidate() vs oracle.check() consistency ---")
    good = oracle.SELFTEST_24_GOOD
    a = oracle.check(good)
    valid, matched, addr, path = check_candidate(good)
    consistent = (matched == a[0]) and (addr == a[1]) and (path == a[2])
    print(f"oracle.check(SELFTEST_24_GOOD)      = {a}")
    print(f"check_candidate(SELFTEST_24_GOOD)   = matched={matched} addr={addr} path={path}")
    print(f"consistent: {'OK' if consistent else 'FAIL'}")
    if not consistent:
        return False

    print("\n--- step 3: mixed-radix index<->words round-trip check ---")
    wordlist_2048 = load_bip39_wordlist(cfg["bip39_wordlist_path"])
    order, word_lists = resolve_word_lists(cfg, "phase1", wordlist_2048)
    total = total_count(word_lists)
    print(f"phase1 total from config words: {total:,} (expected {cfg['phase1_expected_total']:,})")
    if total != cfg["phase1_expected_total"]:
        print("MISMATCH -- stopping.")
        return False
    test_indices = [0, 1, total - 1, total // 2, 12345]
    for idx in test_indices:
        words = index_to_words(idx, word_lists)
        if len(words) != 24:
            print(f"index {idx}: FAIL, got {len(words)} words, expected 24")
            return False
    print(f"round-trip length check on indices {test_indices}: OK (all produced 24 words)")

    print("\n--- step 4: small dry run (first 100 phase-1 candidates) ---")
    checksum_valid = 0
    for idx in range(100):
        words = index_to_words(idx, word_lists)
        mnemonic = words_to_mnemonic(words)
        assert len(mnemonic.split()) == 24
        valid, matched, addr, path = check_candidate(mnemonic)
        if valid:
            checksum_valid += 1
        if matched:
            print(f"  UNEXPECTED MATCH at index {idx}: {mnemonic} -> {addr} via {path}")
    print(f"100 candidates checked, no exceptions, {checksum_valid} passed BIP39 checksum "
          f"(expected roughly 100/256 ~ 0.4 on average, so 0 or 1 is typical)")

    print("\nSELFTEST + DRY RUN: ALL OK")
    return True


def run_dry_run(cfg: dict, phase: str, n: int) -> None:
    wordlist_2048 = load_bip39_wordlist(cfg["bip39_wordlist_path"])
    order, word_lists = resolve_word_lists(cfg, phase, wordlist_2048)
    total = total_count(word_lists)
    n = min(n, total)
    t0 = time.time()
    checksum_valid = 0
    for idx in range(n):
        mnemonic = words_to_mnemonic(index_to_words(idx, word_lists))
        valid, matched, addr, path = check_candidate(mnemonic)
        checksum_valid += int(valid)
        if matched:
            print(f"MATCH at index {idx}: {mnemonic} -> {addr} via {path}")
    dt = time.time() - t0
    rate = n / dt if dt > 0 else 0.0
    print(f"dry run: {n} candidates in {dt:.2f}s ({rate:.1f}/s single-process), "
          f"{checksum_valid} checksum-valid")
    print(f"single-process ETA for full {phase} ({total:,} candidates): {_fmt_eta(total / rate) if rate else 'unknown'}")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    ap.add_argument("--outdir", default=str(DEFAULT_OUTDIR))
    ap.add_argument("--phase", choices=["1", "2a", "2b"], default="1")
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 4) - 1))
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--dry-run", type=int, metavar="N")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--auto", action="store_true",
                     help="run phase1 to completion; if 0 matches, automatically run phase2a; "
                          "then print the phase2b explanation and stop (phase3 is a separate script).")
    args = ap.parse_args()

    cfg = load_config(Path(args.config))
    outdir = Path(args.outdir)
    phase_name = {"1": "phase1", "2a": "phase2a", "2b": "phase2b"}[args.phase]

    if args.selftest:
        return 0 if run_selftest(cfg) else 1

    if args.dry_run is not None:
        run_dry_run(cfg, phase_name if phase_name != "phase2b" else "phase1", args.dry_run)
        return 0

    if args.status:
        print_status(outdir, phase_name)
        return 0

    if args.phase == "2b" or phase_name == "phase2b":
        print(cfg["phase2b_status"])
        return 0

    if args.auto:
        log(outdir, "AUTO MODE: phase1 -> (if 0 matches) phase2a -> report phase2b/phase3")
        m1 = run_phase(cfg, "phase1", outdir, args.workers, resume=True)
        if m1 > 0:
            log(outdir, f"phase1 found {m1} match(es). STOPPING per instructions -- "
                        "do not continue to phase2a when a match exists.")
            return 0
        log(outdir, "phase1 complete with 0 matches. Proceeding to phase2a automatically.")
        m2 = run_phase(cfg, "phase2a", outdir, args.workers, resume=True)
        if m2 > 0:
            log(outdir, f"phase2a found {m2} match(es). STOPPING.")
            return 0
        log(outdir, "phase2a complete with 0 matches.")
        log(outdir, cfg["phase2b_status"])
        log(outdir, "phase3 (one-in/one-out) is a separate script: "
                     "analysis/bruteforce_phase3_oneinoneout.py -- run its --cost-report first.")
        return 0

    if args.run or args.resume:
        run_phase(cfg, phase_name, outdir, args.workers, resume=args.resume or False)
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
