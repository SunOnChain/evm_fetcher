from models.event_types import *

assert NATIVE_TRANSFER == "NATIVE_TRANSFER"
assert INTERNAL_TRANSFER == "INTERNAL_TRANSFER"
assert ERC20_TRANSFER == "ERC20_TRANSFER"
assert ERC721_TRANSFER == "ERC721_TRANSFER"
assert ERC1155_TRANSFER == "ERC1155_TRANSFER"
assert GAS_FEE == "GAS_FEE"
assert UNKNOWN == "UNKNOWN"

print("Event type tests passed.")
