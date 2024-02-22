import sounddevice as sd
import numpy as np


frames = []


def send_audio(s):
    samplerate = 44100
    duration = 5
    print("Recording...")
    myrecording = sd.rec(
        int(samplerate * duration), samplerate=samplerate, channels=1, dtype="int16"
    )
    sd.wait()

    for i in range(0, len(myrecording)):
        data = myrecording[i].tobytes()
        s.sendall(data)

    print("Recording finished.")


def receive_audio(s):
    while True:
        data = s.recv(1024)
        if data == b"end":
            break
        # frames.append(data)

        data_len = len(data)
        if data_len % 2 != 0:
            data += s.recv(1)
        print("Playing")
        audio_array = np.frombuffer(data, dtype=np.int16)
        sd.play(audio_array, samplerate=44100)
