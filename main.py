import sys
import os
import pandas as pd

from report_builder import analyze_csv
from html_writer import write_html
from plots import miss_bar_chart
from plots import hist_plots


def main() -> int:
    if len(sys.argv) < 2:
        print(
            "Usage: python main.py <path_to_csv> <path_to_output(default='output/report.html')> <delimiter(default=',')>"
        )
        return 1

    filepath = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "output/report.html"
    delimiter = sys.argv[3] if len(sys.argv) > 3 else ","

    if not os.path.exists(filepath):
        print(f"File '{filepath}' does not exist.")
        return 1

    df = pd.read_csv(filepath, delimiter=delimiter)

    try:
        (
            rows,
            cols,
            preview_df,
            missing_df,
            total_missing_cells,
            overall_missing_pct,
            warnings,
        ) = analyze_csv(df)
    except FileNotFoundError as e:
        print(e)
        return 1

    missingness_plot_path = miss_bar_chart(
        missing_df, "output/assets"
    )  # str ("" if none)
    histogram_plot_paths = hist_plots(df, "output/assets")  # list[str]

    write_html(
        filepath=filepath,
        rows=rows,
        cols=cols,
        preview_df=preview_df,
        missing_df=missing_df,
        total_missing_cells=total_missing_cells,
        overall_missing_pct=overall_missing_pct,
        warnings=warnings,
        output_file=output_path,
        missingness_plot_path=missingness_plot_path,
        histogram_plot_paths=histogram_plot_paths,
    )

    print(f"Report generated: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
