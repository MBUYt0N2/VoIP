import socket
import threading

# Create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the local machine name
host = "10.20.202.60"
port = 9999

# Bind to the port
serversocket.bind((host, port))

# Queue up to 5 requests
serversocket.listen(5)

clients = []


def receive_conn():
    while True:
        clientsocket, addr = serversocket.accept()
        print(f"Got a connection from {str(addr)} at {str(clientsocket)}")
        clients.append(clientsocket)
        if len(clients) == 2:
            send_message(
                clients[0], "You are connected with another client".encode("ascii")
            )
            send_message(
                clients[1], "You are connected with another client".encode("ascii")
            )
            threading.Thread(target=receive_message).start()


def send_message(clientsocket, message):
    clientsocket.send(message)


def receive_message():
    while True:
        data = clients[0].recv(1024)
        if data:
            send_message(clients[1], data)
        data = clients[1].recv(1024)
        if data:
            send_message(clients[0], data)


threading.Thread(target=receive_conn).start()
