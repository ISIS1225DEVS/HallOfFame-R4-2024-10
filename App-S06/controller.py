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
from haversine import haversine, Unit
import os

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    control={"model":None}
    control["model"]=model.new_data_structs()
    return control


# Funciones para la carga de datos

def load_data(control ):
    """
    Carga los datos del reto
    """
    data_structs=control["model"]
    aeropuertos=loadaeropuertos(data_structs)
    vuelos=loadvuelos(data_structs)
    model.cargar_arboles_concurrencias(data_structs)
    return aeropuertos, vuelos
    
def loadaeropuertos(data_structs):
    archivo=cf.data_dir+"airports-2022.csv"
    input_file= csv.DictReader(open(archivo,encoding="utf-8"), delimiter=";")
    for aeropuerto in input_file:
        model.add_node(data_structs, aeropuerto)
    return model.data_size(data_structs,"nodes")

def loadvuelos(data_structs):
    archivo=cf.data_dir+"fligths-2022.csv"
    input_file= csv.DictReader(open(archivo,encoding="utf-8"), delimiter=";")
    for vuelo in input_file:
        model.add_edge(data_structs, vuelo)
    return model.data_size(data_structs,"edges")


def req_1(control, punto_origen_lat, punto_origen_long, punto_destino_lat, punto_destino_long):
    """
    Retorna el resultado del requerimiento 1
    """
    start_time = get_time()
    distancia, numero_vuelos, secuencia, tiempo_del_trayecto=model.req_1(control["model"], punto_origen_lat, punto_origen_long, punto_destino_lat, punto_destino_long)
    stop_time = get_time()
    delta_ = delta_time(start_time, stop_time)
    return delta_, distancia, numero_vuelos, secuencia, tiempo_del_trayecto
    


def req_2(control, punto_origen_lat, punto_origen_long, punto_destino_lat, punto_destino_long):
    """
    Retorna el resultado del requerimiento 1
    """
    start_time = get_time()
    distancia, numero_vuelos, secuencia, tiempo_del_trayecto=model.req_2(control["model"], punto_origen_lat, punto_origen_long, punto_destino_lat, punto_destino_long)
    stop_time = get_time()
    delta_ = delta_time(start_time, stop_time)
    return delta_, distancia, numero_vuelos, secuencia, tiempo_del_trayecto
    


def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    start_time = get_time()
    aepto_concurrente, distancia, num_trayectos_posibles, salida, llegada, secuencia=model.req_3(control["model"])
    stop_time = get_time()
    delta = delta_time(start_time, stop_time)
    return delta, aepto_concurrente, distancia, num_trayectos_posibles,salida,llegada, secuencia


def req_4(control):
    """
    Retorna el resultado del requerimiento 4
    """
    start_time = get_time()
    aepto_concurrente, distancia, num_trayectos_posibles, salida, llegada, secuencia=model.req_3(control["model"])
    stop_time = get_time()
    delta = delta_time(start_time, stop_time)
    return delta, aepto_concurrente, distancia, num_trayectos_posibles,salida,llegada, secuencia


def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    start_time = get_time()
    aeropuerto_importante, dist_total, num_trayectos_total, trayectos = model.req_5(control["model"])
    stop_time = get_time()
    delta = delta_time(start_time, stop_time)
    return delta, aeropuerto_importante, dist_total, num_trayectos_total, trayectos
def req_6(control, m):
    """
    Retorna el resultado del requerimiento 6
    """
    start_time = get_time()
    aepto_concurrente, salida, llegada, secuencia=model.req_6(control["model"], m)
    stop_time = get_time()
    delta_ = delta_time(start_time, stop_time)
    return delta_, aepto_concurrente,salida,llegada, secuencia


def req_7(control, lat1, lat2, long1, long2):
    """
    Retorna el resultado del requerimiento 7
    """
    start_time = get_time()
    tiempo_total, dist_total, num_aeropuertos, secuencia = model.req_7(control["model"], lat1, lat2, long1, long2)
    stop_time = get_time()
    delta = delta_time(start_time, stop_time)
    return delta, tiempo_total, dist_total, num_aeropuertos, secuencia

def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    start_time = get_time()
    mapa = model.req_8(control['model'])
    stop_time = get_time()
    delta = delta_time(start_time, stop_time)
    return mapa, delta

def haversine(coord1, coord2):
    """
    Calcula la distancia entre dos puntos geográficos.
    """
    return haversine(coord1, coord2, unit=Unit.KILOMETERS)


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
    memory_diff = stop_memory.compare_to(start_memory, "")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
