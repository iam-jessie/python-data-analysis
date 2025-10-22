# ✨ Equity Fund Financial Analysis

This project contains a Python script for cleaning and analyzing the financial performance of 150 U.S. companies from a quarterly dataset. The program was developed to aid an investment company in rebalancing its equity fund holdings by providing clear, data-driven insights.

---

## 💎 Core Features

This script automates a full data analysis workflow, performing several key tasks:

* **Data Loading & Validation:** Imports the dataset from a CSV file and performs a validation check to identify and report any duplicate records.
* **State-Level Statistics:** Groups all companies by state and calculates descriptive statistics (mean, median, min, max) for all numeric variables to reveal regional trends.
* **Conditional Filtering:** Filters the dataset to isolate and display all companies with a negative debt-to-equity ratio, flagging them for further review.
* **Feature Engineering:** Computes a new 'Debt-to-Income Ratio' for each company using existing financial data.
* **Robust Error Handling:** Safely handles potential division-by-zero errors during the ratio calculation by assigning `NaN` (Not a Number) where a company's revenue is zero, ensuring computational integrity.
* **Data Concatenation:** Merges the newly calculated ratio with the original dataset to produce a final, augmented data frame for comprehensive analysis.

---

## 🛠️ Requirements

To run this script, your environment must be configured with the following:

* **Python 3**
* **pandas** library
* **numpy** library

You can install these dependencies using the following command in your terminal:

```bash
pip install pandas
pip install numpy
```
