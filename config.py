ETHERSCAN_API_KEY = "33K1RQY65FQ159DBJB5G5TQWM7XWXPIK77"

CHAINS = {
    "1": {
        "name": "Somnia",
        "id": "somnia",
        "fetcher": "blockscout",
        "explorer": "https://explorer.somnia.network",
        "native": "SOMI",
    },

    "2": {
        "name": "Ethereum",
        "id": "ethereum",
        "fetcher": "etherscan",
        "api": "https://api.etherscan.io/v2/api",
        "chainid": "1",
        "apikey": ETHERSCAN_API_KEY,
        "native": "ETH",
    },

    "3": {
        "name": "Base",
        "id": "base",
        "fetcher": "etherscan",
        "api": "https://api.etherscan.io/v2/api",
        "chainid": "8453",
        "apikey": ETHERSCAN_API_KEY,
        "native": "ETH",
    },

    "4": {
        "name": "Arbitrum",
        "id": "arbitrum",
        "fetcher": "etherscan",
        "api": "https://api.etherscan.io/v2/api",
        "chainid": "42161",
        "apikey": ETHERSCAN_API_KEY,
        "native": "ETH",
    },

    "5": {
        "name": "Optimism",
        "id": "optimism",
        "fetcher": "etherscan",
        "api": "https://api.etherscan.io/v2/api",
        "chainid": "10",
        "apikey": ETHERSCAN_API_KEY,
        "native": "ETH",
    },

    "6": {
        "name": "Polygon",
        "id": "polygon",
        "fetcher": "etherscan",
        "api": "https://api.etherscan.io/v2/api",
        "chainid": "137",
        "apikey": ETHERSCAN_API_KEY,
        "native": "MATIC",
    },

    "7": {
        "name": "BNB Smart Chain",
        "id": "bsc",
        "fetcher": "etherscan",
        "api": "https://api.etherscan.io/v2/api",
        "chainid": "56",
        "apikey": ETHERSCAN_API_KEY,
        "native": "BNB",
    },
}
