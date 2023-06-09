import time
import os


class Experiment:
    do_experiment = False
    experiments_path = None
    experiment_num = 0

    def __init__(self):
        self.experiments_path = f'experiments/{(int(max(os.listdir("experiments"), default=0)) + 1)}'

    def write_to_file(self, string):
        string_array = string.split(',')
        mode = string_array[1]
        mac = string_array[2]
        print(f'{self.experiment_num},{time.time()},{string}')
        file = open(f'{self.experiments_path}/{self.experiment_num}/{mac}_{mode}.csv', 'a')
        file.write(f'{self.experiment_num},{time.time()},{string}')

    def stop_start_experiment(self):
        if not self.do_experiment:  # so start an experiment
            self.experiment_num += 1
            print("starting experiment:", self.experiment_num)
            os.mkdir(f'{self.experiments_path}/{self.experiment_num}')

        else:
            print("stopping experiment:", self.experiment_num)
        self.do_experiment = not self.do_experiment
