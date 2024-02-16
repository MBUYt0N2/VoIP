import socket

# Create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the local machine name
host = "10.20.202.60"  # replace with your server's IP address
port = 9999  # replace with your server's port

# Bind to the port
serversocket.bind((host, port))

# Queue up to 5 requests
serversocket.listen(5)

# Establish a connection
clientsocket1, addr1 = serversocket.accept()
clientsocket2, addr2 = serversocket.accept()

print("Got a connection from %s" % str(addr1))
print("Got a connection from %s" % str(addr2))

while True:
    data = clientsocket1.recv(1024)
    if not data:
        break
    clientsocket2.sendall(data)
