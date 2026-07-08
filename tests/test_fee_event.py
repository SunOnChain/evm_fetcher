from models.event_factory import build_fee_event
from models.event_types import GAS_FEE

row = {
    "from": "0xwallet",
    "gasUsed": "21000",
    "gasPrice": "1000000000",
}

event = build_fee_event(row)

assert event.event_type == GAS_FEE
assert event.is_fee is True

print("Fee event passed.")
