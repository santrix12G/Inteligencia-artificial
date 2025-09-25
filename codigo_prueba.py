import numpy as np

class Perceptron:
    def __init__(self, n_entradas, tasa_aprendizaje=0.1, epocas=100):
        self.ts = tasa_aprendizaje
        self.epocas = epocas
        self.pesos = np.random.rand(n_entradas) * 2 - 1  # Entre -1 y 1
        self.bias = np.random.rand() * 2 - 1

    def activacion(self, x):
        z = np.dot(self.pesos, x)
        return 1 if z + self.bias > 0 else 0

    def entrenamiento(self, entradas, salidas):
        entradas = np.array(entradas)
        salidas = np.array(salidas)
        
        for epoca in range(self.epocas):
            errores_totales = 0
            
            for i in range(len(entradas)):
                entrada = entradas[i]
                salida_esperada = salidas[i]
                
                prediccion = self.activacion(entrada)
                error = salida_esperada - prediccion
                errores_totales += abs(error)
                
                if error != 0:
                    for j in range(len(self.pesos)):
                        self.pesos[j] += self.ts * entrada[j] * error
                    self.bias += self.ts * error
            
            if errores_totales == 0:
                print(f"Perceptrón convergió en época {epoca + 1}")
                break

    def predecir(self, entrada):
        return self.activacion(entrada)

class MultiPerceptronColor:
    """
    Sistema de 3 perceptrones independientes para clasificar colores
    Cada perceptrón se especializa en detectar UN color específico
    """
    def __init__(self, tasa_aprendizaje=0.1, epocas=100):
        # Crear 3 perceptrones independientes
        self.perceptron_rojo = Perceptron(3, tasa_aprendizaje, epocas)
        self.perceptron_verde = Perceptron(3, tasa_aprendizaje, epocas)
        self.perceptron_azul = Perceptron(3, tasa_aprendizaje, epocas)
        
        # Umbral de confianza para cada perceptrón
        self.threshold_rojo = 0.8
        self.threshold_verde = 0.8
        self.threshold_azul = 0.8
        
        self.entrenado = False
    
    def entrenar_sistema(self):
        """
        Entrena los 3 perceptrones con datos específicos de colores
        """
        print("=== ENTRENANDO SISTEMA MULTI-PERCEPTRÓN ===")
        
        # Datos de entrenamiento RGB normalizados (0-1)
        entradas = [
            # Rojos
            [1.0, 0.0, 0.0], [0.9, 0.1, 0.1], [0.8, 0.2, 0.1], [1.0, 0.3, 0.2],
            # Verdes  
            [0.0, 1.0, 0.0], [0.1, 0.9, 0.1], [0.2, 0.8, 0.1], [0.1, 1.0, 0.3],
            # Azules
            [0.0, 0.0, 1.0], [0.1, 0.1, 0.9], [0.2, 0.1, 0.8], [0.1, 0.3, 1.0],
            # No-colores (grises, mixtos)
            [0.5, 0.5, 0.5], [0.3, 0.3, 0.3], [0.7, 0.7, 0.7], [0.4, 0.6, 0.5]
        ]
        
        # Etiquetas para cada perceptrón
        etiquetas_rojo = [1, 1, 1, 1,  # Rojos = 1
                         0, 0, 0, 0,  # Verdes = 0
                         0, 0, 0, 0,  # Azules = 0
                         0, 0, 0, 0]  # Otros = 0
        
        etiquetas_verde = [0, 0, 0, 0,  # Rojos = 0
                          1, 1, 1, 1,  # Verdes = 1
                          0, 0, 0, 0,  # Azules = 0
                          0, 0, 0, 0]  # Otros = 0
        
        etiquetas_azul = [0, 0, 0, 0,  # Rojos = 0
                         0, 0, 0, 0,  # Verdes = 0
                         1, 1, 1, 1,  # Azules = 1
                         0, 0, 0, 0]  # Otros = 0
        
        # Entrenar cada perceptrón
        print("Entrenando detector de ROJO...")
        self.perceptron_rojo.entrenamiento(entradas, etiquetas_rojo)
        
        print("Entrenando detector de VERDE...")
        self.perceptron_verde.entrenamiento(entradas, etiquetas_verde)
        
        print("Entrenando detector de AZUL...")
        self.perceptron_azul.entrenamiento(entradas, etiquetas_azul)
        
        self.entrenado = True
        print("✅ Sistema entrenado completamente\n")
    
    def predecir(self, rgb_values):
        """
        Predice el color usando los 3 perceptrones
        
        Args:
            rgb_values: Lista [R, G, B] con valores 0-255
            
        Returns:
            Tupla (color_predicho, confianzas)
        """
        if not self.entrenado:
            print("⚠️ Sistema no entrenado. Entrenando primero...")
            self.entrenar_sistema()
        
        # Normalizar RGB a 0-1
        rgb_norm = np.array(rgb_values) / 255.0
        
        # Obtener predicciones de cada perceptrón
        pred_rojo = self.perceptron_rojo.predecir(rgb_norm)
        pred_verde = self.perceptron_verde.predecir(rgb_norm)
        pred_azul = self.perceptron_azul.predecir(rgb_norm)
        
        predicciones = [pred_rojo, pred_verde, pred_azul]
        colores = ["Rojo", "Verde", "Azul"]
        
        # Contar cuántos perceptrones activaron
        activaciones = sum(predicciones)
        
        if activaciones == 0:
            return "Indefinido", predicciones
        elif activaciones == 1:
            # Solo un perceptrón activó - predicción clara
            indice = predicciones.index(1)
            return colores[indice], predicciones
        else:
            # Múltiples perceptrones activaron - conflicto
            return "Conflicto", predicciones
    
    def probar_sistema(self):
        """
        Prueba el sistema con colores de ejemplo
        """
        if not self.entrenado:
            self.entrenar_sistema()
        
        print("=== PROBANDO SISTEMA ===")
        
        colores_prueba = [
            [255, 50, 50],
            [200, 20, 20],
            [150, 0, 0],
            [180, 45, 45],
            [255, 120, 80],
            [220, 10, 10],
            [190, 35, 35],
            [139, 0, 0],
            [255, 99, 71],
            [178, 34, 34],
            [205, 92, 92],
            [165, 42, 42],
            [128, 0, 0],
            [255, 0, 0],
            [220, 20, 60],
            [255, 140, 0],
            [165, 40, 40],
            [210, 80, 80],
            [255, 182, 193],
            [250, 128, 114],
            [0, 255, 0],
            [50, 205, 50],
            [34, 139, 34],
            [0, 128, 0],
            [107, 142, 35],
            [144, 238, 144],
            [46, 139, 87],
            [0, 100, 0],
            [127, 255, 0],
            [85, 107, 47],
            [152, 251, 152],
            [0, 255, 127],
            [0, 153, 51],
            [193, 255, 193],
            [50, 200, 0],
            [90, 170, 90],
            [189, 183, 107],
            [140, 190, 140],
            [124, 252, 0],
            [0, 139, 139],
            [0, 0, 255],
            [0, 0, 128],
            [0, 191, 255],
            [25, 25, 112],
            [65, 105, 225],
            [135, 206, 235],
            [70, 130, 180],
            [30, 144, 255],
            [100, 149, 237],
            [0, 0, 205],
            [173, 216, 230],
            [0, 70, 140],
            [95, 158, 160],
            [112, 128, 144],
            [100, 110, 150],
            [0, 255, 255],
            [0, 0, 139],
            [72, 61, 139],
            [25, 25, 112],
            [0, 191, 255]
        ]
        
        rojos=0
        verdes=0
        azules=0
        indefinido=0
        for rgb in colores_prueba:
            prediccion, activaciones = self.predecir(rgb)
            print(f"{rgb} -> {prediccion:10} | R:{activaciones[0]} G:{activaciones[1]} B:{activaciones[2]}")
            if(sum(activaciones)==0):
                indefinido+=1
            else:
                rojos+=activaciones[0]
                verdes+=activaciones[1]
                azules+=activaciones[2]
        
        print("Verdes",verdes)
        print("Rojos",rojos)
        print("Azules",azules)
        print("Indefinido",indefinido)

# Función para integrar con la cámara
def crear_sistema_camara():
    """
    Crea el sistema multi-perceptrón para usar con la cámara
    """
    sistema = MultiPerceptronColor(tasa_aprendizaje=0.1, epocas=50)
    sistema.entrenar_sistema()
    return sistema

if __name__ == "__main__":
    # Crear y probar el sistema
    sistema = MultiPerceptronColor()
    sistema.probar_sistema()
    
    print("\n=== EJEMPLO DE USO CON CÁMARA ===")
    print("Para usar con la cámara, reemplaza PerceptronColor con MultiPerceptronColor")
    print("y cambia el método predict() por predecir()")