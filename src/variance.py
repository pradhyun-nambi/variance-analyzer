import pandas as pd


def add_variance(df):
    """Add variance $, variance %, and a favorable/unfavorable status.
    Expects columns: type, budget, actual."""
    out = df.copy()
    out["variance"] = out["actual"] - out["budget"]

    # Budget of 0 would divide by zero, so make the % blank (NaN) instead
    safe_budget = out["budget"].where(out["budget"] != 0)
    out["variance_pct"] = out["variance"] / safe_budget * 100

    is_revenue = out["type"] == "revenue"
    is_expense = out["type"] == "expense"

    def status(row):
        if pd.isna(row["actual"]):
            return "missing"
        if row["variance"] == 0:
            return "on budget"
        if row["type"] == "revenue":
            return "favorable" if row["variance"] > 0 else "unfavorable"
        return "favorable" if row["variance"] < 0 else "unfavorable"

    out["status"] = out.apply(status, axis=1)
    return out


def flag_material(df, pct_threshold=10, dollar_threshold=500, mode="and"):
    """Flag variances big enough to matter.
    mode='and': must exceed BOTH thresholds. mode='or': either one."""
    out = df.copy()
    big_dollar = out["variance"].abs() > dollar_threshold

    big_pct = out["variance_pct"].abs() > pct_threshold
    # Zero budget with a real variance = infinite %, so count it as big
    unbudgeted = (out["budget"] == 0) & out["variance"].notna() & (out["variance"] != 0)
    big_pct = big_pct | unbudgeted

    out["flagged"] = (big_pct & big_dollar) if mode == "and" else (big_pct | big_dollar)
    return out