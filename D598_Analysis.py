import os
import sys
import pandas as pd
import numpy as np


def main():
    # Try to find the dataset in the working directory. Prefer Excel, fall back to CSV.
    data_file_xlsx = "D598 Data Set.xlsx"
    data_file_csv = "D598 Data Set.csv"

    if os.path.exists(data_file_xlsx):
        data_path = data_file_xlsx
    elif os.path.exists(data_file_csv):
        data_path = data_file_csv
    else:
        print(f"ERROR: data file not found in working directory ({os.getcwd()}).")
        print("Expected one of:\n - D598 Data Set.xlsx\n - D598 Data Set.csv")
        sys.exit(2)

    try:
        if data_path.lower().endswith(('.xls', '.xlsx')):
            company_data = pd.read_excel(data_path)
        else:
            company_data = pd.read_csv(data_path)
    except Exception as exc:
        print(f"ERROR reading data file '{data_path}': {exc}")
        sys.exit(3)

    print("--- Initial Data Loaded ---")
    print(f"File: {data_path}")
    print(f"Rows: {len(company_data):,}, Columns: {company_data.shape[1]}")
    print("Columns:", list(company_data.columns))
    print(company_data.head(3).to_string(index=False))
    print("\n")

    # Check expected columns and warn if missing
    expected_cols = [
        'Business ID', 'Business State', 'Debt to Equity',
        'Total Revenue', 'Total Long-term Debt'
    ]
    missing = [c for c in expected_cols if c not in company_data.columns]
    if missing:
        print("WARNING: The following expected columns are missing from the dataset:", missing)

    # 2. Identify and display duplicate rows (if any)
    duplicate_rows = company_data[company_data.duplicated()]
    print("--- Duplicate Rows Found ---")
    if duplicate_rows.empty:
        print("No duplicate rows found.")
    else:
        print(duplicate_rows)
    print("\n")

    # 3. Group by state and calculate descriptive statistics for numeric columns
    if 'Business State' in company_data.columns:
        numeric_cols = company_data.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            state_summary = company_data.groupby('Business State')[numeric_cols].agg(['mean', 'median', 'min', 'max'])
            print("--- Descriptive Statistics by State (Sample) ---")
            print(state_summary.head())
        else:
            print("No numeric columns found for descriptive statistics by state.")
    else:
        print("Column 'Business State' not found; skipping state-level summary.")
    print("\n")

    # 4. Filter for businesses with negative debt-to-equity ratios
    if 'Debt to Equity' in company_data.columns:
        negative_debt_companies = company_data[company_data['Debt to Equity'] < 0]
        print("--- Companies with Negative Debt-to-Equity ---")
        if not negative_debt_companies.empty and 'Business ID' in company_data.columns:
            print(negative_debt_companies[['Business ID', 'Debt to Equity']].head())
        elif not negative_debt_companies.empty:
            print(negative_debt_companies[['Debt to Equity']].head())
        else:
            print("No companies found with negative Debt-to-Equity.")
    else:
        print("Column 'Debt to Equity' not found; skipping negative-debt filter.")
    print("\n")

    # 5. Create the debt-to-income ratio with error handling
    if 'Total Revenue' in company_data.columns and 'Total Long-term Debt' in company_data.columns:
        revenue = company_data['Total Revenue']
        debt = company_data['Total Long-term Debt']
        # avoid division by zero; where revenue == 0 or NaN, set NaN
        dti_ratio = np.where(revenue == 0, np.nan, debt / revenue)

        debt_to_income_df = pd.DataFrame({
            'Business ID': company_data['Business ID'] if 'Business ID' in company_data.columns else company_data.index,
            'Debt-to-Income Ratio': dti_ratio
        })
        print("--- New Debt-to-Income DataFrame (Sample) ---")
        print(debt_to_income_df.head())
    else:
        debt_to_income_df = None
        print("Required columns for Debt-to-Income calculation not found; skipping this step.")
    print("\n")

    # 6. Concatenate the new data frame with the original (if possible)
    if debt_to_income_df is not None and 'Business ID' in company_data.columns:
        final_data = pd.concat([
            company_data.set_index('Business ID'),
            debt_to_income_df.set_index('Business ID')
        ], axis=1).reset_index()

        display_cols = [c for c in ['Business ID', 'Business State', 'Debt-to-Income Ratio'] if c in final_data.columns]
        print("--- Final Augmented Data (Sample) ---")
        print(final_data[display_cols].head())
    else:
        print("Skipping concatenation - either Business ID is missing or Debt-to-Income wasn't computed.")
    print("\n")

    print("--- Analysis Complete ---")


if __name__ == '__main__':
    main()
