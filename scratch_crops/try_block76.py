import hashlib
import sys
sys.path.insert(0, "scratch_crops")
from bip_oracle import check_candidate

TARGETS = {
    "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W": "Real Big Block",
    "13Cv6SXUnzGDT8JHqzzJ8xMPtsSdhJA4wd": "Block 76",
}


def block76_filter(solution, tomi):
    h_sol = hashlib.md5(solution.encode("utf-8")).hexdigest()
    full = f"{solution} TOMI {tomi}"
    h_full = hashlib.md5(full.encode("utf-8")).hexdigest()
    return h_sol.startswith("1d"), h_full.startswith("f8e"), full


def test_pair(solution, tomi, indices=range(21)):
    sol_ok, full_ok, full = block76_filter(solution, tomi)
    if not (sol_ok and full_ok):
        return f"filters fail (sol={sol_ok}, full={full_ok})"
    hits = check_candidate(full, indices=indices)
    matched = [h for h in hits if h[2] in TARGETS or h[3] in TARGETS]
    return f"filters PASS, wide-index({indices.start}-{indices.stop-1}) match: {'YES!!! ' + str(matched) if matched else 'no'}"


if __name__ == "__main__":
    print("format / before TOMI:", test_pair("format", "before TOMI"))
