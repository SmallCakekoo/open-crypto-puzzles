#!/usr/bin/env python3
"""
secp256k1_pure.py -- pure-Python secp256k1 scalar multiplication, used only as
a fallback when coincurve is unavailable.

Why this exists: coincurve needs a wheel or a compiler, and a locked-down lab
machine may allow neither. This module lets the whole toolchain run on a
stdlib-only Python. It is used for exactly one operation: turning a 32-byte
private key into a 33-byte compressed public key.

Cost, measured rather than estimated: a full candidate derivation drops from
403/sec/core with coincurve to 36/sec/core with this module -- about 11x
slower, because the seven point multiplications per candidate end up costing
several times the PBKDF2 step they were previously dwarfed by.

Practical consequence: the small sweeps (transpose, ranges core, appbytes)
still finish in minutes to an hour on this fallback, but the two large ones
become impractical. Treat this module as the way to get useful work done on a
locked-down machine, not as a substitute for installing coincurve.

Self-test: python3 tools/secp256k1_pure.py
"""

from __future__ import annotations

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8


def _jac_double(pt):
    x, y, z = pt
    if y == 0:
        return (0, 0, 0)
    ysq = (y * y) % P
    s = (4 * x * ysq) % P
    m = (3 * x * x) % P  # a = 0 for secp256k1
    nx = (m * m - 2 * s) % P
    ny = (m * (s - nx) - 8 * ysq * ysq) % P
    nz = (2 * y * z) % P
    return (nx, ny, nz)


def _jac_add(p1, p2):
    x1, y1, z1 = p1
    x2, y2, z2 = p2
    if z1 == 0:
        return p2
    if z2 == 0:
        return p1
    z1sq = (z1 * z1) % P
    z2sq = (z2 * z2) % P
    u1 = (x1 * z2sq) % P
    u2 = (x2 * z1sq) % P
    s1 = (y1 * z2sq * z2) % P
    s2 = (y2 * z1sq * z1) % P
    if u1 == u2:
        if s1 != s2:
            return (0, 0, 0)
        return _jac_double(p1)
    h = (u2 - u1) % P
    r = (s2 - s1) % P
    hsq = (h * h) % P
    hcu = (hsq * h) % P
    u1hsq = (u1 * hsq) % P
    nx = (r * r - hcu - 2 * u1hsq) % P
    ny = (r * (u1hsq - nx) - s1 * hcu) % P
    nz = (h * z1 * z2) % P
    return (nx, ny, nz)


def _jac_mul(pt, k: int):
    if k % N == 0 or pt[1] == 0:
        return (0, 0, 0)
    result = (0, 0, 0)
    addend = pt
    while k:
        if k & 1:
            result = _jac_add(result, addend)
        addend = _jac_double(addend)
        k >>= 1
    return result


def _to_affine(pt):
    x, y, z = pt
    if z == 0:
        raise ValueError("point at infinity")
    zinv = pow(z, P - 2, P)
    zinv2 = (zinv * zinv) % P
    return (x * zinv2) % P, (y * zinv2 * zinv) % P


def pubkey_compressed(privkey: bytes) -> bytes:
    """32-byte private key -> 33-byte compressed public key (SEC1)."""
    k = int.from_bytes(privkey, "big")
    if not 0 < k < N:
        raise ValueError("private key out of range")
    x, y = _to_affine(_jac_mul((GX, GY, 1), k))
    return bytes([2 + (y & 1)]) + x.to_bytes(32, "big")


class PrivateKey:
    """Minimal stand-in for coincurve.PrivateKey, covering only the one call
    fastderive.py makes: .public_key.format(compressed=True)."""

    __slots__ = ("_secret",)

    def __init__(self, secret: bytes):
        self._secret = secret

    @property
    def public_key(self):
        return _PublicKey(self._secret)


class _PublicKey:
    __slots__ = ("_secret",)

    def __init__(self, secret: bytes):
        self._secret = secret

    def format(self, compressed: bool = True) -> bytes:
        if not compressed:
            raise NotImplementedError("only compressed output is needed here")
        return pubkey_compressed(self._secret)


def selftest() -> bool:
    ok = True

    # Generator point: private key 1 must give the well-known compressed G.
    g = pubkey_compressed((1).to_bytes(32, "big")).hex()
    expect_g = "0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798"
    p1 = g == expect_g
    print(f"  privkey 1 -> compressed G .......... {'OK' if p1 else 'FAIL ' + g}")
    ok = ok and p1

    # A second published vector: privkey 2.
    g2 = pubkey_compressed((2).to_bytes(32, "big")).hex()
    expect_g2 = "02c6047f9441ed7d6d3045406e95c07cd85c778e4b8cef3ca7abac09b95c709ee5"
    p2 = g2 == expect_g2
    print(f"  privkey 2 -> published vector ...... {'OK' if p2 else 'FAIL ' + g2}")
    ok = ok and p2

    # Agreement with coincurve on random keys, when it is installed.
    try:
        import os

        from coincurve import PrivateKey as CCPriv

        agree = True
        for _ in range(20):
            s = os.urandom(32)
            if not 0 < int.from_bytes(s, "big") < N:
                continue
            agree = agree and (
                CCPriv(s).public_key.format(compressed=True) == pubkey_compressed(s)
            )
        print(f"  agrees with coincurve, 20 keys ..... {'OK' if agree else 'FAIL'}")
        ok = ok and agree
    except ImportError:
        print("  agrees with coincurve .............. SKIPPED (not installed)")

    return ok


if __name__ == "__main__":
    import sys

    print("secp256k1 pure-Python self-test:")
    sys.exit(0 if selftest() else 1)
