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
from DISClib.DataStructures import mapentry as me
import config as cf
import model
import time
import csv
import tracemalloc
from DISClib.ADT import map as mp
"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
   control = {
        'model': None }
   control['model'] = model.new_data_structs()
   return control


# Funciones para la carga de datos

def load_data(control):
    aeropuertos=airports(control['model'])
    aeropuertos=mp.size(aeropuertos)
    cargaint,comercialint,militarint=vuelos(control['model'])
    carga,comercial,militar=tabulador(control['model'])
    lista = model.lista_de_importancia_comercial(control['model'])
    model.lista_in_data_struct(control['model'])
    model.carga_datos_req6(control['model'])
    model.carga_datos_req4(control['model'])
    

    return carga,comercial,militar,cargaint,comercialint,militarint,aeropuertos, lista


# Funciones de ordenamiento
def airports(catalog):
    filename = f"{cf.data_dir}airports-2022.csv"
    input_file = csv.DictReader(open(filename, encoding='utf-8'), delimiter=";")
    for airport in input_file:
        model.add_data_airpot(catalog,airport)
    retorno=(catalog['airport_map'])
    return retorno
def vuelos(catalog):
    filename = f"{cf.data_dir}fligths-2022.csv"
    input_file = csv.DictReader(open(filename, encoding='utf-8'), delimiter=";")
    for vuelo in input_file:
        model.add_data_flight(catalog,vuelo)
    comercial=mp.size(me.getValue(mp.get(catalog['flights'],"AVIACION_COMERCIAL")))
    carga=mp.size(me.getValue(mp.get(catalog['flights'],"AVIACION_CARGA")))
    militar=mp.size(me.getValue(mp.get(catalog['flights'],"MILITAR")))
    return carga,comercial,militar
def tabulador(catalog):
    carga,comercial,militar=model.tabulador(catalog)
    return carga,comercial,militar
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


def req_1(control):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(control):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    lista, mayor = model.req_3(control['model'])
    return lista, mayor


def req_4(control):
    lista,mayor=model.req_4(control['model'],0)
    return lista,mayor


def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(control, n):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    lista, mayor = model.req_6_intento(control['model'],n)
    return lista, mayor


def req_7(control,inicio,final):
    retorno=model.req_7(control['model'],inicio,final)
    return retorno


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
