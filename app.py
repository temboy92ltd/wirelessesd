from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Danh sách các thiết bị cần mô phỏng
 #devices = ["C2-131", "C2-132", "C2-133", "C2-134","C2-135","C2-136","C2-137","C2-138","C2-139","C2-140","C2-141","C2-142"]

# Danh sách thiết bị: C2-083 → C2-150
addresses = [f'C2-{i:03}' for i in range(81, 151)]
devices = {addr: [] for addr in addresses}

@app.route("/")
def index():
    return render_template("Buiding.html",devices=devices.items())

@app.route("/api/data")
def receive_data():
    data = []
    try:
        json_data = request.get_json()
        addr = json_data.get('address')
        data = json_data.get('data')

        if addr and isinstance(data, list):
            if addr in devices:
                devices[addr] = data
                print(f"[RECV API] {addr}: {data}")
                return jsonify({"status": "OK"}), 200
            else:
                return jsonify({"error": "Unknown device"}), 400
        else:
            return jsonify({"error": "Invalid JSON"}), 400

    except Exception as e:
        print("[ERROR /api/data]", e)
        return jsonify({"error": str(e)}), 500


    # data = []
    # for device in devices:
    #     num_led = random.randint(1, 3)  # từ 1 đến 5 LED
    #     led_data = [random.choice([0, 1]) for _ in range(num_led)]  # 0: đỏ, 1: xanh
    #     data.append({"address": device, "data": led_data})
    # return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)


#/
