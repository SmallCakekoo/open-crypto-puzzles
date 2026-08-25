#!/usr/bin/env python3
"""
sweep.py -- parallel candidate sweeps for Real Big Block, built on fastderive.

Modes (see analysis/leads.md for why each one exists):

  ranges     Every contiguous paragraph range of the chapter, crossed with a
             serialization matrix. Closes the biggest coverage gap in
             analysis/tested.md: only 12 hand-picked sections were ever tried,
             out of 37,401 possible contiguous ranges.

  appbytes   Lead 5. The full app-behaviour matrix (trailing newline, CRLF/LF
             normalisation, BOM, whitespace trim, encoding, NBSP handling)
             applied to the highest-prior base texts. Targets the hypothesis
             that the author's tablet hashing app silently altered the bytes.

  edit2      Lead 2. Two simultaneous character edits, bounded to
             structurally-meaningful positions (line-break characters and
             NBSPs). The exhaustive edit-distance-1 sweep is already negative;
             this is the bounded 2-edit follow-up.

  transpose  Lead 6. Order-changing transforms, which no prior test covered.

Every run is witness-verified: a candidate drawn from the sweep's own
enumeration has its HASH160 added to the target set before the run starts, and
the sweep must report finding it. A run that does not recover its witness is
reported as INVALID and its negative result must not be recorded. This mirrors
the "Witness" column already used in analysis/tested.md.

Usage:
    python3 tools/fetch_source.py                     # once, populates the cache
    python3 tools/fastderive.py --selftest            # once, certifies the transform
    python3 tools/sweep.py --mode ranges  --profile core --workers 24
    python3 tools/sweep.py --mode appbytes --workers 24
    python3 tools/sweep.py --mode edit2   --workers 24
    python3 tools/sweep.py --mode transpose --workers 24
    python3 tools/sweep.py --mode ranges --profile full --workers 24 --resume

Any hit is written to tools/HIT_<mode>.txt immediately and printed. A hit on
the Stage One calibration address means the pipeline works but you have found
the already-solved block; a hit on either Real Big Block address is the prize.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import sys
import time
from multiprocessing import Pool

import fastderive as fd

_HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(_HERE, "source_cache.json")

# Confirmed separators (README established fact 5) first; the two LF-only
# variants are included because a hashing app may have normalised CRLF away.
SEPARATORS = {
    "crlfcrlf": "\r\n\r\n",   # confirmed, current escrow
    "crlf": "\r\n",           # confirmed, superseded escrow
    "lflf": "\n\n",
    "lf": "\n",
}

# The confirmed Stage One case-flip rule. Copied from tools/oracle.py rather
# than imported, so this script does not pull in bip_utils.
NO_FLIP_INITIALS = set("ITASM")


def flip_case(paragraph: str) -> str:
    chars = list(paragraph)
    letters = [i for i, c in enumerate(chars) if c.isalpha()]
    if not letters:
        return paragraph
    chars[letters[0]] = chars[letters[0]].lower()
    chars[letters[-1]] = chars[letters[-1]].upper()
    return "".join(chars)


def transform_paragraphs(paras: list[str], mode: str) -> list[str]:
    if mode == "none":
        return paras
    if mode == "itasm":
        return [p if p and p[0] in NO_FLIP_INITIALS else flip_case(p) for p in paras]
    if mode == "flipall":
        return [flip_case(p) for p in paras]
    if mode == "itasm_only":  # keep only ITASM-initial paragraphs, drop the rest
        return [p for p in paras if p and p[0] in NO_FLIP_INITIALS]
    raise ValueError(mode)


def apply_nbsp(text: str, mode: str) -> str:
    if mode == "keep":
        return text
    if mode == "space":
        return text.replace("\u00a0", " ")
    if mode == "strip":
        return text.replace("\u00a0", "")
    raise ValueError(mode)


def serialize(paras, sep, transform, nbsp, trailing, leading, rstrip_each):
    ps = transform_paragraphs(paras, transform)
    if rstrip_each:
        ps = [p.rstrip() for p in ps]
    text = sep.join(ps)
    text = apply_nbsp(text, nbsp)
    return leading + text + trailing


# --------------------------------------------------------------------------
# Variant matrices
# --------------------------------------------------------------------------

PROFILES = {
    # 6 variants: the two confirmed separators x three transforms, clean bytes.
    "core": dict(
        seps=["crlfcrlf", "crlf"],
        transforms=["none", "itasm", "flipall"],
        nbsps=["keep"],
        trailings=[""],
        leadings=[""],
        rstrips=[False],
        encodings=["utf-8"],
    ),
    # 1,152 variants: adds the full app-behaviour cross product.
    "full": dict(
        seps=["crlfcrlf", "crlf", "lflf", "lf"],
        transforms=["none", "itasm", "flipall"],
        nbsps=["keep", "space", "strip"],
        trailings=["", "\n", "\r\n", "\r\n\r\n"],
        leadings=["", "\ufeff"],
        rstrips=[False, True],
        encodings=["utf-8", "iso-8859-1"],
    ),
}


def variant_specs(profile: str):
    p = PROFILES[profile]
    return list(
        itertools.product(
            p["seps"], p["transforms"], p["nbsps"],
            p["trailings"], p["leadings"], p["rstrips"], p["encodings"],
        )
    )


# --------------------------------------------------------------------------
# Task generation. A task is a small descriptor; a worker expands it into many
# candidate texts. Tasks are deterministic and ordered, so --resume works.
# --------------------------------------------------------------------------

def make_tasks(mode: str, n_paras: int, profile: str):
    if mode == "ranges":
        return [(s, e) for s in range(n_paras) for e in range(s + 1, n_paras + 1)]
    if mode == "appbytes":
        # Whole chapter plus every "top-level" contiguous block: the chapter
        # start to each paragraph, and each paragraph to the end. These are the
        # shapes a person actually selects by hand in a browser.
        tasks = [(0, n_paras)]
        tasks += [(0, e) for e in range(1, n_paras)]
        tasks += [(s, n_paras) for s in range(1, n_paras)]
        return tasks
    if mode == "transpose":
        return list(range(6))
    if mode == "edit2":
        return None  # built separately, needs the joined text
    raise ValueError(mode)


TRANSPOSE_OPS = {
    0: ("reversed_all", lambda ps: ps[::-1]),
    1: ("reversed_within_halves", lambda ps: ps[: len(ps) // 2][::-1] + ps[len(ps) // 2:][::-1]),
    2: ("halves_swapped", lambda ps: ps[len(ps) // 2:] + ps[: len(ps) // 2]),
    3: ("interleave_halves", lambda ps: [x for pair in itertools.zip_longest(ps[: (len(ps) + 1) // 2], ps[(len(ps) + 1) // 2:]) for x in pair if x is not None]),
    4: ("even_then_odd", lambda ps: ps[::2] + ps[1::2]),
    5: ("odd_then_even", lambda ps: ps[1::2] + ps[::2]),
}


# --------------------------------------------------------------------------
# Worker
# --------------------------------------------------------------------------

_PARAS: list[str] = []
_SPECS = []
_MODE = ""
_EXTRA_TARGET = None


def _init(paras, specs, mode, extra_target):
    global _PARAS, _SPECS, _MODE, _EXTRA_TARGET
    _PARAS, _SPECS, _MODE, _EXTRA_TARGET = paras, specs, mode, extra_target
    if extra_target:
        fd.TARGETS[bytes.fromhex(extra_target)] = "PLANTED WITNESS"


def _candidates(task):
    """Yield (label, text, encoding) for one task."""
    if _MODE in ("ranges", "appbytes"):
        s, e = task
        chunk = _PARAS[s:e]
        for sep, tr, nb, tl, ld, rs, enc in _SPECS:
            yield (
                f"{_MODE} p{s}-{e} sep={sep} tr={tr} nbsp={nb} "
                f"trail={tl!r} lead={ld!r} rstrip={rs} enc={enc}",
                serialize(chunk, SEPARATORS[sep], tr, nb, tl, ld, rs),
                enc,
            )
    elif _MODE == "transpose":
        name, op = TRANSPOSE_OPS[task]
        chunk = op(list(_PARAS))
        for sep, tr, nb, tl, ld, rs, enc in _SPECS:
            yield (
                f"transpose {name} sep={sep} tr={tr} nbsp={nb} enc={enc}",
                serialize(chunk, SEPARATORS[sep], tr, nb, tl, ld, rs),
                enc,
            )
    elif _MODE == "edit2":
        base, positions, ops, i0 = task
        for a, b in positions:
            for oa, ob in ops:
                text = _apply_edits(base, [(a, oa), (b, ob)])
                yield (f"edit2 base={i0} pos=({a},{b}) ops=({oa},{ob})", text, "utf-8")


EDIT_OPS = ["del", "ins_sp", "ins_cr", "ins_lf", "sub_sp", "sub_lf", "sub_cr"]


def _apply_edits(text: str, edits) -> str:
    """Apply edits at descending positions so earlier indices stay valid."""
    chars = list(text)
    for pos, op in sorted(edits, key=lambda t: -t[0]):
        if op == "del":
            del chars[pos]
        elif op == "ins_sp":
            chars.insert(pos, " ")
        elif op == "ins_cr":
            chars.insert(pos, "\r")
        elif op == "ins_lf":
            chars.insert(pos, "\n")
        elif op == "sub_sp":
            chars[pos] = " "
        elif op == "sub_lf":
            chars[pos] = "\n"
        elif op == "sub_cr":
            chars[pos] = "\r"
    return "".join(chars)


def _work(task):
    hits = []
    n = 0
    for label, text, enc in _candidates(task):
        n += 1
        try:
            data = text.encode(enc)
        except UnicodeEncodeError:
            continue
        ent = hashlib.md5(data).digest()
        for i, h in enumerate(fd.derive_hash160s(ent, 6)):
            if h in fd.TARGETS:
                hits.append((fd.TARGETS[h], i, fd.b58encode_check(b"\x00" + h), label))
    return n, hits


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def build_edit2_tasks(paras, chunk_pairs=400):
    """Bounded 2-edit tasks: positions restricted to line-break characters and
    NBSPs, under both confirmed separators, on the whole chapter."""
    tasks = []
    for i0, sep_key in enumerate(("crlfcrlf", "crlf")):
        base = SEPARATORS[sep_key].join(paras)
        positions = [i for i, c in enumerate(base) if c in "\r\n\u00a0"]
        pairs = list(itertools.combinations(positions, 2))
        ops = list(itertools.product(EDIT_OPS, EDIT_OPS))
        for k in range(0, len(pairs), chunk_pairs):
            tasks.append((base, pairs[k:k + chunk_pairs], ops, i0))
    return tasks


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", required=True, choices=["ranges", "appbytes", "edit2", "transpose"])
    ap.add_argument("--profile", default="core", choices=list(PROFILES))
    ap.add_argument("--workers", type=int, default=os.cpu_count())
    ap.add_argument("--resume", action="store_true", help="skip tasks already done per the checkpoint")
    ap.add_argument("--no-witness", action="store_true", help="skip witness planting (not recommended)")
    args = ap.parse_args()

    if not os.path.exists(CACHE):
        print("source cache missing. Run: python3 tools/fetch_source.py")
        return 1
    with open(CACHE, encoding="utf-8") as fh:
        paras = json.load(fh)["paragraphs"]
    print(f"loaded {len(paras)} paragraphs")

    specs = variant_specs(args.profile)
    if args.mode == "edit2":
        tasks = build_edit2_tasks(paras)
        per_task = len(tasks[0][1]) * len(tasks[0][2]) if tasks else 0
        specs = []
    else:
        tasks = make_tasks(args.mode, len(paras), args.profile)
        per_task = len(specs)

    total = len(tasks) * per_task
    print(f"mode={args.mode} profile={args.profile} tasks={len(tasks):,} "
          f"variants/task={per_task:,} candidates={total:,}")

    # ---- witness -------------------------------------------------------
    extra = None
    if not args.no_witness:
        _init(paras, specs, args.mode, None)
        probe_task = tasks[len(tasks) // 2]
        probe = None
        for label, text, enc in _candidates(probe_task):
            probe = (label, text, enc)
            break
        if probe is None:
            print("could not build a witness candidate")
            return 1
        ent = hashlib.md5(probe[1].encode(probe[2])).digest()
        extra = fd.derive_hash160s(ent, 1)[0].hex()
        print(f"witness planted from a real sweep candidate: {probe[0][:70]}")

    ckpt = os.path.join(_HERE, f".sweep_{args.mode}_{args.profile}.ckpt")
    done = 0
    if args.resume and os.path.exists(ckpt):
        with open(ckpt) as fh:
            done = int(fh.read().strip() or 0)
        print(f"resuming: skipping the first {done:,} tasks")
        tasks = tasks[done:]

    hitfile = os.path.join(_HERE, f"HIT_{args.mode}.txt")
    t0 = time.perf_counter()
    seen = 0
    witness_found = False
    real_hits = []

    # Tasks are individually tiny (a handful of derivations each), so a
    # chunksize of 1 leaves the pool IPC-bound: measured at barely one core of
    # throughput across 8 workers. Batch enough tasks per dispatch that worker
    # time dominates the round trip, while keeping enough chunks that the
    # checkpoint stays fine-grained and stragglers cannot starve the pool.
    chunksize = max(1, min(64, len(tasks) // (args.workers * 16) or 1))
    print(f"workers={args.workers} chunksize={chunksize}")

    with Pool(args.workers, initializer=_init, initargs=(paras, specs, args.mode, extra)) as pool:
        for k, (n, hits) in enumerate(pool.imap(_work, tasks, chunksize=chunksize), start=1):
            seen += n
            for label_t, idx, addr, cand in hits:
                if label_t == "PLANTED WITNESS":
                    witness_found = True
                    continue
                real_hits.append((label_t, idx, addr, cand))
                line = f"HIT {label_t} address={addr} index={idx}\n  candidate: {cand}\n"
                print("\n" + "=" * 70 + "\n" + line + "=" * 70)
                with open(hitfile, "a", encoding="utf-8") as fh:
                    fh.write(line)
            if k % 500 == 0 or k == len(tasks):
                el = time.perf_counter() - t0
                rate = seen / el if el else 0
                remain = (total - seen) / rate if rate else 0
                pct = 100 * seen / total if total else 0
                print(f"\r{pct:5.1f}%  {seen:,}/{total:,}  {rate:,.0f}/s  "
                      f"ETA {remain/3600:.2f}h  hits={len(real_hits)}", end="", flush=True)
                with open(ckpt, "w") as fh:
                    fh.write(str(done + k))

    el = time.perf_counter() - t0
    print(f"\n\ndone: {seen:,} candidates in {el/3600:.2f}h ({seen/el:,.0f}/s)")

    if not args.no_witness:
        if witness_found:
            print("witness RECOVERED -- this run is valid, the negative result can be recorded")
        else:
            print("witness NOT recovered -- run is INVALID, do not record this negative")
            return 2
    print(f"real hits: {len(real_hits)}")
    return 0 if not real_hits else 0


if __name__ == "__main__":
    sys.exit(main())
