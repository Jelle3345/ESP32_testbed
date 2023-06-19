import pandas
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# transfer_type, experiment_number, hz_setting, station_amount
experiments_array = [
    ("serial", 1, 10, 9),
    ("serial", 2, 20, 9),
    ("serial", 3, 40, 9),
    ("serial", 13, 60, 9),
    ("serial", 14, 80, 9),
    ("serial", 16, 100, 9),
    ("serial", 17, 120, 9),

    ("wifi", 5, 10, 9),
    ("wifi", 7, 20, 9),
    ("wifi", 8, 40, 9),
    ("wifi", 11, 60, 9),
    ("wifi", 9, 80, 9),
    ("wifi", 12, 100, 9),
    ("wifi", 10, 120, 9),

    ("serial", 20, 10, 2),
    ("serial", 30, 20, 2),
    ("serial", 28, 40, 2),
    ("serial", 24, 60, 2),
    ("serial", 22, 80, 2),
    ("serial", 26, 100, 2),
    ("serial", 18, 120, 2),

    ("serial", 21, 10, 1),
    ("serial", 31, 20, 1),
    ("serial", 29, 40, 1),
    ("serial", 25, 60, 1),
    ("serial", 23, 80, 1),
    ("serial", 27, 100, 1),
    ("serial", 19, 120, 1),

    ("wifi", 32, 10, 2),
    ("wifi", 34, 20, 2),
    ("wifi", 36, 40, 2),
    ("wifi", 38, 60, 2),
    ("wifi", 40, 80, 2),
    ("wifi", 42, 100, 2),
    ("wifi", 44, 120, 2),

    ("wifi", 33, 10, 1),
    ("wifi", 35, 20, 1),
    ("wifi", 37, 40, 1),
    ("wifi", 39, 60, 1),
    ("wifi", 41, 80, 1),
    ("wifi", 43, 100, 1),
    ("wifi", 45, 120, 1),
]

serial_results = []
wifi_results = []

all_results = pd.DataFrame(columns=[
    'station_amount',
    'transfer_type',
    'hz_setting',
    'hz_actual',
    'expected_time_between_packets',
    'mean_time_between_packets',
    'CV_time_between_packets'
])

for experiment in experiments_array:

    result_amounts = []
    time_between_packets = []

    for file_name in os.listdir(f"experiments/{experiment[1]}/1"):
        if "bad_" not in file_name:
            df = pd.read_csv(f'experiments/{experiment[1]}/1/{file_name}', header=None)
            times = df.iloc[:, 22] / 1000000  # convert from microseconds to seconds
            time_diffs = times.diff().dropna()

            time_between_packets.extend(time_diffs.tolist())
            result_amounts.append(df.shape[0])

    np_array = np.array(time_between_packets)
    mean = np.mean(np_array)
    std = np.std(np_array)
    cv_normalized = (std / mean)

    list_row = [
        experiment[3],
        experiment[0],
        experiment[2],
        round(sum(result_amounts) / len(result_amounts) / 15, 4),
        round(1 / int(experiment[2]), 4),
        mean,
        cv_normalized
    ]

    all_results.loc[len(all_results)] = list_row

plt.show()
all_results = all_results.sort_values(by='hz_setting')
print(all_results)

all_results.to_csv('results.csv', index=False)

