import sounddevice as sd
import numpy as np
import queue
import socket
import g711
from zfec import easyfec

frames = []
audio_buffer = queue.Queue()
fec_encoder = easyfec.Encoder(10, 12)
fec_decoder = easyfec.Decoder(10, 12)
last_received_audio = None

def send_audio(s, host, port):
    samplerate = 48000
    print("Recording...")

    def callback(indata, frames, time, status):
        data = indata.astype(np.float32)
        encoded_audio = g711.encode_ulaw(data)
        sharenums, padlen, packets, _ = fec_encoder.encode(encoded_audio)
        for packet in packets:
            s.sendto(packet + bytes([sharenums, padlen]), (host, port))

    with sd.InputStream(
        callback=callback, channels=1, samplerate=samplerate, dtype="int16"
    ):
        while True:
            sd.sleep(1000)

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

    packets = []  # Define the packets list here

    while True:
        data, addr = s1.recvfrom(16384)
        if data == b"end":
            break

        packets.append(data[:-2])
        if len(packets) >= 12:  # 10 data packets + 2 FEC packets
            try:
                sharenums = data[-2]
                padlen = data[-1]
                decoded_data = fec_decoder.decode(packets, sharenums, padlen)
                decoded_audio = g711.decode_ulaw(decoded_data)
                audio_buffer.put(decoded_audio)
                print(decoded_audio[:5])
            except Exception as e:
                print("Failed to decode packets", str(e))
                packets = []

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
