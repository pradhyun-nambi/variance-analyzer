import pandas as pd


def _month_name(m):
    return pd.Period(m).strftime("%B")


def _money(x):
    return f"${abs(x):,.0f}"


def generate_commentary(df):
    """Turn calculated variances into plain-English bullets.
    Expects columns from add_variance + flag_material."""
    bullets = []

    # Overall net result (revenue variance minus expense variance)
    have_actual = df.dropna(subset=["variance"])
    if not have_actual.empty:
        rev = have_actual.loc[have_actual["type"] == "revenue", "variance"].sum()
        exp = have_actual.loc[have_actual["type"] == "expense", "variance"].sum()
        net = rev - exp
        if net == 0:
            bullets.append("Net result was exactly on budget across the months shown.")
        else:
            word = "favorable" if net > 0 else "unfavorable"
            bullets.append(
                f"Net result was {_money(net)} {word} to budget across the months "
                f"shown (rows with actuals only)."
            )

    # Flagged items, biggest dollar impact first
    flagged = df[df["flagged"]].copy()
    flagged["abs_var"] = flagged["variance"].abs()
    for _, r in flagged.sort_values("abs_var", ascending=False).iterrows():
        month = _month_name(r["month"])
        if r["budget"] == 0:
            bullets.append(
                f"{r['line_item']} was {_money(r['variance'])} against a $0 budget "
                f"in {month} ({r['status']})."
            )
        else:
            direction = "over" if r["variance"] > 0 else "under"
            bullets.append(
                f"{r['line_item']} was {_money(r['variance'])} "
                f"({abs(r['variance_pct']):.1f}%) {direction} budget in {month} "
                f"({r['status']})."
            )
    if flagged.empty:
        bullets.append("No items exceeded the materiality thresholds.")

    # Data gaps
    for _, r in df[df["status"] == "missing"].iterrows():
        bullets.append(
            f"No actual recorded for {r['line_item']} in {_month_name(r['month'])}; "
            f"excluded from totals."
        )
    return bullets