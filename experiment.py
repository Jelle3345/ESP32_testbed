import time
import os

import keyboard


class Experiment:
    do_experiment = False
    experiments_path = None
    experiment_num = 0

    def __init__(self):
        self.experiments_path = f'experiments/{(int(max(os.listdir("experiments"), default=0)) + 1)}'
        os.mkdir(self.experiments_path)
        keyboard.on_release_key("num_lock", lambda _: self.stop_start_experiment())

    def write_to_file(self, string):
        string_array = string.split(',')
        mode = string_array[2]
        mac = string_array[3].replace(":", "_")
        file = open(f'{self.experiments_path}/{self.experiment_num}/{mac}_{mode}.csv', 'a')
        for string_part in string.splitlines():
            file.write(f'{self.experiment_num},{time.time()},{string_part}\n')

    def stop_start_experiment(self):
        if not self.do_experiment:  # so start an experiment
            self.experiment_num += 1
            print("starting experiment:", self.experiment_num)
            os.mkdir(f'{self.experiments_path}/{self.experiment_num}')

        else:
            print("stopping experiment:", self.experiment_num)
        self.do_experiment = not self.do_experiment
