from pipeline.runner import Pipeline

rows = [
    {
        "hash": "0x1",
        "blockNumber": "100",
        "timeStamp": "1",
        "from": "0xwallet",
        "to": "0xabc",
        "value": "100",
    },
    {
        "hash": "0x1",
        "blockNumber": "100",
        "timeStamp": "1",
        "from": "0xdex",
        "to": "0xwallet",
        "tokenSymbol": "USDC",
        "tokenValue": "100",
    },
]

pipeline = Pipeline(
    chain="ethereum",
    wallet="0xwallet",
)

txs = pipeline.run(rows)

assert len(txs) == 1
assert txs[0].tx_type == "SWAP"

print("Pipeline test passed.")
