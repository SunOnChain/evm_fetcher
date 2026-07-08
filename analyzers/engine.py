from analyzers.transfer import analyze as transfer
from analyzers.swap import analyze as swap


ANALYZERS = [
    transfer,
    swap,
]


def analyze(group, wallets):
    for analyzer in ANALYZERS:
        try:
            result = analyzer(group, wallets)
        except TypeError:
            result = analyzer(group)

        if result:
            return result

    return "UNKNOWN"
