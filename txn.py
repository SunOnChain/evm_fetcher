import os
from fetch import fetch

print("=" * 40)
print("TXN v0.4")
print("=" * 40)

wallet = input("\nWallet Address: ").strip()

from config import CHAINS

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

print("\nFetching...")
fetch(chain, wallet)

print("\nNormalizing...")
os.system("python normalize.py")

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
