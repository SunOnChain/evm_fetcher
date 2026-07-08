import os
import shutil

from fetch import fetch
from config import CHAINS

print("=" * 40)
print("TXN v0.5")
print("=" * 40)

print("\nPaste wallet addresses (one per line).")
print("Press Enter on an empty line when finished.\n")

wallets = []

while True:
    wallet = input().strip()

    if wallet == "":
        break

    wallets.append(wallet)

if not wallets:
    print("No wallets entered.")
    exit()

print("\nChains")

for key, chain in CHAINS.items():
    print(f"{key}. {chain['name']}")

choice = input("\nSelect chain: ").strip()

if choice not in CHAINS:
    print("Invalid chain.")
    exit()

chain = CHAINS[choice]["id"]

print("\nExporter")
print("1. Cryptact")
print("2. Koinly")
print("3. Both")

exporter = input("\nSelect exporter: ").strip()

# Clear previous wallet cache
if os.path.exists("data/wallets"):
    shutil.rmtree("data/wallets")

os.makedirs("data/wallets", exist_ok=True)

print("\nFetching...")

for wallet in wallets:
    print(f"\n→ {wallet}")
    fetch(chain, wallet)

print("\nMerging...")
if os.system("python merge.py") != 0:
    exit(1)

print("\nNormalizing...")
if os.system("python normalize.py") != 0:
    exit(1)

if exporter == "1":
    os.system("python exporters/cryptact.py")

elif exporter == "2":
    os.system("python exporters/koinly.py")

elif exporter == "3":
    os.system("python exporters/cryptact.py")
    os.system("python exporters/koinly.py")

else:
    print("Invalid exporter.")
    exit()

print("\n✅ Done!")
print("Check the output/ folder.")
