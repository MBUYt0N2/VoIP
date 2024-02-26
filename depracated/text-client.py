import socket
import threading
import sys
import termios
import tty

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "10.20.202.60"
port = 9999

def receive_message():
    while True:
        data = s.recv(1024)
        if not data:
            continue
        else:
            print(f"Received message: {data.decode('ascii')}")


def send_message():
    while True:
        message = getch()
        if message == "\x1b": 
            s.close()
            print("\nConnection closed.")
            break
        else:
            s.send(message.encode("ascii"))


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


try:
    s.connect((host, port))
    threading.Thread(target=receive_message).start()
    threading.Thread(target=send_message).start()
except ConnectionRefusedError:
    print("Connection failed. Is the server running?")
