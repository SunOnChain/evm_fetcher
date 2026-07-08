import json
import urllib.request

EXPLORER = "https://explorer.somnia.network"
ADDRESS = "0x64E5aDa896E70FA216dE47EFe132eb7Df10DD06E"

ENDPOINTS = {
    "transactions": "txlist",
    "internal": "txlistinternal",
    "erc20": "tokentx",
    "erc721": "tokennfttx",
    "erc1155": "token1155tx",
}

for name, action in ENDPOINTS.items():
    url = f"{EXPLORER}/api?module=account&action={action}&address={ADDRESS}"
    print("Downloading", name)

    with urllib.request.urlopen(url) as r:
        data = json.loads(r.read().decode())

    with open(f"{name}.json", "w") as f:
        json.dump(data, f, indent=2)

print("Done!")
