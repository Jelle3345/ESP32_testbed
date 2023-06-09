import os
import subprocess
import threading
import time
import keyboard
import http.server
import socketserver

esp_idf_folder = "C:/eps/esp-idf"
esp32_csi_toolkit_folder = "C:/eps/ESP32-CSI-Tool"

experiments_path = f'experiments/{(int(max(os.listdir("experiments"), default=0)) + 1)}'
experiment_num = 0
do_experiment = False


def start_server():
    # Set up the server
    host = '192.168.4.2'
    port = 80  # Use a specific port number
    with socketserver.TCPServer((host, port), RequestHandler) as server:
        print("Server listening on {}:{}".format(host, port))
        server.serve_forever()


# Define the request handler class
class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        message = self.rfile.read(content_length).decode('utf-8')

        # Process the message as needed
        if do_experiment:
            write_to_file(message)

        # Send a response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Message received")


def start_node(port, mode):
    string = ""
    process = subprocess.Popen(
        [esp_idf_folder + "/export.bat", "&&", "cd", esp32_csi_toolkit_folder + "/" + mode, "&&", "idf.py",
         "-p" if port != "" else "", port,
         "build",
         "flash", "monitor"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in process.stdout:
        try:  # some output is not utf-8
            string = line.decode('utf-8').replace("\n", "")
        except:
            pass

        if "CSI_DATA" in string and string != "":
            # if mode == 'passive':
            #     print(f'{port},{experiment_num},{time.time()},{string}')
            if do_experiment and not send_csi_over_wifi:
                write_to_file(string)

        else:
            print(f'{port},{string}')


def write_to_file(string):
    string_array = string.split(',')
    mode = string_array[1]
    mac = string_array[2]
    print(f'{experiment_num},{time.time()},{string}')
    file = open(f'{experiments_path}/{experiment_num}/{mac}_{mode}.csv', 'a')
    file.write(f'{experiment_num},{time.time()},{string}')


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

    # the settings
    build_flash_monitor = True
    # change this to either send csi over wifi or log the serial info, menuconfig setting needed for the esp to enable wifi
    send_csi_over_wifi = False

    keyboard.on_release_key("num_lock", lambda _: stop_start_experiment())

    if build_flash_monitor:
        os.mkdir(experiments_path)
        nodes = [  # pos1 is port and can be empty for auto assignment
            # ("", "passive"),
            ("COM4", "active_ap"),
            # ("", "active_sta"),
        ]
        start_nodes(nodes)

    # active_ap needs to be started and connected to before startin the server
    # only if using an esp32 as AP of course
    if send_csi_over_wifi:
        if build_flash_monitor:
            raise Exception("wait for the esp32 build before starting the server")
        start_server()
