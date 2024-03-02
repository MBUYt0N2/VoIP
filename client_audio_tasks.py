import time
import sounddevice as sd
import numpy as np
import queue

frames = []
audio_buffer = queue.Queue()


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
    s.sendall(b"end")


def receive_audio(s):
    global audio_buffer
    stream = sd.OutputStream(callback=audio_callback)
    stream.start()

    while True:
        data = s.recv(1024)
        if b"end" in data:
            break
        data_len = len(data)
        if data_len % 2 != 0:
            data += s.recv(1)
        audio_array = np.frombuffer(data, dtype=np.int16)
        print(audio_array[:5])

        audio_buffer.put(audio_array)

    print("done")

    time.sleep(5)

    stream.stop()


def audio_callback(outdata, frames, time, status):
    global audio_buffer
    if not audio_buffer.empty():
        audio_array = audio_buffer.get()
        outdata[:] = audio_array[:frames].reshape(-1, 1)
        if len(audio_array) > frames:
            audio_buffer.put(audio_array[frames:])
    else:
        outdata.fill(0)
