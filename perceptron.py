import numpy as np
import random

class Perceptron:
    def __init__(self,pesos,bias):
        self.pesos=pesos
        self.bias=bias
        
    def __init__(self, n_entradas, tasa_aprendizaje=0.1, epocas=100):
        self.ts= tasa_aprendizaje
        self.epocas = epocas
        self.pesos = np.random.rand(n_entradas)
        self.bias=random.random()

    def activacion(self, x):
        z = np.dot(self.pesos, x)
        return 1 if z + self.bias> 0 else 0

    def entrenamiento(self, entradas, salidas):
        total_bias=set()
        total_pesos1=[]
        total_pesos2=[]
        total_pesos3=[]
        cont_error=[]
        for _ in range(self.epocas):
            j=0
            error_total=0
            for entrada in entradas:
                z=self.activacion(entrada)
                error = salidas[j] - z
                error_total+=error**2
                for i in range(len(self.pesos)):
                    self.pesos[i]+=(self.ts*entrada[i]*error)
                self.bias+= self.ts * error
                total_bias.add(self.bias)
                j+=1
            cont_error.append(error_total)
            total_pesos1.append(self.pesos[0])
            total_pesos2.append(self.pesos[1])
            total_pesos3.append(self.pesos[2])
        
        print("pesos 1 : [",end="")
        for pesos1 in total_pesos1:
            print(pesos1,end=",")
        print("]")
        print("Pesos 2: [",end="")
        for pesos2 in total_pesos2:
            print(pesos2,end=",")
        print("]")
        print("Pesos 3 : [",end="")
        for pesos3 in total_pesos3:
            print(pesos3,end=",")
        print("]")
        print("Bias: [",end="")
        for bias in total_bias:
            print(bias,end=",")
        print("]")
        print("Errores: [",end="")
        for error in cont_error:
            print(error,end=",")   
        print("]")         
        

if __name__=="__main__":
    entradas_verdes = np.array([
        [0,   255, 0], #verde
        [30,  200, 30],#verde
        [60,  220, 40],#verde
        [50,  180, 50],#verde
        [70,  240, 60],#verde
        [20,  210, 20],#verde
        [40,  190, 40],#verde
        [10,  230, 30],#verde
        [80,  200, 70],#verde
        [90,  250, 80],#verde
        [0, 255, 0],    # Verde 
        [50, 205, 50],  # Verde 
        [34, 139, 34],  # Verde 
        [0, 100, 0],    # Verde 
        [127, 255, 0],  # verde
        [46, 139, 87],  # Verde 
        [144, 238, 144],# Verde  
        [107, 142, 35], # Verde 
        [0, 128, 0],    # Verde 
        [152, 251, 152], # Verde
        [0, 255, 0],
        [0, 255, 255],
        [54, 103, 85],
        [57, 109, 86],
        [56, 108, 85],
        [56, 108, 86],
        [57, 108, 85],
        [57, 74, 62],
        [59, 76, 63],
        [58, 76, 64],
        [58, 76, 65],
        [59, 76, 65],
        [76, 83, 67],
        [91, 117, 90],
        [86, 121, 93],
        [85, 121, 93],
        [85, 121, 94],
        [86, 121, 94],
        [87, 118, 89],
        [79, 115, 92],
        [79, 116, 94],
        [79, 115, 93],
        [79, 115, 94],
        [77, 111, 91],
        [50, 133, 116],
        [44, 122, 108],
        [54, 113, 87],
        [58, 113, 85],
        [58, 113, 86],
        [45, 75, 64],
        [57, 122, 95],
        [60, 122, 92],
        [59, 122, 93],
        [69, 95, 82],
        [78, 124, 106],
        [81, 123, 104],
        [80, 123, 104]
    ])
    salidas_verdes= np.full(len(entradas_verdes),1)

    entradas_rojos=[
        [255, 0,   0],#rojo
        [200, 30,  20],#rojo
        [180, 50,  40],#rojo
        [150, 40,  60],#rojo
        [220, 60,  50],#rojo
        [240, 30,  70],#rojo
        [210, 80,  90],#rojo
        [190, 40,  30],#rojo
        [230, 20,  20],#rojo
        [255, 100, 90],#rojo
        [255, 0, 0],   #rojo 
        [220, 20, 60],#rojo
        [178, 34, 34], #rojo
        [139, 0, 0],  #rojo
        [255, 69, 0], #rojo 
        [205, 92, 92], #rojo
        [240, 128, 128],#rojo
        [128, 0, 0],  #rojo
        [255, 99, 71],  #rojo
        [196, 30, 58],  #rojo
        [255, 0, 0],
        [255, 255, 0],
        [114, 61, 67],
        [114, 61, 68],
        [114, 61, 69],
        [157, 75, 86],
        [160, 74, 85],
        [161, 74, 85],
        [159, 74, 87],
        [109, 75, 84],
        [106, 74, 85],
        [107, 73, 84],
        [106, 73, 83],
        [106, 73, 84],
        [107, 73, 83],
        [108, 73, 83],
        [114, 75, 86],
        [116, 75, 85],
        [115, 75, 84],
        [116, 75, 86]
    ]

    salidas_rojos=np.full(len(entradas_rojos),1)

    entradas_azules=[
        [0, 0, 255],      # Azul Puro (Estándar)
        [0, 0, 128],      # Azul Marino (Navy Blue)
        [100, 149, 237],  # Azul Acero (Cornflower Blue)
        [65, 105, 225],   # Azul Real
        [0, 191, 255],    # Azul Cielo Profundo
        [70, 130, 180],   # Azul Grisáceo (Steel Blue)
        [0, 255, 255],    # Cian Puro (Aqua)
        [0, 128, 128],    # Teal
        [173, 216, 230],  # Azul Claro (Light Blue)
        [135, 206, 235],  # Azul Cielo
        [30, 144, 255],   # Azul Dodjer
        [25, 25, 112],    # Azul Medianoche
        [0, 139, 139],    # Azul Oscuro de Mar (Dark Cyan)
        [10, 50, 100],    # Azul Profundo Oscuro
        [0, 70, 150],     # Azul Zafiro
        [15, 82, 186],    # Azul Cobalto
        [138, 43, 226],   # Azul Violeta (Blue Violet)
        [176, 224, 230],  # Azul Polvo
        [5, 10, 150],     # Azul Tinta
        [0, 51, 102],     # Azul Cerúleo Oscuro
        [0, 0, 255],
        [38, 42, 47],
        [40, 61, 84],
        [41, 62, 84],
        [35, 38, 43],
        [40, 43, 49],
        [39, 44, 49],
        [39, 43, 47],
        [38, 43, 48],
        [39, 43, 48],
        [40, 43, 48],
        [36, 40, 47],
        [53, 56, 68],
        [58, 61, 78],
        [58, 61, 77],
        [73, 71, 90],
        [65, 68, 89],
        [64, 68, 89],
        [65, 68, 88],
        [43, 82, 123],
        [44, 82, 123],
        [43, 82, 124],
        [36, 40, 46],
        [36, 40, 45],
        [38, 42, 46]
    ]
    salidas_azules=np.full(len(entradas_azules),1)

    entradas_cualquieras = np.array([
    # Tonos grises
        [50, 50, 50],     # gris oscuro
        [80, 80, 80],
        [100, 100, 100],
        [120, 120, 120],
        [150, 150, 150],
        [180, 180, 180],
        [200, 200, 200],
        [220, 220, 220],
        [240, 240, 240],  # gris muy claro
        [30, 30, 30],     # casi negro
        [139, 69, 19],    # saddle brown
        [160, 82, 45],    # sienna
        [165, 42, 42],    # brown
        [210, 105, 30],   # chocolate
        [205, 133, 63],   # peru
        [244, 164, 96],   # sandy brown
        [222, 184, 135],  # burlywood
        [210, 180, 140],  # tan
        [188, 143, 143],  # rosy brown
        [255, 228, 196]   # bisque (marrón muy claro)
    ])

    salidas_cualquieras=np.full(len(entradas_cualquieras),0)


    epocas=50
    tasa_aprendizaje=0.001

    print("Entrenando perceptrones...")
    print("error del primero perceptron")
    #primer perceptron solo clasifica verde(1) y no es verde(0)
    perceptron1=Perceptron(3,tasa_aprendizaje,epocas)
    entradas_verdes=np.vstack((entradas_verdes,entradas_cualquieras))
    salidas_verdes=np.hstack((salidas_verdes,salidas_cualquieras))
    perceptron1.entrenamiento(entradas_verdes,salidas_verdes)

    print("error del segundo perceptron")
    #segundo perceptron clasifica rojo(1) y azul (0)
    perceptron2=Perceptron(3,tasa_aprendizaje,epocas)
    entradas_rojos=np.vstack((entradas_rojos,entradas_azules))
    salidas_rojos=np.hstack((salidas_rojos,np.zeros(len(entradas_azules))))

    perceptron2.entrenamiento(entradas_rojos,salidas_rojos)
    
    #Salidad esperada de 20 verdes, 20 rojos y 20 azules
    Ejemplos_complicado = [
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

    #Salidad esperada de 10 verdes, 10 rojos y 10 azules
    Ejemplos_simple=[
        [255, 0, 0],
        [0, 255, 0],
        [0, 0, 255],
        [200, 30, 20],
        [30, 200, 30],
        [20, 30, 200],
        [180, 50, 40],
        [60, 220, 40],
        [40, 60, 220],
        [150, 40, 60],
        [50, 180, 50],
        [60, 50, 180],
        [220, 60, 50],
        [70, 240, 60],
        [50, 70, 240],
        [240, 30, 70],
        [20, 210, 20],
        [30, 20, 210],
        [210, 80, 90],
        [40, 190, 40],
        [90, 40, 190],
        [190, 40, 30],
        [10, 230, 30],
        [30, 10, 230],
        [230, 20, 20],
        [80, 200, 70],
        [70, 80, 200],
        [200, 70, 80],
        [255, 100, 90],
        [90, 255, 100],
        [100, 90, 255]
    ]

    Ejemplos_complicado=np.vstack((Ejemplos_complicado,Ejemplos_simple))
    rojos=0
    verdes=0
    azules=0
    for entradas in Ejemplos_complicado:
        z=perceptron1.activacion(entradas)
        if z:
            verdes+=1
        else:
            z2=perceptron2.activacion(entradas)
            if z2:
                rojos+=1
            else:
                azules+=1
    print("Perceptron 1")
    print("Pesos",perceptron1.pesos)
    print("Bias",perceptron1.bias)
    print("Perceptron 2")
    print("Pesos",perceptron2.pesos)
    print("Bias",perceptron2.bias)
    print("Cantidad de verdes",verdes)
    print("Cantidad de rojos :",rojos)
    print("Cantidad de azules",azules)
    #Salidad espreradad debe ser 20 azules, 20 rojos y 20 verdes
    