from models.transaction import Transaction
from models.event import Event

from analyzers.engine import analyze


tx = Transaction(
    hash="0xswap",
    chain="ethereum",
    wallet="0xwallet",
    timestamp=1,
)

tx.add_event(
    Event(
        event_type="RAW",
        sender="0xwallet",
        receiver="0xdex",
        asset="ETH",
    )
)

tx.add_event(
    Event(
        event_type="RAW",
        sender="0xdex",
        receiver="0xwallet",
        asset="USDC",
    )
)

assert analyze(tx) == "SWAP"

print("Swap analyzer passed.")
