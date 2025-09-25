import plotly.express as px
import numpy as np
import pandas as pd
import plotly.graph_objects as go

def plano(c1,x,c2,y,c3,i):
    return (i + c1*x +c2*y)/-c3

# ---- Datos ----
entradas = np.array([
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
        [80, 123, 104],
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
        [94, 69, 78],
        [92, 68, 77],
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
        [116, 75, 86],
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
])

# ---- Procesar datos ----
r, g, b = entradas[:,0], entradas[:,1], entradas[:,2]

# Clasificación simple:
# mayor componente define la categoría (R, G o B)
categorias = []
for i in range(len(r)):
    if g[i] >= r[i] and g[i] >= b[i]:
        categorias.append("Verde")
    elif b[i] >= r[i] and b[i] >= g[i]:
        categorias.append("Azul")
    else:
        categorias.append("Rojo")

# Asignar color puro según la categoría
mapa_colores = {
    "Verde": "rgb(0,255,0)",
    "Azul": "rgb(0,0,255)",
    "Rojo": "rgb(255,0,0)"
}
colores_puros = [mapa_colores[c] for c in categorias]

# Crear DataFrame
df = pd.DataFrame({
    "R": r,
    "G": g,
    "B": b,
    "Categoria": categorias,
    "Color": colores_puros
})

# ---- Graficar ----
fig = px.scatter_3d(
    df,
    x="R", y="G", z="B",
    color="Categoria",
    color_discrete_map=mapa_colores,
    title="Espacio RGB: puntos pintados con su color base"
)

fig.update_layout(
    scene=dict(
        xaxis=dict(title="Rojo (R)", range=[0, 255]),
        yaxis=dict(title="Verde (G)", range=[0, 255]),
        zaxis=dict(title="Azul (B)", range=[0, 255]),
        aspectmode="cube"   # 👉 hace que todos los ejes tengan la misma escala
    )
)

# ---- Agregar planos ----
x = np.linspace(0, 255, 100)
y = np.linspace(0, 255, 100)
X, Y = np.meshgrid(x, y)

# Ecuaciones de tus planos
Z1 = plano(-0.16321143,X,0.19252114,Y,-0.10862646,0.50256194)
Z2 = plano(0.3241371,X ,0.03054328,Y,-0.50709092,0.80362685)

fig.add_trace(go.Surface(x=X, y=Y, z=Z1, colorscale='Viridis', opacity=0.6))
fig.add_trace(go.Surface(x=X, y=Y, z=Z2, colorscale='Cividis', opacity=0.6))

fig.show()
