from flask import Flask, render_template, jsonify, request
import time

app = Flask(__name__)

# Bộ nhớ tạm lưu trạng thái các thiết bị
device_states = {}

@app.route("/")
def index():
    return render_template("Buiding.html")

# 🟢 API ESP32 gửi dữ liệu vào
@app.route("/api/update", methods=["POST"])
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
    threading.Thread(target=monitor_devices, daemon=True).start()
    app.run(debug=True, host='0.0.0.0', port=5000)
