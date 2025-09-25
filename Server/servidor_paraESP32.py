from flask import Flask, request, jsonify
import os
from datetime import datetime
import cv2
import numpy as np
import serial
import serial.tools.list_ports
import time
import subprocess
import platform

app = Flask(__name__) 


# Configuración Arduino salida
ARDUINO_OUT_PORT = "COM4"
ARDUINO_OUT_BAUDRATE = 9600
ARDUINO_OUT = None

#configuracion arduino entrada
ARDUINO_IN_PORT = "COM6"
ARDUINO_IN_BAUDRATE = 9600
ARDUINO_IN = None

def configurar_permisos_puerto(puerto, ARDUINO_BAUDRATE):
    """
    Configura permisos del puerto COM en Windows
    """
    if platform.system() == "Windows":
        try:
            # Usar mode comando para configurar el puerto
            comando = f'mode {puerto} BAUD={ARDUINO_BAUDRATE} DATA=8 PARITY=N STOP=1'
            result = subprocess.run(comando, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Permisos configurados para {puerto}")
                return True
            else:
                print(f"⚠️  No se pudieron configurar permisos automáticamente")
                return False
                
        except Exception as e:
            print(f"❌ Error configurando permisos: {e}")
            return False
    return True

def liberar_puerto(puerto):
    """
    Intenta liberar el puerto COM
    """
    if platform.system() == "Windows":
        try:
            # Cerrar procesos que puedan estar usando el puerto
            comando = f'for /f "tokens=5" %a in (\'netstat -ano ^| findstr "{puerto}"\') do taskkill /f /pid %a'
            subprocess.run(comando, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(1)
            return True
        except:
            return False
    return True

def conectar_arduino(ARDUINO_PORT,ARDUINO_BAUDRATE,ARDUINO):
    
    if ARDUINO is not None:
        print("✅ Arduino ya está conectado")
        return True
    
    # Primero intentar liberar el puerto si ya está definido
    if ARDUINO_PORT:
        liberar_puerto(ARDUINO_PORT)
    
        try:
            print(f"🔄 Intentando conectar a {ARDUINO_PORT}...")
            
            # Configurar permisos primero
            configurar_permisos_puerto(ARDUINO_PORT, ARDUINO_BAUDRATE)
            
            # Intentar conexión
            arduino1 = serial.Serial(
                port=ARDUINO_PORT,
                baudrate=ARDUINO_BAUDRATE,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1,
                write_timeout=1
            )
            
            time.sleep(2)  # Esperar a que Arduino se reinicie
            
            # Testear conexión
            arduino1.write(b"TEST\n")
            time.sleep(0.1)
            
            if arduino1.in_waiting > 0:
                respuesta = arduino1.readline().decode().strip()
                print(f"✅ Arduino respondió: {respuesta}")
            else:
                print("✅ Conexión establecida (sin respuesta)")
            print(f"✅ Arduino conectado en: {ARDUINO_PORT}")
            ARDUINO = arduino1
            
            return ARDUINO
            
        except serial.SerialException as e:
            print(f"❌ Error en {ARDUINO_PORT}: {e}")
            # continue
        except Exception as e:
            print(f"❌ Error inesperado en {ARDUINO_PORT}: {e}")
            # continue
    
    print("❌ No se pudo conectar a ningún puerto Arduino")
    return None

def enviar_a_arduino(datos, ARDUINO):
    try:
        # Convertir datos a string y enviar
        mensaje = f"{datos}\n"  # Añadir newline para que Arduino sepa que terminó el mensaje
        ARDUINO.write(mensaje.encode())
        print(f"📤 Enviado a Arduino: {mensaje.strip()}")
        
        # Esperar respuesta (opcional)
        time.sleep(0.1)
        if ARDUINO.in_waiting > 0:
            linea = ARDUINO.readline().decode('utf-8', errors='ignore').strip()
            print("📥 Respuesta 1 : ", linea)
            
        return True
        
    except Exception as e:
        print(f"❌ Error enviando a Arduino: {e}")
        return False

def recibir_de_arduino(ARDUINO):
    try:
        if ARDUINO.in_waiting > 0:
            linea = ARDUINO.readline().decode('utf-8', errors='ignore').strip()
            print("📥 Recibido de Arduino: ", linea)
            return linea
        return None
    except Exception as e:
        print(f"❌ Error leyendo de Arduino: {e}")
        return None



#perceptron

def predict(rgb_values):
    
    pesos_verdes=[-0.16321143 ,0.19252114,-0.10862646]
    bias_verdes=[0.50256194]
    perceptron1=Perceptron(pesos_verdes,bias_verdes)    

    pesos_rojos=[ 0.3241371,0.03054328,-0.50709092]
    bias_rojos=[0.80362685]
    perceptron2=Perceptron(pesos_rojos,bias_rojos)
    
    color=-1
    if perceptron1.activacion(rgb_values):
        color=1
    else:
        if perceptron2.activacion(rgb_values):
            color=2
        else:
            color=3
    
    colors = {1:"Verde", 2:"Rojo", 3:"Azul"}
        
    return colors[color]

class Perceptron:
    def __init__(self,pesos,bias):
        self.pesos=pesos
        self.bias=bias
    
    def activacion(self, x):
        z = np.dot(self.pesos, x)
        return 1 if z + self.bias> 0 else 0

# Configuración de servidor
UPLOAD_FOLDER = 'capturas'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

print("=== Servidor de Captura de Imágenes ESP32-CAM ===")
print("Carpeta de destino:", os.path.abspath(UPLOAD_FOLDER))


def procesar_color_imagen(image_data, region_centro_porcentaje=0.3):
    try:
        # Decodificar la imagen
        image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
        
        if image is None:
            return {"error": "Imagen no válida"}
        
        height, width = image.shape[:2]
        
        # Calcular región central
        centro_x, centro_y = width // 2, height // 2
        tamaño_region = int(min(width, height) * region_centro_porcentaje)
        
        # Coordenadas del recuadro central
        x1 = max(0, centro_x - tamaño_region // 2)
        y1 = max(0, centro_y - tamaño_region // 2)
        x2 = min(width, centro_x + tamaño_region // 2)
        y2 = min(height, centro_y + tamaño_region // 2)
        
        # Extraer región central
        region_central = image[y1:y2, x1:x2]
        
        if region_central.size == 0:
            return {"error": "Región central demasiado pequeña"}
        
        # Convertir de BGR a RGB (OpenCV usa BGR por defecto)
        region_rgb = cv2.cvtColor(region_central, cv2.COLOR_BGR2RGB)
        
        # Calcular promedios
        promedio_rgb = np.mean(region_rgb, axis=(0, 1)).astype(int)
        r, g, b = promedio_rgb
        

        return promedio_rgb
        
    except Exception as e:
        return {"error": f"Error procesando color: {str(e)}"}



@app.route('/upload', methods=['POST', 'GET'])
def upload_image():
    try:
        # Verificar método HTTP
        if request.method == 'GET':
            return jsonify({"status": "error", "message": "Use POST method"})
        
        # Recibir imagen binaria
        image_data = request.data
        
        if not image_data or len(image_data) == 0:
            print("❌ No se recibieron datos")
            return jsonify({"status": "error", "message": "No data received"}), 400
        
        print(f"📥 Datos recibidos: {len(image_data)} bytes")
        
        # Crear nombre de archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        filename = f"esp32_{timestamp}.jpg"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Guardar imagen
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        print(f"✅ Imagen guardada: {filename} ({len(image_data)} bytes)")
        
        # Verificar que la imagen sea válida
        try:
            image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
            if image is not None:
                print(f"   📐 Dimensiones: {image.shape[1]}x{image.shape[0]} pixels")
                # Guardar miniatura para verificación
                thumbnail_path = os.path.join(UPLOAD_FOLDER, f"thumb_{filename}")
                cv2.imwrite(thumbnail_path, image)
                rgb=procesar_color_imagen(image_data,0.3)
                print(rgb)
                print("Color predecido",predict(rgb))
                enviar_a_arduino(predict(rgb))
                print(f"   🖼️  Miniatura guardada: thumb_{filename}")
            else:
                print("   ⚠️  Imagen no válida (posiblemente corrupta)")
        except Exception as e:
            print(f"   ⚠️  Error procesando imagen: {e}")
        
        return jsonify({
            "status": "success", 
            "filename": filename,
            "size": len(image_data),
            "message": "Image saved successfully"
        })
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/test', methods=['GET'])
def test_connection():
    return jsonify({
        "status": "active", 
        "message": "Server is running!",
        "endpoints": {
            "upload": "POST /upload",
            "test": "GET /test"
        }
    })

@app.route('/')
def index():
    return jsonify({
        "message": "ESP32-CAM Image Server",
        "version": "1.0",
        "endpoints": {
            "upload": "POST /upload - Send image data",
            "test": "GET /test - Test connection"
        }
    })


if __name__ == '__main__':
    print("\n📡 Servidor iniciado en http://0.0.0.0:5000")
    print("📍 Accesible desde: http://localhost:5000")
    print("📍 O desde tu IP local: http://192.168.1.10:5000")
    print("📁 Imágenes se guardan en:", os.path.abspath(UPLOAD_FOLDER))
    print("\n🟢 Esperando imágenes del ESP32-CAM...")
    print("=" * 60)
    # Solo conectar al Arduino en el proceso principal
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        ARDUINO_IN=conectar_arduino(ARDUINO_IN_PORT,ARDUINO_IN_BAUDRATE,ARDUINO_IN)
    recibir_de_arduino(ARDUINO_IN)
    app.run(host='0.0.0.0', port=5000, debug=True)