import pandas as pd
from src.variance import add_variance, flag_material
from src.commentary import generate_commentary


def build(rows):
    df = pd.DataFrame(rows, columns=["month", "line_item", "type", "budget", "actual"])
    return flag_material(add_variance(df))


def test_expense_over_budget_bullet():
    df = build([["2026-05", "Equipment rental", "expense", 350, 1100]])
    text = " ".join(generate_commentary(df))
    assert "Equipment rental" in text
    assert "$750" in text
    assert "214.3%" in text
    assert "May" in text
    assert "unfavorable" in text


def test_zero_budget_bullet():
    df = build([["2026-06", "Marketing", "expense", 0, 900]])
    text = " ".join(generate_commentary(df))
    assert "$0 budget" in text


def test_missing_actual_noted():
    df = build([["2026-09", "Insurance", "expense", 60, float("nan")]])
    text = " ".join(generate_commentary(df))
    assert "No actual recorded for Insurance" in text
    assert "September" in text


def test_net_result_hand_calculated():
    # revenue -625, expense +750 -> net = -625 - 750 = -1375 (unfavorable)
    df = build([
        ["2026-08", "Shoot fees - standard", "revenue", 2500, 1875],
        ["2026-05", "Equipment rental", "expense", 350, 1100],
    ])
    first = generate_commentary(df)[0]
    assert "$1,375" in first
    assert "unfavorable" in first