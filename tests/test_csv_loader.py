from pipeline.csv_loader import load_csv

rows = load_csv("data/ledger.csv")

assert isinstance(rows, list)
assert len(rows) > 0

print(f"Loaded {len(rows)} rows.")
print("CSV loader passed.")
