"""Generates SYNTHETIC budget and actuals data for a hypothetical
photography business. Not real financial data."""
import csv
from pathlib import Path

MONTHS = ["2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"]

# (line_item, type, monthly_budget, actuals per month; None = missing)
LINES = [
    ("Shoot fees - standard", "revenue", 2500, [2500, 2500, 2500, 2500, 1875, 2500]),
    ("Shoot fees - rush",     "revenue",  975, [975, 1300, 975, 975, 975, 975]),
    ("Software",              "expense",   50, [50, 50, 50, 35, 35, 35]),
    ("Marketing",             "expense",    0, [0, 0, 40, 0, 0, 0]),
    ("Travel",                "expense",  100, [100, 100, 100, 105, 110, 115]),
    ("Equipment rental",      "expense",  350, [350, 1100, 350, 350, 350, 350]),
    ("Insurance",             "expense",   60, [60, 60, 60, 60, 60, None]),
]

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def write_csv(filename, rows):
    with open(DATA_DIR / filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["month", "line_item", "type", "amount"])
        writer.writerows(rows)


def main():
    DATA_DIR.mkdir(exist_ok=True)
    budget_rows, actual_rows = [], []
    for name, line_type, budget, actuals in LINES:
        for month, actual in zip(MONTHS, actuals):
            budget_rows.append([month, name, line_type, budget])
            if actual is not None:  # missing month = row left out on purpose
                actual_rows.append([month, name, line_type, actual])
    write_csv("budget.csv", budget_rows)
    write_csv("actuals.csv", actual_rows)
    print(f"Wrote {len(budget_rows)} budget rows and {len(actual_rows)} actual rows.")


if __name__ == "__main__":
    main()