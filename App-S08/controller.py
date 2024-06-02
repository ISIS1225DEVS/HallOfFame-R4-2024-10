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
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bellmanford as bf
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
assert cf
import time

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = {"model":None}
    control["model"] = model.new_data_structs()

    return control


# Funciones para la carga de datos

def load_data(control):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    start_time = get_time()
    total_airports =load_data_airports(control)
    total_fligths =load_data_fligths(control)
    load_data_concurrence(control)
    end_time = get_time()
    delta = delta_time(start_time,end_time)
    return control, total_airports,total_fligths,delta
    
def load_data_concurrence(control):
    
    """
    Lista organizada con de menor a mayor según el numero de concurrencia, en cada lista se guardan tuplas donde 
    el primer elemento es el número de concurrencia que se determina por la suma de los vuelos que entraron y salieron
    del aeropuerto y el segundo elemento es el codigo ICAO que identifica a cada aeropuerto
    """
    
    data_structs = control["model"]
    fligths_file = cf.data_dir + "fligths-2022.csv"
    input_file = csv.DictReader(open(fligths_file,encoding="utf-8"),delimiter=";")
    
    for fligth in input_file:
        model.add_concurrence(data_structs,fligth)


def load_data_fligths(control):
        
    """
    Carga los datos de los vuelos como arcos en los grafos
    """
    fligths_file = cf.data_dir + "fligths-2022.csv"
    input_file = csv.DictReader(open(fligths_file,encoding="utf-8"),delimiter=";")
    
    data_strutcs = control["model"]

    for fligth in input_file:
        model.add_data_fligths(data_strutcs,fligth)
 
    return gr.numEdges(data_strutcs["comercial_airports_distance_directed"]) + gr.numEdges(data_strutcs["carga_airports_distance_directed"]) +  gr.numEdges(data_strutcs["militar_airports_distance_directed"])
 
        
def load_data_airports(control):
    """
    Carga los datos de cada aeropuerto en una tabla de hash
    Args:
        control (_type_): 
    """
    
    airports_file = cf.data_dir + "airports-2022.csv"
    input_file = csv.DictReader(open(airports_file,encoding="utf-8"),delimiter=";")
    
    data_structs = control["model"]
    
    for airport in input_file:
        model.add_data_airports(data_structs,airport)
        
    return mp.size(data_structs["airports_map"])
    
    
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


def req_1(control,origen_latitud,origen_longitud,destino_latitud,destino_longitud,method):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    start_time = get_time()
    data = model.req_1(control["model"],origen_latitud,origen_longitud,destino_latitud,destino_longitud,method)
    if data is not None:
        distancia_total,total_airports,respuesta,tiempo_total = data
        end_time = get_time()
        delta = delta_time(start_time, end_time)
        return delta,distancia_total,total_airports,respuesta,tiempo_total
    else:
        end_time = get_time()
        delta = delta_time(start_time, end_time)
        return delta,data



def req_2(control,origen_latitud,origen_longitud,destino_latitud,destino_longitud):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    start_time = get_time()
    data = model.req_2(control["model"],origen_latitud,origen_longitud,destino_latitud,destino_longitud)
    end_time = get_time()
    delta = delta_time(start_time, end_time)
    if data is not None:
        distancia_total,total_airports,respuesta,tiempo_total = data
        return delta,distancia_total,total_airports,respuesta,tiempo_total
    else:
        return delta,data


def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3

    start_time = get_time()
    data,data_aeropuerto_mayor,total_trayectos,distancia_total= model.req_3(control["model"])
    end_time = get_time()
    delta = delta_time(start_time, end_time)
    
    return delta,data,data_aeropuerto_mayor,total_trayectos,distancia_total


def req_4(control):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    
    start_time = get_time()
    data,data_aeropuerto_mayor,total_trayectos,distancia_total= model.req_4(control["model"])
    end_time = get_time()
    delta = delta_time(start_time, end_time)
    
    return delta,data,data_aeropuerto_mayor,total_trayectos,distancia_total


def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    start_time = get_time()
    data,data_aeropuerto_mayor,total_trayectos,distancia_total= model.req_5(control["model"])
    end_time = get_time()
    delta = delta_time(start_time, end_time)
    
    return delta,data,data_aeropuerto_mayor,total_trayectos,distancia_total

def req_6(control,num):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    start_time = get_time()
    data,airport_mayor= model.req_6(control["model"],num)
    end_time = get_time()
    delta = delta_time(start_time, end_time)
    airport_m =lt.newList()
    lt.addLast(airport_m,airport_mayor)
    return delta,data,airport_m

def req_7(control,origen_latitud,origen_longitud,destino_latitud,destino_longitud):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    start_time = get_time()
    data = model.req_7(control["model"],origen_latitud,origen_longitud,destino_latitud,destino_longitud)
    if data is not None:
        distancia_total,total_airports,respuesta,tiempo_total = data
        end_time = get_time()
        delta = delta_time(start_time, end_time)
        return delta,distancia_total,total_airports,respuesta,tiempo_total
    else:
        return delta,data
    


def req_8(control,respuesta):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    start_time = get_time()
    model.req_8(control["model"],respuesta)
    stop_time = get_time()
    time_delta = delta_time(start_time, stop_time)
    return time_delta


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

def get_first_last_n(lista, n_ultimos_primeros):
    """
    Crea una sublista de los ultimos n y primeros n elementos de la lista entrante
    """
    sublista = model.get_first_last_n(lista, n_ultimos_primeros)
    
    return sublista 