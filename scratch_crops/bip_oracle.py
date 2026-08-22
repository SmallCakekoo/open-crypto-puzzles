"""Standalone BIP39/BIP32/BIP44 derivation, no bip_utils dependency.
Verifies against the Aoi Nakamoto Quizchain calibration vector.
"""
import hashlib
import hmac
import struct

import base58
from ecdsa import SigningKey, SECP256k1
from ecdsa.ellipticcurve import Point
from mnemonic import Mnemonic

MNEMO = Mnemonic("english")
CURVE_ORDER = SECP256k1.order
G = SECP256k1.generator


def ripemd160(data: bytes) -> bytes:
    h = hashlib.new("ripemd160")
    h.update(data)
    return h.digest()


def hash160(data: bytes) -> bytes:
    return ripemd160(hashlib.sha256(data).digest())


def entropy_to_mnemonic(entropy: bytes) -> str:
    return MNEMO.to_mnemonic(entropy)


def mnemonic_to_seed(mnemonic: str, passphrase: str = "") -> bytes:
    return Mnemonic.to_seed(mnemonic, passphrase)


def master_key_from_seed(seed: bytes):
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    return I[:32], I[32:]  # (priv_key, chain_code)


def point_from_priv(priv_int: int) -> Point:
    return priv_int * G


def ser_p(point: Point) -> bytes:
    x = point.x()
    y = point.y()
    prefix = b"\x02" if y % 2 == 0 else b"\x03"
    return prefix + x.to_bytes(32, "big")


def ckd_priv(k_par: bytes, c_par: bytes, index: int):
    if index & 0x80000000:
        data = b"\x00" + k_par + struct.pack(">L", index)
    else:
        priv_int = int.from_bytes(k_par, "big")
        pub_point = point_from_priv(priv_int)
        data = ser_p(pub_point) + struct.pack(">L", index)
    I = hmac.new(c_par, data, hashlib.sha512).digest()
    IL, IR = I[:32], I[32:]
    IL_int = int.from_bytes(IL, "big")
    k_par_int = int.from_bytes(k_par, "big")
    child_int = (IL_int + k_par_int) % CURVE_ORDER
    child_key = child_int.to_bytes(32, "big")
    return child_key, IR


def derive_path(seed: bytes, path: str) -> bytes:
    """path like m/44'/0'/0'/0/5"""
    k, c = master_key_from_seed(seed)
    parts = path.split("/")[1:]
    for p in parts:
        hardened = p.endswith("'")
        idx = int(p[:-1]) if hardened else int(p)
        if hardened:
            idx |= 0x80000000
        k, c = ckd_priv(k, c, idx)
    return k


def privkey_to_wif(priv: bytes, compressed=True) -> str:
    payload = b"\x80" + priv + (b"\x01" if compressed else b"")
    return base58.b58encode_check(payload).decode()


def privkey_to_address(priv: bytes, compressed=True) -> str:
    priv_int = int.from_bytes(priv, "big")
    point = point_from_priv(priv_int)
    if compressed:
        pub = ser_p(point)
    else:
        pub = b"\x04" + point.x().to_bytes(32, "big") + point.y().to_bytes(32, "big")
    return base58.b58encode_check(b"\x00" + hash160(pub)).decode()


def check_candidate(text: str, indices=range(6)):
    entropy = hashlib.md5(text.encode("utf-8")).digest()
    mnemonic = entropy_to_mnemonic(entropy)
    seed = mnemonic_to_seed(mnemonic)
    results = []
    for i in indices:
        priv = derive_path(seed, f"m/44'/0'/0'/0/{i}")
        addr_c = privkey_to_address(priv, compressed=True)
        addr_u = privkey_to_address(priv, compressed=False)
        results.append((i, mnemonic, addr_c, addr_u, privkey_to_wif(priv, True)))
    return results


if __name__ == "__main__":
    # Certification vector from the puzzle's own README:
    # entropy 2941774a2abec9f30c7d6777d1d53d91, BIP44 index 1 ("my 2nd private key")
    # -> WIF L5Z66qPmUkTAsWQywjRNHDxHrX6J1X1SQedp6V8QsbaXR7rGd6ex
    entropy = bytes.fromhex("2941774a2abec9f30c7d6777d1d53d91")
    mnemonic = entropy_to_mnemonic(entropy)
    print("mnemonic:", mnemonic)
    seed = mnemonic_to_seed(mnemonic)
    priv = derive_path(seed, "m/44'/0'/0'/0/1")
    wif = privkey_to_wif(priv, compressed=True)
    expected = "L5Z66qPmUkTAsWQywjRNHDxHrX6J1X1SQedp6V8QsbaXR7rGd6ex"
    print("derived WIF: ", wif)
    print("expected WIF:", expected)
    print("SELFTEST", "OK" if wif == expected else "FAIL")
