import cv2
import numpy as np
import requests
import os
import time
from datetime import datetime

IP_WEBCAM_URL = "http://192.168.1.23:8080/photo.jpg"
SAVE_PATH = "./capturas/"
os.makedirs(SAVE_PATH, exist_ok=True)

CAPTURE_INTERVAL = 2   # cada 2 segundos
MOTION_THRESHOLD = 50000  # sensibilidad (ajustar según pruebas)

last_frame = None

def capture_frame():
    response = requests.get(IP_WEBCAM_URL, timeout=5)
    if response.status_code != 200:
        return None
    img_array = np.frombuffer(response.content, dtype=np.uint8)
    return cv2.imdecode(img_array, cv2.IMREAD_COLOR)

def detect_motion(frame, last_frame):
    if last_frame is None:
        return False

    # Convertir a gris para simplificar
    gray1 = cv2.cvtColor(last_frame, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calcular diferencia
    diff = cv2.absdiff(gray1, gray2)
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    # Calcular área de movimiento
    motion_pixels = np.sum(thresh > 0)
    return motion_pixels > MOTION_THRESHOLD

def save_frame(frame):
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
    filepath = os.path.join(SAVE_PATH, filename)
    cv2.imwrite(filepath, frame)
    print(f"📸 Movimiento detectado → guardado en {filepath}")

if __name__ == "__main__":
    print("🚀 Detector de movimiento iniciado...")
    while True:
        frame = capture_frame()
        if frame is None:
            print("⚠️ Error obteniendo frame")
            continue

        if detect_motion(frame, last_frame):
            save_frame(frame)

        last_frame = frame
        time.sleep(CAPTURE_INTERVAL)
