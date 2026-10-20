import pandas as pd

REQUIRED_COLUMNS = ["month", "line_item", "type", "amount"]
VALID_TYPES = {"revenue", "expense"}


def load_csv(path):
    """Read a budget or actuals CSV and validate it."""
    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    if df.empty:
        raise ValueError("File has no rows")
    bad_types = set(df["type"]) - VALID_TYPES
    if bad_types:
        raise ValueError(f"Invalid type values: {bad_types}")
    if df.duplicated(["month", "line_item"]).any():
        raise ValueError("Duplicate month/line_item rows found")
    df["amount"] = pd.to_numeric(df["amount"], errors="raise")
    return df


def combine(budget, actuals):
    """One row per budget line, with the actual next to it.
    If an actual is missing for a month, it shows up as NaN."""
    merged = budget.merge(
        actuals,
        on=["month", "line_item", "type"],
        how="left",
        suffixes=("_budget", "_actual"),
    )
    return merged.rename(columns={"amount_budget": "budget", "amount_actual": "actual"})