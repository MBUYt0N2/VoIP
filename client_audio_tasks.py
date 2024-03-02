import sounddevice as sd
import numpy as np
import queue

frames = []


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


# def receive_audio(s):
#     while True:
#         data = s.recv(1024)
#         if b"end" in data:
#             break
#         data_len = len(data)
#         if data_len % 2 != 0:
#             data += s.recv(1)
#         audio_array = np.frombuffer(data, dtype=np.int16)
#         print(audio_array[:5])
#         sd.play(audio_array, samplerate=44100)
#         sd.wait()
#         print("playing")
#     print("done")


def receive_audio(s):
    audio_buffer = queue.Queue()

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

    # Stop the stream after all audio has been played
    stream.stop()
    with open("output.json", "w") as f:
        while not audio_buffer.empty():
            i = audio_buffer.get()
            f.write("key : "  + str(i) + "\n")


def audio_callback(outdata, audio_buffer):
    if not audio_buffer.empty():
        sd.play(audio_buffer, samplerate=44100)
        sd.wait()
        outdata[:] = audio_buffer.get().reshape(-1, 1)
    else:
        outdata.fill(0) 


# def receive_audio(s):
#     audio_data = b""
#     while True:
#         data = s.recv(1024)
#         if b"end" in data:
#             break
#         data_len = len(data)
#         if data_len % 2 != 0:
#             data += s.recv(1)
#         audio_data += data
#     print("done")
#     a = random.randint(1, 100)
#     with wave.open(f"output{a}.wav", "wb") as wav_file:
#         wav_file.setnchannels(1)
#         wav_file.setsampwidth(2)  # 2 bytes for int16
#         wav_file.setframerate(44100)
#         wav_file.writeframes(audio_data)
