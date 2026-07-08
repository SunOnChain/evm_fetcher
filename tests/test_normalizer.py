from pipeline.normalizer import Normalizer

rows = [
    {
        "hash": "0xabc",
        "blockNumber": "100",
        "timeStamp": "123456",
    },
    {
        "hash": "0xabc",
        "blockNumber": "100",
        "timeStamp": "123456",
    },
    {
        "hash": "0xdef",
        "blockNumber": "101",
        "timeStamp": "123457",
    },
]

normalizer = Normalizer(
    chain="ethereum",
    wallet="0xwallet",
)

txs = normalizer.build_transactions(rows)

assert len(txs) == 2
assert txs[0].hash == "0xabc"
assert txs[1].hash == "0xdef"

print("Normalizer tests passed.")
