#!/usr/bin/env python3
"""
bip39_validate.py -- check a candidate phrase against the three BIP39 rules.

Purpose:
    Take a space-separated phrase and report, rule by rule, whether it could be a valid
    BIP39 mnemonic: (1) word count, (2) every word in the English wordlist, (3) checksum.
    This is a diagnostic tool, not a solver -- it tells you WHY a phrase is invalid, which
    plain IsValid()-style checks do not.

Input:
    A phrase on the command line, or one phrase per line on stdin with --stdin.

Output:
    One VALID or INVALID verdict per phrase, plus the specific rule that failed.

Usage:
    python examples/bip39_validate.py "dad butter wink follow trophy mixed erosion abandon abandon abandon abandon abandon"
    echo "some twelve word phrase ..." | python examples/bip39_validate.py --stdin

The math behind rule 3 (checksum), see README.md "How the BIP39 checksum works" for the
full derivation:
    A 12-word mnemonic encodes 128 bits of entropy (ENT) plus a 4-bit checksum (CS), where
    CS = the first ENT/32 bits of SHA-256(entropy). ENT + CS = 132 bits = 12 x 11 bits, one
    11-bit group per word. So changing any word changes the entropy that group encodes,
    which almost always changes the recomputed checksum -- only 1 in 16 random 12-word
    combinations from otherwise-fixed entropy will have a matching checksum. This is why
    the search space in candidate_checker.py divides by 16 for the last unknown word.

Study next: the Decode() call below is the same one bip_utils runs internally in
Bip39MnemonicValidator; examples/bip39_demo.py shows the reverse direction (entropy ->
mnemonic) that this checksum is built from.
"""
import argparse
import sys

from bip_utils import Bip39Languages, MnemonicChecksumError
from bip_utils.bip.bip39.bip39_mnemonic_decoder import Bip39MnemonicDecoder, Bip39WordsListGetter

VALID_WORD_COUNTS = (12, 15, 18, 21, 24)


def check(phrase: str) -> dict:
    words = phrase.strip().split()
    result = {
        "phrase": phrase.strip(),
        "word_count": len(words),
        "word_count_ok": len(words) in VALID_WORD_COUNTS,
        "unknown_words": [],
        "checksum_ok": False,
        "checksum_error": None,
    }

    wordlist = Bip39WordsListGetter().GetByLanguage(Bip39Languages.ENGLISH)
    for w in words:
        try:
            wordlist.GetWordIdx(w.lower())
        except ValueError:
            result["unknown_words"].append(w)

    if result["word_count_ok"] and not result["unknown_words"]:
        try:
            Bip39MnemonicDecoder(Bip39Languages.ENGLISH).Decode(phrase.strip())
            result["checksum_ok"] = True
        except MnemonicChecksumError as exc:
            result["checksum_error"] = str(exc)
        except Exception as exc:  # malformed input bip_utils rejects for another reason
            result["checksum_error"] = str(exc)

    return result


def report(result: dict) -> bool:
    is_valid = result["word_count_ok"] and not result["unknown_words"] and result["checksum_ok"]
    print(f"phrase: {result['phrase']}")
    print(f"  word count: {result['word_count']} "
          f"({'OK' if result['word_count_ok'] else 'expected one of ' + str(VALID_WORD_COUNTS)})")
    if result["unknown_words"]:
        print(f"  unknown words (not in BIP39 English wordlist): {result['unknown_words']}")
    elif result["word_count_ok"]:
        print("  all words are in the BIP39 English wordlist: OK")
    if result["word_count_ok"] and not result["unknown_words"]:
        if result["checksum_ok"]:
            print("  checksum: VALID")
        else:
            print(f"  checksum: INVALID ({result['checksum_error']})")
    print(f"  => {'VALID' if is_valid else 'INVALID'}")
    print()
    return is_valid


def main():
    parser = argparse.ArgumentParser(description="Check a phrase against the BIP39 rules.")
    parser.add_argument("phrase", nargs="?", help="space-separated candidate phrase")
    parser.add_argument("--stdin", action="store_true", help="read one phrase per line from stdin")
    args = parser.parse_args()

    if args.stdin:
        any_invalid = False
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            if not report(check(line)):
                any_invalid = True
        sys.exit(1 if any_invalid else 0)

    if not args.phrase:
        parser.error("provide a phrase, or use --stdin")

    ok = report(check(args.phrase))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
