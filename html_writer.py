# html_writer.py
import os

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
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

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
    warnings_section_html = ""
    for warning in warnings:
         warnings_section_html += "<li>" + warning + '</li>\n'
    

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"""
<html><body>
<h1>EDA Report | {os.path.basename(filepath)}</h1>

<p>Rows: {rows}</p>
<p>Columns: {cols}</p>

<h2>Preview</h2>
{preview_df.to_html(index=False)}

<h2>Warnings</h2>
<ul>
{warnings_section_html}
</ul>

<h2>Missing Values</h2>
<p>Total missing cells: {total_missing_cells}</p>
<p>Overall missing %: {overall_missing_pct:.2f}%</p>

{missing_section_html}

</body></html>
""")
