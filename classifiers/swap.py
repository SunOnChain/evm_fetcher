def is_swap(group):
    symbols = set()

    for row in group:
        sym = row.get("tokenSymbol")
        if sym:
            symbols.add(sym)

    if len(symbols) >= 2:
        return True

    for row in group:
        method = (row.get("method") or "").lower()

        if "swap" in method:
            return True

    return False
