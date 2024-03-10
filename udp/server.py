#!/usr/bin/env python3
import socket
import threading
import zdynamicip
import time

serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host = zdynamicip.get_server_ip()
port = 9999

serversocket.bind((host, port))
print(f"Running on {host}")


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
        data, addr = serversocket.recvfrom(1024)
        print(f"Got a connection from {str(addr)}")
        clients.append(addr)
        if len(clients) >= 2:
            for client in clients:
                serversocket.sendto(socket.inet_aton(addr[0]), client)


threading.Thread(target=receive_connection).start()
threading.Thread(target=broadcast_ip, args=(host,)).start()
