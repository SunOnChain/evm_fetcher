from analyzers.protocol import analyze as protocol
from analyzers.swap import analyze as swap
from analyzers.transfer import analyze as transfer

from models.transaction_types import UNKNOWN


ANALYZERS = [
    swap,
    transfer,
]


def analyze(tx):
    # Enrich transaction first
    protocol(tx)

    # Then classify it
    for analyzer in ANALYZERS:
        result = analyzer(tx)

        if result:
            tx.tx_type = result
            return result

    tx.tx_type = UNKNOWN
    return tx.tx_type
