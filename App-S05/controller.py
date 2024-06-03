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

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    control = {"model": None}
    control["model"] = model.new_data_structs()
    return control


# Funciones para la carga de datos

def load_data(control, memflag):
    """
    Carga los datos del reto
    """
    database = control["model"]
    start = get_time()
    if memflag is True:
        tracemalloc.start()
        start_memory = get_memory()

    # Direcciones de Archivos
    flights = cf.data_dir + "fligths-2022.csv"
    airports = cf.data_dir + "airports-2022.csv"

    input_flights = csv.DictReader(open(flights, encoding="utf-8"), delimiter=";")
    input_airports = csv.DictReader(open(airports, encoding="utf-8"), delimiter=";")

    for airport in input_airports:
        model.load_data_airport(database, airport)
    
    for flight in input_flights:
        model.load_connection(database, flight)
    
    model.create_ordered_maps_airports(database)
    str1, str2, most_com, least_com, most_cargo, least_cargo, most_mil, least_mil = model.analyzer(database)

    end = get_time()
    elapsed = delta_time(start, end)

    if memflag is True:
        stop_memory = get_memory()
        tracemalloc.stop()
        deltaMemory = delta_memory(stop_memory, start_memory)
        return elapsed, deltaMemory, str1, str2, most_com, least_com, most_cargo, least_cargo, most_mil, least_mil
    else:
        return elapsed, str1, str2, most_com, least_com, most_cargo, least_cargo, most_mil, least_mil

# Funciones de consulta sobre el catálogo

def req_1_2(control, origin, dest, req):
    
    """
    Retorna el resultado del requerimiento 1
    """
    database = control["model"]
    start_time = get_time()
    result = model.req_1_2(database, origin, dest, req)
    end_time = get_time()
    elapsed = delta_time(start_time, end_time)
    return result, elapsed

def req_3_4_5(control, req):
    """
    Retorna el resultado del requerimiento 3
    """
    database = control["model"]
    start_time = get_time()
    result = model.req_3_4_5(database, req)
    end_time = get_time()
    
    elapsed = delta_time(start_time, end_time)
    return result, elapsed

def req_6(control, num):
    """
    Retorna el resultado del requerimiento 6
    """
    database = control["model"]
    start_time = get_time()
    result = model.req_6(database, num)
    end_time = get_time()
    
    elapsed = delta_time(start_time, end_time)
    return result, elapsed


def req_7(control, origin, dest):
    """
    Retorna el resultado del requerimiento 7
    """
    database = control["model"]
    start_time = get_time()
    result = model.req_7(database, origin, dest)
    end_time = get_time()
    elapsed = delta_time(start_time, end_time)
    return result, elapsed

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
