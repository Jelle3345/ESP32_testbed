import pandas as pd
import matplotlib.pyplot as plt


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

    df = pd.read_csv(f'experiments/{experiment[1]}/1/EC_94_CB_49_B2_F0_STA.csv', header=None)

    # print(df.to_string())
    if experiment[0] == "serial":
        serial_results.append([experiment[2]*15, df.shape[0]])
    else:
        wifi_results.append([experiment[2]*15, df.shape[0]])

print(serial_results)
plt.plot(*zip(*serial_results), label="serial")
plt.plot(*zip(*wifi_results), label="wifi")
plt.legend()
plt.title('Random Figure')
plt.xlabel('X-Axis')
plt.ylabel('Y-Axis')
plt.show()