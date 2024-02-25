#!/usr/bin/env python3
import socket
import threading
import zdynamicip
import time

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = zdynamicip.get_server_ip()
port = 9999

serversocket.bind((host, port))
print(f"Running on {host}")
serversocket.listen(2)


def broadcast_ip(ip):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server.settimeout(0.2)
    server.bind(("", 44444))
    while True:
        server.sendto(ip.encode(), ("<broadcast>", 37020))
        time.sleep(2)


clients = []


def receive_connection():
    while True:
        clientsocket, addr = serversocket.accept()
        print(f"Got a connection from {str(addr)}")
        clients.append(clientsocket)
        if len(clients) >= 2:
            for i in clients:
                i.sendall(b"start")
            threading.Thread(target=send_message, args=(clients)).start()


def send_message(*clients):
    while True:
        data = [sender.recv(1024) for sender in clients]

        if any(not d for d in data):
            break
        for i, receiver in enumerate(clients):
            if i == 0:
                receiver.sendall(data[1])
            else:
                receiver.sendall(data[0])
    for receiver in clients:
        receiver.sendall(b"end")
        receiver.close()


threading.Thread(target=receive_connection).start()
threading.Thread(target=broadcast_ip, args=(host,)).start()
