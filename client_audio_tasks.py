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
        frames.append(data)

    # wf = wave.open("receiver.wav", "wb")
    # wf.setnchannels(1)
    # wf.setsampwidth(2)
    # wf.setframerate(44100)
    # wf.writeframes(b"".join(frames))
    # wf.close()

    # print("Output saved to output.wav.")

    audio_data = b"".join(frames)
    audio_array = np.frombuffer(audio_data, dtype=np.int16)
    sd.play(audio_array, samplerate=44100)
