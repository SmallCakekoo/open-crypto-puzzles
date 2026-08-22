import re
import html as htmllib
import sys
sys.path.insert(0, "scratch_crops")
from bip_oracle import check_candidate

TARGETS = {
    "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W": "Real Big Block",
    "13Cv6SXUnzGDT8JHqzzJ8xMPtsSdhJA4wd": "Block 76",
}

STAGE_ONE_NO_FLIP_INITIALS = set("ITASM")


def flip_case(paragraph: str) -> str:
    chars = list(paragraph)
    letters = [i for i, c in enumerate(chars) if c.isalpha()]
    if not letters:
        return paragraph
    first, last = letters[0], letters[-1]
    chars[first] = chars[first].lower()
    chars[last] = chars[last].upper()
    return "".join(chars)


def load_paragraphs(path):
    raw = open(path, encoding="utf-8", errors="ignore").read()
    ps = re.findall(r"<p[^>]*>(.*?)</p>", raw, re.S)
    out = []
    for p in ps:
        # strip inner tags (e.g. <b>, <i>), unescape entities
        text = re.sub(r"<[^>]+>", "", p)
        text = htmllib.unescape(text)
        text = text.strip()
        if text:
            out.append(text)
    return out


def test_all(paragraphs, label):
    variants = {
        "raw + \\r\\n\\r\\n": "\r\n\r\n".join(paragraphs),
        "raw + \\n\\n": "\n\n".join(paragraphs),
        "raw + \\r\\n": "\r\n".join(paragraphs),
        "flip(ITASM) + \\r\\n\\r\\n": "\r\n\r\n".join(
            p if p and p[0] in STAGE_ONE_NO_FLIP_INITIALS else flip_case(p) for p in paragraphs
        ),
        "flip(ITASM) + \\n\\n": "\n\n".join(
            p if p and p[0] in STAGE_ONE_NO_FLIP_INITIALS else flip_case(p) for p in paragraphs
        ),
    }
    for name, text in variants.items():
        hits = check_candidate(text, indices=range(6))
        matched = [h for h in hits if h[2] in TARGETS or h[3] in TARGETS]
        status = "MATCH!!!" if matched else "no match"
        print(f"[{label}] {name}: {status}  (len={len(text)} bytes~{len(text.encode('utf-8'))})")
        if matched:
            print("   ", matched)


if __name__ == "__main__":
    paras = load_paragraphs("scratch_crops/wattpad.html")
    print("total paragraphs:", len(paras))
    print("first 3 paragraph lengths:", [len(p) for p in paras[:3]])

    # widen the index range: a Reddit comment says "the 7th private key in
    # the list... contains the number 7 three times" -- test indices 0-20
    # instead of just 0-5, in case the real answer lives past index 5.
    variants = {
        "raw + \\r\\n\\r\\n": "\r\n\r\n".join(paras),
        "raw + \\n\\n": "\n\n".join(paras),
        "flip(ITASM) + \\r\\n\\r\\n": "\r\n\r\n".join(
            p if p and p[0] in STAGE_ONE_NO_FLIP_INITIALS else flip_case(p) for p in paras
        ),
        "flip(ITASM) + \\n\\n": "\n\n".join(
            p if p and p[0] in STAGE_ONE_NO_FLIP_INITIALS else flip_case(p) for p in paras
        ),
    }
    for name, text in variants.items():
        hits = check_candidate(text, indices=range(21))
        matched = [h for h in hits if h[2] in TARGETS or h[3] in TARGETS]
        print(f"[wide index 0-20] {name}: {'MATCH!!!' if matched else 'no match'}")
        if matched:
            print("   ", matched)
