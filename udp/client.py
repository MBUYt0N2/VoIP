import socket
import threading
import client_audio_tasks as ct


def receive_broadcast():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind(("", 37020))
    while True:
        data, addr = client.recvfrom(16384)
        if data:
            print("received broadcast")
            return data.decode()


def main():

    host = receive_broadcast()
    port = 9999

    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.sendto(b'hello', (host, port))

        data, addr = udp_socket.recvfrom(1024)
        print(socket.inet_ntoa(data))

        threading.Thread(
            target=ct.send_audio, args=(udp_socket, socket.inet_ntoa(data), port)
        ).start()
        threading.Thread(target=ct.receive_audio, args=(udp_socket, socket.inet_ntoa(data), port)).start()

    except ConnectionRefusedError:
        print("Connection failed. Is the server running?")

main()
