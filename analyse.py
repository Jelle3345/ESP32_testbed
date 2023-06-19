import pandas as pd
import matplotlib.pyplot as plt
import os


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

all_results = pd.DataFrame(columns=['station_amount', 'transfer_type', 'hz_setting', 'hz_actual'])


for experiment in experiments_array:

    result_amounts = []

    for file_name in os.listdir(f"experiments/{experiment[1]}/1"):
        if "bad_" not in file_name:
            df = pd.read_csv(f'experiments/{experiment[1]}/1/{file_name}', header=None)
            result_amounts.append(df.shape[0])

    list_row = [experiment[3], experiment[0], experiment[2], sum(result_amounts)/len(result_amounts)/15]
    all_results.loc[len(all_results)] = list_row

all_results = all_results.sort_values(by='hz_setting')
print(all_results)

all_results.to_csv('results.csv', index=False)

