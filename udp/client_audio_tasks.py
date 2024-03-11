import sounddevice as sd
import numpy as np
import queue
import pydub
import socket

frames = []
audio_buffer = queue.Queue()


def send_audio(s, host, port):
    samplerate = 96000
    duration = 50
    print("Recording...")

    def callback(indata, frames, time, status):
        data = indata.tobytes()
        encoded_audio = pydub.AudioSegment(
            data, frame_rate=96000, sample_width=2, channels=1
        )
        s.sendto(encoded_audio.raw_data, (host, port))

    with sd.InputStream(
        callback=callback, channels=1, samplerate=samplerate, dtype="int16"
    ):
        sd.sleep(duration * 1000)

    print("Recording finished.")

def receive_audio(s1, host, port):
    s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s1.bind(("", 9000))   
    global audio_buffer
    samplerate = 96000
    dtype = "int16"
    channels = 1
    stream = sd.OutputStream(
        callback=audio_callback, samplerate=samplerate, channels=channels, dtype=dtype
    )

    stream.start()

    while True:
        data, addr = s1.recvfrom(16384)
        if b"end" in data:
            break

        g711_encoded_audio = pydub.AudioSegment(
            data, frame_rate=samplerate, sample_width=2, channels=1
        )
        decoded_audio = np.frombuffer(g711_encoded_audio.raw_data, dtype=np.int16)

        audio_buffer.put(decoded_audio)
        print(decoded_audio[:5])

    print("done")

    stream.stop()


def audio_callback(outdata, frames, time, status):
    global audio_buffer
    while len(outdata) > 0:
        if not audio_buffer.empty():
            audio_array = audio_buffer.get()
            print(f"queue :  {audio_buffer.qsize()}")
            chunk = min(len(outdata), len(audio_array))
            outdata[:chunk] = audio_array[:chunk].reshape(-1, 1)
            outdata = outdata[chunk:]
            if len(audio_array) > chunk:
                audio_buffer.put(audio_array[chunk:])
        else:
            outdata.fill(0)
            break
