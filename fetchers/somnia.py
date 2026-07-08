import json
import urllib.request
import os

ENDPOINTS = {
    "transactions": "txlist",
    "internal": "txlistinternal",
    "erc20": "tokentx",
    "erc721": "tokennfttx",
    "erc1155": "token1155tx",
}


def fetch(chain, address):
    explorer = chain["explorer"]

    wallet_dir = f"data/wallets/{address.lower()}"
    os.makedirs(wallet_dir, exist_ok=True)

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

        with open(f"{wallet_dir}/{name}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    print("Download complete.")
