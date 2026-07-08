from analyzers.transfer import analyze as transfer

from analyzers.swap import analyze as swap

ANALYZERS = [
    swap,
    transfer,
]


def analyze(tx):
    for analyzer in ANALYZERS:
        result = analyzer(tx)

        if result:
            tx.tx_type = result
            return result

    tx.tx_type = "UNKNOWN"
    return tx.tx_type
