from flask import Flask, render_template, redirect, url_for
import threading
import client
from flask_cors import CORS
import client_audio_tasks as ct


app = Flask(__name__)
CORS(
    app, resources={r"/run-script": {"origins": "*"}}
)

@app.route("/")
def home():
    return render_template("client.html")


@app.route("/run-script", methods=["POST"])
def run_script():
    threading.Thread(target=client.main).start()
    return redirect(url_for("call_screen"))

@app.route("/call-screen")
def call_screen():
    return render_template("call-screen.html")


@app.route("/start-audio", methods=["POST"])
def start_audio():
    threading.Thread(target=client.listen_for_data).start()
    return "Started audio"


@app.route("/mute-audio", methods=["POST"])
def mute_audio():
    ct.mute()
    return "muted audio"


@app.route("/close-socket", methods=["POST"])
def close_socket():
    client.close_sock()
    return "Closed socket"


if __name__ == "__main__":
    app.run(port=3000)
