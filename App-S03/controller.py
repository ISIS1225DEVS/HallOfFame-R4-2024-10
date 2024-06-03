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
globalSufijo = "20-por"
prueba = "Rapidez"

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

def cambiar_pruebas(respuesta):
    global prueba
    prueba = respuesta
    return prueba

def cambiarTamañoMuestra(sufijo):
    global globalSufijo
    globalSufijo = sufijo



# Funciones para la carga de datos

def load_data(control):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    catalog = control['model']
    if prueba == "Rapidez":
        start_time = get_time()
    else:
        tracemalloc.start()
        start_memory = get_memory()

    
    # TODO: Realizar la carga de datos
    loadAirPorts(control["model"])
    loadFlights(control["model"])
    primerosCo, ultimosCo, primerosCa, ultimosCa, primerosM, ultimosM, total_aeropuertos, total_vuelos= model.getSortedList(control["model"])
    
    
    
    if prueba == "Rapidez":
        end_time = get_time()
        return control, delta_time(start_time, end_time), prueba, primerosCo, ultimosCo, primerosCa, ultimosCa, primerosM, ultimosM, total_aeropuertos, total_vuelos
    else:
        stop_memory = get_memory()
        tracemalloc.stop()
        A_memory = delta_memory(stop_memory, start_memory)
        return control, A_memory, prueba, primerosCo, ultimosCo, primerosCa, ultimosCa, primerosM, ultimosM, total_aeropuertos, total_vuelos
    
    #model.add_data_major_structure(control["model"])
    
    

def loadAirPorts(catalog):
    file = cf.data_dir + 'data/'+'airports-2022.csv'
    
    input_file = csv.DictReader(open(file, encoding='utf-8'), delimiter=";")
    
    for airport in input_file:
        airport["LONGITUD"]= airport["LONGITUD"].replace(",", ".")
        airport["LATITUD"] = airport["LATITUD"].replace(",", ".")
        airport["ALTITUD"] = airport["ALTITUD"].replace(",", ".")
        
        model.add_data(catalog,"airport", airport)
    return catalog

def loadFlights(catalog):
    #OJOOOO cambiar esto
    
    file = cf.data_dir + 'data/'+'fligths-2022.csv'
    
    input_file = csv.DictReader(open(file, encoding='utf-8'), delimiter=";")
    conteo = 0
    diccionario = {}
    for flight in input_file:
        if flight["TIPO_VUELO"] == "AVIACION_CARGA":
            if flight["ORIGEN"] not in diccionario:
                diccionario[flight["ORIGEN"]] = 0
            if flight["DESTINO"] not in diccionario:
                diccionario[flight["DESTINO"]] = 0
            diccionario[flight["ORIGEN"]]+=1
            diccionario[flight["DESTINO"]] +=1
            
        model.add_data(catalog,"flight", flight)
    print(f"CONTEOOOOO {conteo}")
    print(f"MAXIMOOOOO {max(diccionario.values())}")
    return catalog
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
    start_time = get_time()
    kilometros_camino, distance1, distance2, cantidad_paradas , trayectory_time, trayectory_sequence, trayectories_times =model.req_1(control["model"],float(latitud_origen), float(longitud_origen), float(latitud_destino), float(longitud_destino))
    end_time = get_time()
    time= delta_time(start_time, end_time)
    return kilometros_camino, distance1, distance2, cantidad_paradas , trayectory_time, trayectory_sequence, time, trayectories_times
    

def req_2(control, latitud_origen, longitud_origen, latitud_destino, longitud_destino):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    start_time = get_time()
    kilometros_camino, distance1, distance2, cantidad_paradas , trayectory_time, trayectory_sequence =model.req_2(control["model"],float(latitud_origen), float(longitud_origen), float(latitud_destino), float(longitud_destino))
    end_time = get_time()
    time= delta_time(start_time, end_time)
    return kilometros_camino, distance1, distance2, cantidad_paradas , trayectory_time, trayectory_sequence, time


def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    return model.req_3(control["model"])


def req_4(control):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    if prueba == "Rapidez":
        start_time = get_time()
    else:
        tracemalloc.start()
        start_memory = get_memory()

    
    trayectos, paths, airportMC, distancia_total_trayectos, pesoMST, cantidad_trayectos = model.req_4(control["model"])
    if prueba == "Rapidez":
        end_time = get_time()
        return trayectos, paths, airportMC, distancia_total_trayectos, pesoMST, cantidad_trayectos, delta_time(start_time, end_time), prueba
    else:
        stop_memory = get_memory()
        tracemalloc.stop()
        A_memory = delta_memory(stop_memory, start_memory)
        return trayectos, paths, airportMC, distancia_total_trayectos, pesoMST, cantidad_trayectos, A_memory, prueba
    
    

def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    start_time = get_time()
    nombre_mayor, kilometros_totales, nombres_aeropuertos, trayectos_posibles, trayectory_sequence, total_weights = model.req_5(control["model"])
    end_time = get_time()
    time= delta_time(start_time, end_time)
    return nombre_mayor, kilometros_totales, nombres_aeropuertos, trayectos_posibles, trayectory_sequence, total_weights, time



def req_6(control,M):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    return model.req_6(control["model"],M)


def req_7(control, latitud_origen, longitud_origen, latitud_destino, longitud_destino):
    """
    Retorna el resultado del requerimiento 7
    """
    # TODO: Modificar el requerimiento 7
    if prueba == "Rapidez":
        start_time = get_time()
    else:
        tracemalloc.start()
        start_memory = get_memory()

    
    trayectory_time, path_distance1, path_distance2, airports_visited, airports_sequence = model.req_7(control["model"], latitud_origen, longitud_origen, latitud_destino, longitud_destino)
    if prueba == "Rapidez":
        end_time = get_time()
        return trayectory_time, path_distance1, path_distance2, airports_visited, airports_sequence, delta_time(start_time, end_time), prueba
    else:
        stop_memory = get_memory()
        tracemalloc.stop()
        A_memory = delta_memory(stop_memory, start_memory)
        return trayectory_time, path_distance1, path_distance2, airports_visited, airports_sequence, A_memory, prueba
    
def densidad(grafo):
    return model.densidad(grafo)
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
