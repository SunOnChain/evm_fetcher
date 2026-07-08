import json
import urllib.request
import os

from config import CHAINS

ENDPOINTS = {
    "transactions": "txlist",
    "internal": "txlistinternal",
    "erc20": "tokentx",
    "erc721": "tokennfttx",
    "erc1155": "token1155tx",
}


def fetch(chain, address):
    chain_info = next(
        (c for c in CHAINS.values() if c["id"] == chain),
        None
    )

    if chain_info is None:
        raise Exception(f"Unsupported chain: {chain}")

    explorer = chain_info["explorer"]

    os.makedirs("data", exist_ok=True)

    for name, action in ENDPOINTS.items():
        url = (
            f"{explorer}/api"
            f"?module=account"
            f"&action={action}"
            f"&address={address}"
        )

        print(f"Downloading {name}...")

        with urllib.request.urlopen(url) as r:
            data = json.loads(r.read().decode())

        wallet_dir = f"data/wallets/{address.lower()}"
        os.makedirs(wallet_dir, exist_ok=True)

        with open(f"{wallet_dir}/{name}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    print("Download complete.")

    return {
        "transactions": json.load(open("data/transactions.json")),
        "internal": json.load(open("data/internal.json")),
        "erc20": json.load(open("data/erc20.json")),
        "erc721": json.load(open("data/erc721.json")),
        "erc1155": json.load(open("data/erc1155.json")),
    }
