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
    explorer = None

    for c in CHAINS.values():
        if c["id"] == chain:
            explorer = c["explorer"]
            break

    if explorer is None:
        raise Exception(f"Unsupported chain: {chain}")

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

        with open(f"data/{name}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    print("Download complete.")
