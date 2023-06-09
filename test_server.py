import requests

# Server settings
server_url = 'http://192.168.125.79:80'  # Replace with the appropriate server URL


def test_server():
    # Send test messages
    messages = [
        'Hello',
        'This is a test message',
        'Another message',
        'Testing 123'
    ]

    for message in messages:
        response = requests.post(server_url, data=message)
        print(f"Sent message: {message}")
        print(f"Response: {response.text}\n")


if __name__ == '__main__':
    test_server()
