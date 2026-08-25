#!/usr/bin/env python3
"""
oracle.py -- candidate checker for the Bitcoin Movie Enigma puzzle.

Purpose:
    The puzzle's own rules say the wallet is restored from a 24-word BIP39 mnemonic,
    obtained by dropping 10 "intruder" words from a 34-word sequence (one word per
    movie panel, in panel order). The author does not state the derivation path,
    account, or address index, so this oracle checks a 24-word candidate against
    BIP84, BIP49 and BIP44 (5 accounts, 10 address indices each, both the
    external and internal/change chains -- widened 2026-08-24 from the original
    2 accounts x 3 indices, external chain only, after an extended negative
    result across every other tested hypothesis made "we're checking too narrow
    a set of derivation paths" worth ruling out too) plus 3 raw derivation paths
    some simple wallets use. This is a verifier, not a search tool: it checks the
    24-word candidate you give it, it does not generate the C(34,10) ways to pick
    it.

    Widening the path coverage makes each check() call slower (153 addresses
    derived per candidate now, vs. 21 before, roughly 7x) -- see git history for
    the narrower 2-account/3-index/external-only version if reverting.

    To search which 10 of 34 known words to drop, generate the 24-word reductions
    yourself (Python's itertools.combinations) and pipe them through --stdin. That
    bound only applies once all 34 words and their order are known, which is not
    yet the case for this puzzle.

Usage:
    python3 tools/oracle.py --selftest                # must print SELFTEST OK
    python3 tools/oracle.py "w1 w2 ... w24"            # 24 space-separated BIP39 words
    python3 tools/oracle.py --stdin                    # one 24-word candidate per line

Input:
    A 24-word, space-separated candidate mnemonic on the command line or one per
    line on stdin.

Output:
    "MATCH <address> via <path>" on a hit, "NO MATCH" otherwise (including for a
    candidate that fails the BIP39 checksum, since no address can be derived from
    it). Exit 0 on any match, 1 if none.

Dependencies:
    stdlib, bip_utils.
"""

from __future__ import annotations

import argparse
import sys

from bip_utils import (
    Bip32Slip10Secp256k1,
    Bip39MnemonicValidator,
    Bip39SeedGenerator,
    Bip44,
    Bip44Changes,
    Bip44Coins,
    Bip49,
    Bip49Coins,
    Bip84,
    Bip84Coins,
    P2WPKHAddrEncoder,
)

TARGET_ADDRESS = "bc1q94ecsn0qk8lap2gefrycnms3ruepy889z969a6"

# Public BIP39/BIP84 test vectors (not specific to this puzzle). No solved sibling
# exists for this puzzle, so these certify the derivation path.
SELFTEST_12 = ("abandon " * 11 + "about").strip()
SELFTEST_12_ADDRESS = "bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu"
SELFTEST_24_GOOD = ("abandon " * 23 + "art").strip()
SELFTEST_24_BAD = ("abandon " * 23 + "about").strip()  # wrong checksum for 24 words


ACCOUNTS = 5   # widened 2026-08-24 from 2 -- the author never states an account number
INDICES = 10   # widened 2026-08-24 from 3 -- the author never states an address index
INCLUDE_INTERNAL_CHAIN = True  # also check the internal/change chain (CHAIN_INT), not just external


def addresses(mnemonic: str, passphrase: str = "") -> dict[str, str]:
    """Every plausible address for a mnemonic: BIP84/49/44, ACCOUNTS accounts x
    INDICES indices each, external and internal chains, plus 3 raw paths some
    simple wallets use. The author does not state a path, account, or index."""
    seed = Bip39SeedGenerator(mnemonic).Generate(passphrase)
    out = {}
    changes = (Bip44Changes.CHAIN_EXT, Bip44Changes.CHAIN_INT) if INCLUDE_INTERNAL_CHAIN else (Bip44Changes.CHAIN_EXT,)
    for name, cls, coin in (
        ("bip84", Bip84, Bip84Coins.BITCOIN),
        ("bip49", Bip49, Bip49Coins.BITCOIN),
        ("bip44", Bip44, Bip44Coins.BITCOIN),
    ):
        try:
            ctx = cls.FromSeed(seed, coin)
            for acct in range(ACCOUNTS):
                acct_ctx = ctx.Purpose().Coin().Account(acct)
                for change in changes:
                    change_ctx = acct_ctx.Change(change)
                    for i in range(INDICES):
                        node = change_ctx.AddressIndex(i)
                        chain_label = "ext" if change == Bip44Changes.CHAIN_EXT else "int"
                        out[f"{name} account {acct} {chain_label} index {i}"] = node.PublicKey().ToAddress()
        except Exception:  # noqa: BLE001
            pass
    try:
        root = Bip32Slip10Secp256k1.FromSeed(seed)
        for path in ("m/0/0", "m/0'/0'", "m/44'/0'/0'/0/0"):
            k = root.DerivePath(path).PublicKey().RawCompressed().ToBytes()
            out[f"raw {path} (p2wpkh)"] = P2WPKHAddrEncoder.EncodeKey(k, hrp="bc")
    except Exception:  # noqa: BLE001
        pass
    return out


def check(mnemonic: str) -> tuple[bool, str | None, str | None]:
    """Return (matched, address, path) for a 24-word candidate."""
    words = mnemonic.split()
    if len(words) != 24 or not Bip39MnemonicValidator().IsValid(mnemonic):
        return False, None, None
    for path, addr in addresses(mnemonic).items():
        if addr == TARGET_ADDRESS:
            return True, addr, path
    return False, None, None


def selftest() -> bool:
    ok = True

    addr = addresses(SELFTEST_12).get("bip84 account 0 ext index 0")
    found = addr == SELFTEST_12_ADDRESS
    print(f"public BIP84 test vector (12 words) -> {SELFTEST_12_ADDRESS}: {'OK' if found else 'FAIL'}")
    ok = ok and found

    valid_24 = Bip39MnemonicValidator().IsValid(SELFTEST_24_GOOD)
    addr24 = addresses(SELFTEST_24_GOOD).get("bip84 account 0 ext index 0")
    found24 = valid_24 and bool(addr24)
    print(f"24-word chain derives a non-empty address: {'OK' if found24 else 'FAIL'}")
    ok = ok and found24

    rejects = not Bip39MnemonicValidator().IsValid(SELFTEST_24_BAD)
    print(f"checksum filter rejects a 1-word-off variant: {'OK' if rejects else 'FAIL'}")
    ok = ok and rejects

    matched, _, _ = check(SELFTEST_24_GOOD)
    clean = not matched
    print(f"negative control (public vector vs escrow) -> no match: {'OK' if clean else 'FAIL'}")
    ok = ok and clean

    if ok:
        print("SELFTEST OK")
    return ok


def _print_result(candidate: str) -> bool:
    matched, addr, path = check(candidate)
    if matched:
        print(f"MATCH {addr} via {path}")
    else:
        print("NO MATCH")
    return matched


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", nargs="?", help="24 space-separated BIP39 words")
    parser.add_argument("--stdin", action="store_true", help="read candidates, one per line")
    parser.add_argument("--selftest", action="store_true", help="run the certification vectors")
    args = parser.parse_args()

    if args.selftest:
        return 0 if selftest() else 1

    if args.stdin:
        any_hit = False
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            any_hit = _print_result(line) or any_hit
        return 0 if any_hit else 1

    if not args.candidate:
        parser.print_help()
        return 0

    return 0 if _print_result(args.candidate) else 1


if __name__ == "__main__":
    sys.exit(main())
