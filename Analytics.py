
# import necessary libraries
import pandas as pd           # For data manipulation and analysis
import numpy as np            # For numerical operations and handling missing data
import matplotlib.pyplot as plt # For data visualization
import seaborn as sns          # For enhanced data visualization
import chardet                 # For detecting file encoding
from datetime import datetime  # For handling date and time operations
from scipy import stats # For statistical analysis
from sklearn.linear_model import LinearRegression  # for predictive analytics

""" _________ 4.  Data Analysis: Identify the products with the highest breakages for 2024. ________________________ """
# Load the CSV file; change accordingly to reflect your file path
file_path = r'C:\Users\OtienBer\anaconda3\Lib\venv\SQLite Database\agl_inventory_db\aglBreakagesYear8_transformed.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')  # Try 'ISO-8859-1' or 'cp1252' if 'ISO-8859-1' doesn't work

# Convert Dates to Datetime
data['Date'] = pd.to_datetime(data['Date'])

# Filter data for 2024
data_2024 = data[data['Date'].dt.year == 2024]

# Find Total Breakages and Cost for 2024
total_cost_2023 = data_2024['Total_Cost'].sum()

# Aggregate data for 2024
total_breakages_2024 = data_2024['Quantity_Cases'].sum()
total_cost_2024 = data_2024['Total_Cost'].sum()
# You can remove extra spaces in Description column Make an explicit copy of the data_2024 DataFrame
data_2024 = data_2024.copy()
data_2024.loc[:, 'Description'] = data_2024['Description'].str.replace(r'\s+', ' ', regex=True).str.strip()
# Identify the Products with the Highest Breakages for 2024
product_breakages_2024 = data_2024.groupby('Description')['Quantity_Cases'].sum()
top_products_2024 = product_breakages_2024.sort_values(ascending=False)

# Select the top 10 products
top_10_products_2024 = top_products_2024.head(10)

# Aggregate total cost for the top 10 products
top_10_costs_2024 = data_2024[data_2024['Description'].isin(top_10_products_2024.index)]
product_costs_2024 = top_10_costs_2024.groupby('Description')['Total_Cost'].sum()
top_10_costs_2024 = product_costs_2024.reindex(top_10_products_2024.index)

# Visualization
fig, ax1 = plt.subplots(figsize=(15, 8))

# Create bar plot for Quantity of Breakages
sns.barplot(x=top_10_products_2024.values, y=top_10_products_2024.index, palette='viridis', ax=ax1, label='Breakages')

ax1.set_xlabel('Quantity of Breakages (Cases)', fontsize=14)
ax1.set_ylabel('Product Description', fontsize=14)
ax1.set_title('Top 10 Products with Highest Breakages for 2024', fontsize=18)
ax1.tick_params(axis='y', labelsize=12)
plt.xticks(fontsize=12)

# Create a secondary y-axis for the Total Cost line plot
ax2 = ax1.twiny()

ax2.plot(top_10_costs_2024.values, top_10_costs_2024.index, color='red', marker='o', linestyle='-',
         linewidth=1, label='Total Cost', markersize=4, mfc='yellow')
ax2.set_xlabel('Total Cost (Currency)', fontsize=12, color='red')
ax2.tick_params(axis='x', labelsize=12, colors='red')

# Improve layout
fig.tight_layout()

# Show plot
# plt.show()

""" _________________ 4.1  Data Analysis: Determine the leading causes of breakages for 2024 ________________________ """
# Group by the breakage cause and sum the Quantity_Cases for each cause
leading_causes = data_2024.groupby('Breakages_Cause')['Quantity_Cases'].sum()

# Sort the results in descending order to identify the leading causes
leading_causes = leading_causes.sort_values(ascending=False)
# Plot the leading causes of breakages
plt.figure(figsize=(12, 6))
sns.barplot(x=leading_causes.values, y=leading_causes.index, palette='coolwarm')

# Adding labels and title
plt.xlabel('Total Quantity Cases')
plt.ylabel('Breakage Cause')
plt.title('Leading Causes of Breakages for 2024')

# Adding data labels to the bars
for i, (value, name) in enumerate(zip(leading_causes.values, leading_causes.index)):
    plt.text(value + 0.5, i, f'{value:,.2f}', va='center', ha='left')

plt.tight_layout()
plt.show()
# Display the top causes of breakages
# print("Leading Causes of Breakages for 2024:")
# print(leading_causes.head(20))

""" _________________ 4.2  Data Analysis: Comparison responsible categories ________________________ """
# Group by responsible category and sum the Quantity_Cases for each category
breakages_by_category = data_2024.groupby('Responsible_Category')['Quantity_Cases'].sum()

# Sort the results in descending order
breakages_by_category = breakages_by_category.sort_values(ascending=False)
# Plotting pie chart
plt.figure(figsize=(10, 8))
patches, texts, autotexts = plt.pie(
    breakages_by_category,
    labels=breakages_by_category.index,
    autopct='%1.1f%%',
    startangle=140,
    colors=plt.cm.Paired(range(len(breakages_by_category))),
    shadow=True,
    explode=[0.1 if max(breakages_by_category) == value else 0.05 for value in breakages_by_category]
)

# Customize text labels
for text in texts:
    text.set_horizontalalignment('center')

# Customize percent labels
for autotext in autotexts:
    autotext.set_horizontalalignment('center')
    autotext.set_fontstyle('italic')
    autotext.set_fontweight('bold')

# Add a title
plt.title('Breakages by Responsible Category for 2024'.upper(), c='darkorange', weight='bold', fontdict={'fontsize': 14})

# Equal aspect ratio ensures that pie is drawn as a circle.
plt.axis('equal')

# Show plot
plt.show()

# Display the results
# print("Breakages by Responsible Category for 2024:")
# print(breakages_by_category)

""" _________________ 4.3  Data Analysis: Comparison shifts ________________________ """
# Group by shift and sum the Quantity_Cases and Total_Cost for each shift
breakages_by_shift = data_2024.groupby('Shift').agg({'Quantity_Cases': 'sum', 'Total_Cost': 'sum'})

# Sort the results in descending order
breakages_by_shift = breakages_by_shift.sort_values(by='Quantity_Cases', ascending=False)

# Create the plot
fig, ax1 = plt.subplots(figsize=(12, 7))

# Bar plot for Quantity Cases
bars = ax1.bar(breakages_by_shift.index, breakages_by_shift['Quantity_Cases'], color=sns.color_palette('Set1', len(breakages_by_shift)), label='Quantity of Breakages')

# Set labels and title for the primary y-axis (Quantity Cases)
ax1.set_xlabel('Shift', c='blue', style='italic')
ax1.set_ylabel('Quantity of Breakages (Cases)', c='blue', style='italic')
ax1.set_title('Breakages and Cost by Shift for 2024', c='blue', weight='bold')
ax1.tick_params(axis='y', labelcolor='blue')

# Create a second y-axis to plot the line chart for Total Cost
ax2 = ax1.twinx()
ax2.plot(breakages_by_shift.index, breakages_by_shift['Total_Cost'], color='black', marker='o', linestyle='-', linewidth=2, markersize=8, label='Total Cost')

# Set labels for the secondary y-axis (Total Cost)
ax2.set_ylabel('Total Cost(Kshs)', c='blue', style='italic')
ax2.tick_params(axis='y', labelcolor='blue')

# Add legends and grid
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')
# ax1.grid(axis='y', linestyle='--', alpha=0.7)

plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()

# Show plot
# plt.show()

# Display the results
# print("Breakages by Shift for 2024:")
# print(breakages_by_shift)

""" _________________ 4.4  Data Analysis: Comparison shifts by Time NIGHT, DAY ________________________ """
# Group by shift category and sum the Total_Cost
breakages_by_shiftCategory = data_2024.groupby('Category')['Total_Cost'].sum()

# Sort the results in descending order
breakages_by_shiftCategory = breakages_by_shiftCategory.sort_values(ascending=False)

# Create the plot
plt.figure(figsize=(12, 7))

# Bar plot for Total Cost
bars = plt.bar(breakages_by_shiftCategory.index, breakages_by_shiftCategory.values,
               color=sns.color_palette('Set2', len(breakages_by_shiftCategory)))

# Add data labels for bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval:.2f}',
             va='bottom', ha='center', fontsize=10, weight='bold')

# Set labels and title
plt.xlabel('Category', c='blue', style='italic')
plt.ylabel('Total Cost of Breakages', c='blue', style='italic')
plt.title('Breakages Analysis by Category', c='blue', weight='bold')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

# Show plot
plt.tight_layout()
# plt.show()
# Display the results:
# print("Breakages by Shift for 2024:")
# print(breakages_by_shift)

""" _________________ 4.5 Predictive Analytics  ________________________ """
# Sample breakages data (assuming you have a DataFrame named data_2024)
# Ensure 'Date' is a datetime column
data_2024['Date'] = pd.to_datetime(data_2024['Date'])

# Extract month and year
data_2024['Month_Year'] = data_2024['Date'].dt.to_period('M')

# Aggregate monthly breakages
monthly_breakages = data_2024.groupby('Month_Year')['Quantity_Cases'].sum().reset_index()

# Convert Month_Year to datetime for plotting
monthly_breakages['Month_Year'] = monthly_breakages['Month_Year'].dt.to_timestamp()

# Prepare data for forecasting
monthly_breakages['Month_Year_Num'] = np.arange(len(monthly_breakages))  # Numeric representation for months

# Fit a linear regression model
model = LinearRegression()
X = monthly_breakages[['Month_Year_Num']]
y = monthly_breakages['Quantity_Cases']
model.fit(X, y)

# Forecast the next 3 months
last_month_num = len(monthly_breakages)
future_months = pd.date_range(start=monthly_breakages['Month_Year'].max() + pd.DateOffset(months=1), periods=3, freq='M')
future_months_num = np.arange(last_month_num, last_month_num + 3).reshape(-1, 1)
future_forecast = model.predict(future_months_num)

# Convert future months to DataFrame for plotting
future_forecast_df = pd.DataFrame({
    'Month_Year': future_months,
    'Quantity_Cases': future_forecast
})

# Create the plot
plt.figure(figsize=(14, 7))

# Plot historical data
plt.plot(monthly_breakages['Month_Year'], monthly_breakages['Quantity_Cases'], marker='o', color='b', label='Monthly Breakages')

# Plot forecast data
plt.plot(future_forecast_df['Month_Year'], future_forecast_df['Quantity_Cases'], marker='o', linestyle='--', color='r', label='Forecast')

# Annotate forecast values
for i, (month, forecast) in enumerate(zip(future_forecast_df['Month_Year'], future_forecast_df['Quantity_Cases'])):
    plt.text(month, forecast, f'{forecast:.2f}', color='r', fontsize=10, ha='center')

# Customize plot
plt.xlabel('Month', c='blue', style='italic')
plt.ylabel('Quantity Cases', c='blue', style='italic')
plt.title('Monthly Breakages Trend with 3-Month Forecast', c='blue', weight='bold')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show plot
plt.show()
