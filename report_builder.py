import os
import pandas as pd

def analyze_csv(filepath: str, delimiter: str):
    if not os.path.exists(filepath):
        print(f"File: {filepath} doesn't exist!")
        os._exit(1)

    df = pd.read_csv(filepath, delimiter=delimiter)

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

    columns_with_missing = (missing_df["missing_count"] > 0).sum()  

    # Initializaion of warning list
    # It'll potentially contain bullet-points warnings about data 
    warnings = []

    duplicated_rows = df.duplicated(keep='first').sum()
    duplicated_rows_pct = (duplicated_rows / rows) * 100 

    if duplicated_rows > 0:
        warnings.append(f"Duplicated rows detected: {duplicated_rows} ({duplicated_rows_pct}%) ❗")
    else:
        warnings.append("No duplicate rows detected ✅")
    
    if columns_with_missing > 0:
        warnings.append(f"{columns_with_missing} columns have missing values.")
        worst_column = missing_df.sort_values("missing_count", ascending=False).index[0]
        warnings.append(f"Worst column(highest missing %) is: {worst_column} with {missing_df.sort_values("missing_count", ascending=False)["missing_count"][0]}% ❗")
    else: 
        warnings.append("No missing values detected in any columns ✅")

    return (
        rows,
        cols,
        df.head(),
        missing_df.reset_index().rename(columns={"index": "column"}),
        total_missing_cells,
        overall_missing_pct,
    )
