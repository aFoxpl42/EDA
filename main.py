import sys
import os

from report_builder import analyze_csv
from html_writer import write_html

def main() -> int:
    if len(sys.argv) != 4:
        print("Usage: python main.py <path_to_csv> <path_to_output> <delimiter>")
        return 1

    filepath = sys.argv[1]
    output_path = sys.argv[2]
    delimiter = sys.argv[3]

    if not os.path.exists(filepath):
        print(f"File '{filepath}' does not exist.")
        return 1

    rows, cols, preview_df, missing_df, total_missing_cells, overall_missing_pct = analyze_csv(filepath, delimiter)

    write_html(
        filepath=filepath,
        rows=rows,
        cols=cols,
        preview_df=preview_df,
        missing_df=missing_df,
        total_missing_cells=total_missing_cells,
        overall_missing_pct=overall_missing_pct,
        output_file=output_path,
    )

    print(f"Report generated: {output_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
