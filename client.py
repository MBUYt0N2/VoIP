import pyaudio
import socket
import wave
import threading
import random

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "10.20.202.95" 
port = 9999  
p = pyaudio.PyAudio()
frames = []


def send_audio():
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=1024,
    )

    print("Recording...")
    for i in range(0, int(44100 / 1024 * 5)): 
        data = stream.read(1024)
        s.sendall(data)

    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    p.terminate()


# Save the recording as a wave file
def receive_audio():
    while True:
        data = s.recv(1024)
        if data == b"end":  
            break
        frames.append(data)

    x = random.randint(0, 100000)
    wf = wave.open(f"output{x}.wav", "wb")
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100)
    wf.writeframes(b"".join(frames))
    wf.close()

    print("Output saved to output.wav.")


try:
    s.connect((host, port))
    data = s.recv(1024)
    if data == b"start":
        send_audio()
    else:
        threading.Thread(target=receive_audio).start()

except ConnectionRefusedError:
    print("Connection failed. Is the server running?")
