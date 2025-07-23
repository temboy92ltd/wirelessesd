from flask import Flask, render_template, jsonify, request
import threading

app = Flask(__name__)
devices = {}  # Cập nhật từ ESP32

@app.route("/")
def index():
    return render_template("Buiding.html")

# ESP32 gửi dữ liệu vào đây
@app.route("/api/update", methods=["POST"])
def receive_data():
    try:
        json_data = request.get_json()
        addr = json_data.get('address')
        data = json_data.get('data')

        if addr and isinstance(data, list):
            devices[addr] = data
            print(f"[RECV API] {addr}: {data}")
            return jsonify({"status": "OK"}), 200
        else:
            return jsonify({"error": "Invalid JSON"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Web frontend gọi để lấy dữ liệu mới
@app.route("/api/data")
def get_data():
    return jsonify([
        {"address": addr, "data": data} for addr, data in devices.items()
    ])

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
