# 📊 Equity Fund Quarterly Analysis

---

## 📜 Purpose & Audience

This repository contains a single analysis script, `D598_Analysis.py`, developed for a small investment firm that manages an equity fund composed of 150 U.S. companies.

The script is intended for **Fund Managers** and **Research Analysts** who need a quick, reproducible quarterly view of portfolio company performance across states and key financial ratios.

---

## 💎 What the Script Does

* **Loads the dataset** (Excel or CSV). The script looks for `D598 Data Set.xlsx` or a CSV fallback named `D598 Data Set.csv`.
* Reports basic dataset information and displays the first three records for **quick verification**.
* Detects and reports **duplicate rows**.
* Computes state-level **descriptive statistics** (mean, median, min, max) for all numeric variables.
* Identifies companies with **negative Debt-to-Equity ratios** for immediate review.
* Calculates a **Debt-to-Income ratio** per company, handling zero revenue safely by producing `NaN`.
* **Appends the new metric** back to the original dataset.

---

## 🛠️ Environment & Dependencies

* Python 3.8+
* pandas
* numpy

Install dependencies (PowerShell):

```
python -m pip install --upgrade pip; python -m pip install pandas numpy
```

---

## 🚀 How to Run (PowerShell)

1.  Place the data file (`D598 Data Set.xlsx` or the CSV fallback) into the project folder.
2.  From PowerShell, run:

```
python .\D598_Analysis.py
```

---

## 🔮 Assumptions & Notes

* The analysis assumes column names are consistent (e.g., `Business ID`, `Business State`, `Total Revenue`). If column names differ, the script will skip the relevant steps.
* Debt-to-Income is defined as `Total Long-term Debt / Total Revenue`. Rows with zero revenue have `NaN` for this ratio to avoid misleading infinite values.