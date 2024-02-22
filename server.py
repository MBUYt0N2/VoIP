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
        server.sendto(ip.encode(), ('<broadcast>', 37020))
        time.sleep(1)


clients = []

def receive_connection():
    while True:
        clientsocket, addr = serversocket.accept()
        print(f"Got a connection from {str(addr)}")
        clients.append(clientsocket)
        if len(clients) % 2 == 0 and len(clients) != 0:
            clients[-2].sendall(b"start")  
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
threading.Thread(target=broadcast_ip, args=(host,)).start()