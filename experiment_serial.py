import subprocess
import threading
import time

from experiment import Experiment

esp_idf_folder = "C:/eps/esp-idf"
esp32_csi_toolkit_folder = "C:/eps/ESP32-CSI-Tool"


def monitor_node(port):
    string = ""
    process = subprocess.Popen(
        [esp_idf_folder + "/export.bat", "&&", "cd", esp32_csi_toolkit_folder + "/active_sta", "&&", "idf.py",
         "-p" if port != "" else "", port,
         "monitor"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in process.stdout:
        try:  # some output is not utf-8
            string = line.decode('utf-8').replace("\n", "")
        except:
            pass
        if "CSI_DATA" in string and experiment.do_experiment:
            experiment.write_to_file(string)
        elif "CSI_DATA" not in string:
            print(f'{port},{string}')


def monitor_nodes(ports):
    node_threads = []
    for port in ports:
        thread = threading.Thread(target=monitor_node, args=[port], daemon=True)
        thread.start()
        node_threads.append(thread)
        time.sleep(2)  # to fix the startup .bat file being used by the other thread
    for thread in node_threads:
        thread.join()


# active_ap, active_sta, passive
if __name__ == '__main__':
    print("make sure Send CSI data over WiFi is disabled for best results")
    experiment = Experiment()
    node_ports = [  # leave empty string for auto assignment
        "COM8",
        "COM9",
        "COM10",
        "COM13",
        "COM14",
        "COM26",
        "COM27",
        "COM28",
        "COM29",
    ]
    monitor_nodes(node_ports)
