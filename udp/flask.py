from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

mute_status = False
connected = False

@app.route('/mute', methods=['POST'])
def mute():
    global mute_status
    mute_status = not mute_status
    return jsonify({'status': 'success', 'mute_status': mute_status})

@app.route('/unmute', methods=['POST'])
def unmute():
    global mute_status
    mute_status = not mute_status
    return jsonify({'status': 'success', 'mute_status': mute_status})

@app.route('/connect', methods=['POST'])
def connect():
    global connected
    connected = True
    return jsonify({'status': 'success', 'connected': connected})

@app.route('/disconnect', methods=['POST'])
def disconnect():
    global connected
    connected = False
    return jsonify({'status': 'success', 'connected': connected})

@app.route('/')
def index():
    return render_template('index.html', mute_status=mute_status, connected=connected)

if __name__ == '__main__':
    app.run(debug=True)
