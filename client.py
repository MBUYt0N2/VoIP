import socket
import threading
import client_audio_tasks as ct


def receive_broadcast():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind(("", 37020))
    while True:
        data, addr = client.recvfrom(1024)
        if data:
            return data.decode()


def main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = receive_broadcast()
    port = 9999

    try:
        s.connect((host, port))
        data = s.recv(1024)
        if data == b"start":
            threading.Thread(target=ct.send_audio, args=(s,)).start()
            threading.Thread(target=ct.receive_audio, args=(s,)).start()

    except ConnectionRefusedError:
        print("Connection failed. Is the server running?")
