import matplotlib.pyplot as plt
import math
from metodo_polar import generar_velocidades

n = 1000000
media = 7800  # m/s
desviacion = 100  # m/s

velocidades = generar_velocidades(n, media, desviacion)
for velocidad in velocidades:
    print(round(velocidad, 2), "m/s")

# Media estimada
media_estimada = sum(velocidades) / len(velocidades)

# Desviación estándar estimada
desviacion_estimada = math.sqrt(sum((v - media_estimada)**2 for v in velocidades)/ (len(velocidades) - 1))

print("Media real:", media)
print("Media obtenida:", media_estimada)

print("Desviación real:", desviacion)
print("Desviación obtenida:", desviacion_estimada)

# Histograma
plt.hist(velocidades, bins=40, edgecolor="black")
plt.xlabel("Velocidad (m/s)")
plt.ylabel("Frecuencia")
plt.title("Distribución de velocidades generadas con el Método Polar")
plt.axvline(media, linestyle="--", label=f"Media nominal = {media} m/s")
plt.legend()
plt.show()