import os
import pandas as pd

def analyze_csv(filepath: str):
    if not os.path.exists(filepath):
        print(f"File: {filepath} doesn't exist!")
        os._exit(1)

    df = pd.read_csv(filepath, delimiter=',')

    rows, cols = df.shape

    # Per-column missing summary
    missing_df = (
        df.isna()
          .sum()
          .rename("missing_count")
          .to_frame()
    )
    missing_df["missing_pct"] = (missing_df["missing_count"] / rows) * 100

    # Overall missing stats
    total_missing_cells = int(missing_df["missing_count"].sum())
    total_cells = rows * cols
    overall_missing_pct = (total_missing_cells / total_cells) * 100 if total_cells else 0.0

    return (
        rows,
        cols,
        df.head(),
        missing_df.reset_index().rename(columns={"index": "column"}),
        total_missing_cells,
        overall_missing_pct,
    )
