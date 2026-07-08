def analyze(group, wallets):
    wallets = {w.lower() for w in wallets}

    incoming = False
    outgoing = False

    for row in group:
        sender = (row.get("from") or "").lower()
        receiver = (row.get("to") or "").lower()

        if sender in wallets:
            outgoing = True

        if receiver in wallets:
            incoming = True

    if incoming and outgoing:
        return "SELF"

    if incoming:
        return "RECEIVE"

    if outgoing:
        return "SEND"

    return None
