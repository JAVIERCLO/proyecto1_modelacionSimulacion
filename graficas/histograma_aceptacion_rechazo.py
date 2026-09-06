import os
import sys
import math

import matplotlib.pyplot as plt

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from metodo_aceptacion_rechazo import generar_combustibles


n = 1000000
media = 500000       # kg
desviacion = 5000    # kg


# Generar las cantidades de combustible
combustibles, estadisticas = generar_combustibles(
    n,
    media,
    desviacion
)


# Calcular la media estimada
media_estimada = sum(combustibles) / len(combustibles)


# Calcular la desviación estándar estimada
desviacion_estimada = math.sqrt(
    sum(
        (combustible - media_estimada) ** 2
        for combustible in combustibles
    ) / (len(combustibles) - 1)
)


print("\nVALIDACIÓN ESTADÍSTICA")
print("Media real:", media)
print("Media obtenida:", media_estimada)
print("Desviación real:", desviacion)
print("Desviación obtenida:", desviacion_estimada)


print("\nESTADÍSTICAS DE ACEPTACIÓN-RECHAZO")
print("Propuestas:", estadisticas["propuestas"])
print("Aceptados:", estadisticas["aceptados"])
print("Rechazados:", estadisticas["rechazados"])
print(
    "Tasa de aceptación:",
    round(estadisticas["tasa_aceptacion"] * 100, 2),
    "%"
)


#histograma
plt.hist(
    combustibles,
    bins=40,
    density=True,
    edgecolor="black",
    color="cornflowerblue",
    alpha=0.75
)

plt.xlabel("Cantidad de combustible (kg)")
plt.ylabel("Densidad")
plt.title(
    "Distribución del combustible generado "
    "con aceptación-rechazo"
)
plt.axvline(
    media,
    color="red",
    linestyle="--",
    label=f"Media nominal = {media} kg"
)
plt.legend()
plt.tight_layout()
plt.show()
