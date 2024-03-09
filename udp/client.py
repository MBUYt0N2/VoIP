import socket
import threading
import client_audio_tasks as ct


def receive_broadcast():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind(("", 37020))
    while True:
        data, addr = client.recvfrom(16384)
        if data:
            return data.decode()


def main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = receive_broadcast()
    port = 9999

    try:
        s.connect((host, port))
        data = s.recv(16384)
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        threading.Thread(
            target=ct.send_audio, args=(udp_socket, socket.inet_ntoa(data), port)
        ).start()
        threading.Thread(target=ct.receive_audio, args=(udp_socket, socket.inet_ntoa(data), port)).start()

    except ConnectionRefusedError:
        print("Connection failed. Is the server running?")

main()
