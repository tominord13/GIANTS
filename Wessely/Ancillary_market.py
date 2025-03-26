import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load the Excel file
file_path = "C:/Users/TomiNordi2m/OneDrive - i2m Unternehmensentwicklung GmbH/Documents/Python/Wessely/2022_05.xlsx"
xls = pd.ExcelFile(file_path, engine="openpyxl")
df = pd.read_excel(xls, sheet_name=xls.sheet_names[0], engine="openpyxl")


# Load the data from the first sheet
df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])

# Clean and rename relevant columns
df_clean = df.iloc[1:].copy()  # Remove header row

# Convert date column to datetime format
df_clean.iloc[:, 0] = pd.to_datetime(df_clean.iloc[:, 0], errors='coerce')
df_clean.rename(columns={df_clean.columns[0]: "Date_Local"}, inplace=True)
df_clean["Date_Local"] = pd.to_datetime(df_clean["Date_Local"], errors='coerce')


# Identify columns related to mFRR (tertiary control reserve) activations
tertiary_activation_columns = [
    col for col in df_clean.columns if "Tertiary" in col and "Activated" in col
]

# Convert relevant columns to numeric values
df_clean[tertiary_activation_columns] = df_clean[tertiary_activation_columns].apply(pd.to_numeric, errors='coerce')

# Count the number of activations per day where either positive or negative tertiary control was activated
df_clean["Total_mFRR_Activations"] = df_clean[tertiary_activation_columns].ne(0).sum(axis=1)

# Group by date to count total activations per day
mfrr_activations_per_day = df_clean.groupby(df_clean["Date_Local"].dt.date)["Total_mFRR_Activations"].sum()

# Plot the data
plt.figure(figsize=(12, 6))
plt.bar(mfrr_activations_per_day.index, mfrr_activations_per_day.values, color='blue', alpha=0.7)
plt.xlabel("Date", fontsize=14)
plt.ylabel("Total mFRR Activations", fontsize=14)
plt.title("Daily Tertiary (mFRR) Activations", fontsize=16)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.show()
