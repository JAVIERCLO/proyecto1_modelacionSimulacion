import random
import math


def exponencial_inversa(lmbda):
    """Genera una variable exponencial Exp(lmbda) via transformada inversa.

    X = -ln(1 - U) / lmbda  con U ~ Uniforme(0, 1).
    """
    u = random.uniform(0, 1)
    return -math.log(1.0 - u) / lmbda


def generador_exponenciales(n, lmbda):
    """Genera n variables exponenciales independientes Exp(lmbda)."""
    return [exponencial_inversa(lmbda) for _ in range(n)]


def generar_viento(n, media):
    """Genera n muestras de la velocidad del viento W ~ Exp(1/media).

    Para variables exponenciales, la media es 1/lmbda, por lo que
    lmbda = 1 / media.
    """
    lmbda = 1.0 / media
    return generador_exponenciales(n, lmbda)


def generar_tiempos_anomalias(n, media):
    """Genera n tiempos entre anomalias (Exponenciales) con media dada."""
    lmbda = 1.0 / media
    return generador_exponenciales(n, lmbda)