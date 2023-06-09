import os
import subprocess
import threading
import time
import keyboard
import http.server
import socketserver

from experiment import Experiment


# Define the request handler class
class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        message = self.rfile.read(content_length).decode('utf-8')
        # Process the message as needed
        if experiment.do_experiment:
            experiment.write_to_file(message)

        # Send a response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Message received")


def start_server():
    # Set up the server
    host = '192.168.4.2'
    port = 80  # Use a specific port number
    with socketserver.TCPServer((host, port), RequestHandler) as server:
        print("Server listening on {}:{}".format(host, port))
        print("make sure Send CSI data over WiFi is enabled")
        server.serve_forever()


if __name__ == '__main__':
    # active_ap needs to be started and connected to before startin the server
    # only if using an esp32 as AP of course also, make sure the setting is selected in
    # menuconfig to enable sending over wifi

    experiment = Experiment()

    start_server()
