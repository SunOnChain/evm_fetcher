from protocols.registry import get_protocol

info = get_protocol(
    "0xE592427A0AEce92De3Edee1F18E0157C05861564"
)

assert info["name"] == "Uniswap V3"
assert info["category"] == "DEX"

assert get_protocol(
    "0x0000000000000000000000000000000000000000"
) is None

print("Protocol registry passed.")
