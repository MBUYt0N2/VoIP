# import sounddevice as sd
# import soundfile as sf

# samplerate = 44100  # Sample rate in Hertz
# duration = 3  # Duration in seconds

# # Record audio
# myrecording = sd.rec(
#     int(samplerate * duration), samplerate=samplerate, channels=1, dtype="float32"
# )
# sd.wait()  # Wait for the recording to finish

# # Save to file
# sf.write("output.wav", myrecording, samplerate)

import pydub
import sounddevice as sd


def x():
    samplerate = 48000
    duration = 5
    print("Recording...")
    audio_segments = []  # List to store the incoming audio data

    def callback(indata, frames, time, status):
        # Convert the indata array to bytes and ensure it's the correct length
        data = indata.tobytes()
        if (
            len(data) % (2 * 1) == 0
        ):  # 2 is the sample width, 1 is the number of channels
            encoded_audio = pydub.AudioSegment(
                data, frame_rate=96000, sample_width=2, channels=1
            )
            audio_segments.append(encoded_audio)  # Append the audio data to the list

    with sd.InputStream(
        callback=callback, channels=1, samplerate=samplerate, dtype="int16"
    ):
        sd.sleep(duration * 1000)

    print("Recording finished.")

    # Concatenate all the audio segments into a single audio segment
    if audio_segments:
        recorded_audio = sum(audio_segments)
        # Export the recorded audio to a file
        recorded_audio.export("recorded_audio.wav", format="wav")
    else:
        print("No audio data was recorded.")


x()
