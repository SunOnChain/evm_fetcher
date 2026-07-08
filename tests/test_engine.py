from models.transaction import Transaction
from models.event import Event

from analyzers.engine import analyze


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

result = analyze(tx)

assert result == "SEND"
assert tx.tx_type == "SEND"

print("Analyzer engine passed.")
