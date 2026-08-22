"""
Systematic LSB / bit-plane scan of clues/arweave-puzzle-11.png against the
escrow address, closing open lead #1 in analysis/leads.md.

For each of the grayscale and alpha channels, for each bit position (0=LSB..
7=MSB), for each pixel scan order (row-major top-left, row-major reversed,
column-major top-left, column-major reversed), and for each bit-packing order
(MSB-first, LSB-first) when assembling 8 extracted bits into a byte, this
extracts the first 256 bits and the last 256 bits of the resulting bitstream,
treats each as a 32-byte candidate private key, derives its Ethereum address,
and compares it to the target. It also repeats the whole sweep restricted to
the large-sailboat bounding box (the region the author's own hint points at)
using the coordinates in data/geometry.json, and to multi-bit-per-pixel
packings (2, 3, and 4 bits/pixel) on the full image.

Run: python tools/lsb_scan.py
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from eth_keys import keys

ROOT = Path(__file__).resolve().parents[1]
IMG_PATH = ROOT / "clues" / "arweave-puzzle-11.png"
GEOM_PATH = ROOT / "data" / "geometry.json"
TARGET = "0xff2142e98e09b5344994f9beb9c56c95506b9f17"


def eth_address(privkey_bytes: bytes) -> str:
    return keys.PrivateKey(privkey_bytes).public_key.to_checksum_address().lower()


def orderings(arr: np.ndarray):
    """Yield (name, flat_pixel_array) for the 4 raster scan orders."""
    h, w = arr.shape
    yield "row_tl", arr.reshape(-1)
    yield "row_br", arr[::-1, ::-1].reshape(-1)
    yield "col_tl", arr.T.reshape(-1)
    yield "col_br", arr.T[::-1, ::-1].reshape(-1)


def bits_to_bytes(bits: np.ndarray, msb_first: bool) -> bytes:
    """Pack a length-256 0/1 array into 32 bytes."""
    bits = bits.reshape(32, 8)
    if not msb_first:
        bits = bits[:, ::-1]
    weights = (1 << np.arange(7, -1, -1)).astype(np.uint16)
    byte_vals = (bits * weights).sum(axis=1).astype(np.uint8)
    return byte_vals.tobytes()


def scan_region(name: str, arr: np.ndarray, results: list, near_misses: list):
    for chan_name, chan in [("gray", arr)]:
        for bitplane in range(8):
            plane = (chan >> bitplane) & 1
            for order_name, flat in orderings(plane):
                if flat.size < 256:
                    continue
                for pack_name, msb_first in [("msb", True), ("lsb", False)]:
                    for pos_name, bits in [
                        ("first256", flat[:256]),
                        ("last256", flat[-256:]),
                    ]:
                        cand = bits_to_bytes(bits, msb_first)
                        try:
                            addr = eth_address(cand)
                        except Exception:
                            continue
                        results.append(1)
                        if addr == TARGET:
                            print(f"MATCH! region={name} chan={chan_name} "
                                  f"bit={bitplane} order={order_name} "
                                  f"pack={pack_name} pos={pos_name} "
                                  f"key={cand.hex()}")
                            sys.exit(0)
                        if addr[:6] == TARGET[:6]:
                            near_misses.append(
                                (name, chan_name, bitplane, order_name,
                                 pack_name, pos_name, addr, cand.hex())
                            )


def multibit_scan(name: str, arr: np.ndarray, results: list, near_misses: list):
    """2, 3, 4 bits-per-pixel packings, MSB-aligned, full range 0..255 value
    truncated to the low N bits, row-major TL order only (the dominant
    natural reading order), first 256 bits worth of pixels."""
    for chan_name, chan in [("gray", arr)]:
        flat = chan.reshape(-1)
        for n_bits in (2, 3, 4):
            n_pixels_needed = -(-256 // n_bits)  # ceil
            if flat.size < n_pixels_needed:
                continue
            vals = (flat[:n_pixels_needed] & ((1 << n_bits) - 1)).astype(np.uint32)
            bitstream = []
            for v in vals:
                for b in range(n_bits - 1, -1, -1):
                    bitstream.append((v >> b) & 1)
            bits = np.array(bitstream[:256], dtype=np.uint8)
            cand = bits_to_bytes(bits, True)
            try:
                addr = eth_address(cand)
            except Exception:
                continue
            results.append(1)
            if addr == TARGET:
                print(f"MATCH! region={name} chan={chan_name} multibit={n_bits} "
                      f"key={cand.hex()}")
                sys.exit(0)
            if addr[:6] == TARGET[:6]:
                near_misses.append(
                    (name, chan_name, f"{n_bits}bpp", "row_tl", "msb",
                     "first256", addr, cand.hex())
                )


def main():
    img = Image.open(IMG_PATH)
    print("mode:", img.mode, "size:", img.size)
    rgba = np.array(img.convert("RGBA"))
    gray = rgba[:, :, 0]  # source is grayscale-with-alpha; R=G=B
    alpha = rgba[:, :, 3]

    geom = json.loads(GEOM_PATH.read_text())
    sb = geom["large_sailboat"]

    results = []
    near_misses = []

    # Full image, both channels
    scan_region("full_gray", gray, results, near_misses)
    scan_region("full_alpha", alpha, results, near_misses)
    multibit_scan("full_gray", gray, results, near_misses)
    multibit_scan("full_alpha", alpha, results, near_misses)

    # Sailboat bounding box only, both channels
    sb_gray = gray[sb["y0"]:sb["y1"], sb["x0"]:sb["x1"]]
    sb_alpha = alpha[sb["y0"]:sb["y1"], sb["x0"]:sb["x1"]]
    scan_region("sailboat_gray", sb_gray, results, near_misses)
    scan_region("sailboat_alpha", sb_alpha, results, near_misses)
    multibit_scan("sailboat_gray", sb_gray, results, near_misses)
    multibit_scan("sailboat_alpha", sb_alpha, results, near_misses)

    print(f"Total candidates tested: {len(results)}")
    print(f"Near-misses (ff2142 prefix on first 3 bytes): {len(near_misses)}")
    for nm in near_misses:
        print(" ", nm)


if __name__ == "__main__":
    main()
