import subprocess
import threading
import time

esp_idf_folder = "C:/eps/esp-idf"
esp32_csi_toolkit_folder = "C:/eps/ESP32-CSI-Tool"


def flash_all(port, mode):
    process = subprocess.Popen(
        [esp_idf_folder + "/export.bat", "&&", "cd", esp32_csi_toolkit_folder + "/" + mode, "&&", "idf.py",
         "-p" if port != "" else "", port,
         "flash"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in process.stdout:
        try:  # some output is not utf-8
            string = line.decode('utf-8').replace("\n", "")
            print(f'{port},{string}')

        except:
            pass


def build_flash_nodes(nodes):
    # only builds the active_sta
    process = subprocess.Popen([esp_idf_folder + "/export.bat", "&&", "cd", esp32_csi_toolkit_folder + "/" +
                                "active_sta", "&&", "idf.py", "build"], shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for line in process.stdout:
        try:  # some output is not utf-8
            string = line.decode('utf-8').replace("\n", "")
            print(f'building: {string}')

        except:
            pass

    # flash all a threaded
    node_threads = []
    for node in nodes:
        thread = threading.Thread(target=flash_all, args=[node[0], node[1]], daemon=True)
        thread.start()
        node_threads.append(thread)
        time.sleep(3)  # to fix the startup .bat file being used by the other thread
    for thread in node_threads:
        thread.join()


if __name__ == '__main__':
    # todo add check for success on all nodes
    # active_ap, active_sta, passive
    nodes = [  # pos1 is port and can be empty for auto assignment
        ("COM27", "active_sta"),
        ("COM28", "active_sta"),
    ]
    build_flash_nodes(nodes)
