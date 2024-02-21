import socket
import wave
import threading
import sounddevice as sd
import zdynamicip

def receive_broadcast():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    client.bind(("", 37020))
    while True:
        data, addr = client.recvfrom(1024)
        if data:
            return data.decode()

def main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = receive_broadcast()
    port = 9999
    frames = []

    def send_audio():
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

    def receive_audio():
        while True:
            data = s.recv(1024)
            if data == b"end":
                break
            frames.append(data)

        wf = wave.open("receiver.wav", "wb")
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(b"".join(frames))
        wf.close()

        print("Output saved to output.wav.")

    try:
        s.connect((host, port))
        data = s.recv(1024)
        if data == b"start":
            send_audio()
        else:
            threading.Thread(target=receive_audio).start()

    except ConnectionRefusedError:
        print("Connection failed. Is the server running?")
