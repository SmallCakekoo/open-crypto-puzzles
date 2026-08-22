# Tested (full negatives ledger)

No certified oracle exists for this puzzle: the target is a raw 256-bit private key with no
intermediate checksum, so every candidate below was checked by deriving its ETH address
(`eth_keys`, compressed public key) and comparing it byte-exact (case-insensitive on the hex)
against `0xFF2142E98E09b5344994F9bEB9C56C95506B9F17`. The derivation code itself (SHA-256,
Keccak-256, and secp256k1 point multiplication) is standard and was checked against public
test vectors, but I have no known-answer candidate specific to this puzzle to certify the
mapping from image to key, so every row below is "uncertified" in the sense that a clean run
proves the tested candidates are wrong, not that the harness would have caught every possible
right answer. I also flag near-misses (an ETH address starting with the same 2 bytes, `ff21`)
as an extra check; none occurred in any family below.

## Geometry-derived candidates

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Building height/width/roof-y/x0 sequences (raw, sorted ascending, sorted descending, interleaved), joined with 5 separator styles, padded left/right to 32 bytes, first/last 32 bytes, 2-hex-digit encoding per value | about 460 candidates total across this and the next 3 rows | SHA-256, double SHA-256, Keccak-256, compared to target address | 0 match, 0 near-miss (no derived address even starts with `ff21`) | uncertified (no known-answer vector for this puzzle) | 2026-06-13 |
| Raw pixel hashes: grayscale channel, alpha channel, full PNG file, first/last 32 bytes of the flat grayscale array | included above | SHA-256, Keccak-256 | 0 match, 0 near-miss | uncertified | 2026-06-13 |
| cHRM chunk (32 bytes) and its byte-reversed form, raw and hashed | included above | direct, SHA-256, Keccak-256 | 0 match, 0 near-miss | uncertified | 2026-06-13 |
| Object counts (12 buildings, 1 large sail, 5 small sails, 2 clusters, left/right counts) as a byte sequence | included above | SHA-256 | 0 match, 0 near-miss | uncertified | 2026-06-13 |
| Matrix reshape of the grayscale channel at 7 column widths, first/last row and column strips | 56 strips | first 32 bytes, SHA-256 | 0 match, 0 near-miss | uncertified | 2026-06-13 |
| Value-band pixel masks (bands including 240 to 245, 235 to 254, 248 to 254, 1 to 30) | 4 bands | SHA-256, first 32 bytes | 0 match, 0 near-miss | uncertified | 2026-06-13 |

## Metadata-derived candidates (the date:create / date:modify anomaly)

The PNG's own `tEXt` chunks (confirmed present in `clues/arweave-puzzle-11.png`, reproduced
2026-08-16) read `date:create 2020-03-30T11:38:07+03:00` and
`date:modify 2020-03-30T11:34:44+03:00`: the modify timestamp precedes the create timestamp,
an anomaly present only in this puzzle and its sibling puzzle #9.

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| ISO date strings, digit strings, Unix epochs, and their difference/sum/XOR, in decimal and big/little-endian 4 and 8-byte encodings, alone and concatenated or XORed with the address and the cHRM bytes | dozens of encodings times {SHA-256, double SHA-256, Keccak-256, BLAKE2s, first 32 bytes, last 32 bytes} | direct address comparison | 0 match, 0 near-miss | uncertified | 2026-06-13 |

## Alpha channel and sibling-puzzle-calibrated candidates

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| 260 near-white pixels from the sibling puzzle #9's own 8-level image, tested as a carrier under many bit orders (raster, polar, radial), bit widths (1 to 3 bits per pixel, MSB and LSB first), and symbol mappings, plus several passphrase guesses hashed with SHA-256, double SHA-256, and Keccak-256 | several hundred combinations | address comparison, calibrated against puzzle #9's real (and already spent) address as a positive control | 0 match, 0 near-miss on #9 itself (so the method is confirmed not to reproduce the known #9 answer either) | yes, on the #9 positive control only | 2026-06-13 |
| Container-level myths (embedded executable or filesystem inside the PNG) | full file | binwalk, manual chunk inspection | refuted: file is a clean, valid PNG (IHDR, gAMA, cHRM, bKGD, pHYs, 22 IDAT, 3 tEXt, IEND chunks), 0 bytes after IEND; the "executable" reports from other solvers are binwalk false positives on near-random decompressed pixel bytes | yes (direct chunk inspection) | 2026-06-13 |
| Alpha channel as a data carrier | full channel | direct pixel inspection | 434 pixels have alpha under 255, all clustered on the large sailboat's outline (an anti-aliasing halo from a copy-paste), values 1 to 30, consistent with a smoothed edge rather than structured data | yes | 2026-06-13 |

## Systematic bit-plane / LSB scan (closes open lead #1)

Ran `tools/lsb_scan.py` on 2026-08-21: for the grayscale and alpha channels, both full-image and
restricted to the large sailboat's bounding box (`data/geometry.json`), swept all 8 bit planes
across 4 raster scan orders (row-major top-left, row-major reversed, column-major top-left,
column-major reversed) and 2 bit-packing orders (MSB-first, LSB-first), taking both the first and
last 256 bits of each resulting bitstream as a 32-byte candidate key. Also swept 2/3/4-bits-per-
pixel packings (row-major, MSB-aligned) on the same 4 channel/region combinations.

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Single bit-plane (0-7) extraction, grayscale and alpha, full image and sailboat bbox, 4 scan orders x 2 packing orders x {first 256 bits, last 256 bits} | 8 bit-planes x 2 channels x 2 regions x 4 orders x 2 packings x 2 positions = 512 candidate slots (dedup where region/order overlap, see script) | direct address comparison (`eth_keys`) | 0 match, 0 near-miss (checked against a stricter 3-byte `ff2142` address prefix) | uncertified | 2026-08-21 |
| 2/3/4-bits-per-pixel packing, grayscale and alpha, full image and sailboat bbox, row-major MSB-aligned | 3 bit-widths x 2 channels x 2 regions | direct address comparison | 0 match, 0 near-miss | uncertified | 2026-08-21 |

Total for this run: 110 candidates (the script dedupes trivially-identical slots, e.g. bit-plane 0
in row-major order over a region smaller than 256 pixels is skipped). This closes lead #1 as
stated (an exhaustive bit-order/bit-width sweep with no match): the single-bit and small-multi-bit
"whole channel, whole stream" readings are now ruled out. It does **not** rule out sparser
encodings (e.g. one bit only from specific marked pixels, a bit-plane read only within one
building's silhouette, or a scheme requiring a passphrase/salt not present in the image alone).

## Sparse/localized pixel-marker scan (closes open lead #2, partially)

Ran `tools/anomaly_scan.py` on 2026-08-21: for the grayscale and alpha channels, computed each
pixel's residual against the median of its 8 immediate neighbors (median filter over a 3x3
footprint with the center excluded), on the theory that a deliberately implanted "marker" pixel
would stand out as an isolated speckle against a hand-drawn, locally smooth pencil sketch. Swept
every integer residual threshold from 5 to 255 and looked for thresholds whose outlier count
landed near a bit-budget number (256 markers for 1 bit each, or 128/86/64 for 2/3/4 bits each).

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Median-of-8-neighbors residual outliers, grayscale and alpha, thresholds with outlier counts near 64/86/128/256, 4 orderings (raster, raster-reversed, residual-magnitude descending/ascending), 4 bit-extraction encodings (sign of residual, parity of value, packed nibbles, raw byte value, first and last slices) | 4 threshold/channel combinations x 4 orderings x up to 6 encodings = 84 candidates | direct address comparison | 0 match, 0 near-miss | uncertified | 2026-08-21 |

No threshold produced an outlier count exactly equal to a bit-budget target: the closest was 262
outliers at residual >=252 in the grayscale channel (target 256, off by 6) and 85 outliers at
residual >=5 in the alpha channel (target 86 for 3 bits/marker, off by 1, and this is the same
434-pixel sailboat-outline halo already characterized as anti-aliasing, not structured data). The
grayscale channel has far more high-contrast, locally-isolated pixels than a clean vector drawing
would (255,867 pixels differ from their neighbor median by >=40, about 14% of the image), which
is consistent with a scanned/dithered pencil-sketch texture rather than a marker scheme, and makes
"stands out from its neighbors" a weak discriminator here. This closes the specific
median-residual-outlier method as a lead; it does **not** rule out sparse marker schemes that pick
pixels by a rule other than local statistical contrast (e.g. a fixed pseudo-random coordinate
list, or specific named features such as window centers or mast tips that would need to be
identified by eye rather than by a generic anomaly filter).

## Direct visual inspection and ink-density feature (2026-08-21)

Zoomed into each of the 12 buildings, the large sailboat, and the 5-sail jetty at 2-3x
magnification looking for embedded text, digits, or a QR-like pattern hidden in the hatching.
None found: the strokes are irregular hand-drawn hatching with no legible structure, consistent
with a real pencil sketch rather than an encoding hidden in the linework itself. A visual
impression that some buildings look "solid black" and others look like an "open outline" turned
out, on measurement, to be a continuous gradient (dark-pixel fraction per building bounding box
ranged smoothly from 0.235 to 0.488 with no bimodal gap), not a discrete per-building bit; tested
anyway as a new geometry feature not in the original ~460-candidate sweep.

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Per-building ink/dark-pixel fraction (12 buildings, and 12+sailboat), raw sequence and sorted asc/desc, padded to 32 bytes and hashed | 4 sequences x {2 direct paddings, 3 hash functions} | SHA-256, double SHA-256, Keccak-256, address comparison | 0 match, 0 near-miss | uncertified | 2026-08-21 |

## What all families together rule out

Across the geometry sweep, the metadata sweep, the bit-plane/LSB scan, the median-residual
marker scan, and the ink-density/visual-inspection pass, on the order of 1,214 candidates were
checked, all through the same address-comparison harness, with 0 matches and 0 near-misses
anywhere. This rules out every direct,
single-transform reading of the measured geometry, the metadata anomaly, the whole-channel
bit-plane content, and generic statistical-outlier marker pixels that I was able to enumerate. It
does not rule out a reading that depends on information outside this image, such as the promised
but never-delivered "$100" hint (see "Open leads, ranked"), or a marker scheme selected by a rule
a generic filter cannot discover (a fixed coordinate list, or specific hand-identified features
like window or mast positions).
