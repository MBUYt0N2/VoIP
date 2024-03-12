import sounddevice as sd
import numpy as np
import queue
import socket
import g711

frames = []
audio_buffer = queue.Queue()
last_received_audio = None


def send_audio(s, host, port):
    samplerate = 48000
    duration = 50
    print("Recording...")

    def callback(indata, frames, time, status):
        data = indata.astype(np.float32)
        encoded_audio = g711.encode_ulaw(data)
        s.sendto(encoded_audio, (host, port))

    with sd.InputStream(
        callback=callback, channels=1, samplerate=samplerate, dtype="int16"
    ):
        sd.sleep(duration * 1000)

    print("Recording finished.")
    s.sendto(b"end", (host, port))


def receive_audio(s1, host, port):
    s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s1.bind(("", 9000))
    global audio_buffer
    global last_received_audio
    samplerate = 48000
    dtype = "float32"
    channels = 1
    stream = sd.OutputStream(
        callback=audio_callback, samplerate=samplerate, channels=channels, dtype=dtype
    )

    stream.start()

    while True:
        data, addr = s1.recvfrom(16384)
        if data == b"end":
            break

        if data:
            decoded_audio = g711.decode_ulaw(data)
            last_received_audio = decoded_audio
        else:
            # If no data was received, use the last received audio
            decoded_audio = last_received_audio

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
