import pyaudio
import socket

# Create a socket connection.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
host = "10.20.202.60"  # replace with your server's IP address
port = 9999  # replace with your server's port
s.connect((host, port))

# Initalize PyAudio
p = pyaudio.PyAudio()

# Open stream
stream = p.open(
    format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024
)

print("Recording...")

# Record and send audio in chunks
while True:
    data = stream.read(1024)
    s.sendall(data)

# Close the stream
stream.stop_stream()
stream.close()  
p.terminate()
