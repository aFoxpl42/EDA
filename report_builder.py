import os
import pandas as pd
import validators

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
    df_obj = df.select_dtypes(include=object)
    # per column metrics
    non_null_count_per_col = df_obj.count()
    unique_count_per_col = df_obj.nunique(0, dropna=True)
    # uniqueness ration per column
    unique_ratio = unique_count_per_col / non_null_count_per_col
    
    print(df_obj["Stock"].values[:200])

    likely_id = (
        unique_ratio[
            (unique_ratio >= 0.8) & # high uniquenesss
            (unique_count_per_col >= 20) & # enough data
            (non_null_count_per_col >= 20) # avoid tiny columns
        ]
        .index
        .to_list()
    )        
    
    email_like_columns = []
    id_like_columns = []
    
    for i in likely_id:
        email_like = 0
        sample = df_obj[i].dropna().astype(str).head(200)
        for j in sample:
            if validators.email(j.lower().strip()):
                email_like += 1
        if len(sample) > 0:
            email_like_score = email_like/len(sample)
            if email_like_score >= 0.6:
                email_like_columns.append(i)
            else:
                id_like_columns.append(i)
    
    return (
        rows,
        cols,
        df.head(),
        missing_df.reset_index().rename(columns={"index": "column"}),
        total_missing_cells,
        overall_missing_pct,
    )
