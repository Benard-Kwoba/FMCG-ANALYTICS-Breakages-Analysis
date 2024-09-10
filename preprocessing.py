# import necessary libraries
import pandas as pd           # For data manipulation and analysis
import numpy as np            # For numerical operations and handling missing data
import matplotlib.pyplot as plt # For data visualization
import seaborn as sns          # For enhanced data visualization
import chardet                 # For detecting file encoding
from datetime import datetime  # For handling date and time operations
import csv
from datetime import datetime

def parse_date(date_str):
    return datetime.strptime(date_str, '%m/%d/%Y').date()

def get_shift(selected_date):
    shifts = ['A', 'B', 'C']
    shift_day_types = []
    start_date = datetime(2024, 4, 30).date()
    days_since_start = (selected_date - start_date).days

    for shift in shifts:
        shift_index = shifts.index(shift)
        day_type_index = (days_since_start + shift_index * 2) % 6
        day_type = ['DAY', 'NIGHT', 'OFF'][day_type_index // 2]
        shift_day_types.append(f"{shift}: {day_type}")

    return shift_day_types

input_file = 'data/aglBreakagesYear8_raw.csv'
output_file = 'data/aglBreakagesYear8.csv'

with open(input_file, mode='r', newline='') as infile, \
        open(output_file, mode='w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        selected_date = parse_date(row['Date'])
        shift = get_shift(selected_date)
        shift_category = next(category.split(': ')[1] for category in shift if category.startswith(row['Shift']))
        row['Category'] = shift_category
        writer.writerow(row)

print(f"Updated CSV written to {output_file}.")


""" _______________________________ 1. Load and Inspect the Preprocessed Data ______________________________________ """
# Load the CSV file; change accordingly to reflect your file path
file_path = r'C:\Users\OtienBer\anaconda3\Lib\venv\SQLite Database\agl_inventory_db\aglBreakagesYear8.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')  # Try 'ISO-8859-1' or 'cp1252' if 'ISO-8859-1' doesn't work

# Display the first few rows of the DataFrame
# print(data.head())

# Display summary statistics
# print(data.describe(include='all'))
# print(data.isnull().sum())

""" _______________________________ Step 2: Data Cleaning and Preparation __________________________________________ """
# Step 1: Convert date columns to datetime format
data['Date'] = pd.to_datetime(data['Date'], format='%m/%d/%Y', errors='coerce')  # 'coerce' -> NaT

# Step 2: Remove leading or trailing whitespaces from column names
data.columns = data.columns.str.strip()

# Step 3: Handle missing values or incorrect data entries
# Display initial count of missing values
# print("Initial missing values per column:")
# print(data.isnull().sum())

# Handling missing values
# For numeric columns, you can fill missing values with the mean, median, or a specific value
data['Quantity_Cases'] = data['Quantity_Cases'].fillna(data['Quantity_Cases'].mean())  # normally distributed data
data['Total_Cost'] = data['Total_Cost'].fillna(data['Total_Cost'].median())  # median is less affected by extreme values

# For categorical columns, you can fill missing values with the mode or a placeholder
data['Breakages_Cause'] = data['Breakages_Cause'].fillna('Unknown')
data['Responsible_Category'] = data['Responsible_Category'].fillna('Unknown')
data['Location'] = data['Location'].fillna('Unknown')
data['Shift'] = data['Shift'].fillna('Unknown')

# Display the updated count of missing values
# print("Missing values after handling:")
# print(data.isnull().sum())

# Additional data cleaning: Removing any rows with incorrect or unrealistic values (if applicable)
# Example: Remove rows where 'Quantity_Cases' or 'Total_Cost' are negative
data = data[(data['Quantity_Cases'] >= 0) & (data['Total_Cost'] >= 0)]

# Display the cleaned data summary
print("Cleaned data summary:")
print(data.describe(include='all', datetime_is_numeric=True))  #  datetime_is_numeric: future behavior of pandas

""" ____________________________________ Step 3: Data Transformation _______________________________________________ """
# Add 'Year' and 'Month' columns
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month

# Save the transformed data to a new CSV
data.to_csv('aglBreakagesYear8_transformed.csv', index=False)  #  index=False: exclude the index from the output CSV file






