#!/usr/bin/env python3
"""
bip39_demo.py -- educational walkthrough of the BIP39 -> BIP32 -> BIP84 pipeline.

Purpose:
    Generate a fresh, random 12-word BIP39 mnemonic (TEST DATA ONLY, thrown away when the
    process exits) and print every stage of the pipeline: entropy -> mnemonic -> seed ->
    BIP32 master key -> BIP84 account/change/address-index derivation -> extended keys ->
    public key -> Bitcoin address. This is a learning tool, not a wallet: nothing it prints
    is meant to hold real funds, and no real seed phrase should ever be pasted into it.

Input:
    None (random entropy each run), or --entropy-hex <32 hex chars> to make a run
    reproducible with a chosen TEST entropy value (still not for real funds).

Output:
    A labeled, step-by-step printout of entropy, mnemonic, seed, derivation path, extended
    keys, public key, and address.

Usage:
    python examples/bip39_demo.py
    python examples/bip39_demo.py --entropy-hex 00000000000000000000000000000000
    python examples/bip39_demo.py --path "m/84'/0'/0'/0/0"

Cryptographic parts worth studying:
    1. Entropy -> mnemonic (Bip39MnemonicGenerator.FromEntropy): 128 bits of entropy plus a
       4-bit checksum (SHA-256 of the entropy, first 4 bits) become 132 bits, split into 12
       groups of 11 bits, each group indexing one of the 2048 words in the wordlist.
    2. Mnemonic -> seed (Bip39SeedGenerator.Generate): PBKDF2-HMAC-SHA512 over the mnemonic
       string, salted with "mnemonic" + passphrase, 2048 rounds, producing a 512-bit seed.
       This one-way stretch is why a strong mnemonic does not make a weak passphrase safe.
    3. Seed -> BIP32 master key -> BIP84 path (Bip84.FromSeed + Purpose/Coin/Account/Change/
       AddressIndex): HMAC-SHA512 keyed derivation down m/84'/0'/0'/0/0, the path native
       segwit (bc1...) wallets use for the first receiving address.
    4. Public key -> address: compressed secp256k1 public key -> SHA256 -> RIPEMD160 ->
       bech32 encoding (P2WPKH), which is why the address is deterministic once the seed
       and path are fixed.

Study next: examples/bip39_validate.py for how the checksum in step 1 is checked in
isolation, and 3-small-prizes/exitonly-challenge-14-30ksats/tools/candidate_checker.py for
how this whole pipeline is reused to test one candidate mnemonic against a real puzzle.
"""
import argparse
import os

from bip_utils import (
    Bip39MnemonicGenerator,
    Bip39SeedGenerator,
    Bip39EntropyBitLen,
    Bip84,
    Bip84Coins,
    Bip44Changes,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1].strip())
    parser.add_argument(
        "--entropy-hex", default=None,
        help="32 hex chars (128 bits) of TEST entropy; random if omitted",
    )
    parser.add_argument(
        "--passphrase", default="",
        help="optional BIP39 passphrase (default: none)",
    )
    args = parser.parse_args()

    print("=== 1. Entropy ===")
    if args.entropy_hex:
        entropy = bytes.fromhex(args.entropy_hex)
        if len(entropy) * 8 != Bip39EntropyBitLen.BIT_LEN_128:
            raise SystemExit(f"--entropy-hex must be 32 hex chars (128 bits), got {len(entropy)*8} bits")
        print(f"source: --entropy-hex (fixed, for reproducibility -- TEST DATA ONLY)")
    else:
        entropy = os.urandom(Bip39EntropyBitLen.BIT_LEN_128 // 8)
        print("source: os.urandom (fresh random TEST entropy, not saved anywhere)")
    print(f"entropy (128 bits, hex): {entropy.hex()}")

    print("\n=== 2. BIP39 mnemonic ===")
    mnemonic = Bip39MnemonicGenerator().FromEntropy(entropy)
    print(f"mnemonic (12 words):     {mnemonic}")
    print("  (128 bits entropy + 4-bit checksum = 132 bits = 12 x 11-bit word indices)")

    print("\n=== 3. BIP39 seed ===")
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate(args.passphrase)
    print(f"passphrase used:          {'(none)' if not args.passphrase else '(a passphrase was set)'}")
    print(f"seed (512 bits, hex):     {seed_bytes.hex()}")
    print("  (PBKDF2-HMAC-SHA512, 2048 rounds, salt = 'mnemonic' + passphrase)")

    print("\n=== 4. BIP32/BIP84 derivation ===")
    path = "m/84'/0'/0'/0/0"
    print(f"derivation path:          {path}  (BIP84, native segwit / bech32)")
    acct_ctx = Bip84.FromSeed(seed_bytes, Bip84Coins.BITCOIN).Purpose().Coin().Account(0)
    leaf_ctx = acct_ctx.Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)

    print(f"account xprv (extended):  {acct_ctx.PrivateKey().ToExtended()}")
    print(f"account zpub (extended):  {acct_ctx.PublicKey().ToExtended()}")

    print("\n=== 5. Leaf key and address ===")
    print(f"public key (compressed):  {leaf_ctx.PublicKey().RawCompressed().ToHex()}")
    print(f"private key (WIF):        {leaf_ctx.PrivateKey().ToWif()}")
    print(f"Bitcoin address:          {leaf_ctx.PublicKey().ToAddress()}")

    print(
        "\nThis mnemonic and every key above are throwaway TEST data generated locally for "
        "this demo run only. Never enter a real seed phrase or private key into this or any "
        "similar script."
    )


if __name__ == "__main__":
    main()
