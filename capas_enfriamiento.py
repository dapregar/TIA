from datetime import datetime
import random
import matplotlib.pyplot as plt
import numpy as np
import time
import os

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


def calcular_fitness(individuo: list) -> int:
    resistencia = 0
    for i in range(num_capas - 1):
        resistencia += aislamiento[individuo[i + 1]][individuo[i]]
    return resistencia


if __name__ == '__main__':
    caso = 'A'

    directorio_base = './resultados_enfriamiento/'
    ejecucion_actual = str(datetime.now().strftime("%d_%m_%Y_%H%M%S"))
    if not os.path.exists(directorio_base + ejecucion_actual):
        os.makedirs(directorio_base + ejecucion_actual)
    fichero = open(directorio_base + ejecucion_actual + "/" + ejecucion_actual + ".txt", "w")

    capa_inicial = []
    if caso == 'A':
        capa_inicial = crear_individuo_caso_a()
    elif caso == 'B':
        capa_inicial = crear_individuo_caso_b()

    solucion_actual, solucion_mejor = capa_inicial, capa_inicial

    iteracion = 0
    temperatura_actual = 1000
    temperatura_minima = 1
    e = 2.718
    tiempos = []
    temperaturas = []
    resultados = []
    while temperatura_actual > temperatura_minima:
        if caso == 'A':
            while True:
                pos1 = random.randint(min(capas), max(capas))
                pos2 = random.randint(min(capas), max(capas))
                if pos1 != pos2:
                    break

            solucion_mejor[pos1], solucion_mejor[pos2] = solucion_mejor[pos2], solucion_mejor[pos1]
            solucion_actual = solucion_mejor[:]
            solucion_mejor[pos1], solucion_mejor[pos2] = solucion_mejor[pos2], solucion_mejor[pos1]
        elif caso == 'B':
            while True:
                pos1 = random.randint(min(capas), max(capas))
                pos2 = random.randint(min(capas), max(capas))
                solucion_mejor[pos1], solucion_mejor[pos2] = solucion_mejor[pos2], solucion_mejor[pos1]
                if pos1 != pos2 and \
                        (pos1 == 0 or solucion_mejor[pos1] != solucion_mejor[pos1 - 1]) and \
                        (pos1 == 11 or solucion_mejor[pos1] != solucion_mejor[pos1 + 1]) and \
                        (pos2 == 0 or solucion_mejor[pos2] != solucion_mejor[pos2 - 1]) and \
                        (pos2 == 11 or solucion_mejor[pos2] != solucion_mejor[pos2 + 1]):
                    solucion_actual = solucion_mejor[:]
                    solucion_mejor[pos1], solucion_mejor[pos2] = solucion_mejor[pos2], solucion_mejor[pos1]
                    break
                solucion_mejor[pos1], solucion_mejor[pos2] = solucion_mejor[pos2], solucion_mejor[pos1]

        mejora = calcular_fitness(solucion_actual) - calcular_fitness(solucion_mejor)
        if mejora > 0 or e ** (mejora / temperatura_actual) > random.random():
            solucion_mejor = solucion_actual
            tiempos.append(time.process_time())
            temperaturas.append(temperatura_actual)
            resultados.append(calcular_fitness(solucion_mejor))
            texto = "Solucion {}, con evaluación {} a temperatura {}\n".format(solucion_mejor,
                                                                               calcular_fitness(solucion_mejor),
                                                                               temperatura_actual)
            fichero.write(texto)
            print(texto)

        temperatura_actual = 0.9999 * temperatura_actual

    fichero.close()

    plt.figure(figsize=(10, 5))
    plt.subplot(121)
    plt.plot(tiempos, temperaturas)
    plt.grid(True)
    plt.xlabel("Tiempo(s)")
    plt.ylabel("Temperatura")

    plt.subplot(122)
    plt.plot(tiempos, resultados)
    plt.grid(True)
    plt.xlabel("Tiempo(s)")
    plt.ylabel("Fitness")
    z = np.polyfit(tiempos, resultados, 1)
    p = np.poly1d(z)
    mejor_resultado = '{} {}\n{}s'.format(calcular_fitness(solucion_mejor), solucion_mejor, round(max(tiempos), 2))
    plt.annotate(mejor_resultado,
                 xy=(max(tiempos), max(resultados)),
                 xytext=(max(tiempos), max(resultados) + 20),
                 )
    plt.suptitle(capa_inicial)
    plt.plot(tiempos, p(tiempos), "r--")
    plt.savefig(directorio_base + ejecucion_actual + "/" + ejecucion_actual, bbox_inches='tight')
    plt.show()

    exit()
