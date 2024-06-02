"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrollado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
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
 * along withthis program.If not, see <http://www.gnu.org/licenses/>.
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
    control = {'model': None}
    control['model'] = model.newCatalog()
    
    return control


# Funciones para la carga de datos

def load_data(control):
    """
    Carga los datos del reto
    """
    control=control["model"]
    start_time = timeIs() #! Manejo de tiempo
    #filename_airports = cf.data_dir+"smol_airports-2022.csv" #! SMALL
    #filename_flights = cf.data_dir+"smol_flights-2022.csv" #! SMALL
    filename_airports = cf.data_dir+"airports-2022.csv" #! LARGE
    filename_flights = cf.data_dir+"flights-2022.csv" #! LARGE
    airports_list = model.templist(filename_airports)
    flights_list = model.templist(filename_flights)
    model.createkeysmaptypes(control)
    model.add_nodes(control,airports_list)
    ##! No cambiar el puto orden, nos lleva de la mierda.
    model.add_edges_time_y_escalas(control,flights_list)
    model.add_edges_distance(control,flights_list)
    model.hashmap_concurrencia(control, flights_list) #revisar si jode algo
    stop_time = timeIs() #! Manejo de tiempo
    deltaTime(start_time, stop_time,do_print=True) #! Manejo de tiempo
    
    respuesta = model.infocarga(control)
    keeper = ['ICAO', 'NOMBRE', 'CIUDAD', 'CONCURRENCIA']
    respuesta[2] = model.DicKeepOnly(keeper, respuesta[2])['elements']
    respuesta[3] = model.DicKeepOnly(keeper, respuesta[3])['elements']
    respuesta[4] = model.DicKeepOnly(keeper, respuesta[4])['elements']
    respuesta[5] = model.DicKeepOnly(keeper, respuesta[5])['elements']
    respuesta[6] = model.DicKeepOnly(keeper, respuesta[6])['elements']
    respuesta[7] = model.DicKeepOnly(keeper, respuesta[7])['elements']
    return control, respuesta

def tabulation3(data, head):
    res = model.declutterLoad3(data,head)
    return res

def tabulation5(data, head, keep):
    res = model.declutterLoad5(data,head,keep)
    return res

def tabulation_N(data, head, keep, N):
    res = model.declutterLoad_N(data, head, keep, N)
    return res

#*########################################
#*######## Funciones de ordenamiento
#*########################################

def Datesort(lista):
    listaord = model.Datesort(lista)
    return listaord

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


#*########################################
#*######## Funciones de consulta sobre el catálogo
#*########################################

def req_1(control, origen, destino):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    control=control["model"]
    start_time = timeIs() #! Manejo de tiempo
    resultado = model.req_1(control, origen, destino)
    stop_time = timeIs() #! Manejo de tiempo
    deltaTime(start_time, stop_time,do_print=True) #! Manejo de tiempo
    # totalDistance, OriginaInfo, DestInfo, valuesList, numAeropuertos
    keeper = ['ICAO', 'NOMBRE', 'CIUDAD', 'PAIS']
    resultado[1] = model.DicKeepOnly(keeper, resultado[1])['elements']
    resultado[2] = model.DicKeepOnly(keeper, resultado[2])['elements']
    resultado[3] = model.DicKeepOnly(keeper, resultado[3])['elements']
    return resultado


def req_2(control, origen, destino):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    control=control["model"]
    start_time = timeIs() #! Manejo de tiempo
    resultado = model.req_2(control, origen, destino)
    # NumeroDeEscalas, OriginInfo, DestinoInfo,  Dics con info de escalas involucradas, distancia total
    keeper = ['ICAO', 'NOMBRE', 'CIUDAD', 'PAIS']
    resultado[1] = model.DicKeepOnly(keeper, resultado[1])['elements']
    resultado[2] = model.DicKeepOnly(keeper, resultado[2])['elements']
    resultado[3] = model.DicKeepOnly(keeper, resultado[3])['elements']
    
    stop_time = timeIs() #! Manejo de tiempo
    deltaTime(start_time, stop_time,do_print=True) #! Manejo de tiempo
    return resultado


def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    control=control["model"]
    start_time = timeIs() #! Manejo de tiempo
    resultado = model.req_3(control)
    stop_time = timeIs() #! Manejo de tiempo
    deltaTime(start_time, stop_time,do_print=True) #! Manejo de tiempo
    # Resultado:
    #TopKeyInfo, Top, totalDistance, numTotal, listaTrayectos
    keeperA = ['ICAO', 'NOMBRE', 'CIUDAD', 'PAIS']
    keeperB = ['ORIGEN', 'DESTINO', 'DISTANCIA', 'TIEMPO']
    resultado[0] = model.DicKeepOnly(keeperA, resultado[0])['elements']
    resultado[4] = model.DicKeepOnly(keeperB, resultado[4])['elements']
    return resultado


def req_4(control):
    """
    Retorna el resultado del requerimiento 4
    """
    control=control["model"]
    start_time = timeIs() #! Manejo de tiempo
    resultado = model.req_4(control)
    stop_time = timeIs() #! Manejo de tiempo
    deltaTime(start_time, stop_time,do_print=True) #! Manejo de tiempo
    
    keeper = ['ICAO', 'NOMBRE', 'CIUDAD', 'PAIS', 'CONCURRENCIA']
    resultado[0] = model.DicKeepOnly(keeper, resultado[0])['elements']
    keeper2 = ['TRAYECTO', 'ORIGEN', 'DESTINO', 'DISTANCIA', 'TIEMPO', 'TIPO_AERONAVE']
    resultado[3] = model.DicKeepOnly(keeper2, resultado[3])['elements']
    return resultado


def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    control=control["model"]
    start_time = timeIs() #! Manejo de tiempo
    lista = model.req_5(control)
    stop_time = timeIs() #! Manejo de tiempo
    delta= deltaTime(start_time, stop_time,do_print=True) #! Manejo de tiempo
    print(f"El tiempo fue de {delta}")
    #[aeropuerto, peso_red, cantidad_trayectos, trayectos_lista]
    keeper = ['ICAO', 'NOMBRE', 'CIUDAD', 'PAIS']
    keeper2= ["aeropuerto_origin", "aeropuerto_destino", "distancia", "tiempo", "tipo_aeronave"]
    lista[0] = model.DicKeepOnly(keeper, lista[0])['elements']
    lista[3] = model.DicKeepOnly(keeper2, lista[3])['elements']
    return lista

def req_6(control, M):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    control=control["model"]
    start_time = timeIs() #! Manejo de tiempo
    resultado = model.req_6(control, M)
    stop_time = timeIs() #! Manejo de tiempo
    deltaTime(start_time, stop_time,do_print=True) #! Manejo de tiempo
    keeper = ['ICAO', 'NOMBRE', 'CIUDAD', 'PAIS']
    resultado[0] = model.DicKeepOnly(keeper, resultado[0])['elements']
    keeperEspecial = ['Total', 'AeropuertosIncluidos', 'VuelosIncluidos', 'Distancia']
    resultado[2] = model.DicKeepOnly(keeperEspecial, resultado[2])['elements']
    return resultado


def req_7(control, origen, destino):
    """
    Retorna el resultado del requerimiento 7
    """
    control=control["model"]
    start_time = timeIs() #! Manejo de tiempo
    resultado = model.req_7(control, origen, destino)
    stop_time = timeIs() #! Manejo de tiempo
    deltaTime(start_time, stop_time,do_print=True) #! Manejo de tiempo
    keeper = ['ICAO', 'NOMBRE', 'CIUDAD', 'PAIS']
    resultado[3] = model.DicKeepOnly(keeper, resultado[3])['elements']
    resultado[4] = resultado[4]['elements']
    return resultado


def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    control=control["model"]
    start_time = timeIs() #! Manejo de tiempo
    resultado = model.req_8(control)
    stop_time = timeIs() #! Manejo de tiempo
    deltaTime(start_time, stop_time,do_print=True) #! Manejo de tiempo
    pass


#*########################################
#*######## Funciones para medir tiempos de ejecucion y memoria
#*########################################

def timeIs():
    return time.time()

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

def deltaTime(start, end, seconds= False, do_print=False):
    elapsed = float(end - start)
    if seconds:
        if do_print:
            print(f"\033[1mEl tiempo fue de {elapsed} s (segundos)\033[0m")
        return elapsed
    else:
        elapsed = elapsed*1000
        if do_print:
            print(f"\033[1mEl tiempo fue de {elapsed} ms (mili-segundos)\033[0m")
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