from protocols.registry import get_protocol


def analyze(tx):
    addresses = set()

    for event in tx.asset_events:
        if event.sender:
            addresses.add(event.sender.lower())

        if event.receiver:
            addresses.add(event.receiver.lower())

        if event.contract:
            addresses.add(event.contract.lower())

    for address in addresses:
        info = get_protocol(address)

        if info:
            tx.protocol = info["name"]
            tx.category = info["category"]
            return info

    tx.protocol = None
    tx.category = None
    return None
