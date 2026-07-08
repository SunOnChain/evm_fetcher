from models.transaction import Transaction
from models.event import Event


tx = Transaction(
    hash="0x123",
    chain="ethereum",
    wallet="0xabc",
    timestamp=1234567890,
)

tx.add_event(
    Event(
        event_type="TRANSFER",
        asset="ETH",
        amount=1,
    )
)

assert len(tx.events) == 1
assert tx.events[0].asset == "ETH"

print("Model tests passed.")
