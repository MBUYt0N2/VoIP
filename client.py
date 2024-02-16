import pyaudio
import socket
import wave

# Create a socket connection.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
host = "10.20.202.95"  # replace with your server's IP address
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
frames = []
for i in range(0, int(44100 / 1024 * 5)):  # 5 seconds of audio
    data = stream.read(1024)
    s.sendall(data)
    frames.append(data)

print("Recording finished.")

# Close the stream
stream.stop_stream()
stream.close()
p.terminate()

# Save the recording as a wave file
wf = wave.open("output.wav", "wb")
wf.setnchannels(1)
wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
wf.setframerate(44100)
wf.writeframes(b"".join(frames))
wf.close()

print("Output saved to output.wav.")
