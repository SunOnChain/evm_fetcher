from pipeline.normalizer import Normalizer
from analyzers.engine import analyze


class Pipeline:
    def __init__(self, chain, wallet):
        self.normalizer = Normalizer(chain, wallet)

    def run(self, rows):
        transactions = self.normalizer.build_transactions(rows)

        for tx in transactions:
            analyze(tx)

        return transactions
