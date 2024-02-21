import socket

def receive_broadcast():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    client.bind(("", 37020))
    while True:
        data, addr = client.recvfrom(1024)
        if data:
            return data.decode()

host = receive_broadcast()
port = 9999  # Assuming the server is listening on port 5000

# Rest of your code...