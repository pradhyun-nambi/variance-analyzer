import pandas as pd
import pytest
from src.variance import add_variance, flag_material


def make(type_, budget, actual):
    return pd.DataFrame(
        [{"month": "2026-04", "line_item": "X", "type": type_,
          "budget": budget, "actual": actual}]
    )


def test_expense_over_budget_is_unfavorable():
    df = add_variance(make("expense", 100, 150))
    assert df.loc[0, "variance"] == 50
    assert df.loc[0, "variance_pct"] == pytest.approx(50)
    assert df.loc[0, "status"] == "unfavorable"


def test_expense_under_budget_is_favorable():
    df = add_variance(make("expense", 50, 35))
    assert df.loc[0, "status"] == "favorable"


def test_revenue_under_budget_is_unfavorable():
    df = add_variance(make("revenue", 2500, 1875))
    assert df.loc[0, "variance"] == -625
    assert df.loc[0, "status"] == "unfavorable"


def test_revenue_over_budget_is_favorable():
    df = add_variance(make("revenue", 975, 1300))
    assert df.loc[0, "status"] == "favorable"


def test_on_budget():
    df = add_variance(make("expense", 60, 60))
    assert df.loc[0, "status"] == "on budget"


def test_zero_budget_gives_blank_percent():
    df = add_variance(make("expense", 0, 40))
    assert pd.isna(df.loc[0, "variance_pct"])


def test_missing_actual():
    df = add_variance(make("expense", 60, float("nan")))
    assert df.loc[0, "status"] == "missing"


def test_small_percent_big_dollars_not_flagged_with_and():
    # the 3% / $600 example
    df = flag_material(add_variance(make("expense", 20000, 20600)))
    assert not df.loc[0, "flagged"]


def test_small_percent_big_dollars_flagged_with_or():
    df = flag_material(add_variance(make("expense", 20000, 20600)), mode="or")
    assert df.loc[0, "flagged"]


def test_big_percent_small_dollars_not_flagged_with_and():
    # the 40% / $400 example
    df = flag_material(add_variance(make("expense", 1000, 1400)))
    assert not df.loc[0, "flagged"]


def test_zero_budget_small_amount_not_flagged():
    df = flag_material(add_variance(make("expense", 0, 40)))
    assert not df.loc[0, "flagged"]


def test_zero_budget_large_amount_flagged():
    df = flag_material(add_variance(make("expense", 0, 900)))
    assert df.loc[0, "flagged"]