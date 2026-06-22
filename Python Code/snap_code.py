import pandas as pd
import os

# 1. Set your exact folder path. 
# The 'r' before the quotes tells Python to read it as a "raw" string, 
# preventing the backslashes from causing errors.
folder_path = r"C:\Users\Assetto Server\Snap Project\FY 69 through FY 26"

# 2. Explicitly list the 5 years we want so we don't accidentally process the 1970s data
target_files = ['FY21.xlsx', 'FY22.xlsx', 'FY23.xlsx', 'FY24.xlsx', 'FY25.xlsx']

# Create the full file paths by combining the folder and file names
file_list = [os.path.join(folder_path, f) for f in target_files]

regions_list = ['NERO', 'MARO', 'SERO', 'MWRO', 'SWRO', 'MPRO', 'WRO']
all_data = []

# 3. Process the selected files
for filepath in file_list:
    # Check if the file actually exists before trying to open it
    if not os.path.exists(filepath):
        print(f"Warning: Could not find {filepath}. Skipping...")
        continue
        
    print(f"Processing {filepath}...")
    
    # Extract just the 'FY25' part from the full path to use as our column label
    filename = os.path.basename(filepath)
    fiscal_year = filename.split('.')[0] 
    
    xls = pd.ExcelFile(filepath)
    sheets_to_process = [s for s in xls.sheet_names if s != 'US Summary']
    
    for sheet in sheets_to_process:
        df = pd.read_excel(xls, sheet_name=sheet)
        df.columns = ['Month', 'Households', 'Persons', 'Cost', 'Cost_Per_Household', 'Cost_Per_Person']
        
        current_state = None
        
        for index, row in df.iloc[6:].iterrows():
            month_val = str(row['Month']).strip()
            
            if pd.isna(row['Month']) or month_val == 'nan' or 'Total' in month_val:
                continue
                
            if pd.isna(row['Households']) or str(row['Households']).strip() == 'nan':
                current_state = month_val
                continue
                
            if current_state and current_state not in regions_list:
                all_data.append({
                    'Fiscal_Year': fiscal_year,
                    'Region': sheet,
                    'State': current_state,
                    'Month_Year': month_val,
                    'Households': row['Households'],
                    'Persons': row['Persons'],
                    'Cost': row['Cost'],
                    'Cost_Per_Household': row['Cost_Per_Household'],
                    'Cost_Per_Person': row['Cost_Per_Person']
                })

clean_df = pd.DataFrame(all_data)

numeric_cols = ['Households', 'Persons', 'Cost', 'Cost_Per_Household', 'Cost_Per_Person']
for col in numeric_cols:
    clean_df[col] = pd.to_numeric(clean_df[col], errors='coerce')

# Save the output file to the same folder
output_path = os.path.join(folder_path, 'SNAP_5Year_Master.csv')
clean_df.to_csv(output_path, index=False)
print(f"\nSuccess! Saved {len(clean_df)} rows of data to {output_path}")