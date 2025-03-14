import customtkinter as ctk
import cv2
import numpy as np
from PIL import Image, ImageTk
import ctypes
import os
from recon import QRCodeProcessor 


lib_path = os.path.abspath("/home/astartes/Escritorio/portafolio/recon/libliblib.so")
lib = ctypes.CDLL(lib_path)

# Configurar la firma de la función para probar conexión
lib.test_mysql_connection.restype = ctypes.c_int
lib.test_mysql_connection.argtypes = [
    ctypes.c_char_p, ctypes.c_uint16, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p
]

# Configurar la función para insertar datos
lib.insert_into_mysql.restype = ctypes.c_int
lib.insert_into_mysql.argtypes = [
    ctypes.c_char_p, ctypes.c_uint16, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p
]

# -------------------------------
# Crear la ventana principal con customtkinter
root = ctk.CTk()
root.title("QR Scanner y Conexión MySQL")
root.geometry("800x700")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# -------------------------------
# Layout 1: Login para conexión a MySQL
frame_login = ctk.CTkFrame(root, width=750, height=400, corner_radius=15)
frame_login.pack(padx=20, pady=20, expand=True, fill="both")

# Label de cabecera en el login (posicionado con place para mostrarlo en coordenadas específicas)
header_label = ctk.CTkLabel(frame_login, text="Bienvenido: Ingrese los datos de conexión", font=("Arial", 18))
header_label.place(x=150, y=20)

title_label = ctk.CTkLabel(frame_login, text="Conectar a MySQL", font=("Arial", 20, "bold"))
title_label.pack(pady=40)

entry_host = ctk.CTkEntry(frame_login, placeholder_text="Host (ej. localhost)")
entry_host.pack(pady=5)

entry_port = ctk.CTkEntry(frame_login, placeholder_text="Puerto (ej. 3306)")
entry_port.pack(pady=5)

entry_user = ctk.CTkEntry(frame_login, placeholder_text="Usuario (ej. root)")
entry_user.pack(pady=5)

entry_password = ctk.CTkEntry(frame_login, placeholder_text="Contraseña", show="*")
entry_password.pack(pady=5)

entry_database = ctk.CTkEntry(frame_login, placeholder_text="Base de datos (ej. Inventario)")
entry_database.pack(pady=5)

# Label para mostrar el estado de la conexión en el login
result_label = ctk.CTkLabel(frame_login, text="", font=("Arial", 14))
result_label.pack(pady=10)

# -------------------------------
# Layout 2: Cámara y detección de QR (inicialmente oculto)
frame_camera = ctk.CTkFrame(root, width=750, height=500, corner_radius=15)

canvas = ctk.CTkCanvas(frame_camera, width=640, height=320, bg="black")
canvas.pack(padx=10, pady=10, expand=True)

# Label para mostrar el estado de inserción en el layout de cámara
camera_status_label = ctk.CTkLabel(frame_camera, text="", font=("Arial", 14))
camera_status_label.pack(pady=10)

# Inicializar el procesador de QR (definido en recon.py)
processor = QRCodeProcessor()

# Variable de control para evitar múltiples inserciones en un corto período
detected = False

def reset_detected():
    global detected
    detected = False

def update_frame():
    global detected
    frame_capture, qr_text = processor.process_frame()
    if frame_capture is None:
        root.after(10, update_frame)
        return

    if qr_text and not detected:
        detected = True
        print("QR Detectado:", qr_text)
        insertar_qr(qr_text)  # Insertar en la BD
        # Reinicia la detección después de 2 segundos sin bloquear la interfaz
        root.after(2000, reset_detected)

    # Mostrar el frame en el canvas
    frame_rgb = cv2.cvtColor(frame_capture, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    img_tk = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, image=img_tk, anchor="nw")
    canvas.image = img_tk

    root.after(10, update_frame)

def insertar_qr(data):
    """Inserta el QR en MySQL llamando a la función Rust."""
    host = entry_host.get()
    port = int(entry_port.get())
    user = entry_user.get()
    password = entry_password.get()
    database = entry_database.get()
    result = lib.insert_into_mysql(host.encode(), port, user.encode(), password.encode(), database.encode(), data.encode())
    if result == 1:
        camera_status_label.configure(text="✅ QR Registrado", text_color="green")
        import sound 
        sound.done()
        print("✅ QR insertado en MySQL")
        root.after(2000, lambda: camera_status_label.configure(text=""))
    else:
        camera_status_label.configure(text="❌ Error en la inserción", text_color="red")
        print("❌ Error en la inserción")

def test_connection():
    try:
        port = int(entry_port.get())
    except ValueError:
        result_label.configure(text="El puerto debe ser un número", text_color="red")
        return

    host_val = entry_host.get().encode("utf-8")
    user_val = entry_user.get().encode("utf-8")
    password_val = entry_password.get().encode("utf-8")
    database_val = entry_database.get().encode("utf-8")

    result = lib.test_mysql_connection(host_val, port, user_val, password_val, database_val)
    if result == 1:
        result_label.configure(text="✅ Conexión Exitosa", text_color="green")
        # Espera 1 segundo y cambia de layout sin bloquear la UI
        root.after(1000, cambiar_a_camera)
    else:
        result_label.configure(text="❌ Error en la conexión", text_color="red")

def cambiar_a_camera():
    """Oculta el login y muestra el layout de la cámara."""
    frame_login.pack_forget()
    frame_camera.pack(padx=20, pady=20, expand=True, fill="both")
    update_frame()

# Botón en el login para probar la conexión
test_button = ctk.CTkButton(frame_login, text="Conectar", command=test_connection)
test_button.pack(pady=15)

def on_close(event):
    processor.release()  # Libera la cámara (definido en recon.py)
    root.quit()

root.bind("<Escape>", on_close)
root.mainloop()
