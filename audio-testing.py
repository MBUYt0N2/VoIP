import pyaudio
import wave

# Set constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "file.wav"

# Initialize PyAudio

# Start recording
audio = pyaudio.PyAudio()
stream = audio.open(
    format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=3, frames_per_buffer=CHUNK
)
print("recording...")
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print("finished recording")

# Stop recording
stream.stop_stream()
stream.close()
audio.terminate()

# Save recording as a .wav file
waveFile = wave.open(WAVE_OUTPUT_FILENAME, "wb")
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b"".join(frames))
waveFile.close()

