#!/usr/bin/env python3
"""
fastderive.py -- fast, dependency-light reimplementation of the Quizchain
transform, for large sweeps.

Why this exists: tools/oracle.py uses bip_utils, which measures at roughly
264 derivations/sec/core. That is fine for checking a handful of candidates
and far too slow for the sweeps in analysis/leads.md. This module does the
same transform with hashlib (C-speed PBKDF2/HMAC) and coincurve
(libsecp256k1), and compares HASH160 digests directly instead of encoding a
base58 address per candidate.

It is NOT a replacement for oracle.py as the certified reference. It carries
its own self-test against the same published vector the README certifies
(entropy 2941774a2abec9f30c7d6777d1d53d91 -> index 1 WIF), plus a cross-check
against bip_utils when that package is importable, so drift between the two
implementations is caught before any sweep result is trusted.

Transform (identical to oracle.py):
    text -> MD5 (16 bytes entropy) -> BIP39 12-word mnemonic
         -> PBKDF2-HMAC-SHA512(mnemonic, "mnemonic", 2048) -> 64-byte seed
         -> BIP32 m/44'/0'/0'/0/i -> compressed pubkey -> HASH160
         -> compare against the target HASH160 set.

Dependencies: stdlib only. coincurve is used when present and a pure-Python
secp256k1 is used when it is not; likewise RIPEMD-160 falls back to
ripemd160_pure.py when hashlib lacks it. The BIP39 English wordlist ships alongside
as bip39-english.txt (public domain, part of the BIP39 spec; sha256
2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda).
"""

from __future__ import annotations

import hashlib
import hmac
import os

try:
    from coincurve import PrivateKey  # libsecp256k1; ~40x faster
    EC_BACKEND = "coincurve"
except ImportError:  # locked-down machine with no wheel and no compiler
    from secp256k1_pure import PrivateKey
    EC_BACKEND = "secp256k1_pure (slow fallback -- install coincurve if you can)"

SECP256K1_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

_HERE = os.path.dirname(os.path.abspath(__file__))
WORDLIST_PATH = os.path.join(_HERE, "bip39-english.txt")
WORDLIST_SHA256 = "2f5eed53a4727b4bf8880d8f3f199efc90e58503646d9ff8eff3a2ed3b24dbda"

# Same three targets as oracle.py, held as HASH160 (the 20 bytes a P2PKH
# address actually commits to). Comparing these skips base58 per candidate.
TARGETS_B58 = {
    "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W": "Real Big Block, current (0.777 BTC, OPEN)",
    "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC": "Real Big Block, superseded pre-rehash",
    "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN": "Block 77 Stage One (solved, calibration only)",
}

VECTOR_ENTROPY = "2941774a2abec9f30c7d6777d1d53d91"
VECTOR_WIF_INDEX1 = "L5Z66qPmUkTAsWQywjRNHDxHrX6J1X1SQedp6V8QsbaXR7rGd6ex"

_B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58decode(s: str) -> bytes:
    n = 0
    for ch in s:
        n = n * 58 + _B58.index(ch)
    body = n.to_bytes((n.bit_length() + 7) // 8, "big")
    pad = len(s) - len(s.lstrip("1"))
    return b"\x00" * pad + body


def b58encode_check(payload: bytes) -> str:
    chk = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    full = payload + chk
    n = int.from_bytes(full, "big")
    out = ""
    while n:
        n, r = divmod(n, 58)
        out = _B58[r] + out
    return "1" * (len(full) - len(full.lstrip(b"\x00"))) + out


def address_to_hash160(addr: str) -> bytes:
    raw = b58decode(addr)
    return raw[1:-4]


TARGETS = {address_to_hash160(a): lbl for a, lbl in TARGETS_B58.items()}


def _load_wordlist() -> list[str]:
    with open(WORDLIST_PATH, "rb") as fh:
        data = fh.read()
    got = hashlib.sha256(data).hexdigest()
    if got != WORDLIST_SHA256:
        raise SystemExit(
            "BIP39 wordlist checksum mismatch\n"
            f"  expected {WORDLIST_SHA256}\n  got      {got}"
        )
    words = data.decode("utf-8").split()
    if len(words) != 2048:
        raise SystemExit(f"wordlist must have 2048 words, got {len(words)}")
    return words


WORDS = _load_wordlist()


def entropy_to_mnemonic(entropy: bytes) -> str:
    """16 bytes -> 12-word BIP39 mnemonic (128 bits + 4-bit checksum)."""
    chk = hashlib.sha256(entropy).digest()[0] >> 4
    n = (int.from_bytes(entropy, "big") << 4) | chk
    return " ".join(WORDS[(n >> (11 * i)) & 0x7FF] for i in range(11, -1, -1))


def _have_ripemd160() -> bool:
    try:
        hashlib.new("ripemd160")
        return True
    except Exception:
        return False


if _have_ripemd160():
    def hash160(data: bytes) -> bytes:
        h = hashlib.new("ripemd160")
        h.update(hashlib.sha256(data).digest())
        return h.digest()
else:  # OpenSSL 3 builds often drop ripemd160
    from ripemd160_pure import ripemd160 as _rmd

    def hash160(data: bytes) -> bytes:
        return _rmd(hashlib.sha256(data).digest())


H = 0x80000000


def _ckd_priv(k: bytes, c: bytes, index: int) -> tuple[bytes, bytes]:
    if index >= H:
        data = b"\x00" + k + index.to_bytes(4, "big")
    else:
        data = PrivateKey(k).public_key.format(compressed=True) + index.to_bytes(4, "big")
    I = hmac.new(c, data, hashlib.sha512).digest()
    child = (int.from_bytes(I[:32], "big") + int.from_bytes(k, "big")) % SECP256K1_N
    return child.to_bytes(32, "big"), I[32:]


def derive_hash160s(entropy: bytes, n_indices: int = 6) -> list[bytes]:
    """entropy -> BIP39 -> m/44'/0'/0'/0/i for i in 0..n-1 -> HASH160 each."""
    seed = hashlib.pbkdf2_hmac(
        "sha512", entropy_to_mnemonic(entropy).encode("utf-8"), b"mnemonic", 2048, 64
    )
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    k, c = I[:32], I[32:]
    for idx in (44 + H, 0 + H, 0 + H, 0):
        k, c = _ckd_priv(k, c, idx)
    out = []
    for i in range(n_indices):
        ki, _ = _ckd_priv(k, c, i)
        out.append(hash160(PrivateKey(ki).public_key.format(compressed=True)))
    return out


def check_text(text: str, encoding: str = "utf-8", n_indices: int = 6):
    """Returns (label, index, address) on a hit, else None."""
    ent = hashlib.md5(text.encode(encoding, errors="strict")).digest()
    for i, h in enumerate(derive_hash160s(ent, n_indices)):
        if h in TARGETS:
            return TARGETS[h], i, b58encode_check(b"\x00" + h)
    return None


def derive_wif(entropy: bytes, index: int) -> str:
    seed = hashlib.pbkdf2_hmac(
        "sha512", entropy_to_mnemonic(entropy).encode("utf-8"), b"mnemonic", 2048, 64
    )
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    k, c = I[:32], I[32:]
    for idx in (44 + H, 0 + H, 0 + H, 0, index):
        k, c = _ckd_priv(k, c, idx)
    return b58encode_check(b"\x80" + k + b"\x01")


def selftest() -> bool:
    ok = True
    ent = bytes.fromhex(VECTOR_ENTROPY)

    wif = derive_wif(ent, 1)
    p1 = wif == VECTOR_WIF_INDEX1
    print(f"[1] author's published vector, index 1 WIF ......... {'OK' if p1 else 'FAIL'}")
    if not p1:
        print(f"    expected {VECTOR_WIF_INDEX1}")
        print(f"    got      {wif}")
    ok = ok and p1

    m = entropy_to_mnemonic(bytes(16))
    p2 = m == ("abandon " * 11) + "about"
    print(f"[2] BIP39 zero-entropy vector ...................... {'OK' if p2 else 'FAIL'}")
    ok = ok and p2

    p3 = all(b58encode_check(b"\x00" + address_to_hash160(a)) == a for a in TARGETS_B58)
    print(f"[3] base58 / HASH160 round-trip on all targets ..... {'OK' if p3 else 'FAIL'}")
    ok = ok and p3

    try:
        from bip_utils import (
            Bip39MnemonicGenerator,
            Bip39SeedGenerator,
            Bip44,
            Bip44Coins,
            Bip44Changes,
        )

        agree = True
        for _ in range(3):
            e = os.urandom(16)
            mn = Bip39MnemonicGenerator().FromEntropy(e)
            sd = Bip39SeedGenerator(mn).Generate()
            acct = (
                Bip44.FromSeed(sd, Bip44Coins.BITCOIN)
                .Purpose()
                .Coin()
                .Account(0)
                .Change(Bip44Changes.CHAIN_EXT)
            )
            ref = [acct.AddressIndex(i).PublicKey().ToAddress() for i in range(3)]
            mine = [b58encode_check(b"\x00" + h) for h in derive_hash160s(e, 3)]
            agree = agree and (ref == mine)
        print(f"[4] cross-check vs bip_utils, random entropy ....... {'OK' if agree else 'FAIL'}")
        ok = ok and agree
    except Exception as exc:
        print(f"[4] cross-check vs bip_utils ....................... SKIPPED ({type(exc).__name__})")

    return ok


if __name__ == "__main__":
    import sys

    print(f"EC backend:       {EC_BACKEND}")
    print(f"RIPEMD-160:       {'hashlib' if _have_ripemd160() else 'ripemd160_pure (fallback)'}")
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        sys.exit(0 if selftest() else 1)
    if len(sys.argv) > 1 and sys.argv[1] == "--bench":
        import time

        t0 = time.perf_counter()
        N = 300
        for i in range(N):
            derive_hash160s(hashlib.md5(str(i).encode()).digest(), 6)
        dt = time.perf_counter() - t0
        print(f"{N / dt:,.0f} candidates/sec/core (6 indices each)")
        sys.exit(0)
    print(__doc__)
