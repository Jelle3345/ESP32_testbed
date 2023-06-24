import matplotlib.pyplot as plt
import pandas as pd

# Read the CSV file
df = pd.read_csv('results.csv')

# Extract the relevant columns
station_amount = df['station_amount']
transfer_type = df['transfer_type']
hz_setting = df['hz_setting']
data_lost = df['data_lost']

# Set up the plot
plt.figure(figsize=(10, 6))
plt.xlabel('hz_setting')
plt.ylabel('data_lost')

# Group the data by station_amount and transfer_type
grouped_data = df.groupby(['station_amount', 'transfer_type'])

# Plot each group as a line
for (station, transfer), group in grouped_data:
    plt.plot(group['hz_setting'], group['data_lost'], marker='o', label=f'{station}, {transfer}')

# Add the ideal line
plt.axhline(y=0, color='red', linestyle='--', label='Ideal')

plt.grid(True)
plt.xticks(hz_setting)
plt.legend()  # Show the legend
plt.show()    # Display the plot
