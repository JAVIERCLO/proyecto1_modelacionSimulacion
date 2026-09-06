import random
import math


def metodo_aceptacion_rechazo(generador):
    propuestas = 0

    while True:
        propuestas += 1

        u1 = generador.random()
        u2 = generador.random()

        while u1 == 0:
            u1 = generador.random()

        # Variable propuesta con distribución exponencial
        y = -math.log(u1)

        probabilidad_aceptacion = math.exp(-((y - 1) ** 2) / 2)

        if u2 <= probabilidad_aceptacion:
            u3 = generador.random()

            if u3 <= 0.5:
                z = y
            else:
                z = -y

            return z, propuestas


def generar_normales(n, semilla=None):
    if not isinstance(n, int) or n <= 0:
        raise ValueError(
            "n debe ser un entero positivo"
        )

    generador = random.Random(semilla)

    normales = []
    total_propuestas = 0

    for _ in range(n):
        z, propuestas = metodo_aceptacion_rechazo(
            generador
        )

        normales.append(z)
        total_propuestas += propuestas

    estadisticas = {
        "aceptados": n,
        "rechazados": total_propuestas - n,
        "propuestas": total_propuestas,
        "tasa_aceptacion": n / total_propuestas
    }

    return normales, estadisticas


def generar_combustibles(n,media=500_000,desviacion=5_000,semilla=None):
    if desviacion <= 0:
        raise ValueError(
            "La desviación debe ser mayor que cero"
        )

    normales, estadisticas = generar_normales(
        n,
        semilla
    )

    combustibles = [
        media + desviacion * z
        for z in normales
    ]

    return combustibles, estadisticas