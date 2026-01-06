import os
import re
import matplotlib.pyplot as plt


def miss_bar_chart(missing_df) -> str:
    output_directory = "output/assets/missingness.png"
    if len(missing_df) == 0:
        return ""
    df_filtered = missing_df[missing_df["missing_pct"] > 0]
    if len(df_filtered) == 0:
        return ""

    df_filtered_sorted = df_filtered.sort_values(by="missing_pct", ascending=False)

    if len(df_filtered_sorted) > 10:
        df_filtered_sorted = df_filtered_sorted.head(10)

    ax = df_filtered.plot.barh(x="column", y="missing_pct", rot=0)
    fig = ax.get_figure()
    dirpath = os.path.dirname(output_directory)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    fig.savefig(output_directory)

    return output_directory


# Function that plots 3 numeric columns, chosen automatically based of standard deviation of them.


def hist_plots(df) -> list[str]:
    df_numeric = df.select_dtypes(include="number")
    if len(df_numeric) == 0:
        return []
    non_null_count_per_col = df_numeric.count()
    unique_count_per_col = df_numeric.nunique(axis=0, dropna=True)
    unique_ratio_per_col = unique_count_per_col / non_null_count_per_col

    columns_filtered = unique_ratio_per_col[
        (unique_count_per_col >= 10) & (unique_ratio_per_col >= 0.01)
    ].index.to_list()

    if len(columns_filtered) == 0:
        return []

    df_numeric_filtered = df_numeric[columns_filtered]
    if df_numeric_filtered.shape[1] >= 3:
        top_std = df_numeric_filtered.std().sort_values(ascending=False)[:3].dropna()
    else:
        top_std = df_numeric_filtered.std().sort_values(ascending=False).dropna()

    os.makedirs("output/assets", exist_ok=True)
    paths = []
    for i in range(len(top_std)):
        col = top_std.index[i]

        fig, ax = plt.subplots(figsize=(8, 4))
        df_numeric_filtered[col].dropna().plot(
            xlabel=col,
            ylabel="Frequency",
            grid=True,
            kind="hist",
            bins=30,
            ax=ax,
            title=f"Distribution: {col}",
        )
        fig.tight_layout()
        filename_safe_col = re.sub(r"\W+ ", "", col).replace(" ", "_")
        out_path = f"output/assets/hist_{filename_safe_col}.png"
        fig.savefig(out_path)
        plt.close(fig)
        paths.append(out_path)

    return paths
