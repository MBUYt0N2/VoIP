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

import wave
import numpy as np
import sounddevice as sd


def play_file():
    # Open file
    wav_file = wave.open("receiver.wav", "rb")

    # Read frames and convert to float32
    data = np.frombuffer(
        wav_file.readframes(wav_file.getnframes()), dtype=np.int16
    ).astype(np.float32)

    # Get sample rate
    samplerate = wav_file.getframerate()

    # Play file
    sd.play(data, samplerate)

    # Wait for the file to finish playing
    # sd.wait()

    # Close file
    wav_file.close()


