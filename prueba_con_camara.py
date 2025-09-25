import cv2
import numpy as np


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
    

class ColorDetector:
    def __init__(self):
        self.cap = None
        
    def initialize_camera(self, camera_index=0):
        """Inicializa la cámara"""
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise Exception("No se pudo acceder a la cámara")
        
        # Configurar resolución (opcional)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1028)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1028)
        
    def get_center_color(self, frame, region_size=100):
        """
        Obtiene el color promedio del centro de la imagen
        """
        height, width = frame.shape[:2]
        center_x, center_y = width // 2, height // 2
        
        # Definir región central
        x1 = max(0, center_x - region_size // 2)
        y1 = max(0, center_y - region_size // 2)
        x2 = min(width, center_x + region_size // 2)
        y2 = min(height, center_y + region_size // 2)
        
        # Extraer región de interés
        roi = frame[y1:y2, x1:x2]
        
        # Calcular color promedio (BGR en OpenCV, convertimos a RGB)
        mean_color_bgr = np.mean(roi, axis=(0, 1))
        mean_color_rgb = [mean_color_bgr[2], mean_color_bgr[1], mean_color_bgr[0]]  # BGR -> RGB
        
        return mean_color_rgb, (x1, y1, x2, y2)
    
    def run_detection(self):
        """
        Ejecuta la detección en tiempo real
        """
        if self.cap is None:
            self.initialize_camera()
        
        print("Presiona 'q' para salir, 'c' para capturar y clasificar")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Obtener color del centro
            rgb_values, region_coords = self.get_center_color(frame)
            
            # Dibujar rectángulo de muestreo
            cv2.rectangle(frame, (region_coords[0], region_coords[1]), 
                         (region_coords[2], region_coords[3]), (0, 255, 0), 2)
            
            # Mostrar valores RGB
            rgb_text = f"RGB: ({int(rgb_values[0])}, {int(rgb_values[1])}, {int(rgb_values[2])})"
            cv2.putText(frame, rgb_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Clasificar con el perceptrón
            predicted_color = predict(rgb_values)
            
            # Mostrar predicción
            prediction_text = f"Prediccion: {predicted_color}"
            cv2.putText(frame, prediction_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Mostrar frame
            cv2.imshow('Detector de Colores', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('c'):
                # Captura manual para análisis detallado
                print(f"\n--- CAPTURA ---")
                print(f"Valores RGB: {rgb_values}")
                print(f"Color predicho: {predicted_color}")
                print("---------------\n")
        
        self.cleanup()
    
    def cleanup(self):
        """Libera recursos"""
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()

# Función para probar con colores específicos
# def test_with_manual_colors():
#     """
#     Función para probar el perceptrón con valores RGB manuales
#     """
#     perceptron = PerceptronColor()
    
#     # Colores de prueba
#     test_colors = {
#         "Rojo puro": [255, 0, 0],
#         "Verde puro": [0, 255, 0],
#         "Azul puro": [0, 0, 255],
#         "Rojo oscuro": [150, 50, 50],
#         "Verde claro": [100, 200, 100],
#         "Azul marino": [50, 50, 150],
#         "Blanco": [255, 255, 255],
#         "Negro": [0, 0, 0]
#     }
    
#     print("=== PRUEBAS CON COLORES MANUALES ===")
#     for color_name, rgb_values in test_colors.items():
#         predicted, activations = perceptron.predict(rgb_values)
#         print(f"{color_name} {rgb_values} -> {predicted} (Act: R:{activations[0]:.2f} G:{activations[1]:.2f} B:{activations[2]:.2f})")

if __name__ == "__main__":
    # Primero probar con colores manuales
    # test_with_manual_colors()
    
    print("\n=== INICIANDO DETECCIÓN CON CÁMARA ===")
    print("Asegúrate de tener buena iluminación")
    print("Coloca objetos de colores frente a la cámara")
    
    try:
        detector = ColorDetector()
        detector.run_detection()
    except Exception as e:
        print(f"Error: {e}")
        print("Verifica que tu cámara esté disponible y que tengas OpenCV instalado")