import sounddevice as sd
import numpy as np
import queue
import webrtcvad
from scipy.signal import butter, lfilter

frames = []
audio_buffer = queue.Queue()
vad = webrtcvad.Vad()
vad.set_mode(1)
lowcut = 300  
highcut = 3000


def butter_bandpass(lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype="band")
    return b, a


# Apply the band-pass filter to the incoming audio data
def butter_bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def send_audio(s):
    samplerate = 96000
    duration = 50
    print("Recording...")

    def callback(indata, frames, time, status):
        data = indata.tobytes()  # Convert to 1D array for filtering
        s.sendall(data)


    with sd.InputStream(
        callback=callback, channels=1, samplerate=samplerate, dtype="float32"
    ):
        sd.sleep(duration * 1000)

    print("Recording finished.")
    s.sendall(b"end")


def receive_audio(s):
    global audio_buffer
    samplerate = 96000
    dtype = "float32"
    channels = 1
    stream = sd.OutputStream(
        callback=audio_callback, samplerate=samplerate, channels=channels, dtype=dtype
    )

    stream.start()

    while True:
        data = s.recv(1024)
        if b"end" in data:
            break
        data_len = len(data)
        if data_len % 2 != 0:
            data += s.recv(1)
        audio_array = np.frombuffer(data, dtype=np.float32)
        print(f"audio array : {len(audio_array)}")

        pad_size = 480 - (len(audio_array) % 480)
        audio_array = np.pad(audio_array, (0, pad_size))
        audio_frames = audio_array.reshape(-1, 480).tolist()
        # audio_frames = [
        #     frame
        #     for frame in audio_frames
        #     if vad.is_speech(np.array(frame, dtype=np.float32).tobytes(), samplerate)
        # ]

        audio_frames = [
            butter_bandpass_filter(np.array(frame), lowcut, highcut, samplerate)
            for frame in audio_frames
        ]
        audio_buffer.put(np.array(audio_frames).flatten())

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
