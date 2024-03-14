import sounddevice as sd
import numpy as np
import queue
import socket
import g711
import time

frames = []
audio_buffer = queue.Queue()
last_received_audio = None
sending = True
muter = False


class StreamEnd(Exception):
    pass


def end_call(s):
    global sending
    sending = False
    s.close()


def mute():
    global muter
    muter = True if muter == False else False


def send_audio(s, host, port):
    global sending
    global muter
    samplerate = 48000
    print("Recording...")

    def callback(indata, frames, time_info, status):
        global sending
        data = indata.astype(np.float32)
        encoded_audio = g711.encode_ulaw(data)
        if muter:
            print("muted")
            time.sleep(0.1)
        elif sending:
            s.sendto(encoded_audio, (host, port))
        elif not sending:
            print("Connection closed")
            raise sd.CallbackStop

    with sd.InputStream(
        callback=callback, channels=1, samplerate=samplerate, dtype="float32"
    ):
        while sending:
            sd.sleep(1000)


def receive_audio(s, host, port):
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

    while sending:
        data, addr = s1.recvfrom(16384)
        try:
            decoded_audio = g711.decode_ulaw(data)
            audio_buffer.put(decoded_audio)
            print(decoded_audio[:5])
        except Exception as e:
            print("Failed to decode packets", str(e))

    print("done")

    stream.stop()
    s1.close()
    s.close()


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
