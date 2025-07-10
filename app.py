from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
import serial

app = Flask(__name__)
socketio = SocketIO(app)

ALL_ADDRS = [f'C2-{100 + i}' for i in range(50)]
led_status = {addr: [] for addr in ALL_ADDRS}

@app.route('/')
def index():
    return render_template('index.html', devices=led_status.items())

def read_serial():
    try:
        ser = serial.Serial('COM4', 9600)
        print("[OK] COM4 đã kết nối.")
        while True:
            line = ser.readline().decode().strip()
            if not line or ',' not in line:
                continue

            addr, data = line.split(',', 1)
            leds = [int(c) for c in data.strip() if c in '01']

            if addr in led_status:
                led_status[addr] = leds
            else:
                led_status[addr] = leds  # nếu địa chỉ mới bất ngờ xuất hiện

            socketio.emit('led_update', {'addr': addr, 'leds': leds})
            print(f"[RECV] {addr} -> {leds}")
    except Exception as e:
        print(f"[ERR] COM lỗi: {e}")

if __name__ == '__main__':
    threading.Thread(target=read_serial, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=False)
