from collections import defaultdict

from models.transaction import Transaction
from models.event import Event


class Normalizer:
    def __init__(self, chain, wallet):
        self.chain = chain
        self.wallet = wallet

    def build_transactions(self, rows):
        groups = defaultdict(list)

        for row in rows:
            tx_hash = row.get("hash")
            if tx_hash:
                groups[tx_hash].append(row)

        transactions = []

        for tx_hash, group in groups.items():
            first = group[0]

            tx = Transaction(
                hash=tx_hash,
                chain=self.chain,
                wallet=self.wallet,
                timestamp=int(first.get("timeStamp", 0)),
                block_number=int(first.get("blockNumber", 0)),
            )

            for row in group:
                event = Event(
                    event_type="RAW",
                    asset=row.get("tokenSymbol") or "NATIVE",
                    amount=row.get("tokenValue") or row.get("value") or "0",
                    sender=row.get("from"),
                    receiver=row.get("to"),
                    contract=row.get("contractAddress"),
                    token_id=row.get("tokenID"),
                )

                tx.add_event(event)

            transactions.append(tx)

        return transactions
