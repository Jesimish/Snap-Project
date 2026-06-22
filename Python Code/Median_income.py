import pandas as pd
import re
import os

# Set the directory where your files are located
directory_path = r"C:\Users\Assetto Server\Snap Project\FY 69 through FY 26"

# List of your uploaded files
files = [
    "2020 Snap Median Income.csv",
    "2021 Snap Median Income.csv",
    "2022 Snap Median Income.csv",
    "2023 Snap Median Income.csv",
    "2024 Snap Median Income.csv"
]

all_data = []

for file_name in files:
    # Create the full file path by combining the directory and the file name
    full_path = os.path.join(directory_path, file_name)
    
    # Check if the file actually exists in the directory before trying to open it
    if not os.path.exists(full_path):
        print(f"File not found: {full_path}")
        continue
    
    # Extract the year from the filename
    year = re.search(r'\d{4}', file_name).group()
    
    # Read the CSV
    df = pd.read_csv(full_path)
    
    # Locate the row that contains the Median Income metric
    median_row = df[df['Label (Grouping)'].str.contains("Median income", case=False, na=False)]
    
    if median_row.empty:
        print(f"Could not find Median Income row in {file_name}")
        continue
        
    # Melt the dataframe from Wide to Long format
    melted = median_row.melt(id_vars=['Label (Grouping)'], var_name='Column', value_name='Median Income')
    
    # Filter only for the columns representing households receiving SNAP
    snap_cols = melted[melted['Column'].str.contains("Households receiving food stamps/SNAP!!Estimate", na=False)].copy()
    
    # Extract the State Name by splitting the string at the "!!" delimiter
    snap_cols['State'] = snap_cols['Column'].str.split('!!').str[0]
    
    # Add the year column
    snap_cols['Year'] = year
    
    # Clean the Median Income values (remove commas and dollar signs, convert to numeric)
    snap_cols['Median Income'] = snap_cols['Median Income'].astype(str).str.replace(r'[$,]', '', regex=True)
    snap_cols['Median Income'] = pd.to_numeric(snap_cols['Median Income'], errors='coerce')
    
    # Append the clean subset to our master list
    all_data.append(snap_cols[['State', 'Year', 'Median Income']])

# Combine all yearly data into one DataFrame
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)

    # Sort the data alphabetically by State, then chronologically by Year
    final_df = final_df.sort_values(by=['State', 'Year'])

    # Export the final transformed data back into the same folder
    output_filename = "Combined_SNAP_Median_Income_By_State.csv"
    output_path = os.path.join(directory_path, output_filename)
    
    final_df.to_csv(output_path, index=False)
    print(f"Data successfully transformed and combined! Saved as '{output_path}'")
else:
    print("No data was processed. Please check if the files exist in the directory.")