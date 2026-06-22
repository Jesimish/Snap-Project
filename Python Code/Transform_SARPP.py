import pandas as pd

# 1. Load the BEA file, but tell Pandas to skip those top 3 junk text lines
filepath = 'Snap Project/FY 69 through FY 26/SARPP Regional price parities by state.csv'
df = pd.read_csv(filepath, skiprows=3)

# 2. Clean up any trailing text at the bottom of the file (BEA often puts asterisks or notes there)
df = df.dropna(subset=['GeoFIPS'])
df = df[~df['GeoFIPS'].astype(str).str.contains(r'\*|Note', na=False, regex=True)]

# 3. Unpivot the table from wide to long using pd.melt()
# This grabs all the year columns and stacks them vertically
year_cols = [col for col in df.columns if str(col).isdigit()]
df_unpivoted = pd.melt(df, 
                       id_vars=['GeoFIPS', 'GeoName'], 
                       value_vars=year_cols, 
                       var_name='Calendar_Year', 
                       value_name='RPP_Index')

# 4. Clean up column names to match our SQL schema
df_unpivoted.rename(columns={'GeoName': 'State'}, inplace=True)

# 5. Filter for our specific 5-year project window
target_years = ['2021', '2022', '2023', '2024', '2025']
df_filtered = df_unpivoted[df_unpivoted['Calendar_Year'].isin(target_years)].copy()

# Add the 'FY' prefix so it matches our 'FY21', 'FY22' format perfectly
df_filtered['Fiscal_Year'] = 'FY' + df_filtered['Calendar_Year'].str[-2:]

# 6. Save the final, Tableau-ready file
df_filtered.to_csv('BEA_RPP_Cleaned.csv', index=False)
print("Success! Flattened the BEA index.")
print(df_filtered.head())