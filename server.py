import http.server
import socketserver


# Define the request handler class
class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        message = self.rfile.read(content_length).decode('utf-8')
        print("Received message:", message)

        # Process the message as needed

        # Send a response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Message received")


def handle_message(message):
    message_array = message.split['\n']
    print(len(message_array))
    print(message_array)


if __name__ == '__main__':
    # Set up the server
    host = '192.168.4.2'
    port = 80  # Use a specific port number

    with socketserver.TCPServer((host, port), RequestHandler) as server:
        print("Server listening on {}:{}".format(host, port))
        server.serve_forever()
