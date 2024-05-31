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
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = {
        "model": None
    }
    control["model"] = model.new_data_structs()
    return control


# Funciones para la carga de datos

def load_data(control, resp):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    data_structs = control["model"]
    
    tiempo_inicial = get_time()
    
    
    if resp == True:
        tracemalloc.start()
        memoria_inicial = get_memory()
    
    airports = load_airports(data_structs)
    flights = load_flights(data_structs)
    cantidad_aeropuertos = flights[0]
    cantidad_vuelos = flights[1]
    
    tiempo_final = get_time()
    tiempo_total = delta_time(tiempo_inicial, tiempo_final)
    
    if resp == True:
        memoria_final= get_memory()
        tracemalloc.stop()

        cambio_memoria = delta_memory(memoria_final, memoria_inicial)
        
    if resp == True:
        return cantidad_aeropuertos, cantidad_vuelos, tiempo_total, cambio_memoria
    else:
        return cantidad_aeropuertos, cantidad_vuelos, tiempo_total, None

def load_flights(data_structs):
    name_file = cf.data_dir + "fligths-2022.csv"
    input_file = csv.DictReader(open(name_file, encoding="utf-8"), delimiter=";")

    #conteo_vuelos = 0
    for vuelos in input_file:
        model.add_flight(data_structs, vuelos)
        #conteo_vuelos += 1
    return model.graf_size(data_structs)

def load_airports(data_structs):
    name_file = cf.data_dir + "airports-2022.csv"
    input_file = csv.DictReader(open(name_file, encoding="utf-8"), delimiter=";")
    
    #conteo_aeropuertos = 0
    for aeropuertos in input_file:
        model.add_airport(data_structs, aeropuertos)
        #conteo_aeropuertos += 1
    return None

def mostrar_info(control):
    l1, l2, l3 = model.mostrar_info(control)
    return l1, l2, l3

# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control, latitud_origen, longitud_origen, latitud_destino, longitud_destino):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    
    data_structs = control["model"]
    tiempo_inicial = get_time()
    ae_origen, ae_destino, lista_aeropuertos, cantidad_aeropuerto_visitados, tiempo_trayecto, distancia_trayecto, checking, tiempo_total_trayecto = model.req_1(data_structs, latitud_origen, longitud_origen, latitud_destino, longitud_destino)
    tiempo_final = get_time()
    tiempo_total = delta_time(tiempo_inicial, tiempo_final)
    return tiempo_total, ae_origen, ae_destino, lista_aeropuertos, cantidad_aeropuerto_visitados, tiempo_trayecto, distancia_trayecto, checking, tiempo_total_trayecto


def req_2(control, latitud_origen, longitud_origen, latitud_destino, longitud_destino):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    data_structs = control["model"]
    tiempo_inicial = get_time()
    ae_origen, ae_destino, lista_aeropuertos, cantidad_aeropuerto_visitados, tiempo_trayecto, distancia_trayecto, checking, tiempo_total_trayecto = model.req_2(data_structs, latitud_origen, longitud_origen, latitud_destino, longitud_destino)
    tiempo_final = get_time()
    tiempo_total = delta_time(tiempo_inicial, tiempo_final)
    return tiempo_total, ae_origen, ae_destino, lista_aeropuertos, cantidad_aeropuerto_visitados, tiempo_trayecto, distancia_trayecto, checking, tiempo_total_trayecto


def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    data_structs = control["model"]
    tiempo_inicial = get_time()
    aeropuerto_mayor_ocurrencias, cantidad_ocurrencias, cantidad_trayectos, respuesta = model.req_3(data_structs)
    tiempo_final = get_time()
    tiempo_total = delta_time(tiempo_inicial, tiempo_final)
    return tiempo_total, aeropuerto_mayor_ocurrencias, cantidad_ocurrencias, cantidad_trayectos, respuesta


def req_4(control):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    data_structs = control["model"]
    tiempo_inicial = get_time()
    aeropuerto_mayor_ocurrencias, cantidad_ocurrencias, cantidad_trayectos, respuesta, distancia_total_red = model.req_4(data_structs)
    tiempo_final = get_time()
    tiempo_total = delta_time(tiempo_inicial, tiempo_final)
    return tiempo_total, aeropuerto_mayor_ocurrencias, cantidad_ocurrencias, cantidad_trayectos, respuesta, distancia_total_red


def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    data_structs = control["model"]
    tiempo_inicial = get_time()
    aeropuerto_mayor_ocurrencias, cantidad_ocurrencias, cantidad_trayectos, respuesta, distancia_total_trayectos    = model.req_5(data_structs)
    tiempo_final = get_time()
    tiempo_total = delta_time(tiempo_inicial, tiempo_final)
    return tiempo_total, aeropuerto_mayor_ocurrencias, cantidad_ocurrencias, cantidad_trayectos, respuesta, distancia_total_trayectos   


def req_6(control, M):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    data_structs = control["model"]
    tiempo_inicial = get_time()
    aeropuerto_mayor_ocurrencias, cantidad_ocurrencias, lst_retornar = model.req_6(data_structs, M)
    tiempo_final = get_time()
    tiempo_total = delta_time(tiempo_inicial, tiempo_final)
    
    return tiempo_total, aeropuerto_mayor_ocurrencias, cantidad_ocurrencias, lst_retornar


def req_7(control, latitud_origen, longitud_origen, latitud_destino, longitud_destino):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    data_structs = control["model"]
    tiempo_inicial = get_time()
    ae_origen, ae_destino, duracion, distancia, num_aeropuertos, respuesta, cheking, tiempo_total, distancia_entre_trayectos = model.req_7(data_structs, latitud_origen, longitud_origen, latitud_destino, longitud_destino)
    tiempo_final = get_time()
    time = delta_time(tiempo_inicial, tiempo_final)
    return time, ae_origen, ae_destino, duracion, distancia, num_aeropuertos, respuesta, cheking, tiempo_total, distancia_entre_trayectos


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

def bono_tuplas(control):
    """
    Retorna el bono de tuplas"

    """
    data_structs = control["model"]
    camino_t, cantidad_aeropuerto_visitados_t, distancia_entre_trayectos_t, camino, cantidad_aeropuerto_visitados, distancia_entre_trayectos, lst_tuple, lst = model.bono_tuplas(data_structs)
    
    return camino_t, cantidad_aeropuerto_visitados_t, distancia_entre_trayectos_t, camino, cantidad_aeropuerto_visitados, distancia_entre_trayectos, lst_tuple, lst

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

def convertir_bool(a):
    x = model.convertir_bool(a)
    return x