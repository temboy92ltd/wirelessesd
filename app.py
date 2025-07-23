from flask import Flask, render_template, jsonify, request
import time

app = Flask(__name__)

# Danh sách thiết bị
devices = {
    "C2-081": [],
    "C2-082": [],
    "C2-083": [],
    "C2-084": [],
    "C2-085": [],
    "C2-086": [],
    "C2-087": [],
    "C2-088": [],
    "C2-089": [],
    "C2-140": [],
    "C2-141": [],
    "C2-142": [],
    "C2-112": [],
}
missed_counts = {k: 0 for k in devices}

@app.route("/")
def index():
    return render_template("Buiding.html")
@app.route("/api/data")
def get_data():
    data = []
    for addr, leds in devices.items():
        data.append({"address": addr, "data": leds})
    return jsonify(data)
@app.route("/api/data", methods=["POST"])
def receive_data():
    try:
        json_data = request.get_json()
        addr = json_data.get('address')
        data = json_data.get('data')

        if addr and isinstance(data, list):
            if addr in devices:
                devices[addr] = data
                missed_counts[addr] = 0
                print(f"[RECV API] {addr}: {data}")
                return jsonify({"status": "OK"}), 200
            else:
                return jsonify({"error": "Unknown device"}), 400
        else:
            return jsonify({"error": "Invalid JSON"}), 400

    except Exception as e:
        print("[ERROR /api/data]", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # threading.Thread(target=monitor_devices, daemon=True).start()
    app.run(debug=True, host='0.0.0.0', port=5000)
