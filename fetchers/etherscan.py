import json
import os
import urllib.parse
import urllib.request

ENDPOINTS = {
    "transactions": "txlist",
    "internal": "txlistinternal",
    "erc20": "tokentx",
    "erc721": "tokennfttx",
    "erc1155": "token1155tx",
}


def fetch(chain, address):
    wallet_dir = f"data/wallets/{address.lower()}"
    os.makedirs(wallet_dir, exist_ok=True)

    for filename, action in ENDPOINTS.items():
        params = {
            "chainid": chain["chainid"],
            "module": "account",
            "action": action,
            "address": address,
            "sort": "asc",
        }

        if chain["apikey"]:
            params["apikey"] = chain["apikey"]

        url = f"{chain['api']}?{urllib.parse.urlencode(params)}"

        print(f"Downloading {filename}...")

        with urllib.request.urlopen(url) as r:
            data = json.loads(r.read().decode())

        with open(
            f"{wallet_dir}/{filename}.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(data, f, indent=2)

    print("Download complete.")
