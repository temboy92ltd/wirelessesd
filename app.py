from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# Danh sách địa chỉ từ C2-081 đến C2-151
devices = {f'C2-{i:03}': [] for i in range(81, 152)}

@app.route("/")
def index():
    return render_template("Buiding.html")

# ESP32 gửi dữ liệu vào đây qua POST
@app.route("/api/data", methods=["POST"])
def get_data():
    try:
        json_data = request.get_json()
        addr = json_data.get('address')
        data = json_data.get('data')

        if addr in devices and isinstance(data, list):
            devices[addr] = data
            print(f"[RECEIVED] {addr}: {data}")
            return jsonify({"status": "OK"}), 200
        else:
            return jsonify({"error": "Invalid address or data"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500    
        
# Frontend lấy dữ liệu qua GET
@app.route("/api/data", methods=["GET"])
def get_data():
    return jsonify([
        {"address": addr, "data": devices[addr]} for addr in devices
    ])

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
