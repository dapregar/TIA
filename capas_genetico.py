import os
import random
from datetime import datetime
from pprint import pprint
from typing import List, Any

import matplotlib.pyplot as plt
import time
import numpy as np

aislamiento = [[0, 10, 15, 25, 32, 25, 21, 21, 15, 22, 12, 54],
               [41, 0, 57, 24, 52, 2, 66, 55, 61, 15, 6, 7],
               [21, 31, 0, 21, 21, 44, 21, 22, 22, 61, 47, 61],
               [66, 22, 15, 0, 47, 21, 41, 15, 21, 22, 32, 34],
               [21, 44, 61, 47, 0, 32, 26, 61, 55, 34, 18, 12],
               [22, 18, 22, 23, 41, 0, 21, 22, 44, 55, 54, 54],
               [15, 25, 34, 21, 26, 27, 0, 34, 25, 41, 7, 22],
               [61, 34, 12, 54, 21, 23, 15, 0, 21, 21, 55, 55],
               [22, 54, 54, 65, 3, 25, 61, 77, 0, 47, 22, 22],
               [34, 7, 22, 23, 54, 42, 22, 54, 21, 0, 12, 15],
               [26, 61, 55, 22, 18, 18, 22, 18, 34, 21, 0, 12],
               [22, 18, 25, 34, 21, 22, 18, 61, 55, 2, 22, 0]]
capas = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
num_capas = 12
tamano_poblacion = 1000


# CAS0 1 Se deben utilizar todos los materiales.
def reordenar_capas() -> None:
    capas.sort()


def crear_individuo_caso_a() -> list:
    random.shuffle(capas)
    return capas[:]


def crear_individuo_caso_b() -> list:
    nuevo_individuo = []
    while len(nuevo_individuo) != len(capas):
        nuevo_elemento = np.random.choice(capas, 1)[0]
        if not nuevo_individuo or nuevo_elemento != nuevo_individuo[-1]:
            nuevo_individuo.append(nuevo_elemento)

    return nuevo_individuo


def crear_poblacion(caso: str) -> list:
    nueva_poblacion = []
    for iteracion in range(tamano_poblacion):
        if caso == 'A':
            nueva_poblacion.append(crear_individuo_caso_a())
        elif caso == 'B':
            nueva_poblacion.append(crear_individuo_caso_b())
    reordenar_capas()  # Devolvemos las capas al orden original, por si lo necesitamos más adelante...
    return nueva_poblacion


def calcular_fitness(individuo: list) -> int:
    resistencia = 0
    for iteracion in range(num_capas - 1):
        resistencia += aislamiento[individuo[iteracion + 1]][individuo[iteracion]]
    return resistencia


def evaluacion(poblacion) -> list:
    # Calculamos el fitness de la población
    poblacion_con_fitness = [(calcular_fitness(individuo), individuo) for individuo in
                             poblacion]  # Tipo (fitness, [poblacion])

    # print("Población con fitness: ")
    # pprint(poblacion_con_fitness)
    # print()

    poblacion_con_fitness.sort()

    return poblacion_con_fitness[:]


def calcular_probabilidad_eleccion(individuo: list, sumatorio_fitness: int):
    individuo_con_probabilidad = [(individuo[0] / sumatorio_fitness, individuo)]
    return individuo_con_probabilidad[:]


def evolucion(poblacion: list, caso: str) -> list:
    # 1ª fase: Selección con ruleta
    sumatorio_fitness = 0
    for indiviuo in poblacion:
        sumatorio_fitness += indiviuo[0]

    poblacion_con_probabilidad_de_eleccion = [(calcular_probabilidad_eleccion(individuo, sumatorio_fitness))
                                              for individuo in poblacion]

    poblacion_sin_probabilidades: List[Any] = []
    probabilidades = []
    for individuo in poblacion_con_probabilidad_de_eleccion:
        poblacion_sin_probabilidades.append(individuo[0][1][1])
        probabilidades.append(individuo[0][0])

    indice_padre = np.random.choice(
        [iteracion for iteracion in range(tamano_poblacion)],
        1,
        p=probabilidades
    )[0]

    while True:
        indice_madre = np.random.choice(
            [iteracion for iteracion in range(tamano_poblacion)],
            1,
            p=probabilidades
        )[0]
        if indice_padre != indice_madre:
            break

    padre = poblacion_sin_probabilidades[indice_padre]
    madre = poblacion_sin_probabilidades[indice_madre]
    # print("Padre: ", padre)
    # print("Madre: ", madre)

    # 2ª fase Cruce de permutación
    hijo = ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
    hija = ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']

    if caso == 'A':
        hijo[3:9] = padre[3:9]
        for elemento in reversed(madre):
            if elemento not in hijo:
                # rreplace(hijo, 'X', i, 1)
                hijo[find_last(hijo, 'X')] = elemento

        hija[3:9] = madre[3:9]
        for elemento in reversed(padre):
            if elemento not in hija:
                # rreplace(hijo, 'X', i, 1)
                hija[find_last(hija, 'X')] = elemento
    elif caso == 'B':
        hijo[0:3], hijo[3:9], hijo[9:12] = padre[0:3], madre[3:9], padre[9:12]
        if hijo[2] == hijo[3]:
            hijo[3], hijo[4] = hijo[4], hijo[3]
        if hijo[8] == hijo[9]:
            hijo[9], hijo[10] = hijo[10], hijo[9]

        hija[0:3], hija[3:9], hija[9:12] = madre[0:3], padre[3:9], madre[9:12]
        if hija[2] == hija[3]:
            hija[3], hija[4] = hija[4], hija[3]
        if hija[8] == hija[9]:
            hija[9], hija[10] = hija[10], hija[9]

    # print("Hijo: ", hijo)
    # print("Hija: ", hija)

    # 3ª fase Mutación por intercambio recíproco
    mutacion(hijo, caso)
    mutacion(hija, caso)
    # print("Hijo tras mutación:", hijo)
    # print("Hija tras mutación:", hija)
    # print()

    # 4ª fase Reemplazo
    poblacion[0] = (calcular_fitness(hijo), hijo)
    poblacion[1] = (calcular_fitness(hija), hija)

    return poblacion[:]


def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


def mutacion(hijo, caso_mutacion):
    for elemento in hijo:
        probabilidad_mutacion = random.random()
        if 0.0001 <= probabilidad_mutacion <= 0.05:
            posicion_elemento = hijo.index(elemento)
            while True:
                if caso_mutacion == 'A':
                    posicion_cambio = random.randint(0, len(capas) - 1)
                    if posicion_elemento != posicion_cambio:
                        break

                if caso_mutacion == 'B':
                    posicion_cambio = random.randint(0, len(capas) - 1)
                    if posicion_elemento != posicion_cambio:
                        if (posicion_elemento == 0 and hijo[posicion_elemento + 1] != hijo[posicion_cambio]) or \
                                (posicion_cambio == 0 and hijo[posicion_cambio + 1] != hijo[posicion_elemento]):
                            break
                        elif (posicion_elemento == 11 and hijo[posicion_elemento - 1] != hijo[posicion_cambio]) or \
                                (posicion_cambio == 11 and hijo[posicion_cambio - 1] != hijo[posicion_elemento]):
                            break
                        elif posicion_elemento in [0, 11] or posicion_cambio in [0, 11]:
                            continue
                        elif (hijo[posicion_elemento - 1] != hijo[posicion_cambio] or
                              hijo[posicion_elemento + 1] != hijo[posicion_cambio]) or \
                                (hijo[posicion_cambio - 1] != hijo[posicion_elemento] or
                                 hijo[posicion_cambio + 1] != hijo[posicion_elemento]):
                            break
                        else:
                            continue
            hijo[posicion_elemento] = hijo[posicion_cambio]
            hijo[posicion_cambio] = elemento


def find_last(lst, sought_elt):
    for r_idx, elt in enumerate(reversed(lst)):
        if elt == sought_elt:
            return len(lst) - 1 - r_idx


def juicio_final(poblacion, caso) -> list:
    nueva_poblacion = evaluacion(crear_poblacion(caso))
    nueva_poblacion[tamano_poblacion - 1] = poblacion[tamano_poblacion - 1]
    nueva_poblacion.sort()
    return nueva_poblacion


if __name__ == '__main__':
    caso_actual = 'B'

    # Creamos la poblacion
    poblacion_inicial = crear_poblacion(caso_actual)

    poblacion_con_evaluacion = evaluacion(poblacion_inicial)
    poblacion_inicial_con_evaluacion = poblacion_con_evaluacion[:]
    i = 0

    num_iteraciones_misma_evaluacion = 0
    ultima_mejor_evaluacion = 0
    resultados_names = []
    resultados_values = []
    tiempos = []
    while True:
        poblacion_con_evaluacion = evolucion(poblacion_con_evaluacion, caso_actual)
        poblacion_con_evaluacion.sort()

        if poblacion_con_evaluacion[tamano_poblacion - 1] == ultima_mejor_evaluacion:
            num_iteraciones_misma_evaluacion += 1
            if num_iteraciones_misma_evaluacion % 1000 == 0:
                juicio_final(poblacion_con_evaluacion, caso_actual)
                print("Propuesta en iteracion {}: ".format(num_iteraciones_misma_evaluacion))
                pprint(poblacion_con_evaluacion[tamano_poblacion - 1])
                print()
        else:
            resultados_names.append(poblacion_con_evaluacion[tamano_poblacion - 1])
            resultados_values.append(poblacion_con_evaluacion[tamano_poblacion - 1][0])
            tiempos.append(time.process_time())
            print("Se ha encontrado una mejora, reinicio de las iteraciones")
            print(poblacion_con_evaluacion[tamano_poblacion - 1])
            print()
            ultima_mejor_evaluacion = poblacion_con_evaluacion[tamano_poblacion - 1]
            num_iteraciones_misma_evaluacion = 0

        if (caso_actual == 'A' and num_iteraciones_misma_evaluacion == 20000) or \
                (caso_actual == 'B' and num_iteraciones_misma_evaluacion == 20000):
            break

    print("--------------------------------------")
    print("Propuesta inicial: ")
    print(poblacion_inicial_con_evaluacion[tamano_poblacion - 1])
    print()

    print("Propuesta final:")
    print(poblacion_con_evaluacion[tamano_poblacion - 1])

    directorio_base = './resultados_genetico/'
    ejecucion_actual = str(datetime.now().strftime("%d_%m_%Y_%H%M%S"))
    if not os.path.exists(directorio_base + ejecucion_actual):
        os.makedirs(directorio_base + ejecucion_actual)

    plt.plot(tiempos, resultados_values)
    plt.plot(tiempos, resultados_values, 'ro')
    plt.grid(True)
    plt.xlabel("Tiempo(s)")
    plt.ylabel("Valor")
    plt.title("Resultados")
    plt.xlim(min(tiempos) - 0.25, max(tiempos) + 0.25)
    mejor_resultado = '{}\n{}s'.format(poblacion_con_evaluacion[tamano_poblacion - 1], round(max(tiempos), 2))
    plt.annotate(mejor_resultado,
                 xy=(max(tiempos), max(resultados_values)),
                 xytext=(max(tiempos), max(resultados_values) + 10),
                 )
    plt.savefig(directorio_base + ejecucion_actual + "/" + ejecucion_actual, bbox_inches='tight')
    plt.show()

    exit()
