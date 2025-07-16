from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

devices = {}  # Lưu trạng thái ESP32

@app.route("/")
def index():
    return render_template("index.html", devices=devices.items())

@app.route("/api/data", methods=["POST"])
def receive_data():
    data = request.json
    address = data.get("address")
    leds = data.get("data")

    if address and leds:
        devices[address] = leds
        # Gửi dữ liệu đến tất cả client
        socketio.emit("update_device", {"address": address, "data": leds})
        return jsonify({"status": "ok"}), 200

    return jsonify({"error": "Invalid data"}), 400

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
