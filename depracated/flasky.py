from flask import Flask, render_template
import threading
import client  
from flask_cors import CORS


app = Flask(__name__)
CORS(
    app, resources={r"/run-script": {"origins": "*"}}
)  # Replace with your actual frontend domain

@app.route("/")
def home():
    return render_template("cleint.html")


@app.route("/run-script", methods=["POST"])
def run_script():
    threading.Thread(target=client.main).start()
    return "Script is running", 200


if __name__ == "__main__":
    app.run(port=5000)
