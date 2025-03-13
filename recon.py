# qr_detector.py (versión modificada)
import cv2
import numpy as np
import time

class QRCodeProcessor:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise Exception("No se abrió la cámara")
        self.detector = cv2.QRCodeDetector()
        self.last_qr = None
        self.last_detection_time = 0
        self.cooldown = 2  # Tiempo en segundos antes de aceptar otra detección

    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None

        # Convertir a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        qr_text, points, _ = self.detector.detectAndDecode(gray)
        current_time = time.time()

        if qr_text and points is not None:
            # Solo imprimir si es un QR nuevo o si se cumplió el cooldown
            if qr_text != self.last_qr or (current_time - self.last_detection_time) >= self.cooldown:
                print("Valor del QR:", qr_text)
                self.last_qr = qr_text
                self.last_detection_time = current_time

            # Dibujar el contorno del QR
            points = np.int32(points).reshape(-1, 2)
            cv2.polylines(frame, [points], isClosed=True, color=(0, 255, 0), thickness=2)
        return frame, qr_text

    def release(self):
        self.cap.release()
