# tk_qr_window.py
import tkinter as tk
import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import base64  
from recon import QRCodeProcessor

# Crear la ventana principal
root = ctk.CTk()
root.title("Cámara Web con Detección de QR y OpenCV")
root.geometry("800x600")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Crear un frame para contener el canvas y otros widgets
frame = ctk.CTkFrame(root, width=750, height=500)
frame.pack(padx=20, pady=20, expand=True, fill="both")

# Crear un canvas donde se mostrará la cámara web
canvas = ctk.CTkCanvas(frame, width=640, height=480, bg="black")
canvas.pack(padx=10, pady=10, expand=True)

# Instanciar el procesador de QR
try:
    processor = QRCodeProcessor()
except Exception as e:
    print(e)
    exit()

# Flag para pausar la detección tras un QR
detection_paused = False

def unpause_detection():
    global detection_paused
    detection_paused = False

def update_frame():
    global detection_paused

    frame_capture, qr_text = processor.process_frame()
    if frame_capture is None:
        print("No se pudo leer el frame")
        root.after(10, update_frame)
        return

    # Si se detecta un QR y aún no está en pausa
    if qr_text and not detection_paused:
        try:
            decoded = base64.b64decode(qr_text)
            print("Valor del QR (base64 decodificado):", decoded)
        except Exception:
            print("Valor del QR:", qr_text)
        # Aquí podrías realizar la inserción a la base de datos
        # Por ejemplo: requests.post(url, data=...) o similar

        # Activar la pausa para evitar múltiples inserciones
        detection_paused = True
        root.after(4000, unpause_detection)  # Se reactiva la detección después de 2 segundos

    # Convertir el frame de BGR a RGB para mostrarlo en Tkinter
    frame_rgb = cv2.cvtColor(frame_capture, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    img_tk = ImageTk.PhotoImage(img)

    # Mostrar el frame en el canvas
    canvas.create_image(0, 0, image=img_tk, anchor="nw")
    canvas.image = img_tk

    # Programar la próxima actualización
    root.after(10, update_frame)

# Iniciar la actualización del frame
update_frame()

# Etiqueta de título
label_title = ctk.CTkLabel(root, text="Cámara Web con Detección de QR", font=("Arial", 20, "bold"))
label_title.pack(pady=10)

# Etiqueta informativa
label_info = ctk.CTkLabel(root, text="Presiona ESC para salir", font=("Arial", 14))
label_info.pack(pady=5)

# Función para salir con la tecla ESC
def on_close(event):
    processor.release()
    root.quit()

# Asociar la tecla ESC para salir
root.bind("<Escape>", on_close)

# Ejecutar la aplicación
root.mainloop()

# Liberar recursos al cerrar
processor.release()
