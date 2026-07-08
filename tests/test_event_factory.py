from models.event_factory import build_event
from models.event_types import ERC20_TRANSFER

row = {
    "tokenSymbol": "USDC",
    "tokenValue": "100",
    "from": "0x1",
    "to": "0x2",
}

event = build_event(row)

assert event.event_type == ERC20_TRANSFER
assert event.asset == "USDC"

print("Event factory passed.")
