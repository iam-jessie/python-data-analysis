import os
import sys
import pandas as pd
import numpy as np

# --- Set display options for printing ---
pd.set_option('display.float_format', '{:,.2f}'.format)
pd.set_option('display.width', 120)


def print_header(title):
    """Helper function to print a consistent, centered header."""
    header = f" {title.upper()} "
    print("\n\n" + "="*80)
    print(header.center(80, ' '))
    print("="*80)


def main():
    # --- File Loading Logic ---
    data_file_xlsx = "D598 Data Set.xlsx"
    data_file_csv = "D598 Data Set.csv"

    if os.path.exists(data_file_xlsx):
        data_path = data_file_xlsx
    elif os.path.exists(data_file_csv):
        data_path = data_file_csv
    else:
        print(f"ERROR: Data file not found in working directory ({os.getcwd()}).")
        sys.exit(2)

    try:
        if data_path.lower().endswith('.csv'):
            company_data = pd.read_csv(data_path)
        else:
            company_data = pd.read_excel(data_path)
    except Exception as exc:
        print(f"ERROR reading data file '{data_path}': {exc}")
        sys.exit(3)
    
    # --- 1. Initial Data Summary ---
    print_header("Initial Data Summary")
    print(f"Successfully loaded from: {data_path}")
    print(f"Dimensions: {len(company_data):,} rows, {company_data.shape[1]} columns")
    print("\nInitial records displayed (first 3 rows):")
    print(company_data.head(3).to_string())
    

    # --- 2. Duplicate Row Check ---
    print_header("Duplicate Row Check")
    duplicate_rows = company_data[company_data.duplicated()]
    if duplicate_rows.empty:
        print("Result: No duplicate rows found.")
    else:
        print(f"Result: Found {len(duplicate_rows)} duplicate rows.")
        print(duplicate_rows.to_string())


    # --- 3. Descriptive Statistics by State ---
    print_header("Descriptive Statistics by State")
    if 'Business State' in company_data.columns:
        numeric_cols = company_data.select_dtypes(include=[np.number]).columns.tolist()
        if not numeric_cols:
            print("No numeric columns found to aggregate; skipping state-level statistics.")
            state_summary = pd.DataFrame()
        else:
            state_summary_raw = company_data.groupby('Business State')[numeric_cols].agg(['mean', 'median', 'min', 'max'])
            state_summary_raw.columns = [f"{col}_{stat}" for col, stat in state_summary_raw.columns]
            state_summary = state_summary_raw.reset_index()

            preferred = [
                'Business State',
                'Total Revenue_mean',
                'Profit Margin_mean',
                'Total Long-term Debt_mean',
                'Debt to Equity_mean'
            ]

            display_columns = [c for c in preferred if c in state_summary.columns]

            if len(display_columns) <= 1:
                mean_cols = [c for c in state_summary.columns if c.endswith('_mean')]
                display_columns = ['Business State'] + mean_cols[:4]

            human_readable_summary = state_summary[display_columns].copy()

            for col in human_readable_summary.columns:
                if col != 'Business State':
                    human_readable_summary[col] = human_readable_summary[col].round(2)

            rename_map = {}
            for col in human_readable_summary.columns:
                if col == 'Business State':
                    rename_map[col] = 'State'
                else:
                    parts = col.rsplit('_', 1)
                    if len(parts) == 2:
                        rename_map[col] = f"{parts[0]} ({parts[1]})"
                    else:
                        rename_map[col] = col
            human_readable_summary = human_readable_summary.rename(columns=rename_map)

            print("State-level statistics (first 5 records shown):")
            print(human_readable_summary.head(5).to_string(index=False))
    else:
        print("Column 'Business State' not found; skipping state-level summary.")
    

    # --- 4. Companies with Negative Debt-to-Equity ---
    print_header("Companies with Negative Debt-to-Equity")
    if 'Debt to Equity' in company_data.columns:
        negative_debt_companies = company_data[company_data['Debt to Equity'] < 0]
        print(f"Result: Found {len(negative_debt_companies)} companies with negative Debt-to-Equity.")
        if not negative_debt_companies.empty and 'Business ID' in company_data.columns:
            disp = negative_debt_companies[['Business ID', 'Debt to Equity']].copy()

            disp['Debt to Equity'] = disp['Debt to Equity'].round(2)
            print(disp.to_string(index=False))
        elif not negative_debt_companies.empty:

            disp = negative_debt_companies[['Debt to Equity']].copy()
            disp['Debt to Equity'] = disp['Debt to Equity'].round(2)
            print(disp.to_string())
    else:
        print("Column 'Debt to Equity' not found; skipping negative-debt filter.")


    # --- 5. Debt-to-Income Ratio DataFrame ---
    print_header("New Debt-to-Income DataFrame")
    if 'Total Revenue' in company_data.columns and 'Total Long-term Debt' in company_data.columns:
        dti_ratio = np.where(
            company_data['Total Revenue'] == 0,
            np.nan,
            company_data['Total Long-term Debt'] / company_data['Total Revenue']
        )
        debt_to_income_df = pd.DataFrame({
            'Business ID': company_data['Business ID'],
            'Debt-to-Income Ratio': dti_ratio
        })

        debt_to_income_df['Debt-to-Income Ratio'] = debt_to_income_df['Debt-to-Income Ratio'].round(2)
        print("Debt-to-Income ratios computed for all companies (first 5 records shown):")
        print(debt_to_income_df.head().to_string(index=False))
    else:
        debt_to_income_df = None
        print("Required columns for calculation not found; skipping this step.")


    # --- 6. Final Augmented Data ---
    print_header("Final Augmented Data")
    if debt_to_income_df is not None and 'Business ID' in company_data.columns:
        final_data = pd.concat([
            company_data.set_index('Business ID'),
            debt_to_income_df.set_index('Business ID')
        ], axis=1).reset_index()
        
        display_cols = ['Business ID', 'Business State', 'Debt-to-Income Ratio']

        if 'Debt-to-Income Ratio' in final_data.columns:
            final_data['Debt-to-Income Ratio'] = final_data['Debt-to-Income Ratio'].round(2)

        print("Final dataset with Debt-to-Income ratio appended (first 5 records shown):")
        print(final_data[display_cols].head().to_string(index=False))
    else:
        print("Skipping concatenation as prior steps were incomplete.")

    print("\n\n" + "="*80)
    print(" ANALYSIS COMPLETE ".center(80, ' '))
    print("="*80)


if __name__ == '__main__':
    main()