# import socket

# def receive_broadcast():
#     client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
#     client.bind(("", 37020))
#     while True:
#         data, addr = client.recvfrom(1024)
#         if data:
#             return data.decode()

# host = receive_broadcast()
# port = 9999  # Assuming the server is listening on port 5000

# # Rest of your code...

import sounddevice as sd
import soundfile as sf

def play_file(filename):
    # Read file
    data, samplerate = sf.read(filename, dtype='float32')

    # Play file
    sd.play(data, samplerate)

    # Wait for the file to finish playing
    sd.wait()

play_file('receiver.wav')