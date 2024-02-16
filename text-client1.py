import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "10.20.202.60"
port = 9999


def receive_message():
    while True:
        data = s.recv(1024)
        if not data:
            continue
        else:
            print(data.decode("ascii"))


def send_message():
    while True:
        message = input("Enter your message: ")
        s.send(message.encode("ascii"))


try:
    s.connect((host, port))
    threading.Thread(target=receive_message).start()
    threading.Thread(target=send_message).start()
except ConnectionRefusedError:
    print("Connection failed. Is the server running?")
