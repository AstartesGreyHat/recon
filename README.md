# Registro de Personal con QR

Este proyecto es un sistema de registro de personal basado en la lectura de códigos QR. Está diseñado para empresas y organizaciones que buscan una manera eficiente y segura de gestionar la entrada y salida de su personal. La aplicación utiliza Python con `customtkinter` para la interfaz gráfica, OpenCV para el procesamiento de imágenes y una base de datos MySQL para almacenar todos los registros de asistencia en tiempo real. Además, se integra con una biblioteca en C para la generación de sonidos de confirmación al escanear correctamente un código QR.

## Características
- Escaneo rápido y preciso de códigos QR para registrar entradas y salidas del personal.
- Almacenamiento seguro de los datos en MySQL, con integridad garantizada y soporte para múltiples usuarios.
- Interfaz gráfica moderna y personalizable creada con `customtkinter`.
- Confirmación sonora de registros exitosos mediante una biblioteca en C que utiliza PortAudio.
- Seguridad mejorada con credenciales de conexión configurables y cifradas para mayor protección.
- Soporte para múltiples departamentos y cargos dentro de la organización, permitiendo un control detallado del personal.
- Funcionalidad modular que permite la integración con otros sistemas de control de acceso.

## Requisitos
### Dependencias
Antes de ejecutar el proyecto, asegúrate de instalar los siguientes paquetes de Python ejecutando:

```bash
pip install -r requirements.txt
```

Además, es necesario contar con `PortAudio` para el sistema de sonidos. En Linux, puedes instalarlo con:

```bash
sudo apt-get install portaudio19-dev
```

### Base de Datos (parte en progreso)
Este proyecto está diseñado para funcionar con MySQL. Antes de utilizarlo, asegúrate de crear la base de datos y la tabla correspondiente ejecutando la siguiente consulta SQL:

```sql
CREATE TABLE registros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    identificacion VARCHAR(50) UNIQUE NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    departamento VARCHAR(100) NOT NULL,
    cargo VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    telefono VARCHAR(20),
    foto LONGBLOB
);
```

Esta estructura permite almacenar toda la información esencial del personal, incluyendo una fotografía opcional, garantizando que cada registro sea único y pueda consultarse fácilmente en el futuro.

## Instalación y Uso
Para comenzar a utilizar el sistema de registro de personal, sigue estos pasos:

1. Clona el repositorio desde GitHub y accede al directorio del proyecto:

```bash
git clone https://github.com/AstartesGreyHat/recon.git
cd recon
```

4. Ejecuta la aplicación gráfica con el siguiente comando:

```bash
python Ui.py
```

## Uso de la Aplicación
1. Ingresa los datos de conexión a la base de datos MySQL en la interfaz de usuario.
2. Presiona el botón "Conectar" para verificar la conexión con la base de datos.
3. Una vez conectado, la cámara se activará y podrás escanear códigos QR.
4. Si el código QR es válido y se detecta correctamente, los datos serán almacenados en la base de datos y se emitirá un sonido de confirmación.
5. La interfaz cambiará temporalmente de color para indicar que el escaneo fue exitoso.
6. Los registros pueden ser consultados desde MySQL para su análisis y control.

## Contribuciones
Si deseas contribuir con mejoras o nuevas características al proyecto, puedes hacer un fork del repositorio, realizar los cambios y enviar un pull request. Se aceptan contribuciones en los siguientes aspectos:
- Mejoras en la interfaz gráfica.
- Optimización del procesamiento de QR.
- Implementación de nuevas características, como la generación de reportes o la integración con otras plataformas.

## Licencia
Este proyecto está distribuido bajo la licencia MIT, lo que significa que puedes usarlo, modificarlo y distribuirlo libremente, siempre y cuando se otorgue el crédito correspondiente al autor original. Se recomienda leer el archivo `LICENSE` para más detalles.

