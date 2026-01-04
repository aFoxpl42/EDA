import os
import pandas as pd

def analyze_csv(filepath: str, delimiter: str):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File: '{filepath}' doesn't exist")

    df = pd.read_csv(filepath, delimiter=delimiter)

    rows, cols = df.shape

    # Per-column missing summary
    missing_df = (
        df.isna()
          .sum()
          .rename("missing_count")
          .to_frame()
    )
    missing_df["missing_pct"] = (missing_df["missing_count"] / rows) * 100 if rows > 0 else 0

    # Overall missing stats
    total_missing_cells = int(missing_df["missing_count"].sum())
    total_cells = rows * cols
    overall_missing_pct = (total_missing_cells / total_cells) * 100 if total_cells else 0.0

    columns_with_missing = (missing_df["missing_count"] > 0).sum()  

    # Initializaion of warning list
    # It'll potentially contain bullet-points warnings about data 
    warnings = []

    duplicated_rows = df.duplicated(keep='first').sum() 
    duplicated_rows_pct = (duplicated_rows / rows) * 100 if rows > 0 else 0.0

    if duplicated_rows > 0:
        warnings.append(f"Duplicated rows detected: {duplicated_rows} ({duplicated_rows_pct}%) ❗")
    else:
        warnings.append("No duplicate rows detected ✅")
    
    if columns_with_missing > 0:
        warnings.append(f"{columns_with_missing} columns have missing values.")
        sorted_by_missing_pct = missing_df.sort_values("missing_pct", ascending=False)
        worst_column = sorted_by_missing_pct.index[0]
        warnings.append(f"Worst column(highest missing %) is: {worst_column} with {sorted_by_missing_pct['missing_pct'].iloc[0]}% ❗")
    else: 
        warnings.append("No missing values detected in any columns ✅")

    const_columns = list(df.columns[df.nunique() <=1].values)
    
    if len(const_columns) > 0 and len(const_columns) < 10:
        warnings.append(f"Constant columns: {const_columns} ❗")
    elif len(const_columns) >= 10:
        const_columns_first_10 = const_columns[:10]
        const_columns_first_10.append("and more....")
        warnings.append(f"Constant columns: {const_columns_first_10} ❗")
    else:
        warnings.append(f"No constant columns detected.")
    
    likely_id = []
    if rows > 20:
        df_obj = df.select_dtypes(include=object)
        for k,v in df_obj.count().items() :
            if v == 0:
                continue
            unique_ratio = df_obj.nunique(0, dropna=True).loc[str(k)] / v
            if unique_ratio >= 0.8 and df_obj.nunique(0, dropna=True).loc[str(k)] >= 20:
                likely_id.append(str(k))
        if len(likely_id) >= 10:
            likely_id_first_10 = likely_id[:10]
            likely_id_first_10.append("and more...")
            for i in likely_id_first_10:
                warnings.append(i)
        elif len(likely_id) < 10 and len(likely_id) > 0:
            for i in likely_id:
                warnings.append(i)
        
    
    return (
        rows,
        cols,
        df.head(),
        missing_df.reset_index().rename(columns={"index": "column"}),
        total_missing_cells,
        overall_missing_pct,
    )
