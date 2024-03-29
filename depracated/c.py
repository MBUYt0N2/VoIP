# # import socket

# # def receive_broadcast():
# #     client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# #     client.bind(("", 37020))
# #     while True:
# #         data, addr = client.recvfrom(1024)
# #         if data:
# #             return data.decode()

# # host = receive_broadcast()
# # port = 9999  # Assuming the server is listening on port 5000

# # # Rest of your code...

# import wave
# import numpy as np
# import sounddevice as sd


# def play_file():
#     # Open file
#     wav_file = wave.open("receiver.wav", "rb")

#     # Read frames and convert to float32
#     data = np.frombuffer(
#         wav_file.readframes(wav_file.getnframes()), dtype=np.int16
#     ).astype(np.float32)

#     # Get sample rate
#     samplerate = wav_file.getframerate()

#     # Play file
#     sd.play(data, samplerate)

#     # Wait for the file to finish playing
#     # sd.wait()

#     # Close file
#     wav_file.close()


# import numpy as np
# import sounddevice as sd
# import wave
# import queue

# # Open the .wav file
# wav_file = wave.open("receiver.wav", "rb")

# # Extract the audio data
# nchannels, sampwidth, framerate, nframes, comptype, compname = wav_file.getparams()
# frames = wav_file.readframes(nframes)
# data = np.frombuffer(frames, dtype=np.int16)

# # Create a buffer for the audio data
# audio_buffer = queue.Queue()
# audio_buffer.put(data)


# def audio_callback(outdata, frames, time, status):
#     if not audio_buffer.empty():
#         # Get the next audio array from the buffer
#         audio_array = audio_buffer.get()

#         # Only take as many frames as outdata can hold
#         outdata[:] = audio_array[:frames].reshape(-1, 1)

#         # Put the remaining frames back into the buffer
#         audio_buffer.put(audio_array[frames:])
#     else:
#         # If the buffer is empty, fill outdata with zeros (silence)
#         outdata.fill(0)


# # Create and start the output stream
# stream = sd.OutputStream(
#     samplerate=framerate, channels=nchannels, callback=audio_callback
# )
# stream.start()
# fuck this

# # Wait for the stream to finish playing the audio
# while stream.active:
#     sd.sleep(5)

# # Stop the stream
# stream.stop()

import sounddevice as sd
import numpy as np
from scipy.signal import butter, lfilter
from scipy.io.wavfile import write

# Set the filter parameters
lowcut = 300  # Lower cutoff frequency in Hz
highcut = 3000  # Higher cutoff frequency in Hz
samplerate = 44100  # Sample rate
duration = 5


# Create the band-pass filter using Butterworth design
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


print("Recording...")
audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=2)
sd.wait()  # Wait until recording is finished
print("Recording complete")

filtered_audio = butter_bandpass_filter(
    audio[:, 0], lowcut, highcut, samplerate, order=4
)

# Save the filtered audio to a WAV file
write("output.wav", samplerate, filtered_audio)
print("Saved filtered audio to 'output.wav'")
