import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('results.csv')
# Extract the relevant columns
station_amount = df['station_amount']
transfer_type = df['transfer_type']
hz_setting = df['hz_setting']
hz_actual = df['hz_actual']

# Set up the plot
plt.figure(figsize=(10, 6))
plt.xlabel('hz_setting')
plt.ylabel('hz_actual')

# Group the data by station_amount and transfer_type
grouped_data = df.groupby(['station_amount', 'transfer_type'])

# Plot each group as a line
for (station, transfer), group in grouped_data:
    plt.plot(group['hz_setting'], group['hz_actual'], marker='o', label=f'{station}, {transfer}')

# Add the ideal line
plt.plot(hz_setting, hz_setting, color='red', linestyle='--', label='Ideal')

plt.grid(True)
plt.xticks(hz_setting)
plt.legend()  # Show the legend
plt.show()    # Display the plot