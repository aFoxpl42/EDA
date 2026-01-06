import os
import pandas as pd

from report_builder import analyze_csv
from plots import miss_bar_chart, hist_plots
from html_writer import write_html


def test_full_report_generation_pipeline(tmp_path):
    # Arrange: create a small dataset with numeric cols + missing values
    df = pd.DataFrame(
        {
            "age": [20, 21, 22, None, 24, 25, 26, 27, 28, 29, 30],
            "bmi": [18.1, 22.5, 27.0, 30.2, None, 25.5, 26.1, 28.0, 29.3, 31.0, 33.2],
            "class": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            "email": [
                "a@example.com",
                "b@example.com",
                None,
                "d@example.com",
                "e@example.com",
                "f@example.com",
                "g@example.com",
                "h@example.com",
                "i@example.com",
                "j@example.com",
                "k@example.com",
            ],
        }
    )

    # Write CSV into temp dir
    csv_path = tmp_path / "sample.csv"
    df.to_csv(csv_path, index=False)

    # Output paths inside temp dir
    out_dir = tmp_path / "out"
    assets_dir = out_dir / "assets"
    report_path = out_dir / "report.html"

    # Act: run pipeline
    rows, cols, preview_df, missing_df, total_missing, overall_pct, warnings = (
        analyze_csv(df)
    )

    missing_plot = miss_bar_chart(missing_df, out_dir=assets_dir)
    hist_paths = hist_plots(df, out_dir=assets_dir)

    write_html(
        filepath=str(csv_path),
        rows=rows,
        cols=cols,
        preview_df=preview_df,
        missing_df=missing_df,
        total_missing_cells=total_missing,
        overall_missing_pct=overall_pct,
        warnings=warnings,
        output_file=str(report_path),
        missingness_plot_path=missing_plot,
        histogram_plot_paths=hist_paths,
    )

    # Assert: report created
    assert report_path.exists()

    html = report_path.read_text(encoding="utf-8")

    # Assert: report references at least one image (missingness OR histograms)
    assert "<img" in html

    # Assert: any returned plot files exist
    if missing_plot:
        assert os.path.exists(missing_plot)

    for p in hist_paths:
        assert os.path.exists(p)
