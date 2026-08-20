#!/usr/bin/env python3
"""
bruteforce_phase3_oneinoneout.py -- the "second solver" for Attack 3: one-in/one-out
modifications of H1. Only meaningful if bruteforce_solver.py's phase1 AND phase2a
both finish with 0 matches.

What it does:
  For each of the 10 current H1 intruders (the "in" panel, re-admitted as a keeper)
  paired with each of the 24 current keepers (the "out" panel, removed and made the
  new intruder), builds the resulting 24-keeper word-list set and computes its
  combinatorial size -- WITHOUT running anything. `--cost-report` prints/saves this
  for all 240 pairs, ranked smallest first, so a pair is only ever run after its
  cost is known, never blindly.

What it deliberately does NOT do:
  - It does not run all 240 pairs. Many of them still contain the Raiders
    "__WORDLIST__" sweep (2048) AND would add a second multi-candidate panel on
    top, so several pairs are large; this script reports the exact size of each
    pair instead of guessing which are cheap.
  - It does not invent a word for panel 33 (The Shining): under the same
    whole-word/singular/substring hierarchy validated on the 24 keepers, "shine"
    is NOT a literal substring of "shining" (confirmed: needs silent-e
    restoration, an unvalidated transformation). Any pair with panel 33 as the
    "in" panel is marked INVALID (0 candidates for that panel) and is excluded
    from the runnable list, not silently given a guessed word.
  - It does not touch data/films.csv, tools/oracle.py, or bruteforce_config.json.

Usage:
  python analysis/bruteforce_phase3_oneinoneout.py --cost-report
  python analysis/bruteforce_phase3_oneinoneout.py --run-pair --in 16 --out 32 --workers 8
  python analysis/bruteforce_phase3_oneinoneout.py --resume-pair --in 16 --out 32 --workers 8
  python analysis/bruteforce_phase3_oneinoneout.py --status-pair --in 16 --out 32
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import bruteforce_solver as core

HERE = Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = HERE / "bruteforce_config.json"


def build_pair_word_lists(cfg: dict, in_panel: int, out_panel: int, wordlist_2048: list[str]):
    """Returns (keeper_order, word_lists, valid) for swapping `in_panel` in and
    `out_panel` out of the phase1 24-keeper set. valid=False if the incoming
    panel has no backed candidate (e.g. panel 33, The Shining)."""
    if out_panel not in cfg["keeper_order"]:
        raise ValueError(f"panel {out_panel} is not a current keeper, cannot remove it")
    if in_panel not in cfg["h1_intruders_current"]:
        raise ValueError(f"panel {in_panel} is not a current H1 intruder, cannot admit it")

    in_words = cfg["phase3_intruder_candidate_words"].get(str(in_panel), [])
    if not in_words:
        return None, None, False

    new_order = sorted([p for p in cfg["keeper_order"] if p != out_panel] + [in_panel])
    word_lists = []
    for panel in new_order:
        if panel == in_panel:
            word_lists.append(in_words)
        else:
            entry = cfg["phase1_words"][str(panel)]
            word_lists.append(wordlist_2048 if entry == "__WORDLIST__" else entry)
    return new_order, word_lists, True


def cost_report(cfg: dict, outpath: Path) -> None:
    wordlist_2048 = core.load_bip39_wordlist(cfg["bip39_wordlist_path"])
    rows = []
    for in_panel in cfg["h1_intruders_current"]:
        for out_panel in cfg["keeper_order"]:
            order, word_lists, valid = build_pair_word_lists(cfg, in_panel, out_panel, wordlist_2048)
            if not valid:
                rows.append({
                    "in": in_panel, "in_title": cfg["h1_intruder_titles"][str(in_panel)],
                    "out": out_panel, "out_title": cfg["panel_titles"][str(out_panel)],
                    "total_candidates": None,
                    "status": "INVALID: incoming panel has no backed candidate word (not guessed)",
                })
                continue
            total = core.total_count(word_lists)
            rows.append({
                "in": in_panel, "in_title": cfg["h1_intruder_titles"][str(in_panel)],
                "out": out_panel, "out_title": cfg["panel_titles"][str(out_panel)],
                "total_candidates": total,
                "status": "runnable",
            })

    runnable = [r for r in rows if r["status"] == "runnable"]
    runnable.sort(key=lambda r: r["total_candidates"])
    invalid = [r for r in rows if r["status"] != "runnable"]

    print(f"{len(rows)} total (in,out) pairs. {len(runnable)} runnable, {len(invalid)} invalid "
          f"(incoming panel has no backed word).")
    print(f"\nGrand total candidates if ALL runnable pairs were swept: "
          f"{sum(r['total_candidates'] for r in runnable):,}")
    print("\n10 cheapest runnable pairs:")
    for r in runnable[:10]:
        print(f"  in={r['in']:>2} ({r['in_title']:<25s}) out={r['out']:>2} ({r['out_title']:<35s}) "
              f"-> {r['total_candidates']:,} candidates")
    print("\n10 most expensive runnable pairs:")
    for r in runnable[-10:]:
        print(f"  in={r['in']:>2} ({r['in_title']:<25s}) out={r['out']:>2} ({r['out_title']:<35s}) "
              f"-> {r['total_candidates']:,} candidates")
    if invalid:
        print(f"\n{len(invalid)} invalid pairs (excluded, not guessed):")
        for r in invalid:
            print(f"  in={r['in']:>2} ({r['in_title']}) -> {r['status']}")

    with open(outpath, "w", encoding="utf-8") as f:
        json.dump({"runnable": runnable, "invalid": invalid}, f, indent=2)
    print(f"\nFull report written to {outpath}")
    print("\nNothing was run. Pick a pair from this report and run it explicitly with --run-pair.")


def run_pair(cfg: dict, in_panel: int, out_panel: int, outdir: Path, workers: int, resume: bool) -> None:
    wordlist_2048 = core.load_bip39_wordlist(cfg["bip39_wordlist_path"])
    order, word_lists, valid = build_pair_word_lists(cfg, in_panel, out_panel, wordlist_2048)
    if not valid:
        print(f"Cannot run: panel {in_panel} has no backed candidate word. Not inventing one.")
        return
    total = core.total_count(word_lists)
    phase_tag = f"phase3_in{in_panel}_out{out_panel}"
    print(f"Running pair in={in_panel} out={out_panel}: {total:,} candidates, phase tag '{phase_tag}'")

    # Reuse bruteforce_solver's block/progress/results machinery directly, with a
    # synthetic per-pair config so bruteforce_solver.run_phase()'s expected-total
    # check still applies (no silent size drift).
    synthetic_cfg = dict(cfg)
    synthetic_cfg["keeper_order"] = order
    synthetic_cfg[f"{phase_tag}_words"] = {str(p): w for p, w in zip(order, word_lists)}
    synthetic_cfg[f"{phase_tag}_expected_total"] = total

    # run_phase() expects resolve_word_lists() to look up f"{phase}_words"; patch
    # the module-level function usage by calling the same block loop directly.
    orig_resolve = core.resolve_word_lists

    def _resolve(cfg_, phase, wl):
        if phase == phase_tag:
            return order, word_lists
        return orig_resolve(cfg_, phase, wl)

    core.resolve_word_lists = _resolve
    try:
        core.run_phase(synthetic_cfg, phase_tag, outdir, workers, resume=resume)
    finally:
        core.resolve_word_lists = orig_resolve


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    ap.add_argument("--outdir", default=str(core.DEFAULT_OUTDIR))
    ap.add_argument("--cost-report", action="store_true")
    ap.add_argument("--run-pair", action="store_true")
    ap.add_argument("--resume-pair", action="store_true")
    ap.add_argument("--status-pair", action="store_true")
    ap.add_argument("--in", dest="in_panel", type=int)
    ap.add_argument("--out", dest="out_panel", type=int)
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    cfg = core.load_config(Path(args.config))
    outdir = Path(args.outdir)

    if args.cost_report:
        cost_report(cfg, outdir / "bruteforce_phase3_cost_report.json")
        return 0

    if args.status_pair:
        core.print_status(outdir, f"phase3_in{args.in_panel}_out{args.out_panel}")
        return 0

    if args.run_pair or args.resume_pair:
        if args.in_panel is None or args.out_panel is None:
            ap.error("--run-pair/--resume-pair require --in and --out")
        run_pair(cfg, args.in_panel, args.out_panel, outdir, args.workers, resume=args.resume_pair)
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
