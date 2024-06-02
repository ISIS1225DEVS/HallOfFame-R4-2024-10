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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
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
from DISClib.DataStructures import edge as e
assert cf
import haversine as haver
import folium
import random
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    
    data_structs = {
        "carga_airports_distance_directed": None,
        "carga_airports_time_directed":None,
        "militar_airports_distance_directed": None,
        "militar_airports_time_directed":None,
        "comercial_airports_distance_directed": None,
        "comercial_airports_time_directed":None,
        "airports_map": None,
        "airports_comercial_map":None,
        "airports_militar_map":None,
        "airports_carga_map":None,
        "search":None,
        "carga_airports_distance": None,
        "carga_airports_time":None,
        "militar_airports_distance": None,
        "militar_airports_time":None,
        "comercial_airports_distance": None,
        "comercial_airports_time":None
        
        
    }
    
    data_structs["airports_map"] = mp.newMap(maptype="PROBING")
    
    
    data_structs["carga_airports_distance"] = gr.newGraph(datastructure="ADJ_LIST",
                                                          directed=False)
    
    
    data_structs["carga_airports_time"] = gr.newGraph(datastructure="ADJ_LIST",
                                                          directed=False)
    
    
    data_structs["militar_airports_distance"] = gr.newGraph(datastructure="ADJ_LIST",
                                                          directed=False)
    
    
    data_structs["militar_airports_time"] = gr.newGraph(datastructure="ADJ_LIST",
                                                          directed=False)
    
    
    data_structs["comercial_airports_distance"] = gr.newGraph(datastructure="ADJ_LIST",
                                                          directed=False)
    
    
    data_structs["comercial_airports_time"] = gr.newGraph(datastructure="ADJ_LIST",
                                                          directed=False)
    
    
    data_structs["carga_airports_distance_directed"] = gr.newGraph(datastructure="ADJ_LIST",
                                                          directed=True)
    
    
    data_structs["carga_airports_time_directed"] = gr.newGraph(datastructure="ADJ_LIST",
                                                          directed=True)
    
    
    data_structs["militar_airports_distance_directed"] = gr.newGraph(datastructure="ADJ_LIST",
                                                          directed=True)
    
    
    data_structs["militar_airports_time_directed"] = gr.newGraph(datastructure="ADJ_LIST",
                                                          directed=True)
    
    
    data_structs["comercial_airports_distance_directed"] = gr.newGraph(datastructure="ADJ_LIST",
                                                          directed=True)
    
    
    data_structs["comercial_airports_time_directed"] = gr.newGraph(datastructure="ADJ_LIST",
                                                          directed=True)
    
    data_structs["airports_comercial_map"] = om.newMap()
    
    
    data_structs["airports_militar_map"] = om.newMap()
    
    
    data_structs["airports_carga_map"] = om.newMap()
    
    return data_structs

# Funciones para agregar informacion al modelo


def add_data_fligths(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    type_flight = data["TIPO_VUELO"]
    
    if type_flight == "AVIACION_CARGA":
        
        origen = data["ORIGEN"]
        destino = data["DESTINO"]
        entry1 = mp.get(data_structs["airports_map"],origen)
        data1 = me.getValue(entry1)
        entry2 = mp.get(data_structs["airports_map"],destino)
        data2 = me.getValue(entry2)
        distance = haversine_data(data1,data2)
        time = float(data["TIEMPO_VUELO"])
        aeronave = data["TIPO_AERONAVE"]
        gr.addEdge(data_structs["carga_airports_distance_directed"],origen,destino,distance)
        gr.addEdge(data_structs["carga_airports_time_directed"],origen,destino,time)
        gr.addEdge(data_structs["carga_airports_distance"],origen,destino,distance)
        gr.addEdge(data_structs["carga_airports_time"],origen,destino,(time,aeronave))
        
        
    elif type_flight == "MILITAR":
        
        origen = data["ORIGEN"]
        destino = data["DESTINO"]
        entry1 = mp.get(data_structs["airports_map"],origen)
        data1 = me.getValue(entry1)
        entry2 = mp.get(data_structs["airports_map"],destino)
        data2 = me.getValue(entry2)
        distance = haversine_data(data1,data2)
        time = float(data["TIEMPO_VUELO"])
        aeronave= data["TIPO_AERONAVE"]
        gr.addEdge(data_structs["militar_airports_distance_directed"],origen,destino,distance)
        gr.addEdge(data_structs["militar_airports_time_directed"],origen,destino,time)
        gr.addEdge(data_structs["militar_airports_distance"],origen,destino,(distance,aeronave))
        gr.addEdge(data_structs["militar_airports_time"],origen,destino,time)
        
    elif type_flight== "AVIACION_COMERCIAL":
        
        origen = data["ORIGEN"]
        destino = data["DESTINO"]
        entry1 = mp.get(data_structs["airports_map"],origen)
        data1 = me.getValue(entry1)
        entry2 = mp.get(data_structs["airports_map"],destino)
        data2 = me.getValue(entry2)
        distance = haversine_data(data1,data2)
        time = float(data["TIEMPO_VUELO"])
        aeronave= data["TIPO_AERONAVE"]
        gr.addEdge(data_structs["comercial_airports_distance_directed"],origen,destino,distance)
        gr.addEdge(data_structs["comercial_airports_time_directed"],origen,destino,time)
        gr.addEdge(data_structs["comercial_airports_distance"],origen,destino,distance)
        gr.addEdge(data_structs["comercial_airports_time"],origen,destino,(time,aeronave))
        
def add_data_airports(data_struct,data):
    
    """
    Agrega cada aeropuerto a un mapa donde la llave es el codigo ICAO y el valor es el diccionario con la información
    
    """
    airport_code = data["ICAO"]
    
    map_airport = data_struct["airports_map"]
    
    mp.put(map_airport,airport_code,data)
    
    gr.insertVertex(data_struct["carga_airports_distance_directed"],airport_code)
    gr.insertVertex(data_struct["carga_airports_time_directed"],airport_code)
    gr.insertVertex(data_struct["militar_airports_distance_directed"],airport_code)
    gr.insertVertex(data_struct["militar_airports_time_directed"],airport_code)
    gr.insertVertex(data_struct["comercial_airports_distance_directed"],airport_code)
    gr.insertVertex(data_struct["comercial_airports_time_directed"],airport_code)
    gr.insertVertex(data_struct["carga_airports_distance"],airport_code)
    gr.insertVertex(data_struct["carga_airports_time"],airport_code)
    gr.insertVertex(data_struct["militar_airports_distance"],airport_code)
    gr.insertVertex(data_struct["militar_airports_time"],airport_code)
    gr.insertVertex(data_struct["comercial_airports_distance"],airport_code)
    gr.insertVertex(data_struct["comercial_airports_time"],airport_code)
    
    
# Funciones para creacion de datos

def add_concurrence(data_structs,data):
    
    type_fligth = data["TIPO_VUELO"]
    origen = data["ORIGEN"]
    destino = data["DESTINO"]
    
    if type_fligth== "AVIACION_COMERCIAL":
        
        mapa = data_structs["airports_comercial_map"]
        grafo = data_structs["comercial_airports_distance_directed"]
        indegree_origen = gr.indegree(grafo,origen)
        outgree_origen = gr.outdegree(grafo,origen)
        concurrence_origen= indegree_origen+outgree_origen
        
        indegree_destino = gr.indegree(grafo,destino)
        outgree_destino =  gr.outdegree(grafo,destino)
        concurrence_destino = indegree_destino+ outgree_destino
        
        exist_concurrence_origen = om.contains(mapa,concurrence_origen)
        exist_concurrence_destino =om.contains(mapa,concurrence_destino)
        
        if exist_concurrence_origen:
            entry = om.get(mapa,concurrence_origen)
            mapa_airports = me.getValue(entry)
            exist_origen = mp.contains(mapa_airports,origen)
            if exist_origen:
                pass
            else:
                mp.put(mapa_airports,origen,0)
        else:
            info_concurrence = mp.newMap(maptype="PROBING",loadfactor=1)
            om.put(mapa,concurrence_origen,info_concurrence)
        
        if exist_concurrence_destino:
            entry = om.get(mapa,concurrence_destino)
            mapa_airports = me.getValue(entry)
            exist_destino = mp.contains(mapa_airports,destino)
            if exist_destino:
                pass
            else:
                mp.put(mapa_airports,destino,0)
        else:
            info_concurrence = mp.newMap(maptype="PROBING")
            om.put(mapa,concurrence_destino,info_concurrence)
            
    if type_fligth == "AVIACION_CARGA":
        
        grafo = data_structs["carga_airports_distance_directed"]
        mapa = data_structs["airports_carga_map"]
        indegree_origen = gr.indegree(grafo,origen)
        outgree_origen = gr.outdegree(grafo,origen)
        concurrence_origen= indegree_origen+outgree_origen
        
        indegree_destino = gr.indegree(grafo,destino)
        outgree_destino =  gr.outdegree(grafo,destino)
        concurrence_destino = indegree_destino+ outgree_destino
        

        exist_concurrence_origen = om.contains(mapa,concurrence_origen)
        exist_concurrence_destino =om.contains(mapa,concurrence_destino)
        
        if exist_concurrence_origen:
            entry = om.get(mapa,concurrence_origen)
            mapa_airports = me.getValue(entry)
            exist_origen = mp.contains(mapa_airports,origen)
            if exist_origen:
                pass
            else:
                mp.put(mapa_airports,origen,0)
        else:
            info_concurrence = mp.newMap(maptype="PROBING")
            om.put(mapa,concurrence_origen,info_concurrence)
        
        if exist_concurrence_destino:
            entry = om.get(mapa,concurrence_destino)
            mapa_airports = me.getValue(entry)
            exist_destino = mp.contains(mapa_airports,destino)
            if exist_destino:
                pass
            else:
                mp.put(mapa_airports,destino,0)
        else:
            info_concurrence = mp.newMap(maptype="PROBING")
            om.put(mapa,concurrence_destino,info_concurrence)
        
    
    if type_fligth == "MILITAR":
        
        grafo = data_structs["militar_airports_distance_directed"]
        mapa = data_structs["airports_militar_map"]
        
        indegree_origen = gr.indegree(grafo,origen)
        outgree_origen = gr.outdegree(grafo,origen)
        concurrence_origen= indegree_origen+outgree_origen
        
        indegree_destino = gr.indegree(grafo,destino)
        outgree_destino =  gr.outdegree(grafo,destino)
        concurrence_destino = indegree_destino+ outgree_destino
        
        exist_concurrence_origen = om.contains(mapa,concurrence_origen)
        exist_concurrence_destino =om.contains(mapa,concurrence_destino)
        
        if exist_concurrence_origen:
            entry = om.get(mapa,concurrence_origen)
            mapa_airports = me.getValue(entry)
            exist_origen = mp.contains(mapa_airports,origen)
            if exist_origen:
                pass
            else:
                mp.put(mapa_airports,origen,0)
        else:
            info_concurrence = mp.newMap(maptype="PROBING")
            om.put(mapa,concurrence_origen,info_concurrence)
        
        if exist_concurrence_destino:
            entry = om.get(mapa,concurrence_destino)
            mapa_airports = me.getValue(entry)
            exist_destino = mp.contains(mapa_airports,destino)
            if exist_destino:
                pass
            else:
                mp.put(mapa_airports,destino,0)
        else:
            info_concurrence = mp.newMap(maptype="PROBING")
            om.put(mapa,concurrence_destino,info_concurrence)
        
            
def get_n_first_last_concurrence(data_structs,datas,num):
    
    """
         Función que obtiene las n primeras y ultimas aeropuertos según el número de concurrencia, devuelve una lista con los diccionarios de la información de cada diccionario.
    """
    mayor = mayor_concurrencia(data_structs,datas,num)
    menor = menor_concurrencia(data_structs,datas,num)
    
    
    for airport in lt.iterator(menor):
        lt.addLast(mayor,airport)
        
      
    return mayor
 
        
        
def mayor_concurrencia (data_all,data_structs,num):
    """
    Crea una lista con la cantidad de aeropuertos de mayor recurrencia digitada por el usuario
    Args:
        data_structs (): 
        num (int): cantidad de aeropuertos a buscar

    Returns:
        _type_: Retorna una lista con las informacion de los aeropuertos con mayor recurrencia ordenados alfabeticamente
    """
    respuesta = lt.newList()
    mayor_concurrence = om.maxKey(data_structs)
    entry = om.get(data_structs,mayor_concurrence)
    airports_map = me.getValue(entry)
    airports = mp.keySet(airports_map)
    airports=sort(airports)
    i=1
    tamano = lt.size(airports)
    while (i <= num) and (i <= tamano):
        entry = mp.get(data_all["airports_map"],lt.getElement(airports,i))
        data = me.getValue(entry)
        data["CONCURRENCE"] = mayor_concurrence
        lt.addFirst(respuesta,data)
        i+=1
    if lt.size(respuesta) >= num:
        pass
    else:
        respuesta = mayor_concurrencia_recursiva(data_all,data_structs,om.floor(data_structs,mayor_concurrence-1),respuesta,num,i)
    
    return respuesta
        
def mayor_concurrencia_recursiva(data_all,data_structs,siguiente,lista,num,cont):
    """
    Agrega a una lista la cantidad de aeropuertos de mayor recurrencia digitada por el usuario de manera recursiva
    Args:
        data_structs (): 
        num (int): cantidad de aeropuertos a buscar

    Returns:
        _type_: Retorna una lista con los nombres de los aeropuertos con mayor recurrencia ordenados alfabeticamente
    """
    
    if siguiente is not None:
        entry = om.get(data_structs,siguiente)
        airports_map = me.getValue(entry)
        airports = mp.keySet(airports_map)
        airports=sort(airports)
        tamano = lt.size(airports)
        i=1
        while (cont<= num) and (i <= tamano):
            entry = mp.get(data_all["airports_map"],lt.getElement(airports,i))
            data = me.getValue(entry)
            data["CONCURRENCE"] = siguiente
            lt.addLast(lista,data)
            cont +=1
            i+=1
        if lt.size(lista) >= num:
            pass
        else:
            lista = mayor_concurrencia_recursiva(data_all,data_structs,om.floor(data_structs,siguiente-1),lista,num,cont)
        return lista
    else:
        return lista
            



def menor_concurrencia (data_all,data_structs,num):
    """
    Crea una lista con la cantidad de aeropuertos de menor recurrencia digitada por el usuario
    Args:
        data_structs (): 
        num (int): cantidad de aeropuertos a buscar

    Returns:
        _type_: Retorna una lista con los nombres de los aeropuertos con menor recurrencia ordenados alfabeticamente
    """
    respuesta = lt.newList()
    menor_concurrence = om.minKey(data_structs)
    entry = om.get(data_structs,menor_concurrence)
    airports_map = me.getValue(entry)
    airports = mp.keySet(airports_map)
    airports=sort(airports)
    i=1
    tamano= lt.size(airports)
    while (i <= num) and (i <= tamano):
        entry = mp.get(data_all["airports_map"],lt.getElement(airports,i))
        data = me.getValue(entry)
        data["CONCURRENCE"] = menor_concurrence
        lt.addFirst(respuesta,data)
        i+=1
    if lt.size(respuesta) >= num:
    
        pass
    else:
        respuesta = menor_concurrencia_recursiva(data_all,data_structs,om.ceiling(data_structs,menor_concurrence+1),respuesta,num,i)
    
    return respuesta 
        
def menor_concurrencia_recursiva(data_all,data_structs,siguiente,lista,num,cont):
    """
    Agrega a una lista de manera recursiva la cantidad de aeropuertos de menor recurrencia digitada por el usuario
    Args:
        data_structs (): 
        num (int): cantidad de aeropuertos a buscar

    Returns:
        _type_: Retorna una lista con los nombres de los aeropuertos con menor recurrencia ordenados alfabeticamente
    """
    if siguiente is not None:
        entry = om.get(data_structs,siguiente)
        airports_map = me.getValue(entry)
        airports = mp.keySet(airports_map)
        airports=sort(airports)
        tamano = lt.size(airports)
        i =1
        while (cont<= num) and (i <= tamano):
            entry = mp.get(data_all["airports_map"],lt.getElement(airports,i))
            data = me.getValue(entry)
            data["CONCURRENCE"] = siguiente
            lt.addFirst(lista,data)
            cont +=1
            i+=1
        if lt.size(lista) >= num:
            
            pass
        
        else:
            lista =menor_concurrencia_recursiva(data_all,data_structs,om.ceiling(data_structs,siguiente+1),lista,num,cont)
        
        return lista
    
    else:
        return lista
        
def new_data(data_origen,data_destino,distancia,tiempo,aeronave):
    
    info ={
        "ICAO_origen" : None,
        "name_origen" : None,
        "ciudad_origen" : None,
        "pais_origen" : None,
        "ICAO_destino": None,
        "name_destino" : None,
        "ciudad_destino" : None,
        "pais_destino" : None,
        "distancia" : None,
        "tiempo" : None,
        "aeronave" : None
    }
    info["aeronave"] = aeronave
    
    info["tiempo"] = tiempo
    
    info["distancia"] = distancia
    
    info["pais_destino"] = data_destino["PAIS"]
    
    info["ciudad_destino"] = data_destino["CIUDAD"]
    
    info["name_destino"] = data_destino["NOMBRE"]

    info["ICAO_destino"] = data_destino["ICAO"]
    
    info["pais_origen"] = data_origen["PAIS"]
    
    info["ciudad_origen"] = data_origen["CIUDAD"]
    
    info["name_origen"] = data_origen["NOMBRE"]
    
    info["ICAO_origen"] = data_origen["ICAO"]
    
    return info
    

    
#################################################################################################################################################################
#################################################################################################################################################################
#requerimientos

def req_1(data_structs,origen_latitud,origen_longitud,destino_latitud,destino_longitud,method):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    distance_origen,airport_origen,distance_destino,airport_destino = get_nearby_airports(data_structs,(origen_latitud,origen_longitud),(destino_latitud,destino_longitud))
    
    entry = mp.get(data_structs["airports_map"],airport_origen)
    data_origen = me.getValue(entry)
    entry = mp.get(data_structs["airports_map"],airport_destino)
    data_destino = me.getValue(entry)
    
    respuesta = lt.newList()
    if distance_origen<=30 and distance_destino <= 30:
        tiempo_total =0
        distancia_total = distance_origen+distance_destino
        if method == 1 :
            
            data_structs["search"] = bfs.BreathFirstSearch(data_structs["comercial_airports_distance_directed"],airport_origen)
            exist_camino = bfs.hasPathTo(data_structs["search"],airport_destino)
            if exist_camino:
                
                ruta = bfs.pathTo(data_structs["search"],airport_destino)
                total_airports = st.size(ruta)
                for x in range(0,total_airports):
                    
                    airport=st.pop(ruta)
                    entry = mp.get(data_structs["airports_map"],airport)
                    data_airport= me.getValue(entry)
                    if st.size(ruta)>0:
                        
                        siguiente = st.top(ruta)
                        arco_distance = gr.getEdge(data_structs["comercial_airports_distance_directed"],airport,siguiente)
                        distance = float(arco_distance["weight"])
                        distancia_total += distance
                        arco_time =gr.getEdge(data_structs["comercial_airports_time_directed"],airport,siguiente)
                        time = float(arco_time["weight"])
                        tiempo_total += time
                    lt.addLast(respuesta,data_airport)
                 
        if method == 2:
            
            data_structs["search"] = dfs.DepthFirstSearch(data_structs["comercial_airports_distance_directed"],airport_origen)
            exist_camino = dfs.hasPathTo(data_structs["search"],airport_destino)
            
            if exist_camino:
                
                ruta = dfs.pathTo(data_structs["search"],airport_destino)
                total_airports = st.size(ruta)
                
                for x in range(0,total_airports):
                    
                    airport=st.pop(ruta)
                    entry = mp.get(data_structs["airports_map"],airport)
                    data_airport= me.getValue(entry)
                    if st.size(ruta)>0:
                        
                        siguiente = st.top(ruta)
                        arco_distance = gr.getEdge(data_structs["comercial_airports_distance_directed"],airport,siguiente)
                        distance = float(arco_distance["weight"])
                        distancia_total += distance
                        arco_time =gr.getEdge(data_structs["comercial_airports_time_directed"],airport,siguiente)
                        time = float(arco_time["weight"])
                        tiempo_total += time
                        
                    lt.addLast(respuesta,data_airport)
        
        return distancia_total,total_airports,respuesta,tiempo_total
                    
                 
    
    else:
        
        print("El aeropuerto más cercano al origen es: ",airport_origen, " con una distancia a tu ubicacion de :",distance_origen, " donde su latitud es: ",data_origen["LATITUD"]," y su longitud es: ",data_origen["LONGITUD"])
        print("El aeropuerto más cercano al destino es: ",airport_destino, " con una distancia a tu ubicacion de :",distance_destino," donde su latitud es: ",data_destino["LATITUD"]," y su longitud es: ",data_destino["LONGITUD"])
        
        return None
        
        
def req_2(data_structs,origen_latitud,origen_longitud,destino_latitud,destino_longitud):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    distance_origen,airport_origen,distance_destino,airport_destino = get_nearby_airports(data_structs,(origen_latitud,origen_longitud),(destino_latitud,destino_longitud))
    
    entry = mp.get(data_structs["airports_map"],airport_origen)
    data_origen = me.getValue(entry)
    entry = mp.get(data_structs["airports_map"],airport_destino)
    data_destino = me.getValue(entry)
    
    respuesta = lt.newList()
    if distance_origen<=30 and distance_destino <= 30:
        tiempo_total =0
        distancia_total = distance_origen+distance_destino
        data_structs["search"] = bfs.BreathFirstSearch(data_structs["comercial_airports_distance_directed"],airport_origen)
        exist_camino = bfs.hasPathTo(data_structs["search"],airport_destino)
        if exist_camino:
                
                ruta = bfs.pathTo(data_structs["search"],airport_destino)
                total_airports = st.size(ruta)
                for x in range(0,total_airports):
                    
                    airport=st.pop(ruta)
                    entry = mp.get(data_structs["airports_map"],airport)
                    data_airport= me.getValue(entry)
                    if st.size(ruta)>0:
                        
                        siguiente = st.top(ruta)
                        arco_distance = gr.getEdge(data_structs["comercial_airports_distance_directed"],airport,siguiente)
                        distance = float(arco_distance["weight"])
                        distancia_total += distance
                        arco_time =gr.getEdge(data_structs["comercial_airports_time_directed"],airport,siguiente)
                        time = float(arco_time["weight"])
                        tiempo_total += time
                    lt.addLast(respuesta,data_airport)
                 
        
        return distancia_total,total_airports,respuesta,tiempo_total
                    
                 
    
    else:
        
        print("El aeropuerto más cercano al origen es: ",airport_origen, " con una distancia a tu ubicacion de :",distance_origen, " donde su latitud es: ",data_origen["LATITUD"]," y su longitud es: ",data_origen["LONGITUD"])
        print("El aeropuerto más cercano al destino es: ",airport_destino, " con una distancia a tu ubicacion de :",distance_destino," donde su latitud es: ",data_destino["LATITUD"]," y su longitud es: ",data_destino["LONGITUD"])
        
        return None


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    data_aeropuerto_mayor = mayor_concurrencia(data_structs,data_structs["airports_comercial_map"],1)
    name_aeropuerto_mayor = lt.getElement(data_aeropuerto_mayor,0)["ICAO"]
    
    search = prim.PrimMST(data_structs["comercial_airports_distance"],name_aeropuerto_mayor) 
    
    distancia_total = prim.weightMST(data_structs["comercial_airports_distance"],search)
    
    total_trayectos = lt.size(search["mst"]) 
    
    respuesta = lt.newList(datastructure="ARRAY_LIST")
    
    for ruta in lt.iterator(search["mst"]):
        
        origen = e.either(ruta)
        entry = mp.get(data_structs["airports_map"],origen)
        data_origen = me.getValue(entry)
        destino = e.other(ruta,origen)
        entry = mp.get(data_structs["airports_map"],destino)
        data_destino = me.getValue(entry)
        distancia = e.weight(ruta)
        tiempo,aeronave = e.weight(gr.getEdge(data_structs["comercial_airports_time"],origen,destino))
        
        data = new_data(data_origen,data_destino,distancia,tiempo,aeronave)
        
        lt.addLast(respuesta,data)
    
    return respuesta,data_aeropuerto_mayor,total_trayectos,distancia_total




def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    data_aeropuerto_mayor = mayor_concurrencia(data_structs,data_structs["airports_carga_map"],1)
    name_aeropuerto_mayor = lt.getElement(data_aeropuerto_mayor,0)["ICAO"]
    
    search = prim.PrimMST(data_structs["carga_airports_distance"],name_aeropuerto_mayor)
       
    distancia_total = prim.weightMST(data_structs["carga_airports_distance"],search)
    
    total_trayectos = lt.size(search["mst"])
    
    respuesta = lt.newList(datastructure="ARRAY_LIST")
    
    for ruta in lt.iterator(search["mst"]):
        
        origen = e.either(ruta)
        entry = mp.get(data_structs["airports_map"],origen)
        data_origen = me.getValue(entry)
        destino = e.other(ruta,origen)
        entry = mp.get(data_structs["airports_map"],destino)
        data_destino = me.getValue(entry)
        distancia = e.weight(ruta)
        tiempo,aeronave = e.weight(gr.getEdge(data_structs["carga_airports_time"],origen,destino))
        
        data = new_data(data_origen,data_destino,distancia,tiempo,aeronave)
        
        lt.addLast(respuesta,data)
    return respuesta,data_aeropuerto_mayor,total_trayectos,distancia_total



def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    data_aeropuerto_mayor = mayor_concurrencia(data_structs,data_structs["airports_militar_map"],1)
    name_aeropuerto_mayor = lt.getElement(data_aeropuerto_mayor,0)["ICAO"]
    
    search = prim.PrimMST(data_structs["militar_airports_time"],name_aeropuerto_mayor)
       
    data_rutas = prim.edgesMST(data_structs["militar_airports_time"],search)
    
    total_trayectos = lt.size(search["mst"])
    
    respuesta = lt.newList(datastructure="ARRAY_LIST")
    distancia_total =0 
    
    for ruta in lt.iterator(search["mst"]):
        
        origen = e.either(ruta)
        entry = mp.get(data_structs["airports_map"],origen)
        data_origen = me.getValue(entry)
        destino = e.other(ruta,origen)
        entry = mp.get(data_structs["airports_map"],destino)
        data_destino = me.getValue(entry)
        tiempo = e.weight(ruta)
        distancia,aeronave = e.weight(gr.getEdge(data_structs["militar_airports_distance"],origen,destino))
        distancia_total+=distancia
        
        data = new_data(data_origen,data_destino,distancia,tiempo,aeronave)
        
        lt.addLast(respuesta,data)
        
    return respuesta,data_aeropuerto_mayor,total_trayectos,distancia_total




def req_6(data_structs,num):
    """
    Función que soluciona el requerimiento 6
    """
    num+=1
    # TODO: Realizar el requerimiento 6
    
    airports = mayor_concurrencia(data_structs,data_structs["airports_comercial_map"],num)
    data_airport_mayor = lt.getElement(airports,1)
    lt.deleteElement(airports,1)
    key_airport_mayor = data_airport_mayor["ICAO"] 
    name_airport_mayor = data_airport_mayor["NOMBRE"]
    search = djk.Dijkstra(data_structs["comercial_airports_distance_directed"],key_airport_mayor)
    cont =2
    respuesta = lt.newList()
    for airport in lt.iterator(airports):
        key_airport = airport["ICAO"]
        name_airport = airport["NOMBRE"]
        exist_ruta = djk.hasPathTo(search,key_airport)
        if  exist_ruta:
            distancia_total = djk.distTo(search,key_airport)
            ruta = djk.pathTo(search,key_airport)
            data = new_data_req6(data_structs,ruta,distancia_total,key_airport_mayor)
            
            lt.addLast(respuesta,data)
            
        else:
            print("No existe una ruta entre el aeropuerto de mayor importancia: ",name_airport_mayor, " y el ",cont," de mayor importancia ",name_airport)
        
        cont+=1
    
    return respuesta,data_airport_mayor



def new_data_req6(data,ruta,distancia,key_aiport_mayor):
    
    info ={"distancia":None,
           "ruta": None,
           "airports":None,
           "total":None}
    
    info["distancia"] = distancia
    
    info["ruta"] = lt.newList()
    
    info["total"] = st.size(ruta)+1

    info["airports"] = lt.newList()
    
    airport_mayor = new_data_apoyo_req6(data,key_aiport_mayor)
    
    lt.addLast(info["airports"],airport_mayor)
    
    while (not st.isEmpty(ruta)):
        
        airport = st.pop(ruta)
        
        key_airport = airport["vertexB"]
        
        dato= new_data_apoyo_req6(data,key_airport)
        
        lt.addLast(info["ruta"],airport)
        
        lt.addLast(info["airports"],dato)
    
    return info

    


def new_data_apoyo_req6(data,key_airport):
    
    info =  {"name":None,
             "ICAO":None,
             "ciudad":None,
             "pais":None}
    
    mapa =data["airports_map"]
    
    entry = mp.get(mapa,key_airport)
    data_airport = me.getValue(entry)
    
    info["name"]= data_airport["NOMBRE"]
    
    info["ICAO"] = data_airport["ICAO"]
    
    info["ciudad"] = data_airport["CIUDAD"]
    
    info["pais"] = data_airport["PAIS"]
    
    
    return info

def req_7(data_structs,origen_latitud,origen_longitud,destino_latitud,destino_longitud):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    distance_origen,airport_origen,distance_destino,airport_destino = get_nearby_airports(data_structs,(origen_latitud,origen_longitud),(destino_latitud,destino_longitud))
    
    entry = mp.get(data_structs["airports_map"],airport_origen)
    data_origen = me.getValue(entry)
    entry = mp.get(data_structs["airports_map"],airport_destino)
    data_destino = me.getValue(entry)
    
    respuesta = lt.newList()
    if distance_origen<=30 and distance_destino <= 30:
        tiempo_total =0
        distancia_total = distance_origen+distance_destino
        data_structs["search"] = djk.Dijkstra(data_structs["comercial_airports_time_directed"],airport_origen)
        exist_camino = djk.hasPathTo(data_structs["search"],airport_destino)
        if exist_camino:
                
            ruta = djk.pathTo(data_structs["search"],airport_destino)
            total_airports = st.size(ruta)+1
            while (not st.isEmpty(ruta)):
                airport=st.pop(ruta)
                key_airportA = airport["vertexA"]
                entry_A = mp.get(data_structs["airports_map"],key_airportA)
                airportA= me.getValue(entry_A)
                time_A_B = airport["weight"]
                key_airportB = airport["vertexB"]
                entry_B = mp.get(data_structs["airports_map"],key_airportB)
                airportB= me.getValue(entry_B)
                arco_distance = gr.getEdge(data_structs["comercial_airports_distance_directed"],key_airportA,key_airportB)
                distance_A_B= e.weight(arco_distance)
                tiempo_total+=time_A_B
                distancia_total+=distance_A_B
                data_fligth = new_data_req7(airportA,airportB,time_A_B,distance_A_B)
                lt.addLast(respuesta,data_fligth)
                 
        return distancia_total,total_airports,respuesta,tiempo_total
                    
                 
    
    else:
        
        print("El aeropuerto más cercano al origen es: ",airport_origen, " con una distancia a tu ubicacion de :",distance_origen, " donde su latitud es: ",data_origen["LATITUD"]," y su longitud es: ",data_origen["LONGITUD"])
        print("El aeropuerto más cercano al destino es: ",airport_destino, " con una distancia a tu ubicacion de :",distance_destino," donde su latitud es: ",data_destino["LATITUD"]," y su longitud es: ",data_destino["LONGITUD"])
        
        return None
    
def new_data_req7(airportA,airportB,time_A_B,distance_A_B):
    
    info = {
        "ICAO_origen" :None,
        "Airport_O":None,
        "Ciudad_O":None,
        "Pais_O":None,
        "ICAO_destino" :None,
        "Airport_D":None,
        "Ciudad_D":None,
        "Pais_D":None,
        "tiempo":None,
        "distancia":None   
    }
    
    info["ICAO_origen"] = airportA["ICAO"]
    
    info["Airport_O"] = airportA["NOMBRE"]
    
    info["Ciudad_O"] = airportA["CIUDAD"]
    
    info["Pais_O"] = airportA["PAIS"]
    
    info["ICAO_destino"] = airportB["ICAO"]
    
    info["Airport_D"] = airportB["NOMBRE"]
    
    info["Ciudad_D"] = airportB["CIUDAD"]
    
    info["Pais_D"] = airportB["PAIS"]
    
    info["tiempo"] = time_A_B
    
    info["distancia"] = distance_A_B
    
    return info

def req_8(data_structs,respuesta):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    mapa_interactivo(data_structs,respuesta)


# Funciones auxiliares

def get_nearby_airports(data_structs,punto1,punto2):
    """_summary_
        Obtiene los aeropuertos más cercanos a los puntos dados
    Args:
        data_structs (_type_): _description_
        punto1 (Tuple): Punto de partida
        punto2 (Tuple): Punto de llegada
    """
    airports = mp.keySet(data_structs["airports_map"])
    
    mas_cercano_origen= None
    aeropuerto_origen = None
    mas_cercano_destino =None
    aeropuerto_destino = None
    
    for airport in lt.iterator(airports):
        entry= mp.get(data_structs["airports_map"],airport)
        data_airport = me.getValue(entry)
        latitud_airport = data_airport["LATITUD"]
        longitud_airport = data_airport["LONGITUD"]
        distance_origen = haversine(punto1,(latitud_airport,longitud_airport))
        distance_destino = haversine(punto2,(latitud_airport,longitud_airport))
        
        if aeropuerto_destino== None and aeropuerto_origen == None :
            aeropuerto_origen= airport
            aeropuerto_destino= airport
            mas_cercano_origen= distance_origen
            mas_cercano_destino = distance_destino
        else:
            if distance_origen < mas_cercano_origen:
                mas_cercano_origen = distance_origen
                aeropuerto_origen= airport
            
            if distance_destino < mas_cercano_destino:
                mas_cercano_destino= distance_destino
                aeropuerto_destino = airport
    
    return mas_cercano_origen,aeropuerto_origen,mas_cercano_destino,aeropuerto_destino
            
            
        

def mapa_interactivo(data,mapa):
    """
    Funcion que imprime las ofertas en un mapa interactivo
    Args:
        jobs (_type_): lista de trabajos según el requerimiento
        
    """
    colores = ['red', 'blue', 'green', 'purple', 'orange', 'darkred','lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
    mi_mapa = folium.Map(location=(0, 0),control_scale=True,zoom_start=10)
    for i in range(1,8):
        if (i == 3 or i==4 or i ==5 or i==7) and mp.size(mapa) != None:
            entry= mp.get(mapa,i)
            if entry != None:
                airports = me.getValue(entry)
                req = folium.FeatureGroup(("requerimiento "+str(i))).add_to(mi_mapa)
                color = random.choice(colores)
                for airport in lt.iterator(airports):
                    key_airport_o = airport["ICAO_origen"]
                    key_airport_d = airport["ICAO_destino"]
                    entry_origen = mp.get(data["airports_map"],key_airport_o)
                    data_origen = me.getValue(entry_origen)
                    entry_destino = mp.get(data["airports_map"],key_airport_d)
                    data_destino = me.getValue(entry_destino)
                    latitud_O=float(data_origen["LATITUD"].replace(",","."))
                    longitud_O = float(data_origen["LONGITUD"].replace(",","."))
                    
                    latitud_d=float(data_destino["LATITUD"].replace(",","."))
                    longitud_d = float(data_destino["LONGITUD"].replace(",","."))
        
                    info_origen = str(data_origen["NOMBRE"] + " "+ data_origen["CIUDAD"]+ " " + data_origen["PAIS"])
                    folium.Marker(location=[latitud_O,longitud_O],tooltip=key_airport_o,popup=info_origen,icon=folium.Icon(color=color),).add_to(req)
                    
                    info_destino = str(data_destino["NOMBRE"] + " "+ data_destino["CIUDAD"]+ " " + data_destino["PAIS"])
                    folium.Marker(location=[latitud_d,longitud_d],tooltip=key_airport_d,popup=info_destino,icon=folium.Icon(color=color),).add_to(req)
                    
                    coordenadas = [ (latitud_O,longitud_O),(latitud_d,longitud_d)]
                    
                    folium.PolyLine(coordenadas).add_to(req)
                    
        elif (i == 1 or i==2) and mp.size(mapa) != None:
                entry= mp.get(mapa,i)
                if entry != None:
                    airports = me.getValue(entry)
                    req = folium.FeatureGroup(("requerimiento "+str(i))).add_to(mi_mapa)
                    color = random.choice(colores)
                    for i in range(1,lt.size(airports)):
                        key_airport_o = lt.getElement(airports,i)["ICAO"]
                        key_airport_d = lt.getElement(airports,i+1)["ICAO"]
                        entry_origen = mp.get(data["airports_map"],key_airport_o)
                        data_origen = me.getValue(entry_origen)
                        entry_destino = mp.get(data["airports_map"],key_airport_d)
                        data_destino = me.getValue(entry_destino)
                        latitud_O=float(data_origen["LATITUD"].replace(",","."))
                        longitud_O = float(data_origen["LONGITUD"].replace(",","."))
                        
                        latitud_d=float(data_destino["LATITUD"].replace(",","."))
                        longitud_d = float(data_destino["LONGITUD"].replace(",","."))
            
                        info_origen = str(data_origen["NOMBRE"] + " "+ data_origen["CIUDAD"]+ " " + data_origen["PAIS"])
                        folium.Marker(location=[latitud_O,longitud_O],tooltip=key_airport_o,popup=info_origen,icon=folium.Icon(color=color),).add_to(req)
                        
                        info_destino = str(data_destino["NOMBRE"] + " "+ data_destino["CIUDAD"]+ " " + data_destino["PAIS"])
                        folium.Marker(location=[latitud_d,longitud_d],tooltip=key_airport_d,popup=info_destino,icon=folium.Icon(color=color),).add_to(req)
                        
                        coordenadas = [ (latitud_O,longitud_O),(latitud_d,longitud_d)]
                        
                        folium.PolyLine(coordenadas).add_to(req)
                        
        elif (i == 6 ) and mp.size(mapa) != None:
                entry= mp.get(mapa,i)
                if entry != None:
                    airports = me.getValue(entry)
                    req = folium.FeatureGroup(("requerimiento "+str(i))).add_to(mi_mapa)
                    color = random.choice(colores)
                    for airport in lt.iterator(airports):
                        
                        for arco in lt.iterator(airport["ruta"]):
                            key_airport_o = arco["vertexA"]
                            key_airport_d = arco["vertexB"]
                            entry_origen = mp.get(data["airports_map"],key_airport_o)
                            data_origen = me.getValue(entry_origen)
                            entry_destino = mp.get(data["airports_map"],key_airport_d)
                            data_destino = me.getValue(entry_destino)
                            latitud_O=float(data_origen["LATITUD"].replace(",","."))
                            longitud_O = float(data_origen["LONGITUD"].replace(",","."))
                            
                            latitud_d=float(data_destino["LATITUD"].replace(",","."))
                            longitud_d = float(data_destino["LONGITUD"].replace(",","."))
                
                            info_origen = str(data_origen["NOMBRE"] + " "+ data_origen["CIUDAD"]+ " " + data_origen["PAIS"])
                            folium.Marker(location=[latitud_O,longitud_O],tooltip=key_airport_o,popup=info_origen,icon=folium.Icon(color=color),).add_to(req)
                            
                            info_destino = str(data_destino["NOMBRE"] + " "+ data_destino["CIUDAD"]+ " " + data_destino["PAIS"])
                            folium.Marker(location=[latitud_d,longitud_d],tooltip=key_airport_d,popup=info_destino,icon=folium.Icon(color=color),).add_to(req)
                            
                            coordenadas = [ (latitud_O,longitud_O),(latitud_d,longitud_d)]
                            
                            folium.PolyLine(coordenadas).add_to(req)
                        
        else:
                print("No hay datos según lo reportado por el requerimiento "+str(i))
            
            
    req = folium.LayerControl().add_to(mi_mapa)
    
    mi_mapa.save("reto04.html")       
        


# Funciones de ordenamiento


def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    
    if data_1 > data_2:
        return True
    elif data_1==data_2:
        return data_1<data_2
    else:
        return False

def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    
    lista_ordenada = merg.sort(data_structs,sort_criteria)
    
    return lista_ordenada

def haversine_data(data1,data2):
    """ Función que calcula la distancia entre dos puntos de la tierra usando el algoritmo de haversine

    Args:
        data1 : Contiene la información de un aeropuerto
        data2 : Contiene la información de otro aeropuerto

    Returns:
        float: Devuelve la distancia entre dos puntos
    """
    
    lat1 = float(data1["LATITUD"].replace(",","."))
    long1 = float(data1["LONGITUD"].replace(",","."))
    lat2 = float(data2["LATITUD"].replace(",","."))
    long2 = float(data2["LONGITUD"].replace(",","."))
    distance = haver.haversine((lat1,long1),(lat2,long2))

    return distance

def get_first_last_n(lista, n_primeros_ultimos):
    """
    Retorna una sublizta de los n primeros y n ultimos elementos de una lista
    """
    sublist = lt.subList(lista, 1, n_primeros_ultimos)
    
    for i in range(lt.size(lista) - n_primeros_ultimos + 1, lt.size(lista) + 1):
        lt.addLast(sublist, lt.getElement(lista,i))
        
    return sublist

def haversine (dato1,dato2):
    latitud_data1 = float(dato1[0])
    longitud_dato1 = float(dato1[1])
    latitud_data2 = float(dato2[0].replace(",","."))
    longitud_data2 = float(dato2[1].replace(",","."))
    
    distance = haver.haversine((latitud_data1,longitud_dato1),(latitud_data2,longitud_data2))
    
    return distance