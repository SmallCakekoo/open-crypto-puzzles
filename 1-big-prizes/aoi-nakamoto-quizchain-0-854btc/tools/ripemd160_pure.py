#!/usr/bin/env python3
"""
ripemd160_pure.py -- pure-Python RIPEMD-160, used only as a fallback.

Python's hashlib exposes ripemd160 only when the linked OpenSSL provides it.
OpenSSL 3 moved RIPEMD-160 to the legacy provider, so many current builds raise
on hashlib.new("ripemd160"). Bitcoin's HASH160 needs it, so fastderive.py falls
back to this module when hashlib cannot supply it.

This is slower than the C implementation, but RIPEMD-160 is a negligible share
of per-candidate cost (PBKDF2 dominates by orders of magnitude), so the
practical penalty for a sweep is small.

Self-test: python3 tools/ripemd160_pure.py
"""

from __future__ import annotations

import struct

_R = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
    7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8,
    3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12,
    1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2,
    4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13,
]
_RP = [
    5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12,
    6, 11, 3, 7, 0, 13, 5, 10, 14, 15, 8, 12, 4, 9, 1, 2,
    15, 5, 1, 3, 7, 14, 6, 9, 11, 8, 12, 2, 10, 0, 4, 13,
    8, 6, 4, 1, 3, 11, 15, 0, 5, 12, 2, 13, 9, 7, 10, 14,
    12, 15, 10, 4, 1, 5, 8, 7, 6, 2, 13, 14, 0, 3, 9, 11,
]
_S = [
    11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8,
    7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12,
    11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5,
    11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12,
    9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6,
]
_SP = [
    8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6,
    9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11,
    9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5,
    15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8,
    8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11,
]
_K = [0x00000000, 0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xA953FD4E]
_KP = [0x50A28BE6, 0x5C4DD124, 0x6D703EF3, 0x7A6D76E9, 0x00000000]

_M = 0xFFFFFFFF


def _f(j: int, x: int, y: int, z: int) -> int:
    if j < 16:
        return x ^ y ^ z
    if j < 32:
        return (x & y) | (~x & z)
    if j < 48:
        return (x | ~y & _M) ^ z
    if j < 64:
        return (x & z) | (y & ~z)
    return x ^ (y | ~z & _M)


def _rol(x: int, n: int) -> int:
    x &= _M
    return ((x << n) | (x >> (32 - n))) & _M


def _compress(h, block: bytes):
    x = struct.unpack("<16I", block)
    a, b, c, d, e = h
    ap, bp, cp, dp, ep = h

    for j in range(80):
        t = _rol(a + _f(j, b, c, d) + x[_R[j]] + _K[j // 16], _S[j]) + e
        a, e, d, c, b = e, d, _rol(c, 10), b, t & _M

        t = _rol(ap + _f(79 - j, bp, cp, dp) + x[_RP[j]] + _KP[j // 16], _SP[j]) + ep
        ap, ep, dp, cp, bp = ep, dp, _rol(cp, 10), bp, t & _M

    return [
        (h[1] + c + dp) & _M,
        (h[2] + d + ep) & _M,
        (h[3] + e + ap) & _M,
        (h[4] + a + bp) & _M,
        (h[0] + b + cp) & _M,
    ]


def ripemd160(data: bytes) -> bytes:
    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
    msg = bytearray(data)
    bitlen = (len(data) * 8) & 0xFFFFFFFFFFFFFFFF
    msg.append(0x80)
    while len(msg) % 64 != 56:
        msg.append(0)
    msg += struct.pack("<Q", bitlen)
    for i in range(0, len(msg), 64):
        h = _compress(h, bytes(msg[i:i + 64]))
    return struct.pack("<5I", *h)


_VECTORS = {
    b"": "9c1185a5c5e9fc54612808977ee8f548b2258d31",
    b"a": "0bdc9d2d256b3ee9daae347be6f4dc835a467ffe",
    b"abc": "8eb208f7e05d987a9b044a8e98c6b087f15a0bfc",
    b"message digest": "5d0689ef49d2fae572b881b123a85ffa21595f36",
    b"abcdefghijklmnopqrstuvwxyz": "f71c27109c692c1b56bbdceb5b9d2865b3708dbc",
    b"a" * 1000000: "52783243c1697bdbe16d37f97f68f08325dc1528",
}


def selftest() -> bool:
    ok = True
    for data, expect in _VECTORS.items():
        got = ripemd160(data).hex()
        good = got == expect
        ok = ok and good
        name = f"{len(data)} bytes" if len(data) > 20 else repr(data)
        print(f"  {name:24s} {'OK' if good else 'FAIL ' + got}")
    return ok


if __name__ == "__main__":
    import sys

    print("RIPEMD-160 official test vectors:")
    sys.exit(0 if selftest() else 1)
