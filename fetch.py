import json
import urllib.request
import os

EXPLORERS = {
    "1": ("Somnia", "https://explorer.somnia.network"),
}

print("\nAvailable Chains")
print("----------------")
print("1. Somnia")

choice = input("\nSelect chain: ").strip()

if choice not in EXPLORERS:
    print("Invalid chain.")
    exit()

CHAIN, EXPLORER = EXPLORERS[choice]

ADDRESS = input("Wallet Address: ").strip()

if not ADDRESS:
    print("Wallet address required.")
    exit()

os.makedirs("data", exist_ok=True)

ENDPOINTS = {
    "transactions": "txlist",
    "internal": "txlistinternal",
    "erc20": "tokentx",
    "erc721": "tokennfttx",
    "erc1155": "token1155tx",
}

for name, action in ENDPOINTS.items():
    url = (
        f"{EXPLORER}/api"
        f"?module=account"
        f"&action={action}"
        f"&address={ADDRESS}"
    )

    print(f"Downloading {name}...")

    with urllib.request.urlopen(url) as r:
        data = json.loads(r.read().decode())

    with open(f"data/{name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

print("\nDone.")
