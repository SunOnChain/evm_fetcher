from collections import defaultdict


def analyze(rows):
    groups = defaultdict(list)

    for row in rows:
        groups[row["hash"]].append(row)

    analyzed = []

    for tx_hash, tx_rows in groups.items():
        tags = []

        symbols = {
            r.get("tokenSymbol", "")
            for r in tx_rows
            if r.get("tokenSymbol")
        }

        methods = {
            r.get("method", "")
            for r in tx_rows
            if r.get("method")
        }

        if len(symbols) >= 2:
            tags.append("SWAP")

        elif any("swap" in m.lower() for m in methods):
            tags.append("SWAP")

        elif any("bridge" in m.lower() for m in methods):
            tags.append("BRIDGE")

        elif any("stake" in m.lower() for m in methods):
            tags.append("STAKE")

        elif any("claim" in m.lower() for m in methods):
            tags.append("CLAIM")

        elif any("airdrop" in m.lower() for m in methods):
            tags.append("AIRDROP")

        analyzed.append({
            "hash": tx_hash,
            "tags": tags,
            "rows": tx_rows,
        })

    return analyzed
