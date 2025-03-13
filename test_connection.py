import ctypes

# Cargar la biblioteca compartida
lib = ctypes.CDLL("/home/astartes/Escritorio/portafolio/recon/liblib.so")  # Cambia la ruta según el sistema

# Configurar el tipo de retorno y argumentos
lib.insert_into_mysql.restype = ctypes.c_int
lib.insert_into_mysql.argtypes = [ctypes.c_char_p]

# Datos a insertar en la base de datos
data = "Este es un ejemplo de QR o dato".encode("utf-8")

# Llamar a la función en Rust
result = lib.insert_into_mysql(data)

# Verificar el resultado
if result == 1:
    print("✅ Inserción exitosa en la base de datos MySQL")
else:
    print("❌ Error al insertar en la base de datos")
