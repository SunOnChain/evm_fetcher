import csv
from collections import defaultdict

INPUT = "ledger.csv"
OUTPUT = "ledger_analyzed.csv"


def classify(rows):
    """
    Placeholder classifier.
    Returns a transaction type.
    """
    return "UNKNOWN"


groups = defaultdict(list)

with open(INPUT, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        groups[row["hash"]].append(row)


fieldnames = None

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = None

    for tx_hash, rows in groups.items():

        tx_type = classify(rows)

        for row in rows:

            row["type"] = tx_type

            if writer is None:
                fieldnames = list(row.keys())
                writer = csv.DictWriter(
                    f,
                    fieldnames=fieldnames
                )
                writer.writeheader()

            writer.writerow(row)

print(f"Done. {len(groups)} transactions analyzed.")
