"""
Esqueleto del simulador de lanzamiento de cohetes.

Este archivo servirá para unir los métodos desarrollados
"""

import math
from py_compile import main 

from metodo_polar import generar_velocidades
from metodo_aceptacion_rechazo import generar_combustible

#from transformada_inversa import generar_vientos
#from proceso_poisson import generar_anomalias


# 2. PARÁMETROS GENERALES DEL MODELO

NUMERO_LANZAMIENTOS = 10000

VELOCIDAD_OBJETIVO = 7800       # m/s
MEDIA_VELOCIDAD = 7800          # m/s
DESVIACION_VELOCIDAD = 100       # m/s

COMBUSTIBLE_IDEAL = 500000      # kg
MEDIA_COMBUSTIBLE = 500000      # kg
DESVIACION_COMBUSTIBLE = 5000   # kg


LAMBDA_VIENTO = 1 / 8
LAMBDA_ANOMALIAS = 0.5
TIEMPO_MISION = 1

# Pesos del índice de desempeño
PESO_VELOCIDAD = 0.35
PESO_COMBUSTIBLE = 0.30
PESO_VIENTO = 0.15
PESO_ANOMALIAS = 0.20

UMBRAL_EXITO = 0.85

# Parámetros que controlan la penalización
K_VIENTO = 0.02
Q_ANOMALIAS = 0.25


# 3. FUNCIONES PARA NORMALIZAR LAS VARIABLES

def calcular_factor_velocidad(velocidad):
    """Convierte la velocidad en un factor entre 0 y 1."""
    return min(1, max(0, velocidad / VELOCIDAD_OBJETIVO))


def calcular_factor_combustible(combustible):
    """Convierte el combustible en un factor entre 0 y 1."""
    return min(1, max(0, combustible / COMBUSTIBLE_IDEAL))


def calcular_factor_viento(viento):
    """Un viento más fuerte produce un factor menor."""
    return math.exp(-K_VIENTO * viento)


def calcular_factor_anomalias(anomalias):
    """Una mayor cantidad de anomalías produce un factor menor."""
    return math.exp(-Q_ANOMALIAS * anomalias)


# 4. CALCULAR EL ÍNDICE DE DESEMPEÑO

# 5. SIMULAR UN LANZAMIENTO

# 6. EJECUTAR TODOS LOS LANZAMIENTOS

# 7. RESUMIR LOS RESULTADOS

# 8. PROGRAMA PRINCIPAL

# guardar resultados en CSV para analizarlos.
# enviar los resultados al módulo de gráficas.