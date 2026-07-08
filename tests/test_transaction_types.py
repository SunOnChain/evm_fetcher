from models.transaction_types import *

assert UNKNOWN == "UNKNOWN"
assert SEND == "SEND"
assert RECEIVE == "RECEIVE"
assert SELF_TRANSFER == "SELF_TRANSFER"
assert SWAP == "SWAP"
assert BRIDGE == "BRIDGE"
assert STAKE == "STAKE"
assert UNSTAKE == "UNSTAKE"
assert CLAIM == "CLAIM"
assert NFT_TRADE == "NFT_TRADE"
assert MINT == "MINT"
assert BURN == "BURN"
assert APPROVAL == "APPROVAL"

print("Transaction types passed.")
