import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel file into a DataFrame
file_path = r'C:\Users\sevon\Documents\Project Projects\Electric car data.xlsx'
df = pd.read_excel(file_path)

# Combine 'Brand' and 'Model' columns into a single 'Car' column
df['Car'] = df['Brand'].astype(str) + ' ' + df['Model'].astype(str)

# Define the temperature factors
temperature_factors = {
    '-20°C': 0.50,
    '-10°C': 0.60,
    '0°C': 0.80,
    '10°C': 1.00,
    '21°C': 1.15,
    '40°C': 0.80
}

# Calculate the real range of the EV at each temperature
df['Real_Range_minus20C'] = df['Range_Km'] * temperature_factors['-20°C']
df['Real_Range_minus10C'] = df['Range_Km'] * temperature_factors['-10°C']
df['Real_Range_0C'] = df['Range_Km'] * temperature_factors['0°C']
df['Real_Range_10C'] = df['Range_Km'] * temperature_factors['10°C']
df['Real_Range_21C'] = df['Range_Km'] * temperature_factors['21°C']
df['Real_Range_40C'] = df['Range_Km'] * temperature_factors['40°C']

# Filter to only include the first 25 cars
df_subset = df.head(25)

# Define the x-axis labels (Car) and y-axis values (ranges)
car_labels = df_subset['Car']  # Car names for the x-axis
rated_range = df_subset['Range_Km']  # Rated range for the y-axis

# Real ranges for y-axis (at different temperatures)
real_range_minus20C = df_subset['Real_Range_minus20C']
real_range_minus10C = df_subset['Real_Range_minus10C']
real_range_0C = df_subset['Real_Range_0C']
real_range_10C = df_subset['Real_Range_10C']
real_range_21C = df_subset['Real_Range_21C']
real_range_40C = df_subset['Real_Range_40C']

# Create plots for Rated Range and Real Ranges
plt.figure(figsize=(14, 8))

# Subplot 1: Car vs Rated Range
plt.subplot(1, 2, 1)
plt.plot(car_labels, rated_range, marker='o', color='blue', label='Rated Range')
plt.xticks(rotation=45, ha='right')
plt.xlabel('Car')
plt.ylabel('Range (Km)')
plt.title('Rated Range per Car Model')
plt.grid(True)

# Subplot 2: Car vs Real Ranges at Different Temperatures
plt.subplot(1, 2, 2)
plt.plot(car_labels, real_range_minus20C, marker='o', linestyle='--', color='red', label='Real Range -20°C')
plt.plot(car_labels, real_range_minus10C, marker='o', linestyle='--', color='orange', label='Real Range -10°C')
plt.plot(car_labels, real_range_0C, marker='o', linestyle='--', color='green', label='Real Range 0°C')
plt.plot(car_labels, real_range_10C, marker='o', linestyle='--', color='purple', label='Real Range 10°C')
plt.plot(car_labels, real_range_21C, marker='o', linestyle='--', color='brown', label='Real Range 21°C')
plt.plot(car_labels, real_range_40C, marker='o', linestyle='--', color='pink', label='Real Range 40°C')

plt.xticks(rotation=45, ha='right')
plt.xlabel('Car')
plt.ylabel('Real Range (Km)')
plt.title('Real Range per Car Model at Different Temperatures')
plt.legend()
plt.grid(True)

# Adjust layout and display plots
plt.tight_layout()
plt.show()

# Statistical summary for real ranges
summary_stats = df_subset[['Range_Km', 'Real_Range_minus20C', 'Real_Range_40C']].describe()
print(summary_stats)

# Melt the data for easier plotting
melted_df = df_subset.melt(id_vars=['Car'], value_vars=['Real_Range_minus20C', 'Real_Range_minus10C', 'Real_Range_0C', 'Real_Range_10C', 'Real_Range_21C', 'Real_Range_40C'],
                    var_name='Temperature', value_name='Range')

# Plot using seaborn
plt.figure(figsize=(12, 6))
sns.boxplot(x='Car', y='Range', hue='Temperature', data=melted_df)
plt.xticks(rotation=45, ha='right')
plt.title('Distribution of Real Ranges at Different Temperatures for Each EV')
plt.show()

# Calculate cost per kilometer at rated range and real range at different temperatures
df_subset['Cost_per_Km_Rated'] = df_subset['PriceEuro'] / df_subset['Range_Km']
df_subset['Cost_per_Km_Real_minus20C'] = df_subset['PriceEuro'] / df_subset['Real_Range_minus20C']

print(df_subset[['Car', 'Cost_per_Km_Rated', 'Cost_per_Km_Real_minus20C']])

# Calculate percentage drop in range at -20°C and 40°C compared to rated range
df_subset['Range_Drop_minus20C'] = ((df_subset['Range_Km'] - df_subset['Real_Range_minus20C']) / df_subset['Range_Km']) * 100
df_subset['Range_Drop_40C'] = ((df_subset['Range_Km'] - df_subset['Real_Range_40C']) / df_subset['Range_Km']) * 100

print(df_subset[['Car', 'Range_Drop_minus20C', 'Range_Drop_40C']])

# Sort EVs by the least range drop at -20°C
best_performers = df_subset.sort_values(by='Range_Drop_minus20C').head(5)

# Plot bar chart of the best-performing EVs
plt.bar(best_performers['Car'], best_performers['Range_Drop_minus20C'], color='green')
plt.xticks(rotation=45, ha='right')
plt.xlabel('Car')
plt.ylabel('Range Drop at -20°C (%)')
plt.title('Top 5 EVs with Least Range Drop at -20°C')
plt.show()

# Heatmap of range performance across temperatures
heatmap_data = df_subset[['Car', 'Real_Range_minus20C', 'Real_Range_minus10C', 'Real_Range_0C', 'Real_Range_10C', 'Real_Range_21C', 'Real_Range_40C']]

# Set 'Car' as the index
heatmap_data.set_index('Car', inplace=True)

# Plot the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, annot=True, cmap='coolwarm', linewidths=0.5, fmt='.1f')
plt.title('Heatmap of EV Real Range Across Different Temperatures')
plt.ylabel('Car Model')
plt.xlabel('Temperature')
plt.show()

# Scatter plot showing price vs. real range at 21°C
plt.figure(figsize=(10, 6))
plt.scatter(df_subset['PriceEuro'], df_subset['Real_Range_21C'], color='blue', s=100, alpha=0.6)

# Add labels to points (Car Models)
for i in range(df_subset.shape[0]):
    plt.text(df_subset['PriceEuro'].iloc[i], df_subset['Real_Range_21C'].iloc[i], df_subset['Car'].iloc[i], fontsize=8)

# Customize plot
plt.xlabel('Price (Euro)')
plt.ylabel('Real Range at 21°C (Km)')
plt.title('Price vs Real Range at 21°C')
plt.grid(True)
plt.show()
