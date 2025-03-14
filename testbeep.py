import ctypes
import os

# Cargar la biblioteca compartida libbeep.so (asumiendo que está en el mismo directorio)
lib_path = os.path.abspath("libbeep.so")
lib = ctypes.CDLL(lib_path)

# Configurar la firma de la función beep_function:
# double frequency, double duration, int sample_rate -> int
lib.beep_function.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_int]
lib.beep_function.restype = ctypes.c_int

# Configurar la firma de error_beep y done_beep (sin parámetros, void)
lib.error_beep.argtypes = []
lib.error_beep.restype = None

lib.done_beep.argtypes = []
lib.done_beep.restype = None

# Probar la función beep_function
print("Ejecutando beep_function(1000, 0.3, 44100)...")
if lib.beep_function(1000.0, 0.3, 44100):
    print("Beep ejecutado exitosamente.")
else:
    print("Error al ejecutar beep.")

# Probar la secuencia de error
print("Ejecutando error_beep()...")
lib.error_beep()
print("Secuencia error_beep ejecutada.")

# Probar done (sin sonido)
print("Ejecutando done_beep()...")
lib.done_beep()
print("done_beep ejecutado.")
