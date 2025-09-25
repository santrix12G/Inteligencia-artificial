import numpy as np
import plotly.graph_objects as go

# Definimos la ecuación del plano: 2x + 3y + z - 10 = 0
def plano(c1,x,c2,y,c3,i):
    return (i - c1*x - c2*y)/c3

# Crear grilla de puntos (x,y)
x = np.linspace(-5, 5, 30)
y = np.linspace(-5, 5, 30)
X, Y = np.meshgrid(x, y)
Z = plano(-0.16321143,X,0.19252114,Y,-0.10862646,0.50256194)
Z2= plano(0.3241371,X,0.03054328,Y,-0.50709092,0.80362685)

# Crear figura 3D
fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', opacity=0.8)])
fig.add_trace(go.Surface(x=X, y=Y, z=Z2, colorscale='Cividis', opacity=0.8))


fig.show()
