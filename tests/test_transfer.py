from models.transaction import Transaction
from models.event import Event

from analyzers.transfer import analyze


tx = Transaction(
    hash="0x1",
    chain="ethereum",
    wallet="0xwallet",
    timestamp=1,
)

tx.add_event(
    Event(
        event_type="RAW",
        sender="0xwallet",
        receiver="0xabc",
        asset="ETH",
    )
)

assert analyze(tx) == "SEND"

print("Transfer analyzer passed.")
