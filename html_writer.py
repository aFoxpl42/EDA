# html_writer.py
import os
from html import escape


def load_css(path="assets/style.css") -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f"<style>\n{f.read()}\n</style>"
    except FileNotFoundError:
        return ""


def _relpath_for_html(img_path: str, html_output_path: str) -> str:
    if not img_path:
        return ""
    html_dir = os.path.dirname(os.path.abspath(html_output_path)) or os.getcwd()
    img_abs = os.path.abspath(img_path)
    return os.path.relpath(img_abs, start=html_dir)


def write_html(
    filepath: str,
    rows: int,
    cols: int,
    preview_df,
    missing_df,
    total_missing_cells: int,
    overall_missing_pct: float,
    warnings: list[str],
    output_file="output/report.html",
    missingness_plot_path: str = "",
    histogram_plot_paths: list[str] | None = None,
):
    if histogram_plot_paths is None:
        histogram_plot_paths = []

    css_block = load_css()

    dirpath = os.path.dirname(output_file)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)

    # Missing values section
    if total_missing_cells == 0:
        missing_section_html = "<p><strong>No missing values detected.</strong></p>"
    else:
        missing_section_html = missing_df.sort_values(
            "missing_count", ascending=False
        ).to_html(index=False)

    # Warnings section
    warnings_items = [f"<li>{escape(str(w))}</li>" for w in warnings]
    warnings_section_html = "\n".join(warnings_items)

    # Visual Overview: Missingness image
    if missingness_plot_path:
        rel_missing = _relpath_for_html(missingness_plot_path, output_file)
        missing_img_html = f"""
        <img src="{escape(rel_missing)}" alt="Missingness bar chart"
             style="max-width:100%; height:auto; border:1px solid #e5e7eb; border-radius:10px; padding:8px; background:#fff;" />
        """
    else:
        missing_img_html = (
            "<p class='note'>No missingness plot generated (no missing values).</p>"
        )

    # Visual Overview: Histogram images
    if histogram_plot_paths:
        hist_imgs = []
        for p in histogram_plot_paths:
            rel_hist = _relpath_for_html(p, output_file)
            hist_imgs.append(
                f"""<img src="{escape(rel_hist)}" alt="Histogram"
                        style="max-width:100%; height:auto; border:1px solid #e5e7eb; border-radius:10px; padding:8px; background:#fff; margin-top:10px;" />"""
            )
        hist_imgs_html = "\n".join(hist_imgs)
    else:
        hist_imgs_html = "<p class='note'>No numeric histograms generated (no suitable numeric columns).</p>"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(
            f"""
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
{css_block}
</head>
<body>
  <div class="container">
    <header>
      <h1>EDA Report | {escape(os.path.basename(filepath))}</h1>
      <p class="subtitle">Generated from <code>{escape(os.path.basename(filepath))}</code></p>
    </header>

    <div class="grid">
      <div class="card">
        <div class="label">Rows</div>
        <div class="value">{rows}</div>
      </div>
      <div class="card">
        <div class="label">Columns</div>
        <div class="value">{cols}</div>
      </div>
    </div>

    <div class="section">
      <h2>Visual Overview</h2>

      <h3>Missingness</h3>
      <p class="note">Top columns by missing percentage</p>
      {missing_img_html}

      <h3 style="margin-top:18px;">Numeric Distributions</h3>
      <p class="note">Up to 3 numeric columns with the highest standard deviation</p>
      {hist_imgs_html}
    </div>

    <div class="section">
      <h2>Warnings</h2>
      <div class="warnings">
        <ul>
          {warnings_section_html}
        </ul>
      </div>
    </div>

    <div class="section">
      <h2>Preview</h2>
      <p class="note">First rows of the dataset</p>
      {preview_df.to_html(index=False)}
    </div>

    <div class="section">
      <h2>Missing Values</h2>
      <p class="small">Total missing cells: <strong>{total_missing_cells}</strong></p>
      <p class="small">Overall missing %: <strong>{overall_missing_pct:.2f}%</strong></p>
      {missing_section_html}
    </div>
  </div>
</body>
</html>
"""
        )
