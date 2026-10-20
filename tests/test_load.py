import pytest
from src.load import load_csv, combine

HEADER = "month,line_item,type,amount\n"


def write(tmp_path, text):
    p = tmp_path / "f.csv"
    p.write_text(text)
    return p


def test_missing_column(tmp_path):
    p = write(tmp_path, "month,line_item,amount\n2026-04,Software,50\n")
    with pytest.raises(ValueError):
        load_csv(p)


def test_empty_file(tmp_path):
    p = write(tmp_path, HEADER)
    with pytest.raises(ValueError):
        load_csv(p)


def test_bad_type(tmp_path):
    p = write(tmp_path, HEADER + "2026-04,Software,cost,50\n")
    with pytest.raises(ValueError):
        load_csv(p)


def test_duplicate_rows(tmp_path):
    p = write(tmp_path, HEADER + "2026-04,Software,expense,50\n2026-04,Software,expense,60\n")
    with pytest.raises(ValueError):
        load_csv(p)


def test_missing_actual_becomes_nan(tmp_path):
    b = write(tmp_path, HEADER + "2026-04,Insurance,expense,60\n2026-05,Insurance,expense,60\n")
    a = tmp_path / "a.csv"
    a.write_text(HEADER + "2026-04,Insurance,expense,60\n")
    merged = combine(load_csv(b), load_csv(a))
    assert len(merged) == 2
    assert merged["actual"].isna().sum() == 1