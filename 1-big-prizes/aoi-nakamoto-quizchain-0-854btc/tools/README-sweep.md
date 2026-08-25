# Running the Real Big Block sweeps

Everything here targets the open lot only (0.777 BTC,
`14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W`). Background and prior negatives are in
`../README.md` and `../analysis/tested.md`; the reasoning behind each mode is
in `../analysis/leads.md`.

## What the lab machine needs

| Requirement | Notes |
|---|---|
| Python 3.9 or newer | 3.11+ preferred, it is measurably faster |
| `pip install coincurve` | libsecp256k1 bindings. **Optional but worth fighting for**: without it a pure-Python fallback runs, measured 11x slower |
| Outbound HTTPS to wattpad.com | once, for `fetch_source.py` |
| `pip install bip_utils pynacl` | optional, enables the independent cross-check in the self-test |
| No GPU | every mode here is CPU-bound on PBKDF2 |

Nothing else. No database, no network during the sweep itself, no writes
outside this `tools/` directory.

## If the machine is locked down

None of this needs administrator rights, and nothing here is a `.ps1`, so
PowerShell execution policy does not apply -- these are `.py` files run as
`python script.py`. The likely obstacles, in the order you will hit them:

**`pip install` refused, or no PyPI access.** Try `pip install --user coincurve`
first; failing that, `python -m venv .venv` then install inside it. If neither
works, do nothing: `fastderive.py` falls back to `secp256k1_pure.py`
automatically and prints which backend it chose on every run. The self-test
still passes on the fallback and still reproduces the author's published
vector, so results stay trustworthy -- just slower. On the fallback, run only
`transpose`, `ranges --profile core` and `appbytes`; the two large sweeps are
not realistic at 36 candidates/sec/core.

**`hashlib.new("ripemd160")` raises.** Expected on OpenSSL 3 builds, handled:
`ripemd160_pure.py` takes over, and it passes the official RIPEMD-160 vectors
including the 1,000,000-byte one.

**wattpad.com blocked by the network.** `fetch_source.py` is the only step
needing internet. Run it on a machine that does have access, then copy the
resulting `tools/source_cache.json` across by hand. The sweeps never touch the
network.

**No Python at all, and you cannot install it.** A portable build (WinPython,
or the python.org embeddable zip) is enough; there are no compiled extensions
in the fallback path.

**Whatever you do, do not skip `fastderive.py --selftest`.** It is the check
that whichever combination of backends the machine ended up with still
reproduces the author's own published vector.

## Order of operations

Run these three in order. Do not skip the first two: a sweep whose transform
is wrong produces confident negatives that are worse than no result.

```
pip install coincurve
python tools/fastderive.py --selftest
python tools/fetch_source.py
```

`--selftest` must print OK on the author's own published vector. `fetch_source.py`
must report 273 paragraphs and 6 NBSP; if it does not, stop and investigate
rather than using `--force`.

Then measure this machine before sizing anything:

```
python tools/bench_scale.py
```

Do not size a run from the core count. PBKDF2 does not vectorise and parallel
scaling is usually far worse than the core count suggests -- the laptop these
tools were written on reached only 3.0x with 8 workers. `bench_scale.py` prints
the worker count where throughput stops improving and converts that into wall
times for the two long sweeps. Use its number, not an estimate.

Then the sweeps, cheapest first:

```
python tools/sweep.py --mode transpose --profile full  --workers 24
python tools/sweep.py --mode ranges    --profile core  --workers 24
python tools/sweep.py --mode appbytes  --profile full  --workers 24
python tools/sweep.py --mode ranges    --profile full  --workers 24 --resume
python tools/sweep.py --mode edit2                     --workers 24 --resume
```

## Known results as of 2026-08-25

`transpose --profile full` (6,912) and `ranges --profile core` (224,406) have
both been run to completion and are negative, witness recovered. They are worth
re-running once on the lab machine only as a sanity check that the toolchain
works there; the value is in the modes below them.

## Reading the output

Every run plants a witness drawn from its own enumeration and must report
`witness RECOVERED` at the end. A run that prints `witness NOT recovered` exits
with status 2 and its negative result must be discarded, not recorded.

A hit prints a banner and appends to `tools/HIT_<mode>.txt`. Note that a hit on
the Stage One address (`19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN`) means the pipeline
is working but you have re-found the already-solved calibration block; only the
two Real Big Block addresses matter.

`--resume` picks up from `.sweep_<mode>_<profile>.ckpt`, so long runs survive a
reboot. Checkpoint granularity is one task, so at most one task is repeated.

## Do not commit

`source_cache.json` is the Wattpad chapter text, which this repository does not
redistribute. It and the `.ckpt` / `HIT_*` files are gitignored.
