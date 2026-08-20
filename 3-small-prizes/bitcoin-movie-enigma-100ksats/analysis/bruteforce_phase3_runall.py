#!/usr/bin/env python3
"""
bruteforce_phase3_runall.py -- runs multiple Attack-3 (one-in/one-out) pairs back
to back, unattended, cheapest first by default. Meant to be left running for a
long stretch (the 216 runnable pairs total ~203.5M candidates, ~1h50m at the
~30,000/s this machine showed for phases 1/2a with 8 workers -- actual speed
depends on how many pairs hit the 2048-word Raiders sweep alongside another
multi-candidate panel).

Safety, same as the rest of this attack:
  - Recomputes the runnable pair list itself from bruteforce_config.json (does not
    trust a possibly-stale cost report file).
  - Skips panel 33 (The Shining) as an "in" panel: it has no backed candidate word
    under the validated hierarchy, and none is invented here.
  - Each pair is independently resumable (bruteforce_solver.run_phase's own
    block/checkpoint machinery, called through bruteforce_phase3_oneinoneout.run_pair).
  - If ANY pair produces a match, this script STOPS immediately after that pair
    instead of continuing to the next one, and prints/logs the match prominently.
  - Does not touch data/films.csv, tools/oracle.py, or bruteforce_config.json.

Usage:
  # everything, cheapest first, 8 worker processes per pair
  python analysis/bruteforce_phase3_runall.py --workers 8

  # only the cheap ones (e.g. skip anything over 3,000,000 candidates)
  python analysis/bruteforce_phase3_runall.py --workers 8 --max-total 3000000

  # only the first N pairs in the (cheapest-first) queue
  python analysis/bruteforce_phase3_runall.py --workers 8 --limit 20

  # re-run: already-completed pairs are skipped automatically (checked via each
  # pair's own progress file), so the same command resumes cleanly if interrupted
  python analysis/bruteforce_phase3_runall.py --workers 8
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import bruteforce_solver as core
import bruteforce_phase3_oneinoneout as p3

HERE = Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = HERE / "bruteforce_config.json"


def build_queue(cfg: dict, wordlist_2048: list[str], order: str) -> list[dict]:
    rows = []
    for in_panel in cfg["h1_intruders_current"]:
        for out_panel in cfg["keeper_order"]:
            _, word_lists, valid = p3.build_pair_word_lists(cfg, in_panel, out_panel, wordlist_2048)
            if not valid:
                continue
            rows.append({
                "in": in_panel, "out": out_panel,
                "total": core.total_count(word_lists),
                "tag": f"phase3_in{in_panel}_out{out_panel}",
            })
    rows.sort(key=lambda r: r["total"], reverse=(order == "expensive"))
    return rows


def pair_already_done(outdir: Path, tag: str, expected_total: int) -> tuple[bool, int]:
    """Returns (done, matches_count). done=True only if processed==expected_total."""
    p = core.progress_path(outdir, tag)
    if not p.exists():
        return False, 0
    with open(p, encoding="utf-8") as f:
        prog = json.load(f)
    done = prog.get("processed_count", 0) >= expected_total and prog.get("total_candidates") == expected_total
    return done, prog.get("matches_count", 0)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    ap.add_argument("--outdir", default=str(core.DEFAULT_OUTDIR))
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--order", choices=["cheapest", "expensive"], default="cheapest")
    ap.add_argument("--max-total", type=int, default=None, help="skip pairs with more candidates than this")
    ap.add_argument("--limit", type=int, default=None, help="only run the first N pairs in the queue")
    args = ap.parse_args()

    cfg = core.load_config(Path(args.config))
    outdir = Path(args.outdir)
    wordlist_2048 = core.load_bip39_wordlist(cfg["bip39_wordlist_path"])

    queue = build_queue(cfg, wordlist_2048, args.order)
    if args.max_total is not None:
        queue = [r for r in queue if r["total"] <= args.max_total]
    if args.limit is not None:
        queue = queue[: args.limit]

    grand_total = sum(r["total"] for r in queue)
    core.log(outdir, f"=== phase3 runall === {len(queue)} pairs queued, {grand_total:,} candidates total, "
                      f"order={args.order}, workers={args.workers}")

    run_start = time.time()
    processed_before_this_pair = 0
    for i, row in enumerate(queue, 1):
        tag, total = row["tag"], row["total"]
        done, matches = pair_already_done(outdir, tag, total)
        if done:
            core.log(outdir, f"[{i}/{len(queue)}] {tag} ({total:,} candidates): already complete, "
                              f"matches={matches}. Skipping.")
            if matches > 0:
                core.log(outdir, f"!!! {tag} has a recorded match from a previous run. "
                                  f"See {core.results_path(outdir, tag)}. STOPPING queue.")
                return 0
            processed_before_this_pair += total
            continue

        core.log(outdir, f"[{i}/{len(queue)}] running {tag}: in={row['in']} out={row['out']} "
                          f"({total:,} candidates)")
        p3.run_pair(cfg, row["in"], row["out"], outdir, args.workers, resume=True)

        done, matches = pair_already_done(outdir, tag, total)
        processed_before_this_pair += total
        elapsed = time.time() - run_start
        rate = processed_before_this_pair / elapsed if elapsed > 0 else 0.0
        remaining = grand_total - processed_before_this_pair
        eta = remaining / rate if rate > 0 else float("inf")
        core.log(outdir, f"[{i}/{len(queue)}] {tag} done. matches={matches}. "
                          f"Overall: {processed_before_this_pair:,}/{grand_total:,} "
                          f"({100*processed_before_this_pair/grand_total:.2f}%) | "
                          f"overall_rate={rate:,.0f}/s | ETA_remaining_pairs={core._fmt_eta(eta)}")

        if matches > 0:
            core.log(outdir, f"!!! MATCH FOUND in {tag} !!! See {core.results_path(outdir, tag)}. "
                              f"STOPPING queue -- not running further pairs.")
            return 0

    core.log(outdir, f"=== phase3 runall COMPLETE === {len(queue)} pairs, {grand_total:,} candidates, "
                      f"0 matches across the whole queue. total_elapsed={core._fmt_eta(time.time()-run_start)}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
