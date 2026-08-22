import json
import re
import subprocess
import sys
import time

sys.path.insert(0, r"C:\Users\patat\Desktop\open-crypto-puzzles\2-mid-prizes\teikhos-bipedaljoe-solver-bounties-2eth\tools")
import oracle  # the repo's own certified oracle

RPC = "https://ethereum-rpc.publicnode.com"


def rpc(method, params):
    payload = json.dumps({"jsonrpc": "2.0", "method": method, "params": params, "id": 1})
    out = subprocess.run(
        ["curl", "-s", "-X", "POST", "-H", "Content-Type: application/json",
         "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
         "--data", payload, RPC],
        capture_output=True, text=True, timeout=25,
    )
    return json.loads(out.stdout)


def extract_pubkey_candidates(input_hex: str):
    """authenticate(bytes) ABI-encodes: [4-byte selector][32-byte offset][32-byte length][data...]
    Try to pull out any 64-byte (128 hex char) run that could be the public key, robust to
    slightly different ABI shapes across the 3 variants."""
    data = input_hex[2:] if input_hex.startswith("0x") else input_hex
    candidates = set()
    # standard case: selector(8) + offset(64) + length(64) + payload
    if len(data) >= 8 + 64 + 64:
        payload = data[8 + 64 + 64:]
        if len(payload) >= 128:
            candidates.add(payload[:128])
    # fallback: just take the last 128 hex chars of the whole calldata
    if len(data) >= 128:
        candidates.add(data[-128:])
    return candidates


def main():
    hashes = [h.strip() for h in open(r"scratch_crops\all_hashes.txt") if h.strip().startswith("0x") and len(h.strip()) == 66]
    print(f"checking {len(hashes)} transactions...")
    hits = []
    for h in hashes:
        try:
            r = rpc("eth_getTransactionByHash", [h])
        except Exception as e:
            print(h, "RPC ERROR", e)
            continue
        result = r.get("result")
        if not result:
            print(h, "not found")
            continue
        to = (result.get("to") or "").lower()
        input_hex = result.get("input", "")
        cands = extract_pubkey_candidates(input_hex)
        for cand in cands:
            for tag, spec in oracle.CONTRACTS.items():
                if tag == "735B" or tag == "AEC7":
                    continue  # already solved / permanently dead, skip
                try:
                    res = oracle.check(cand, spec)
                except Exception:
                    continue
                if res.get("ok"):
                    hits.append((h, to, tag, cand, res))
                    print("!!! MATCH !!!", h, "->", tag, res)
        print(h, "to=", to, "checked", len(cands), "candidate(s), no match yet" if not hits else "")
        time.sleep(0.15)
    print()
    print("=== SUMMARY ===")
    print("total hits:", len(hits))
    for hit in hits:
        print(hit)


if __name__ == "__main__":
    main()
