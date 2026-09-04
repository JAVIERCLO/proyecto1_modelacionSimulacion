import random
import math


def metodo_polar():
    # Generar hasta obtener un punto dentro del círculo unitario
    while True:
        # Generar los primeros números aleatorios
        U1 = random.uniform(0, 1)
        U2 = random.uniform(0, 1)

        # Transformar al intervalo [-1, 1]
        X1 = 2*U1 - 1
        X2 = 2*U2 - 1

        # Calcular la suma de los cuadrados
        S = X1**2 + X2**2

        # Comprobar si el punto está dentro del círculo unitario
        if 0 < S < 1:
            break

    # Transformación polar
    F = math.sqrt(-2 * math.log(S) / S)

    # Calcular las variables aleatorias normales estándar
    Z1 = X1 * F
    Z2 = X2 * F

    return Z1, Z2

# Para reutilizar: Z1, Z2 = metodo_polar()

def generar_normales(n):
    # Lista de variables aleatorias normales estándar
    normales = []

    # Generar n variables aleatorias normales estándar
    while len(normales) < n:
        Z1, Z2 = metodo_polar()

        normales.append(Z1)

        # Agregar Z2 solo si aún se necesitan más variables
        if len(normales) < n:
            normales.append(Z2)

    return normales

# Para reutilizar: normales = generar_normales(n)


# Generar velocidades (velocidad al final de la fase propulsada principal)
def generar_velocidades(n, media, desviacion):
    # Generar variables aleatorias normales estándar
    normales = generar_normales(n)

    # Transformar a la distribución normal
    velocidades = [media + desviacion * z for z in normales]

    return velocidades

# Para reutilizar: velocidades = generar_velocidades(n, media, desviacion)