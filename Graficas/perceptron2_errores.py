import matplotlib.pyplot as plt
import numpy as np

# Datos de errores por época
errores = [5.0,3.0,2.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

# Limpiar datos de errores (eliminar valores no numéricos)
errores_limpios = []
for error in errores:
    if isinstance(error, (int, float)):
        errores_limpios.append(error)
    else:
        errores_limpios.append(0.0)  # Reemplazar valores no numéricos con 0

# Número de épocas
epocas = range(1, len(errores_limpios) + 1)

# Crear la gráfica
plt.figure(figsize=(12, 6))
plt.plot(epocas, errores_limpios, label='Error Total', linewidth=2, marker='o', markersize=4, color='red')

# Configuración de la gráfica
plt.xlabel('Épocas', fontsize=12)
plt.ylabel('Error Total', fontsize=12)
plt.title('Evolución del Error durante el Entrenamiento', fontsize=14)
plt.grid(True, alpha=0.3)
plt.xticks(np.arange(0, len(epocas) + 1, 5))

# Añadir anotaciones para los puntos importantes
plt.annotate('Error máximo: 5.0', xy=(1, 5.0), xytext=(10, 1.8),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
             fontsize=10)

plt.annotate('Convergencia (error = 0)', xy=(4, 0), xytext=(15, 0.5),
             arrowprops=dict(facecolor='green', shrink=0.05, width=1.5),
             fontsize=10, color='green')

# Mostrar la gráfica
plt.tight_layout()
plt.savefig('evolucion_errores.png', dpi=300)
plt.show()