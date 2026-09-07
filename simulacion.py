"""
Simulador de lanzamiento de cohetes.

Este archivo une los métodos desarrollados por cada variable del modelo:

- V (velocidad):    metodo_polar.py             (Método Polar, normal)
- C (combustible):  metodo_aceptacion_rechazo.py (Aceptación-Rechazo, normal)
- W (viento):       metodo_inversa.py            (Transformada Inversa, exponencial)
- N (anomalías):    proceso_poisson.py           (Proceso de Poisson)

Con V, C, W, N de cada lanzamiento se calcula un índice de desempeño R y se
determina si el lanzamiento es exitoso o no. El programa principal ejecuta
NUMERO_LANZAMIENTOS simulaciones, resume los resultados y los guarda en un
CSV para su posterior análisis.
"""

import csv
import math
import os
import random

from metodo_polar import generar_velocidades
from metodo_aceptacion_rechazo import generar_combustibles
from metodo_inversa import generar_viento
from proceso_poisson import generar_cantidad_anomalias


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

# Semilla por defecto para reproducibilidad del programa principal
SEMILLA = 42


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

def calcular_indice_desempeno(velocidad, combustible, viento, anomalias):
    """Combina V, C, W, N en un índice de desempeño R entre 0 y 1.

    R es el promedio ponderado de los cuatro factores normalizados, con
    los pesos PESO_VELOCIDAD, PESO_COMBUSTIBLE, PESO_VIENTO y
    PESO_ANOMALIAS (que suman 1).
    """
    factor_velocidad = calcular_factor_velocidad(velocidad)
    factor_combustible = calcular_factor_combustible(combustible)
    factor_viento = calcular_factor_viento(viento)
    factor_anomalias = calcular_factor_anomalias(anomalias)

    indice_desempeno = (
        PESO_VELOCIDAD * factor_velocidad
        + PESO_COMBUSTIBLE * factor_combustible
        + PESO_VIENTO * factor_viento
        + PESO_ANOMALIAS * factor_anomalias
    )

    return indice_desempeno, factor_velocidad, factor_combustible, factor_viento, factor_anomalias


# 5. SIMULAR UN LANZAMIENTO

def simular_lanzamiento(velocidad, combustible, viento, anomalias):
    """Simula un único lanzamiento a partir de sus variables V, C, W, N.

    Devuelve un diccionario con las variables de entrada, los factores
    normalizados, el índice de desempeño R y si el lanzamiento fue exitoso
    (R >= UMBRAL_EXITO).
    """
    (
        indice_desempeno,
        factor_velocidad,
        factor_combustible,
        factor_viento,
        factor_anomalias,
    ) = calcular_indice_desempeno(velocidad, combustible, viento, anomalias)

    exito = indice_desempeno >= UMBRAL_EXITO

    return {
        "velocidad": velocidad,
        "combustible": combustible,
        "viento": viento,
        "anomalias": anomalias,
        "factor_velocidad": factor_velocidad,
        "factor_combustible": factor_combustible,
        "factor_viento": factor_viento,
        "factor_anomalias": factor_anomalias,
        "indice_desempeno": indice_desempeno,
        "exito": exito,
    }


# 6. EJECUTAR TODOS LOS LANZAMIENTOS

def ejecutar_simulaciones(n=NUMERO_LANZAMIENTOS, semilla=None):
    """Genera V, C, W, N para n lanzamientos y simula cada uno.

    V, C y W se generan en bloque con los métodos de cada persona
    (Polar, Aceptación-Rechazo y Transformada Inversa respectivamente).
    N se genera lanzamiento por lanzamiento con el proceso de Poisson,
    ya que depende de simular la ocurrencia de eventos durante
    TIEMPO_MISION.
    """
    if semilla is not None:
        random.seed(semilla)

    velocidades = generar_velocidades(n, MEDIA_VELOCIDAD, DESVIACION_VELOCIDAD)
    combustibles, _ = generar_combustibles(
        n, MEDIA_COMBUSTIBLE, DESVIACION_COMBUSTIBLE, semilla=semilla
    )
    vientos = generar_viento(n, media=1.0 / LAMBDA_VIENTO)
    cantidades_anomalias = generar_cantidad_anomalias(n, TIEMPO_MISION, LAMBDA_ANOMALIAS)

    resultados = [
        simular_lanzamiento(velocidad, combustible, viento, anomalias)
        for velocidad, combustible, viento, anomalias in zip(
            velocidades, combustibles, vientos, cantidades_anomalias
        )
    ]

    return resultados


# 7. RESUMIR LOS RESULTADOS

def resumir_resultados(resultados):
    """Calcula estadísticas agregadas sobre el conjunto de lanzamientos."""
    n = len(resultados)
    exitos = sum(1 for resultado in resultados if resultado["exito"])

    indices = [resultado["indice_desempeno"] for resultado in resultados]
    media_indice = sum(indices) / n
    desviacion_indice = math.sqrt(
        sum((indice - media_indice) ** 2 for indice in indices) / (n - 1)
    )

    return {
        "n_lanzamientos": n,
        "exitos": exitos,
        "fallos": n - exitos,
        "tasa_exito": exitos / n,
        "media_indice_desempeno": media_indice,
        "desviacion_indice_desempeno": desviacion_indice,
    }


# 8. PROGRAMA PRINCIPAL

CAMPOS_CSV = [
    "velocidad",
    "combustible",
    "viento",
    "anomalias",
    "factor_velocidad",
    "factor_combustible",
    "factor_viento",
    "factor_anomalias",
    "indice_desempeno",
    "exito",
]


def guardar_resultados_csv(resultados, ruta):
    """Guarda los resultados brutos de todas las simulaciones en un CSV."""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    with open(ruta, "w", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS_CSV)
        escritor.writeheader()
        escritor.writerows(resultados)


def main():
    resultados = ejecutar_simulaciones(NUMERO_LANZAMIENTOS, semilla=SEMILLA)
    resumen = resumir_resultados(resultados)

    ruta_resultados = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resultados",
        "resultados_simulacion.csv",
    )
    guardar_resultados_csv(resultados, ruta_resultados)

    print("SIMULACIÓN DE LANZAMIENTOS DE COHETES")
    print(f"Lanzamientos simulados: {resumen['n_lanzamientos']}")
    print(f"Éxitos: {resumen['exitos']}")
    print(f"Fallos: {resumen['fallos']}")
    print(f"Tasa de éxito: {resumen['tasa_exito'] * 100:.2f} %")
    print(f"Índice de desempeño medio: {resumen['media_indice_desempeno']:.4f}")
    print(f"Desviación del índice de desempeño: {resumen['desviacion_indice_desempeno']:.4f}")
    print(f"Resultados guardados en: {ruta_resultados}")


if __name__ == "__main__":
    main()
