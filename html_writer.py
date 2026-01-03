import os
import pandas as pd

def write_html(filepath:str, rows:int, cols:int, preview_table, missing_values ,output_file="output/report.html"):
    with open(output_file, 'w') as f:
        f.write(f"""
    <html><body>
    <h1>EDA Report</h1>
    <p>{os.path.basename(filepath)}</p>
    <p>Rows: {rows}</p>
    <p>Cols: {cols}</p>
    <p>Preview of table: </p>
    {preview_table.to_html()}
    <p>Missing values overview: </p>
    {missing_values.to_frame().to_html()}
    </body></html>""")