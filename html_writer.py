# html_writer.py
import os

from html import escape

def load_css(path="assets/style.css") -> str:
    try:
        with open(path, 'r', encoding="utf-8") as f:
            return f"<style>\n{f.read()}\n</style>"
    except FileNotFoundError:
        return ""

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
):
    
    css_block = load_css()
    
    dirpath = os.path.dirname(output_file)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    
    # Decide what to show in the Missing Values section
    if total_missing_cells == 0:
        missing_section_html = """
        <p><strong>No missing values detected.</strong></p>
        """
    else:
        missing_section_html = (
            missing_df
            .sort_values("missing_count", ascending=False)
            .to_html(index=False)
        )
    
    # Warnings section
    warnings_items = [f"<li>{escape(str(w))}</li>" for w in warnings]
    warnings_section_html = "\n".join(warnings_items)
    

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"""
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
{css_block}
</head>
<body>
  <div class="container">
    <header>
      <h1>EDA Report | {os.path.basename(filepath)}</h1>
      <p class="subtitle">Generated from <code>{os.path.basename(filepath)}</code></p>
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
""")
