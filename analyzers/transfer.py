from models.transaction import Transaction


def analyze(tx: Transaction):
    incoming = 0
    outgoing = 0

    wallet = tx.wallet.lower()

    for event in tx.asset_events:

        if event.sender and event.sender.lower() == wallet:
            outgoing += 1

        if event.receiver and event.receiver.lower() == wallet:
            incoming += 1

    if incoming and outgoing:
        return "SELF_TRANSFER"

    if incoming:
        return "RECEIVE"

    if outgoing:
        return "SEND"

    return None
