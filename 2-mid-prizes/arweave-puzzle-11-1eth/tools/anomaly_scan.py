"""
Sparse/localized pixel-marker scan, closing open lead #2 in analysis/leads.md.

Idea: instead of reading a whole channel as one continuous bitstream (lead #1,
closed negative), look for a small set of individually placed "marker"
pixels that stand out from their local neighborhood -- the kind of isolated
speckle a hand-drawn pencil sketch would not naturally contain, since real
strokes are locally smooth/anti-aliased.

For each pixel, compute the median of its 8 neighbors (3x3 footprint minus
the center) and the residual = pixel - median8. A genuine edge/line has
several neighbors sharing its value along the stroke direction, so a true
"marker" pixel -- one whose value was deliberately changed independent of
the drawing -- should show up as a larger, more isolated residual than
ordinary line/edge pixels.

For a sweep of residual thresholds, count how many pixels qualify as
outliers. Thresholds whose outlier count lands near a bit-budget number
(256 for 1 bit/marker, 128/86/64 for 2/3/4 bits/marker, or other round
fractions) are interesting: for each such threshold, the outlier set is
extracted, ordered several ways (raster position, |residual| descending),
and turned into a 32-byte candidate several ways (sign of residual, parity
of value, low bits of value), then checked against the escrow address.

Run: python tools/anomaly_scan.py
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage
from eth_keys import keys

ROOT = Path(__file__).resolve().parents[1]
IMG_PATH = ROOT / "clues" / "arweave-puzzle-11.png"
TARGET = "0xff2142e98e09b5344994f9beb9c56c95506b9f17"

BORDER = 4  # exclude pixels this close to the image edge (filter artifacts)

# 3x3 footprint minus the center pixel: the "8 neighbors" mask.
NEIGHBOR_FOOTPRINT = np.array([
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1],
], dtype=bool)


def eth_address(privkey_bytes: bytes) -> str:
    return keys.PrivateKey(privkey_bytes).public_key.to_checksum_address().lower()


def median8_residual(chan: np.ndarray) -> np.ndarray:
    chan_i = chan.astype(np.int16)
    med8 = ndimage.median_filter(chan_i, footprint=NEIGHBOR_FOOTPRINT, mode="nearest")
    return chan_i - med8


def bits_to_bytes(bits, msb_first=True) -> bytes:
    bits = np.asarray(bits, dtype=np.uint8).reshape(32, 8)
    if not msb_first:
        bits = bits[:, ::-1]
    weights = (1 << np.arange(7, -1, -1)).astype(np.uint16)
    return (bits * weights).sum(axis=1).astype(np.uint8).tobytes()


def try_candidate(cand: bytes, near_misses, label):
    try:
        addr = eth_address(cand)
    except Exception:
        return False
    if addr == TARGET:
        print(f"MATCH! {label} key={cand.hex()}")
        sys.exit(0)
    if addr[:6] == TARGET[:6]:
        near_misses.append((label, addr, cand.hex()))
    return False


def order_variants(ys, xs, residuals, values):
    """Yield (name, index_order) for several natural orderings of outliers."""
    n = len(ys)
    idx = np.arange(n)
    yield "raster", idx[np.lexsort((xs, ys))]
    yield "raster_rev", idx[np.lexsort((xs, ys))][::-1]
    yield "abs_residual_desc", idx[np.argsort(-np.abs(residuals))]
    yield "abs_residual_asc", idx[np.argsort(np.abs(residuals))]


def scan_channel(name: str, chan: np.ndarray, results: list, near_misses: list, hits: list):
    h, w = chan.shape
    resid = median8_residual(chan)
    resid_b = resid[BORDER:h - BORDER, BORDER:w - BORDER]
    chan_b = chan[BORDER:h - BORDER, BORDER:w - BORDER]

    thresholds = list(range(5, 256, 1))
    counts = {}
    for t in thresholds:
        mask = np.abs(resid_b) >= t
        counts[t] = int(mask.sum())

    # Bit-budget targets we care about: enough markers for a 256-bit key at
    # 1..4 bits per marker (ceil), plus a little slack for dedup/padding.
    targets = {256, 128, 86, 64}
    candidate_thresholds = []
    for t, c in counts.items():
        if c == 0:
            continue
        if any(abs(c - target) <= 2 for target in targets) or (256 <= c <= 400):
            candidate_thresholds.append((t, c))

    print(f"[{name}] outlier counts at a few sample thresholds: "
          + ", ".join(f"t={t}:{counts[t]}" for t in (5, 10, 15, 20, 30, 40, 60, 80, 100)))
    if candidate_thresholds:
        print(f"[{name}] thresholds near a bit-budget count: {candidate_thresholds}")

    for t, c in candidate_thresholds:
        mask = np.abs(resid_b) >= t
        ys, xs = np.nonzero(mask)
        residuals = resid_b[ys, xs]
        values = chan_b[ys, xs]
        hits.append((name, t, c))

        for order_name, order in order_variants(ys, xs, residuals, values):
            ordered_vals = values[order]
            ordered_resid = residuals[order]
            n = len(ordered_vals)

            # Encoding A: sign of residual -> 1 bit per marker (need >=256 markers)
            if n >= 256:
                bits = (ordered_resid[:256] > 0).astype(np.uint8)
                cand = bits_to_bytes(bits, True)
                results.append(1)
                try_candidate(cand, near_misses, f"{name}/t{t}/{order_name}/sign_first256")
                bits2 = (ordered_resid[-256:] > 0).astype(np.uint8)
                cand2 = bits_to_bytes(bits2, True)
                results.append(1)
                try_candidate(cand2, near_misses, f"{name}/t{t}/{order_name}/sign_last256")

            # Encoding B: parity (LSB) of the marked pixel's value -> 1 bit per marker
            if n >= 256:
                bits = (ordered_vals[:256] & 1).astype(np.uint8)
                cand = bits_to_bytes(bits, True)
                results.append(1)
                try_candidate(cand, near_misses, f"{name}/t{t}/{order_name}/parity_first256")

            # Encoding C: low nibble packed 2 markers/byte -> need >=64 markers
            if n >= 64:
                nib = (ordered_vals[:64] & 0x0F).astype(np.uint8)
                byte_vals = ((nib[0::2] << 4) | nib[1::2]).astype(np.uint8)
                cand = byte_vals.tobytes()
                results.append(1)
                try_candidate(cand, near_misses, f"{name}/t{t}/{order_name}/nibble_pack64")

            # Encoding D: raw byte value of first/last 32 markers directly as key bytes
            if n >= 32:
                cand = ordered_vals[:32].astype(np.uint8).tobytes()
                results.append(1)
                try_candidate(cand, near_misses, f"{name}/t{t}/{order_name}/raw_first32")
                cand2 = ordered_vals[-32:].astype(np.uint8).tobytes()
                results.append(1)
                try_candidate(cand2, near_misses, f"{name}/t{t}/{order_name}/raw_last32")


def main():
    img = Image.open(IMG_PATH)
    rgba = np.array(img.convert("RGBA"))
    gray = rgba[:, :, 0]
    alpha = rgba[:, :, 3]

    results, near_misses, hits = [], [], []
    scan_channel("gray", gray, results, near_misses, hits)
    scan_channel("alpha", alpha, results, near_misses, hits)

    print(f"\nTotal candidates tested: {len(results)}")
    print(f"Thresholds with a bit-budget-sized outlier set: {len(hits)}")
    for h in hits:
        print(" ", h)
    print(f"Near-misses: {len(near_misses)}")
    for nm in near_misses:
        print(" ", nm)


if __name__ == "__main__":
    main()
