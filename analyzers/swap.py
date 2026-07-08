def analyze(group):
    tokens_in = set()
    tokens_out = set()

    for row in group:
        value = float(row.get("value", 0))

        if value == 0:
            continue

        symbol = row.get("tokenSymbol") or row.get("symbol")

        if row.get("direction") == "IN":
            tokens_in.add(symbol)

        if row.get("direction") == "OUT":
            tokens_out.add(symbol)

    if tokens_in and tokens_out:
        return "SWAP"

    return None
