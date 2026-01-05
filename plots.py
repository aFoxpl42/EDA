import os
import pandas as pd

def miss_bar_chart(missing_df) -> str:
    output_directory = "output/assets/missingness.png"
    if len(missing_df) == 0:
        return ""
    df_filtered = missing_df[missing_df['missing_pct'] > 0]
    if len(df_filtered) == 0:
        return ""
    
    df_filtered_sorted = df_filtered.sort_values(by='missing_pct', ascending=False)
    
    if len(df_filtered_sorted) > 10:
        df_filtered_sorted = df_filtered_sorted.head(10)
    
    ax = df_filtered.plot.barh(x='column', y='missing_pct', rot=0)
    fig = ax.get_figure()
    dirpath = os.path.dirname(output_directory)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    fig.savefig(output_directory)
    
    return output_directory

def hist_plots(df) -> list[str]:
    df_numeric = df.select_dtypes(include='number')
    
    return []