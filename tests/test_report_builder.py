import pandas as pd

from report_builder import analyze_csv


def test_analyze_empty_df():
    df = pd.DataFrame()
    rows, cols, preview_df, missing_df, total_missing, overall_pct, warnings = (
        analyze_csv(df)
    )

    assert rows == 0
    assert cols == 0
    assert total_missing == 0
    assert overall_pct == 0
    assert isinstance(warnings, list)


def test_analyze_no_missing_values():
    df = pd.DataFrame(
        {
            "a": [1, 2, 3],
            "b": [10, 20, 30],
        }
    )
    rows, cols, preview_df, missing_df, total_missing, overall_pct, warnings = (
        analyze_csv(df)
    )

    assert total_missing == 0
    assert overall_pct == 0
    # missing_df has columns: column, missing_count, missing_pct
    assert (missing_df["missing_count"] == 0).all()
    assert (missing_df["missing_pct"] == 0).all()


def test_analyze_missing_values_counts_and_pct():
    df = pd.DataFrame(
        {
            "x": [1, None, 3, None],
            "y": [None, None, 5, 6],
        }
    )
    rows, cols, preview_df, missing_df, total_missing, overall_pct, warnings = (
        analyze_csv(df)
    )

    assert rows == 4
    assert cols == 2
    assert total_missing == 4  # x has 2, y has 2
    # check per-column missing counts
    by_col = dict(zip(missing_df["column"], missing_df["missing_count"]))
    assert by_col["x"] == 2
    assert by_col["y"] == 2
    # overall pct = total missing / (rows*cols) * 100 = 4 / 8 * 100 = 50 (%)
    assert overall_pct == 50.0


def test_duplicates_warning_present_when_duplicates_exist():
    df = pd.DataFrame(
        {
            "a": [1, 1, 2],
            "b": [10, 10, 20],
        }
    )
    *_, warnings = analyze_csv(df)
    # at least one warning should mention duplicates
    assert any("duplicate" in w.lower() for w in warnings)


def test_constant_column_detected():
    df = pd.DataFrame(
        {
            "const": [5, 5, 5, 5],
            "var": [1, 2, 3, 4],
        }
    )
    *_, warnings = analyze_csv(df)
    assert any("constant" in w.lower() for w in warnings)
