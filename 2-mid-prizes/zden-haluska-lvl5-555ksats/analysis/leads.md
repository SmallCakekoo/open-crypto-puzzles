# Open leads, full notes

## 1. A clarification from the author on 3 exact bindings

The geometry is fully certified and the mini-hint formula is read at the pixel level, but 3
specific meanings are not fixed by anything the author has published:

- What "x" refers to in "64/x - x": a value that varies per rectangle or per pair (most
  likely a border-thickness measurement), or a single fixed constant.
- The exact normalization meant by "apply more operations to obtain the results in byte
  range": which specific rounding or scaling step turns a raw sum into a single byte.
- The exact sense of "following": which of the several spatially plausible pairings (or a
  sorted-order pairing not yet fully explored) the author means.

Once any one of these is fixed by new information, the already-certified geometry becomes
the 32 key bytes by direct calculation, with no further search needed. The author has a
track record of eventually clarifying hints for other puzzles in the same series (a
correction was already issued once, in 2021, for this puzzle itself), so a direct question
to the author is the highest-ranked lead here.

## 2. A higher-fidelity source for the mini-hint glyphs

The 2021 mini-hint is read at the pixel level from the published image itself; a source
image at higher resolution than what has been published (if one exists) could resolve
ambiguity in the glyph reading directly, without needing the author's own clarification.

## 3. A wider author-error tolerance sweep

A 3-byte wildcard tolerance sweep on 1 or 2 of the candidate bases already tried (roughly
660 million derivations per base) is a bounded search, not an open-ended one, but its
expected value is marginal against the leads above and it has not been run.

## Correction candidate (unverified): line 4 of the mini-hint may be mis-transcribed

Re-read at the pixel level from `clues/crypto5fix.png` (2026-08-21), comparing exact pixel
runs rather than eyeballing a scaled render. Column positions for the mini-hint's 4 text
lines are identical across lines (glyph slots at x-offsets 8-14, 16-22, 24-30 relative to
each line's left border), which makes a direct pixel diff between lines possible:

- Line 1 (`-I`), line 2 (`×X+`), and line 3 (`LXIV`) read as stated elsewhere in this file
  and in the README: `-1`, `× X +`, `64`.
- Line 4, currently transcribed as "divided by x" (i.e. `÷ X`, or `64/x` in the phrasing
  above): pixel-diffing line 4's middle glyph (slot 16-22) against line 2's small `×` glyph
  (slot 8-14) shows they are **pixel-identical** (same 6-row checkerboard-diagonal pattern).
  Line 4's outer two glyphs (slots 8-14 and 24-30) are a different, diagonal-staircase shape
  that does not match `÷` in this font. The line reads as `/ × /` (slash, times, slash), not
  `÷ X`.

This does not resolve what `/ × /` means (a second multiplication? a modulo bracket? a
purely decorative flourish, given the hint box's framing ticks are a separate decorative
element at rows above/below the 4 text lines, not part of this glyph run?). It only
establishes that the current "divided by x" transcription does not match the image's pixels
as closely as previously assumed.

Tested against this correction, 2026-08-21: `-1 * X + 64` (dropping the disputed division
entirely) across 4 pairing senses (simple, column-major, interleaved-columns, column-blocks)
x 5 definitions of X (outer/inner/shell-area pair-sum, average and summed border-thickness)
x forward/reverse byte order = 200 candidate keys, 0 matches. Also tested reading the tall
"X" in line 2 as the Roman numeral 10 rather than a per-rectangle variable (making the whole
box a fixed constant, `-1*10+64=54`, applied as +54/-54/*54/mod 54 to each pair-sum, or used
as a constant key) = 36 more candidates, 0 matches. Neither closes the lead; both are
reported here so they are not re-tried from scratch. The pixel-mismatch finding itself is
the useful part: whoever revisits this hint should re-derive the line 4 reading from the
image directly rather than trusting the "divided by x" transcription used elsewhere in this
file and in the README.
