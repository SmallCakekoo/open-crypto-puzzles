#!/usr/bin/env python3
"""
fetch_source.py -- fetch the Real Big Block source chapter into a local cache.

This repository deliberately does not redistribute the chapter text (bulk
third-party material). This script pulls it from Wattpad's own public API at
run time and writes tools/source_cache.json, which sweep.py consumes. The
cache file is gitignored; do not commit it.

Validation: the fetch is checked against the byte-level forensic audit already
recorded in the README -- exactly 273 paragraphs and exactly 6 U+00A0
non-breaking spaces, with no other non-ASCII content anywhere. If either check
fails, the chapter has changed since 2026-08-22 (or the parse is wrong) and the
script refuses to write the cache rather than let a sweep run on bad bytes.

Usage:
    python3 tools/fetch_source.py
    python3 tools/fetch_source.py --show 5      # print the first 5 paragraphs
"""

from __future__ import annotations

import argparse
import gzip
import html as html_mod
import json
import os
import re
import sys
import urllib.request

PART_ID = 720888559  # "Second", part 2 of story 184148284; the confirmed source
API = f"https://www.wattpad.com/apiv2/storytext?id={PART_ID}"

EXPECTED_PARAGRAPHS = 273
EXPECTED_NBSP = 6

_HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(_HERE, "source_cache.json")


def fetch_html() -> str:
    req = urllib.request.Request(
        API, headers={"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip"}
    )
    raw = urllib.request.urlopen(req, timeout=60).read()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return raw.decode("utf-8")


def parse_paragraphs(html: str) -> list[str]:
    """One string per <p> tag. <br> becomes an internal newline (the chapter
    has 10 of them, from two draft paragraphs the author merged); all other
    tags are dropped and HTML entities decoded."""
    out = []
    for m in re.finditer(r"<p\b[^>]*>(.*?)</p>", html, re.S):
        body = m.group(1)
        body = re.sub(r"<br\s*/?>", "\n", body, flags=re.I)
        body = re.sub(r"<[^>]+>", "", body)
        out.append(html_mod.unescape(body))
    return out


def validate(paragraphs: list[str]) -> list[str]:
    problems = []
    if len(paragraphs) != EXPECTED_PARAGRAPHS:
        problems.append(
            f"expected {EXPECTED_PARAGRAPHS} paragraphs, got {len(paragraphs)}"
        )
    joined = "\n".join(paragraphs)
    nbsp = joined.count("\u00a0")
    if nbsp != EXPECTED_NBSP:
        problems.append(f"expected {EXPECTED_NBSP} NBSP (U+00A0), got {nbsp}")
    other = sorted({c for c in joined if ord(c) > 127 and c != "\u00a0"})
    if other:
        problems.append(
            "unexpected non-ASCII characters: "
            + ", ".join(f"U+{ord(c):04X}" for c in other[:20])
        )
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--show", type=int, default=0, help="print the first N paragraphs")
    ap.add_argument("--force", action="store_true", help="write cache despite validation failure")
    args = ap.parse_args()

    print(f"fetching part {PART_ID} ...")
    paragraphs = parse_paragraphs(fetch_html())
    print(f"parsed {len(paragraphs)} paragraphs")

    problems = validate(paragraphs)
    if problems:
        print("\nVALIDATION FAILED:")
        for p in problems:
            print("  - " + p)
        if not args.force:
            print("\nRefusing to write the cache. The chapter may have changed since")
            print("2026-08-22, or the parse is wrong. Re-run with --force to override,")
            print("but record the discrepancy in analysis/tested.md if you do.")
            return 1
        print("\n--force given, writing anyway.")
    else:
        print(f"validation OK: {EXPECTED_PARAGRAPHS} paragraphs, {EXPECTED_NBSP} NBSP, no other non-ASCII")

    with open(CACHE, "w", encoding="utf-8") as fh:
        json.dump({"part_id": PART_ID, "paragraphs": paragraphs}, fh, ensure_ascii=False)
    print(f"wrote {CACHE}")

    if args.show:
        print()
        for i, p in enumerate(paragraphs[: args.show]):
            print(f"[{i:3d}] {p[:110]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
