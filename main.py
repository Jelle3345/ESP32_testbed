import os
import subprocess
import threading
import time
import keyboard
import psutil

esp_idf_folder = "D:/esp/esp-idf"
esp32_csi_toolkit_folder = "C:/Users/Jelle/CLionProjects/ESP32-CSI-Tool-1"

experiments_path = f'experiments/{(int(max(os.listdir("experiments"), default=0)) + 1)}'
experiment_num = 0
do_experiment = False


def start_node(port, mode):
    string = ""
    process = subprocess.Popen(
        [esp_idf_folder + "/export.bat", "&&", "cd", esp32_csi_toolkit_folder + "/" + mode, "&&", "idf.py", "-p", port,
         "build",
         "flash", "monitor"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in process.stdout:
        try:  # some output is not utf-8
            string = line.decode('utf-8').replace("\n", "")
        except:
            pass

        if "CSI_DATA" in string and string != "":
            if do_experiment:
                print(f'{port},{experiment_num},{time.time()},{string}')
                file = open(f'{experiments_path}/{experiment_num}/{port}_{mode}.csv', 'a')
                file.write(f'{port},{experiment_num},{time.time()},{string}')

        else:
            print(f'{port},{string}')


def stop_start_experiment():
    global do_experiment, experiment_num
    if not do_experiment:  # so start an experiment
        experiment_num += 1
        print("starting experiment:", experiment_num)
        os.mkdir(f'{experiments_path}/{experiment_num}')

    else:
        print("stopping experiment:", experiment_num)
    do_experiment = not do_experiment


def start_nodes(nodes):
    node_threads = []
    for node in nodes:
        thread = threading.Thread(target=start_node, args=[node[0], node[1]], daemon=True)
        thread.start()
        node_threads.append(thread)
        time.sleep(2)  # to fix the startup .bat file being used by the other thread
    for thread in node_threads:
        thread.join()


# active_ap, active_sta, passive
if __name__ == '__main__':
    os.mkdir(experiments_path)
    keyboard.on_release_key("num_lock", lambda _: stop_start_experiment())

    nodes = [
        ("COM3", "active_sta"),
        ("COM5", "active_ap")
    ]
    start_nodes(nodes)
