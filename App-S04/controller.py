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
import New_Functions as nf

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    analyzer = model.new_data_structs()
    return analyzer


# Funciones para la carga de datos

def load_data(control):
    """
    Carga los datos del reto
    """
    load_airports(control)
    load_flights(control)
    total_aeropuertos= nf.get_size(control['aeropuertos_imp'])
    total_vuelos= nf.get_size(control['vuelos'])
    
def load_airports(catalog):
    file = cf.data_dir + 'airports-2022.csv'
    input_file = csv.DictReader(open(file, encoding='utf-8'), delimiter=';')
    for airport in input_file:
        for i in airport:   
            if airport[i] == "":
                airport[i] = "Unknown"
        model.addAirport(catalog, airport)
        
def load_flights(catalog):
    file = cf.data_dir + 'fligths-2022.csv'
    input_file = csv.DictReader(open(file, encoding='utf-8'), delimiter=';')
    for flight in input_file:
        for i in flight:   
            if flight[i] == "":
                flight[i] = "Unknown"
        model.addFlight(catalog, flight)
    model.organizarAeropuertos(catalog)

# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo

def print_data(control):
    """
    Retorna un dato por su ID.
    """
    lista_comerciales = model.organizarAeropuertosValor(control, "comercial")
    lista_militar = model.organizarAeropuertosValor(control, "militar")
    lista_carga = model.organizarAeropuertosValor(control, "carga")
    return lista_comerciales, lista_militar, lista_carga #retorna tuplas


def req_1(control, o1, o2, d1, d2):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    start_time = get_time()
    info =model.req_1(control, o1, o2, d1, d2)
    stop_time = get_time()
    time = delta_time(start_time, stop_time)
    return time, info


def req_2(control, o1, o2, d1, d2):
    """
    Retorna el resultado del requerimiento 2
    """
    start_time = get_time()
    info = model.req_2(control, o1, o2, d1, d2)
    #falta transferir info
    stop_time = get_time()
    time = delta_time(start_time, stop_time)
    return time, info
    


def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    start_time = get_time()
    info = model.req_3(control)
    base = info[0]
    suma = info[1]
    num_trayectos = info[2]
    trayectos = info[3]
    stop_time = get_time()
    time = delta_time(start_time, stop_time)
    return time, base, suma, num_trayectos, trayectos


def req_4(control):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    start_time = get_time()
    info = model.req_4(control)
    base = info[0]
    suma = info[1]
    num_trayectos = info[2]
    trayectos = info[3]
    stop_time = get_time()
    time = delta_time(start_time, stop_time)
    return time, base, suma, num_trayectos, trayectos


def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    start_time = get_time()
    r=model.req_5(control)
    stop_time = get_time()
    time = delta_time(start_time, stop_time)
    return time, r

def req_6(control, numero):
    """
    Retorna el resultado del requerimiento 6
    """
    start_time = get_time()
    info = model.req_6(control, numero)
    base = info[0]
    general = info[1]
    stop_time = get_time()
    time = delta_time(start_time, stop_time)
    return time, base, general


def req_7(control, origen:tuple, destino:tuple):
    """
    Retorna el resultado del requerimiento 7
    """
    start_time = get_time()
    r=model.req_7(control,origen,destino)
    stop_time = get_time()
    time = delta_time(start_time, stop_time)
    return time, r


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


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
