# Imports
import sys
import os

from report_builder import analyze_csv
from html_writer import write_html

filepath = sys.argv[1]
rows, cols, prewiev_table_html = analyze_csv(filepath)

write_html(filepath, rows, cols, prewiev_table_html)