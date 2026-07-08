from models.transaction import Transaction
from models.transaction_types import SWAP


def analyze(tx: Transaction):
    # Known DEX interaction is a strong signal.
    if tx.category != "DEX":
        return None

    wallet = tx.wallet.lower()

    incoming = set()
    outgoing = set()

    for event in tx.asset_events:
        if event.sender and event.sender.lower() == wallet:
            outgoing.add(event.asset)

        if event.receiver and event.receiver.lower() == wallet:
            incoming.add(event.asset)

    if incoming and outgoing:
        return SWAP

    return None
