"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """


import config as cf
import model
import time
import csv
import tracemalloc

csv.field_size_limit(2147483647)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    control = {
        'model': None
    }
    control['model'] = model.new_data_structs()

    return control


# Funciones para la carga de datos

def load_data(control, memflag):
    """
    Carga los datos del reto
    """
    start_time = get_time()

    if memflag:
        tracemalloc.start()
        start_memory = get_memory()

    analyzer = control['model']

    load_airports(analyzer)
    load_flights(analyzer)
    get_best_airports(analyzer)

    stop_time = get_time()
    deltaTime = delta_time(start_time, stop_time)
    deltaMemory = 0

    if memflag:
        stop_memory = get_memory()
        tracemalloc.stop()
        deltaMemory = delta_memory(stop_memory, start_memory)

    return analyzer, deltaTime, deltaMemory

def load_airports(analyzer):
    """
    Carga las caracteristicas de los aeropuertos
    """
    airports_file = cf.data_dir + 'airports-2022.csv'
    input_file = csv.DictReader(open(airports_file, encoding='utf-8'), delimiter=';')
    for airport in input_file:
        model.new_airport(analyzer, airport)

def load_flights(analyzer, weight='time'):
    """
    Carga las caracteristicas de los vuelos
    """
    flights_file = cf.data_dir + 'fligths-2022.csv'
    input_file = csv.DictReader(open(flights_file, encoding='utf-8'), delimiter=';')
    for flight in input_file:
        model.new_flight(analyzer, flight['TIPO_VUELO'], flight, weight)


# Funciones de ordenamiento

def sort(analyzer):
    """
    Función encargada de ordenar la lista con los datos
    """
    return model.sort(analyzer)

def set_sort_algorithm(algorithm):
    """
    Configura el algoritmo de ordenamiento que se va a utilizar en el
    modelo y lo retorna.
    """
    selected, msg = model.select_sort_algorithm(algorithm)
    model.sort_algorithm = selected

    return msg


# Funciones de consulta

def get_data(analyzer, id):
    """
    Retorna un dato por su ID.
    """
    return model.get_data(analyzer, id)

def get_entry(analyzer, data_structure, key):
    """
    Retorna una entrada a partir de su llave
    """
    return model.get_entry(analyzer, data_structure, key)

def get_data_size(analyzer, data_structure):
    """
    Retorna el tamaño de la lista de datos.
    """
    return model.data_size(analyzer, data_structure)

def totalFlights(analyzer):
    """
    Retorna el total de vuelos
    """
    return model.totalFlights(analyzer)

def get_best_airports(analyzer):
    """
    Retorna los aeropuertos con mayor concurrencia
    """
    for type in 'commercial', 'merchandise', 'military':
        model.airport_flights(analyzer, type)


# Funciones de requerimientos

def req_1(control, origin, destination, memflag, map):
    """
    Retorna el resultado del requerimiento 1
    """
    start_time = get_time()

    if memflag:
        tracemalloc.start()
        start_memory = get_memory()

    analyzer = control['model']

    req_1, airports ,stadistics  = model.req_1(analyzer, origin, destination, map)

    stop_time = get_time()
    deltaTime = delta_time(start_time, stop_time)
    deltaMemory = 0

    if memflag:
        stop_memory = get_memory()
        tracemalloc.stop()
        deltaMemory = delta_memory(stop_memory, start_memory)

    return req_1, airports,stadistics, deltaTime, deltaMemory


def req_2(control, origin, destination, memflag, map):
    """
    Retorna el resultado del requerimiento 7
    """
    start_time = get_time()

    if memflag:
        tracemalloc.start()
        start_memory = get_memory()

    analyzer = control['model']

    load_flights(analyzer, 'distance')
    req_2, airports, stadistics = model.req_2(analyzer, origin, destination, map)

    stop_time = get_time()
    deltaTime = delta_time(start_time, stop_time)
    deltaMemory = 0

    if memflag:
        stop_memory = get_memory()
        tracemalloc.stop()
        deltaMemory = delta_memory(stop_memory, start_memory)

    return req_2, airports, stadistics, deltaTime, deltaMemory 


def req_3(control, memflag, map):
    """
    Retorna el resultado del requerimiento 3
    """
    start_time = get_time()

    if memflag:
        tracemalloc.start()
        start_memory = get_memory()

    analyzer = control['model']

    load_flights(analyzer, 'distance')
    req_3, important_airport, stadistics = model.req_3(analyzer, map)

    stop_time = get_time()
    deltaTime = delta_time(start_time, stop_time)
    deltaMemory = 0

    if memflag:
        stop_memory = get_memory()
        tracemalloc.stop()
        deltaMemory = delta_memory(stop_memory, start_memory)

    return req_3, important_airport, stadistics, deltaTime, deltaMemory


def req_4(control, memflag, map):
    """
    Retorna el resultado del requerimiento 4
    """
    start_time = get_time()

    if memflag:
        tracemalloc.start()
        start_memory = get_memory()

    analyzer = control['model']

    load_flights(analyzer, 'distance')
    req_4, important_airport, total_flights, total_distance = model.req_4(analyzer, map)

    stop_time = get_time()
    deltaTime = delta_time(start_time, stop_time)
    deltaMemory = 0

    if memflag:
        stop_memory = get_memory()
        tracemalloc.stop()
        deltaMemory = delta_memory(stop_memory, start_memory)

    return req_4, important_airport, total_flights, total_distance, deltaTime, deltaMemory


def req_5(control, memflag, map):
    """
    Retorna el resultado del requerimiento 5
    """
    start_time = get_time()

    if memflag:
        tracemalloc.start()
        start_memory = get_memory()

    analyzer = control['model']

    load_flights(analyzer, 'time')
    req_5, important_airport, stadistics = model.req_5(analyzer, map)

    stop_time = get_time()
    deltaTime = delta_time(start_time, stop_time)
    deltaMemory = 0

    if memflag:
        stop_memory = get_memory()
        tracemalloc.stop()
        deltaMemory = delta_memory(stop_memory, start_memory)

    return req_5, important_airport, stadistics, deltaTime, deltaMemory


def req_6(control, num_airports, memflag, map):
    """
    Retorna el resultado del requerimiento 6
    """
    start_time = get_time()

    if memflag:
        tracemalloc.start()
        start_memory = get_memory()

    analyzer = control['model']

    load_flights(analyzer, 'distance')
    req_6, colombian_airports = model.req_6(analyzer, int(num_airports), map)

    stop_time = get_time()
    deltaTime = delta_time(start_time, stop_time)
    deltaMemory = 0

    if memflag:
        stop_memory = get_memory()
        tracemalloc.stop()
        deltaMemory = delta_memory(stop_memory, start_memory)

    return req_6, colombian_airports, deltaTime, deltaMemory


def req_7(control, origin, destination, memflag, map):
    """
    Retorna el resultado del requerimiento 7
    """
    start_time = get_time()

    if memflag:
        tracemalloc.start()
        start_memory = get_memory()

    analyzer = control['model']

    load_flights(analyzer, 'distance')
    req_7, airports, stadistics = model.req_7(analyzer, origin, destination, map)

    stop_time = get_time()
    deltaTime = delta_time(start_time, stop_time)
    deltaMemory = 0

    if memflag:
        stop_memory = get_memory()
        tracemalloc.stop()
        deltaMemory = delta_memory(stop_memory, start_memory)

    return req_7, airports, stadistics, deltaTime, deltaMemory 


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory