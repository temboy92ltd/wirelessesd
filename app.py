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
def update_data():
    content = request.json
    address = content.get("address")
    data = content.get("data")
    if address and data:
        device_states[address] = {
            "data": data,
            "timestamp": time.time()
        }
        return jsonify({"status": "ok"}), 200
    return jsonify({"error": "invalid data"}), 400

# 🟢 Frontend lấy dữ liệu về
@app.route("/api/data")
def get_data():
    result = []
    for address, info in device_states.items():
        result.append({
            "address": address,
            "data": info["data"]
        })
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
