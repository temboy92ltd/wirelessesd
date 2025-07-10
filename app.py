from flask import Flask, render_template, request, jsonify
import threading
import time

app = Flask(__name__)

# Danh sách thiết bị: C2-101 → C2-150
addresses = [f'C2-{100+i}' for i in range(1, 51)]
devices = {addr: [] for addr in addresses}
missed_counts = {addr: 0 for addr in addresses}

# Số lượt không nhận được → reset về "chưa có dữ liệu"
MAX_MISSED = 5

@app.route('/')
def index():
    return render_template('index.html', devices=devices.items())

@app.route('/api/data', methods=['POST'])
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

def monitor_devices():
    while True:
        time.sleep(2)
        for addr in addresses:
            if missed_counts[addr] < MAX_MISSED:
                missed_counts[addr] += 1
            if missed_counts[addr] >= MAX_MISSED:
                devices[addr] = []

if __name__ == '__main__':
    threading.Thread(target=monitor_devices, daemon=True).start()
    app.run(debug=True, host='0.0.0.0', port=5000)
