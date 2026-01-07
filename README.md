# 📊 Automated Exploratory Data Analysis (EDA) Report Generator

A Python tool that automatically analyzes tabular datasets (CSV) and generates a clean, readable **HTML Exploratory Data Analysis (EDA) report** with data-quality warnings and visualizations.

The goal of this project is to **save analyst time** by automating repetitive EDA tasks while keeping the output interpretable, lightweight, and easy to share.

---

## 🖼 Example Output

> _Screenshots of a generated report_

![EDA Report Screenshot](docs/ss1.png)
![EDA Report Screenshot](docs/ss2.png)
![EDA Report Screenshot](docs/ss3.png)


---

## ✨ Features

### Data overview
- Number of rows and columns
- Preview of the first rows of the dataset

### Missing values analysis
- Per-column missing counts and percentages
- Overall missing percentage
- Bar chart showing columns with the highest missingness

### Data-quality warnings
Automatically detects and reports:
- Duplicate rows
- Columns containing missing values
- Constant columns (no variance)
- High-cardinality **ID-like** columns
- High-cardinality **email-like** columns (heuristic-based)

### Numeric distributions
- Automatically selects up to **3 most informative numeric columns**
- Generates histograms based on variance (standard deviation)
- Skips categorical-like numeric columns

### Output
- Clean, responsive **HTML report**
- Embedded plots (PNG)
- No external dependencies required to view the report

---

## 🚀 How to run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

Generate a report from a CSV file:

```bash
python main.py path/to/data.csv
```

Optional arguments:

```bash
python main.py path/to/data.csv output/report.html ","
```

**Arguments**
- `path/to/data.csv` – input dataset  
- `output/report.html` – output HTML file (optional, default: `output/report.html`)  
- `,` – CSV delimiter (optional, default: comma)

Open the generated report in a browser:

```bash
open output/report.html
# or
xdg-open output/report.html
```

---

## 🧠 Design decisions

### Why HTML reports?
HTML reports are portable, easy to share, and require no backend or additional tooling.  
They can be opened in any modern browser and work well for both technical and non-technical stakeholders.

### Why heuristic-based warnings?
Instead of relying on column names, the tool analyzes data characteristics such as:
- uniqueness ratio
- number of non-null values
- value patterns (for example, email validation)

This makes the analysis robust across datasets with unknown or inconsistent schemas.

### Why limit the number of plots?
To keep reports readable and focused, only the most informative visualizations are shown:
- a missingness bar chart for columns with missing data
- up to **three numeric histograms** selected based on variance (standard deviation)

This avoids overwhelming the reader while still highlighting important structure in the data.
