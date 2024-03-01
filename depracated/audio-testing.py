import sounddevice as sd
import soundfile as sf

samplerate = 44100  # Sample rate in Hertz
duration = 3  # Duration in seconds

# Record audio
myrecording = sd.rec(
    int(samplerate * duration), samplerate=samplerate, channels=1, dtype="float32"
)
sd.wait()  # Wait for the recording to finish

# Save to file
sf.write("output.wav", myrecording, samplerate)


