import json

from pipeline.runner import Pipeline


def load(name):
    with open(f"tests/fixtures/somnia/{name}.json", encoding="utf-8") as f:
        return json.load(f)["result"]


rows = []
rows.extend(load("transactions"))
rows.extend(load("internal"))
rows.extend(load("erc20"))
rows.extend(load("erc721"))
rows.extend(load("erc1155"))

pipeline = Pipeline(
    chain="somnia",
    wallet="0x64E5aDa896E70FA216dE47EFe132eb7Df10DD06E",
)

txs = pipeline.run(rows)

assert len(txs) > 0

print(f"Transactions: {len(txs)}")
print("Fixture pipeline passed.")
