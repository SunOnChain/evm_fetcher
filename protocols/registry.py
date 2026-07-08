PROTOCOLS = {
    # DEX
    "0xe592427a0aece92de3edee1f18e0157c05861564": {
        "name": "Uniswap V3",
        "category": "DEX",
    },
    "0x111111125421ca6dc452d289314280a0f8842a65": {
        "name": "1inch",
        "category": "DEX",
    },
}


def get_protocol(address):
    if not address:
        return None

    return PROTOCOLS.get(address.lower())
