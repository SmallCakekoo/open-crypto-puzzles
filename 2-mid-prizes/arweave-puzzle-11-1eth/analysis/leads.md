# Open leads, ranked

## 1. [CLOSED, negative] A systematic LSB scan of the continuous grayscale and alpha channels

Closed 2026-08-21 with `tools/lsb_scan.py`: swept both channels (grayscale and alpha), full image
and the sailboat bounding box, across all 8 bit planes, 4 raster scan orders, 2 bit-packing
orders, first/last 256 bits, plus 2/3/4-bits-per-pixel packings. 110 candidates, 0 matches, 0
near-misses (checked against a 3-byte address prefix). Full ledger in `analysis/tested.md`. This
rules out every "whole channel, single continuous bitstream" reading. What it does **not** rule
out: a sparse encoding that only uses specific marked pixels (not the whole raster), a scheme
localized to one building or sail rather than the whole channel, or any encoding that needs
information from outside the image (e.g. the never-delivered "$100" hint). A tool built
specifically for this, `zsteg -a` (Ruby, not run here since this environment has no Ruby/gem
toolchain), could still be worth a pass for its extra heuristics (XOR keys, palette-based
extraction) beyond what this Python sweep covers, but the core LSB space is now covered.

## 2. [CLOSED, negative, for the generic-outlier method] A sparse/localized pixel-marker scan

Closed 2026-08-21, in part, with `tools/anomaly_scan.py`: computed each pixel's residual against
the median of its 8 neighbors (a generic "isolated speckle" detector) across all residual
thresholds 5-255 for both channels, looked for thresholds whose outlier count landed near a
bit-budget number (256/128/86/64), and tested every such threshold's outlier set under 4
orderings and up to 6 bit-extraction encodings: 84 candidates, 0 matches, 0 near-misses. No
threshold produced an outlier count exactly on a bit-budget target (closest: 262 at residual
>=252 in gray, 85 at residual >=5 in alpha, the latter being the already-characterized sailboat
anti-aliasing halo). The grayscale channel turned out to be far too textured for a generic
"stands out from its neighbors" filter to work (255,867 of ~1.77M pixels differ from their
neighbor median by >=40), which is consistent with a scanned/dithered sketch rather than a clean
vector drawing. Full ledger in `analysis/tested.md`. **Still open**: any marker scheme selected
by a rule a generic statistical filter cannot discover on its own, e.g. a fixed pseudo-random
coordinate list (would need a seed/passphrase not yet identified), or specific hand-identified
visual features (window positions, mast tips, wave-line crossings) that require eyeballing the
image rather than automated anomaly detection. Confirms: an extracted set of hand- or
rule-identified marker pixels, read in some order, derives the target address. Kills: nothing
further technically; this residual branch is exhausted, the feature-identification branch needs
a person to look at the image and enumerate candidate features.

## 3. Join the community Telegram group and search first-hand for the "$100" hint (needs a
person)

I already searched a full local archive of `@arweavep` (55,002 messages, November 2021 to May
2026) and found no later message announcing new hints, plus 47 messages from other members
independently confirming the promised follow-up never arrived. That closes this as a lead
inside the archived window. What remains untested is anything posted before the archive's
start (the announcement itself is from April 2020) or through a channel the archive does not
cover, such as a direct message or a since-deleted post. Confirms: a member with early access
to the group, or Tiamat directly, produces a hint not present in the archive. Kills: nothing
further can kill this lead technically; it depends on information I do not have a channel to.

## 4. Puzzle #9's real solving method, if it ever surfaces (needs new information)

Tiamat described puzzle #9 as "similar" to #11, and #9 was swept by an anonymous solver in
2020 who never published a method; multiple community members describe the last step as
"forced" (brute-forced), not derived from a stated rule. If a #9 write-up ever surfaces, it
would give a real, oracle-certifiable answer to calibrate #11's harness against, which is
exactly what this folder is currently missing. Confirms: a published #9 method that this
folder's harness can reproduce byte-exact, at which point the same method becomes a certified
candidate class for #11. Kills: nothing; this is a standing watch item, not an active search.
