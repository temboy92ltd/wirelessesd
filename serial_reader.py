# serial_reader.py
import serial
import threading

latest_data = {}  # Dạng: {'C2-100': '010'}

def read_serial():
    global latest_data
    try:
        ser = serial.Serial('COM4', 9600, timeout=1)
        while True:
            line = ser.readline().decode().strip()
            if line.startswith("C2-"):
                try:
                    address, leds = line.split(",")
                    latest_data[address] = leds
                except:
                    pass
    except Exception as e:
        print("Lỗi đọc COM:", e)

# Chạy luồng đọc serial khi import
threading.Thread(target=read_serial, daemon=True).start()
