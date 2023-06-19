import pandas as pd
import matplotlib.pyplot as plt
import os



experiments_array = [
    ("serial", 1, 10),
    ("serial", 2, 20),
    ("serial", 3, 40),
    ("serial", 13, 60),
    ("serial", 14, 80),
    ("serial", 16, 100),
    ("serial", 17, 120),

    ("wifi", 5, 10),
    ("wifi", 6, 20),
    ("wifi", 7, 20),
    ("wifi", 8, 40),
    ("wifi", 11, 60),
    ("wifi", 9, 80),
    ("wifi", 12, 100),
    ("wifi", 10, 120),
]

serial_results = []
wifi_results = []

for experiment in experiments_array:

    result_amounts = []

    for file_name in os.listdir(f"experiments/{experiment[1]}/1"):
        if "bad_" not in file_name:
            df = pd.read_csv(f'experiments/{experiment[1]}/1/{file_name}', header=None)
            result_amounts.append(df.shape[0])

    # print(df.to_string())
    print(experiment[2])
    if experiment[0] == "serial":
        serial_results.append([experiment[2], sum(result_amounts)/len(result_amounts)/15])
    else:
        wifi_results.append([experiment[2], sum(result_amounts)/len(result_amounts)/15])

print(serial_results)

x_axis = list(zip(*serial_results))[0]

plt.plot(*zip(*serial_results), label="serial")
plt.plot(*zip(*wifi_results), label="wifi")
plt.plot(x_axis, x_axis, label="ideal")
plt.xticks(x_axis)
plt.grid()
plt.legend()
plt.title('Hz Actual vs Hz Setting')
plt.xlabel('Hz Setting')
plt.ylabel('Hz Actual')
plt.show()