import json
import os
import sys

DATA_DIR = "data"
WALLETS_DIR = os.path.join(DATA_DIR, "wallets")

FILES = [
    "transactions",
    "internal",
    "erc20",
    "erc721",
    "erc1155",
]


def load_json(path):
    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        return data.get("result", [])

    return data


def save_json(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"status": "1", "result": rows}, f, indent=2)


for name in FILES:
    merged = []
    seen = set()

    for wallet in os.listdir(WALLETS_DIR):
        path = os.path.join(WALLETS_DIR, wallet, f"{name}.json")

        rows = load_json(path)

        if not isinstance(rows, list):
            print(f"{name}: result is {type(rows).__name__}")
            print(rows)
            sys.exit(1)

        for i, row in enumerate(rows):
            if not isinstance(row, dict):
                print(f"\nERROR in {path}")
                print(f"Row {i} is {type(row).__name__}")
                print(row)
                sys.exit(1)

            key = row.get("hash")

            if not key:
                merged.append(row)
                continue

            if key in seen:
                continue

            seen.add(key)
            merged.append(row)

    save_json(os.path.join(DATA_DIR, f"{name}.json"), merged)

    print(f"{name}: {len(merged)}")
