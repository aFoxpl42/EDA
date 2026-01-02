
def write_html(filepath:str, rows:int, cols:int, preview_table:str, output_file="output/report.html"):
    with open(output_file, 'w') as f:
        f.write(f"""
    <html><body>
    <h1>EDA Report</h1>
    <p>{filepath.split('/')[-1]}</p>
    <p>Rows: {rows}</p>
    <p>Cols: {cols}</p>
    {preview_table}
    </body></html>""")