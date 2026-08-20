#!/usr/bin/env python3
"""
candidate_checker.py -- verbose, educational single-candidate checker for Challenge 14.

Purpose:
    Take one full 12-word mnemonic candidate and show, step by step, whether it solves this
    puzzle: BIP39 checksum, the derived BIP84 address, and whether that address matches the
    escrow. This is the same check tools/oracle.py performs (and is certified against the
    same public test vector); this script exists to print each step explicitly for learning,
    where oracle.py is written to be a terse pass/fail oracle for scripted use.

Input:
    A single 12-word mnemonic on the command line.

Output:
    CHECKSUM: VALID/INVALID
    DERIVATION PATH: m/84'/0'/0'/0/0
    ADDRESS: <derived address>
    TARGET: <escrow address>
    MATCH: YES/NO
    Exit code 0 on MATCH, 1 otherwise. Never broadcasts or constructs a transaction.

Usage:
    python tools/candidate_checker.py "dad butter wink follow trophy mixed erosion w8 w9 w10 w11 w12"
    python tools/candidate_checker.py --selftest

Cryptographic parts worth studying:
    Bip39MnemonicValidator().IsValid() re-derives the 4-bit checksum from the first 11
    words' worth of entropy and compares it to the 12th word's low bits -- see
    examples/bip39_validate.py for that check in isolation. Bip84.FromSeed(...).Purpose()
    .Coin().Account(0).Change(CHAIN_EXT).AddressIndex(0) walks m/84'/0'/0'/0/0 exactly as a
    native-segwit wallet would for its first receive address; PublicKey().ToAddress() is the
    hash160 + bech32 encoding step. This script only tries BIP84 (the puzzle's stated most
    likely path); tools/oracle.py also tries BIP49/BIP44 as a fallback.

Study next: analysis/search_space.py for how large the space of candidates like this one
is, before generating any of them in bulk.
"""
import argparse
import sys

from bip_utils import (
    Bip39MnemonicValidator, Bip39SeedGenerator,
    Bip84, Bip84Coins, Bip44Changes,
)

TARGET = "bc1q5rjy2cdfy4n4dkk4r6pxtwqlm8tgjcc2dj0ee9"
PATH = "m/84'/0'/0'/0/0"

SELFTEST_MNEMONIC = (
    "abandon abandon abandon abandon abandon abandon "
    "abandon abandon abandon abandon abandon about"
)
SELFTEST_ADDRESS = "bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu"


def derive_bip84_address(mnemonic: str) -> str:
    seed = Bip39SeedGenerator(mnemonic).Generate()
    return (
        Bip84.FromSeed(seed, Bip84Coins.BITCOIN).Purpose().Coin().Account(0)
        .Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        .PublicKey().ToAddress()
    )


def check(mnemonic: str, target: str = TARGET) -> bool:
    checksum_ok = Bip39MnemonicValidator().IsValid(mnemonic)
    print(f"CHECKSUM: {'VALID' if checksum_ok else 'INVALID'}")
    print(f"DERIVATION PATH: {PATH}")

    if not checksum_ok:
        print("ADDRESS: (not derived, checksum invalid)")
        print(f"TARGET: {target}")
        print("MATCH: NO")
        return False

    address = derive_bip84_address(mnemonic)
    match = address == target
    print(f"ADDRESS: {address}")
    print(f"TARGET: {target}")
    print(f"MATCH: {'YES' if match else 'NO'}")
    return match


def selftest():
    address = derive_bip84_address(SELFTEST_MNEMONIC)
    assert address == SELFTEST_ADDRESS, f"selftest derivation mismatch: {address} != {SELFTEST_ADDRESS}"
    print("SELFTEST OK")


def main():
    parser = argparse.ArgumentParser(description="Verbose single-candidate checker for Challenge 14.")
    parser.add_argument("mnemonic", nargs="?", help="space-separated 12-word candidate")
    parser.add_argument("--selftest", action="store_true", help="verify derivation against the public BIP39/BIP84 test vector")
    args = parser.parse_args()

    if args.selftest:
        selftest()
        sys.exit(0)

    if not args.mnemonic:
        parser.error("provide a 12-word mnemonic, or use --selftest")

    words = args.mnemonic.split()
    if len(words) != 12:
        parser.error(f"expected 12 words, got {len(words)}")

    matched = check(args.mnemonic)
    sys.exit(0 if matched else 1)


if __name__ == "__main__":
    main()
