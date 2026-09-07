"""
Proceso de Poisson para modelar la aparición de anomalías durante la misión.

Un proceso de Poisson homogéneo de tasa `lambda` cuenta el número de eventos
que ocurren en un intervalo de tiempo [0, t]. Su propiedad clave es que los
tiempos entre llegadas (el tiempo entre un evento y el siguiente) son
variables aleatorias exponenciales independientes de parámetro `lambda`.

Esto permite simular el proceso sin generar directamente la variable
discreta N: basta con ir acumulando tiempos entre llegadas Exp(lambda)
-generados por transformada inversa en metodo_inversa.py- hasta que la suma
supere el tiempo de la misión t. La cantidad de tiempos que caen dentro de
[0, t] es una realización de N ~ Poisson(lambda * t).

Esta es la definición de proceso de Poisson vista en clase (proceso de
conteo con incrementos independientes y tiempos entre llegadas
exponenciales), y reutiliza el generador exponencial ya validado por
transformada inversa en lugar de reimplementar un muestreo de Poisson
independiente.
"""

from metodo_inversa import exponencial_inversa


def simular_llegadas_poisson(t, lmbda):
    """Simula los instantes de llegada de un proceso de Poisson de tasa
    `lmbda` dentro del intervalo [0, t].

    Acumula tiempos entre llegadas Exp(lmbda) hasta pasarse de t y
    devuelve únicamente los instantes que caen dentro de [0, t].
    """
    if t < 0:
        raise ValueError("El tiempo de la misión debe ser no negativo")
    if lmbda <= 0:
        raise ValueError("La tasa lambda debe ser mayor que cero")

    tiempo_actual = 0.0
    instantes = []

    while True:
        tiempo_actual += exponencial_inversa(lmbda)

        if tiempo_actual > t:
            break

        instantes.append(tiempo_actual)

    return instantes


def generar_anomalias(t, lmbda):
    """Genera una realización del proceso de Poisson en [0, t].

    Devuelve una tupla (N, instantes) donde N es el número de anomalías
    ocurridas durante la misión e `instantes` son los momentos en que
    ocurrieron.
    """
    instantes = simular_llegadas_poisson(t, lmbda)
    return len(instantes), instantes


def generar_cantidad_anomalias(n, t, lmbda):
    """Genera n realizaciones independientes de N ~ Poisson(lambda * t).

    Devuelve solo el conteo N de cada lanzamiento (sin los instantes de
    ocurrencia), que es lo que necesita el motor de simulación para
    combinar N con las demás variables (V, C, W) de cada lanzamiento.
    """
    if not isinstance(n, int) or n <= 0:
        raise ValueError("n debe ser un entero positivo")

    return [generar_anomalias(t, lmbda)[0] for _ in range(n)]
