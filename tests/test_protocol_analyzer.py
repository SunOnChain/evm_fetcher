from analyzers.engine import analyze
from models.event import Event
from models.event_types import ERC20_TRANSFER
from models.transaction import Transaction


tx = Transaction(
    hash="0x1",
    chain="ethereum",
    wallet="0xwallet",
    timestamp=1,
)

tx.add_event(
    Event(
        event_type=ERC20_TRANSFER,
        asset="ETH",
        amount=1,
        sender="0xwallet",
        receiver="0xE592427A0AEce92De3Edee1F18E0157C05861564",
    )
)

analyze(tx)

assert tx.protocol == "Uniswap V3"

print("Protocol analyzer passed.")
