import sounddevice as sd
import numpy as np


frames = []


# def send_audio(s):
#     samplerate = 44100
#     duration = 5
#     print("Recording...")
#     myrecording = sd.rec(
#         int(samplerate * duration), samplerate=samplerate, channels=1, dtype="int16"
#     )
#     sd.wait()

#     for i in range(0, len(myrecording)):
#         data = myrecording[i].tobytes()
#         s.sendall(data)

#     print("Recording finished.")


def send_audio(s):
    samplerate = 44100
    duration = 5
    print("Recording...")

    def callback(indata, frames, time, status):
        data = indata.tobytes()
        s.sendall(data)

    with sd.InputStream(
        callback=callback, channels=1, samplerate=samplerate, dtype="int16"
    ):
        sd.sleep(duration * 1000)

    print("Recording finished.")


def receive_audio(s):
    while True:
        data = s.recv(1024)
        if b"end" in data:
            break
        data_len = len(data)
        if data_len % 2 != 0:
            data += s.recv(1)
        audio_array = np.frombuffer(data, dtype=np.int16)
        print(audio_array[:5])
        sd.play(audio_array, samplerate=44100)
        sd.wait()
        print("playing")
    print("done")
