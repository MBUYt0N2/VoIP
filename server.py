#!/usr/bin/env python3 
import socket
import threading
import zdynamicip

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = zdynamicip.get_server_ip()
port = 9999

serversocket.bind((host, port))
print(f"Running on {host}")
serversocket.listen(2)

clients = []

def receive_connection():
    while True:
        clientsocket, addr = serversocket.accept()
        print(f"Got a connection from {str(addr)}")
        clients.append(clientsocket)
        if len(clients) % 2 == 0 and len(clients) != 0:
            clients[0].sendall(b"start")  
            threading.Thread(
                target=send_message, args=(clients[-2], clients[-1])
            ).start()


def send_message(sender, reciever):
    while True:
        data = sender.recv(1024)

        if not data:
            break
        reciever.sendall(data)
    reciever.sendall(b"end")

threading.Thread(target=receive_connection).start()
