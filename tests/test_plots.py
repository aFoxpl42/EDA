import os
import pandas as pd

from plots import miss_bar_chart, hist_plots

def test_miss_bar_chart_returns_empty_when_no_missing(tmp_path):
    # missing_df structure expected by miss_bar_chart:
    # columns: column, missing_count, missing_pct
    missing_df = pd.DataFrame({
        "column": ["a", "b"],
        "missing_count": [0, 0],
        "missing_pct": [0.0, 0.0],
    })
    # If your function saves to output/assets hardcoded, it will ignore tmp_path.
    # Still: should return "" when no missing.
    out = miss_bar_chart(missing_df)
    assert out == ""

def test_miss_bar_chart_creates_file_when_missing_exists():
    missing_df = pd.DataFrame({
        "column": ["a", "b"],
        "missing_count": [1, 3],
        "missing_pct": [10.0, 30.0],
    })
    out = miss_bar_chart(missing_df)
    assert out != ""
    assert os.path.exists(out)

def test_hist_plots_returns_empty_when_no_numeric_cols():
    df = pd.DataFrame({
        "name": ["a", "b", "c"],
        "city": ["x", "y", "z"],
    })
    paths = hist_plots(df)
    assert paths == []

def test_hist_plots_creates_up_to_three_files():
    df = pd.DataFrame({
        "x": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        "y": [10, 20, 30, 25, 15, 5, 40, 35, 45, 50, 55],
        "z": [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
        "flag": [0, 1] * 5 + [0],  # likely categorical-like
    })
    paths = hist_plots(df)
    assert len(paths) <= 3
    for p in paths:
        assert os.path.exists(p)
