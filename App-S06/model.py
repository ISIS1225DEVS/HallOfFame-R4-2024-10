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
assert cf
from haversine import haversine, Unit
from tabulate import tabulate
import folium 
import webbrowser

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
    data_structs={"grafo_distancia": None}
    data_structs["grafo_distancia"]=gr.newGraph(datastructure='ADJ_LIST',
                                      directed=True,
                                      size=4000)
    data_structs["grafo_tiempo"]=gr.newGraph(datastructure='ADJ_LIST',directed=True,size=4000) 
    data_structs["aeropuertos"]=mp.newMap(430, maptype='PROBING') 
    data_structs["rutas"]=mp.newMap(3022, maptype='PROBING')
    data_structs["Arbol_concurrencia_carga"]=om.newMap(omaptype='RBT', cmpfunction=cmp_mayor_menor)
    data_structs["Arbol_concurrencia_comercial"]=om.newMap(omaptype='RBT', cmpfunction=cmp_mayor_menor)
    data_structs["Arbol_concurrencia_militar"]=om.newMap(omaptype='RBT', cmpfunction=cmp_mayor_menor)
    data_structs["Grafo_Comercial_Tiempo"]=gr.newGraph(datastructure='ADJ_LIST',directed=True,size=4000)
    data_structs["Grafo_Carga_Tiempo"]=gr.newGraph(datastructure='ADJ_LIST',directed=True,size=4000)
    data_structs["Grafo_Militar_Tiempo"]=gr.newGraph(datastructure='ADJ_LIST',directed=True,size=4000)
    data_structs["Grafo_comercial_distancia"]=gr.newGraph(datastructure='ADJ_LIST',directed=True,size=4000)
    data_structs["Grafo_Carga_distancia"]=gr.newGraph(datastructure='ADJ_LIST',directed=True,size=4000)
    data_structs["Grafo_Militar_distancia"]=gr.newGraph(datastructure='ADJ_LIST',directed=True,size=4000)
    
    return data_structs

# Funciones para agregar informacion al modelo

def load_map (mapa, llave, prefijo, valor):
    entry = prefijo.get(mapa, llave)
    if entry == None:
        prefijo.put(mapa, llave, valor)
    else:
        valor = me.getValue(entry)
    return valor

def add_node(data_structs, node):
    """
    Agrega un nodo al grafo.
    """
    node["LATITUD"]=float(node["LATITUD"].replace(",",".") )
    node["LONGITUD"]=float(node["LONGITUD"].replace(",","."))
    node["ALTITUD"]=int(node["ALTITUD"])
    node["AVIACION_CARGA"]=lt.newList('ARRAY_LIST')
    node["AVIACION_COMERCIAL"]=lt.newList('ARRAY_LIST')
    node["MILITAR"]=lt.newList('ARRAY_LIST')
    gr.insertVertex(data_structs["grafo_distancia"], node["ICAO"])
    gr.insertVertex(data_structs["grafo_tiempo"], node["ICAO"])
    gr.insertVertex(data_structs["Grafo_Comercial_Tiempo"], node["ICAO"])
    gr.insertVertex(data_structs["Grafo_Carga_Tiempo"], node["ICAO"])
    gr.insertVertex(data_structs["Grafo_Militar_Tiempo"], node["ICAO"])
    gr.insertVertex(data_structs["Grafo_comercial_distancia"], node["ICAO"])
    gr.insertVertex(data_structs["Grafo_Carga_distancia"], node["ICAO"])
    gr.insertVertex(data_structs["Grafo_Militar_distancia"], node["ICAO"])
    load_map(data_structs["aeropuertos"], node["ICAO"], mp, node)
    

def add_edge(data_structs, edge):
    """
    Agrega una arista al grafo.
    """
    edge["TIEMPO_VUELO"]=int(edge["TIEMPO_VUELO"])
    nodo_origen=me.getValue(mp.get(data_structs["aeropuertos"], edge["ORIGEN"]))
    nodo_destino=me.getValue(mp.get(data_structs["aeropuertos"], edge["DESTINO"]))
    tupla_origen=(nodo_origen["LATITUD"],nodo_origen["LONGITUD"])
    tupla_destino=(nodo_destino["LATITUD"],nodo_destino["LONGITUD"]) 
    distancia=haversine(tupla_origen,tupla_destino)
    gr.addEdge(data_structs["grafo_distancia"], edge["ORIGEN"], edge["DESTINO"], distancia)
    gr.addEdge(data_structs["grafo_tiempo"], edge["ORIGEN"], edge["DESTINO"], edge["TIEMPO_VUELO"])
    lt.addLast(nodo_origen[edge["TIPO_VUELO"]],edge)
    lt.addLast(nodo_destino[edge["TIPO_VUELO"]],edge)
    
    if edge["TIPO_VUELO"]=="AVIACION_COMERCIAL":
        gr.addEdge(data_structs["Grafo_Comercial_Tiempo"], edge["ORIGEN"], edge["DESTINO"], edge["TIEMPO_VUELO"])
        gr.addEdge(data_structs["Grafo_comercial_distancia"], edge["ORIGEN"], edge["DESTINO"], distancia)
        load_map(data_structs["rutas"], edge["ORIGEN"]+edge["DESTINO"]+"COMERCIAL", mp, edge)
    
    elif edge["TIPO_VUELO"]=="AVIACION_CARGA":
        gr.addEdge(data_structs["Grafo_Carga_Tiempo"], edge["ORIGEN"], edge["DESTINO"], edge["TIEMPO_VUELO"])
        gr.addEdge(data_structs["Grafo_Carga_distancia"], edge["ORIGEN"], edge["DESTINO"], distancia)
        load_map(data_structs["rutas"], edge["ORIGEN"]+edge["DESTINO"]+"CARGA", mp, edge)
    
    elif edge["TIPO_VUELO"]=="MILITAR":
        gr.addEdge(data_structs["Grafo_Militar_Tiempo"], edge["ORIGEN"], edge["DESTINO"], edge["TIEMPO_VUELO"])
        gr.addEdge(data_structs["Grafo_Militar_distancia"], edge["ORIGEN"], edge["DESTINO"], distancia)
        load_map(data_structs["rutas"], edge["ORIGEN"]+edge["DESTINO"]+"MILITAR",mp,edge)
   

def data_size(data_structs, element_type):
    """
    Devuelve el número de nodos o aristas en el grafo, según corresponda.
    """
    if element_type == "nodes":
        return gr.numVertices(data_structs["grafo_distancia"])
    elif element_type == "edges":
        return gr.numEdges(data_structs["grafo_distancia"])
    else:
        return None


def cargar_arboles_concurrencias(data_structs):
    for aeropuerto in lt.iterator(mp.keySet(data_structs["aeropuertos"])):
        nodo=me.getValue(mp.get(data_structs["aeropuertos"], aeropuerto))
        nodo["CONCURRENCIA_Comercial"]=lt.size(nodo["AVIACION_COMERCIAL"])
        nodo["CONCURRENCIA_Carga"]=lt.size(nodo["AVIACION_CARGA"])
        nodo["CONCURRENCIA_Militar"]=lt.size(nodo["MILITAR"])
        concurrencia_comercial=lt.size(nodo["AVIACION_COMERCIAL"])
        concurrencia_carga=lt.size(nodo["AVIACION_CARGA"])
        concurrencia_militar=lt.size(nodo["MILITAR"])
        lista_aeropuertos_carga=load_map(data_structs["Arbol_concurrencia_carga"], concurrencia_carga, om, lt.newList('ARRAY_LIST'))
        lt.addLast(lista_aeropuertos_carga, nodo)
        lista_aeropuertos_comercial=load_map(data_structs["Arbol_concurrencia_comercial"], concurrencia_comercial, om, lt.newList('ARRAY_LIST'))
        lt.addLast(lista_aeropuertos_comercial, nodo)
        lista_aeropuertos_militar=load_map(data_structs["Arbol_concurrencia_militar"], concurrencia_militar, om, lt.newList('ARRAY_LIST'))
        lt.addLast(lista_aeropuertos_militar, nodo)
        if lt.size(nodo["AVIACION_COMERCIAL"])==0:
            gr.removeVertex(data_structs["Grafo_Comercial_Tiempo"], aeropuerto)
            gr.removeVertex(data_structs["Grafo_comercial_distancia"], aeropuerto)
        if lt.size(nodo["AVIACION_CARGA"])==0:
            gr.removeVertex(data_structs["Grafo_Carga_Tiempo"], aeropuerto)
            gr.removeVertex(data_structs["Grafo_Carga_distancia"], aeropuerto)
        if lt.size(nodo["MILITAR"])==0:
            gr.removeVertex(data_structs["Grafo_Militar_Tiempo"], aeropuerto)
            gr.removeVertex(data_structs["Grafo_Militar_distancia"], aeropuerto)
        
    
    data_structs["Lista_aeropuertos_comercial"]=convertir_lista_listas(om.valueSet(data_structs["Arbol_concurrencia_comercial"]))
    data_structs["Lista_aeropuertos_carga"]=convertir_lista_listas(om.valueSet(data_structs["Arbol_concurrencia_carga"]))
    data_structs["Lista_aeropuertos_militar"]=convertir_lista_listas(om.valueSet(data_structs["Arbol_concurrencia_militar"])) #lista ordenada por importancia (concurrencia)

    
def convertir_lista_listas(lista):
    lista_listas=lt.newList('ARRAY_LIST')
    for sub_lista in lt.iterator(lista):
        for elemento in lt.iterator(sub_lista):
            lt.addLast(lista_listas, elemento)
    return lista_listas

lista_coordenadas = lt.newList(datastructure="ARRAY_LIST")
req = 0
        
def req_1(data_structs, punto_origen_lat, punto_origen_long, punto_destino_lat, punto_destino_long):
    """
    Función que soluciona el requerimiento 2
    """
    tupla_origen=(punto_origen_lat,punto_origen_long)
    tupla_destino=(punto_destino_lat,punto_destino_long)
    aeropuerto_origen=None
    aeropuerto_destino=None
    menor=100000
    menor2=100000
    distancias=0
    for aeropuerto in lt.iterator(mp.keySet(data_structs["aeropuertos"])):
        nodo=me.getValue(mp.get(data_structs["aeropuertos"], aeropuerto))
        tupla_aeropuerto=(nodo["LATITUD"],nodo["LONGITUD"])
        if tupla_aeropuerto==tupla_origen:
            aeropuerto_origen=aeropuerto
            menor=0
        elif tupla_aeropuerto==tupla_destino:
            aeropuerto_destino=aeropuerto
            menor2=0
        else:
            distancia_aeropuerto1=haversine(tupla_aeropuerto,tupla_origen)
           
            if distancia_aeropuerto1<menor:
                menor=distancia_aeropuerto1
                aeropuerto_origen=aeropuerto
            distancia_aeropuerto2=haversine(tupla_aeropuerto,tupla_destino)
            
            if distancia_aeropuerto2<menor2:
                menor2=distancia_aeropuerto2
                aeropuerto_destino=aeropuerto
    
    if menor/1000>30:
        return "No se encontró un aeropuerto cercano al punto de origen", None, None, None 
      
    distancias=menor/1000 +menor2/1000 + djk.distTo(djk.Dijkstra(data_structs["Grafo_comercial_distancia"], aeropuerto_origen), aeropuerto_destino)
    camino=djk.pathTo(djk.Dijkstra(data_structs["Grafo_comercial_distancia"], aeropuerto_origen), aeropuerto_destino)
    numero_vuelos=st.size(camino)+1
    secuencia=lt.newList('ARRAY_LIST')
    icaos=lt.newList('ARRAY_LIST')
    for i in lt.iterator(camino):
        nodo_destino=me.getValue(mp.get(data_structs["aeropuertos"], str(i["vertexB"])))
        nodo_origen=me.getValue(mp.get(data_structs["aeropuertos"], str(i["vertexA"])))
        if lt.isPresent(icaos, nodo_destino["ICAO"]) == 0:
            lt.addLast(secuencia, nodo_destino)
            lt.addLast(icaos, nodo_destino["ICAO"])
        if lt.isPresent(icaos,nodo_origen["ICAO"]) == 0:
            lt.addLast(secuencia, nodo_origen)
            lt.addLast(icaos, nodo_origen["ICAO"])
            
    tiempo_del_trayecto=djk.distTo(djk.Dijkstra(data_structs["Grafo_Comercial_Tiempo"], aeropuerto_origen), aeropuerto_destino)
    
    global lista_coordenadas, req
    lt.addLast(lista_coordenadas, secuencia)
    req = 1
    
    return distancias, numero_vuelos, secuencia, tiempo_del_trayecto

def compare_dicts(dict1, dict2):
    return dict1 == dict2

def req_2(data_structs, punto_origen_lat, punto_origen_long, punto_destino_lat, punto_destino_long):
    """
    Función que soluciona el requerimiento 1
    """
    
    tupla_origen=(punto_origen_lat,punto_origen_long)
    tupla_destino=(punto_destino_lat,punto_destino_long)
    aeropuerto_origen=None
    aeropuerto_destino=None
    menor=100000
    menor2=100000
    distancias=0
    numero_vuelos=0
    for aeropuerto in lt.iterator(mp.keySet(data_structs["aeropuertos"])):
        nodo=me.getValue(mp.get(data_structs["aeropuertos"], aeropuerto))
        tupla_aeropuerto=(nodo["LATITUD"],nodo["LONGITUD"])
        if tupla_aeropuerto==tupla_origen:
            aeropuerto_origen=aeropuerto
            menor = 0
        elif tupla_aeropuerto==tupla_destino:
            aeropuerto_destino=aeropuerto
            menor2 = 0
        else:
            distancia_aeropuerto1=haversine(tupla_aeropuerto,tupla_origen)
            if distancia_aeropuerto1<menor:
                menor=distancia_aeropuerto1
                aeropuerto_origen=aeropuerto
            distancia_aeropuerto2=haversine(tupla_aeropuerto,tupla_destino)
            if distancia_aeropuerto2<menor2:
                menor2=distancia_aeropuerto2
                aeropuerto_destino=aeropuerto
    if menor/1000>30:
        return "No se encontró un aeropuerto cercano al punto de origen", None, None, None    
    distancias=menor/1000 + menor2/1000
    camino=bfs.pathTo(bfs.BreathFirstSearch(data_structs["Grafo_comercial_distancia"], aeropuerto_origen), aeropuerto_destino)
    secuencia=lt.newList('ARRAY_LIST')
    icaos=lt.newList('ARRAY_LIST')
    numero_vuelos=st.size(camino)
    tiempo_del_trayecto=0
    while not st.isEmpty(camino):
        Aeropuerto = me.getValue(mp.get(data_structs["aeropuertos"], st.pop(camino)))
        if not st.isEmpty(camino):
            Aeropuerto2 = me.getValue(mp.get(data_structs["aeropuertos"], st.pop(camino)))
            distancias += haversine((Aeropuerto["LATITUD"],Aeropuerto["LONGITUD"]),(Aeropuerto2["LATITUD"],Aeropuerto2["LONGITUD"]))
        if lt.isPresent(icaos, Aeropuerto["ICAO"]) == 0:
            lt.addLast(secuencia, Aeropuerto)
            lt.addLast(icaos, Aeropuerto["ICAO"])
        if lt.isPresent(icaos, Aeropuerto2["ICAO"]) == 0:
            lt.addLast(secuencia, Aeropuerto2)
            lt.addLast(icaos, Aeropuerto2["ICAO"])
            tiempo_del_trayecto+=me.getValue(mp.get(data_structs["rutas"], Aeropuerto["ICAO"]+Aeropuerto2["ICAO"]+"COMERCIAL"))["TIEMPO_VUELO"]
        
    global lista_coordenadas, req
    lt.addLast(lista_coordenadas, secuencia)
    req = 2

    return distancias, numero_vuelos, secuencia, tiempo_del_trayecto


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    distancia=0
    num_trayectos_posibles=0
    secuencia=lt.newList('ARRAY_LIST')
    aepto_concurrente=lt.firstElement(data_structs["Lista_aeropuertos_comercial"])
    camino = prim.PrimMST(data_structs["Grafo_comercial_distancia"], aepto_concurrente["ICAO"])
    llegada=gr.indegree(data_structs["Grafo_comercial_distancia"], aepto_concurrente["ICAO"])
    salida=gr.outdegree(data_structs["Grafo_comercial_distancia"], aepto_concurrente["ICAO"])
    for edge in lt.iterator(camino["edgeTo"]["table"]):
        edge_info = edge.get('value')
        if edge_info is not None:
            vertexA = edge_info.get('vertexA')
            vertexB = edge_info.get('vertexB')
            weight = edge_info.get('weight')
            nodo_destino=me.getValue(mp.get(data_structs["aeropuertos"], vertexB))
            nodo_origen=me.getValue(mp.get(data_structs["aeropuertos"], vertexA))
            pareja=diccionario_req3(nodo_origen, nodo_destino)
            pareja["Distancia"]=f"{weight} km"
            tiempo_vuelo = me.getValue(mp.get(data_structs["rutas"], vertexA+vertexB+"COMERCIAL"))["TIEMPO_VUELO"]
            pareja["Tiempo de vuelo"]=f"{round(tiempo_vuelo,2)} min"
            lt.addLast(secuencia, pareja)
            distancia+=weight
            num_trayectos_posibles+=1
            
    global lista_coordenadas, req
    lt.addLast(lista_coordenadas, secuencia)
    req = 3
    
    return aepto_concurrente, distancia, num_trayectos_posibles,salida, llegada, secuencia

def diccionario_req3(nodo1, nodo2):
    dict = {
        "Nodo_origen": nodo1,
        "Nodo_destino": nodo2,
        "Distancia": 0,
        "Tiempo de vuelo": 0
    }
    return dict

def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    
    lista_conc_militar = data_structs["Lista_aeropuertos_carga"]
    aepto_concurrente = lt.firstElement(lista_conc_militar)
    search = prim.PrimMST(data_structs["Grafo_Carga_distancia"],aepto_concurrente["ICAO"])#reisar el arbol de expansion soobre el vertice mayor
    lista_vertices = gr.vertices(data_structs["Grafo_Carga_distancia"])
    secuencia = lt.newList()
    num_trayectos_posibles = 0
    distancia = 0
    for vertice in lt.iterator(lista_vertices):
        entry = mp.get(search["edgeTo"],  vertice)#indexar el diccionario 
        if entry:
            arco = me.getValue(entry)#Arco tiempo
            arco_distancia = gr.getEdge(data_structs["Grafo_Militar_distancia"], arco["vertexA"], arco["vertexB"])
            info_vuelo = me.getValue(mp.get(data_structs["rutas"],arco["vertexA"]+arco["vertexB"]+"MILITAR"))
            diccionario = {"origen": arco["vertexA"], 
                           "destino": arco["vertexB"],
                           "distancia": arco_distancia["weight"],#arco de distancia
                           "tiempo": arco["weight"],
                           "tipo_aeronave": info_vuelo["TIPO_AERONAVE"]
                           }
            lt.addLast(secuencia, diccionario)
            num_trayectos_posibles += 1
            distancia += arco_distancia["weight"]
    llaves = ["ICAO", "NOMBRE", "CIUDAD", "PAIS", "CONCURRENCIA_Militar"]
    aepto_concurrente = filtrar_aeropuerto(aepto_concurrente, llaves)
    
    global lista_coordenadas, req
    lt.addLast(lista_coordenadas, secuencia)
    req = 4

    return aepto_concurrente, distancia, num_trayectos_posibles, secuencia

def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    lista_conc_militar = data_structs["Lista_aeropuertos_militar"]
    aeropuerto_importante = lt.firstElement(lista_conc_militar)
    search = prim.PrimMST(data_structs["Grafo_Militar_Tiempo"],aeropuerto_importante["ICAO"])#reisar el arbol de expansion soobre el vertice mayor
    lista_vertices = gr.vertices(data_structs["Grafo_Militar_Tiempo"])
    trayectos = lt.newList()
    num_trayectos_total = 0
    dist_total = 0
    for vertice in lt.iterator(lista_vertices):
        entry = mp.get(search["edgeTo"],  vertice)#indexar el diccionario 
        if entry:
            arco = me.getValue(entry)#Arco tiempo
            arco_distancia = gr.getEdge(data_structs["Grafo_Militar_distancia"], arco["vertexA"], arco["vertexB"])
            info_vuelo = me.getValue(mp.get(data_structs["rutas"],arco["vertexA"]+arco["vertexB"]+"MILITAR"))    
            diccionario = {"origen": arco["vertexA"], 
                           "destino": arco["vertexB"],
                           "distancia": arco_distancia["weight"],#arco de distancia
                           "tiempo": arco["weight"],
                           "tipo_aeronave": info_vuelo["TIPO_AERONAVE"]}
            lt.addLast(trayectos, diccionario)
            num_trayectos_total += 1
            dist_total += arco_distancia["weight"]
    llaves = ["ICAO", "NOMBRE", "CIUDAD", "PAIS", "CONCURRENCIA_Militar"]
    aeropuerto_importante = filtrar_aeropuerto(aeropuerto_importante, llaves)
    
    global lista_coordenadas, req
    lt.addLast(lista_coordenadas, trayectos)
    req = 5

    return aeropuerto_importante, dist_total, num_trayectos_total, trayectos

def req_6(data_structs, m):
    """
    Función que soluciona el requerimiento 6
    """
    secuencia=lt.newList('ARRAY_LIST')
    aepto_concurrente=lt.firstElement(data_structs["Lista_aeropuertos_comercial"])
    aeropuertos_m=lt.subList(data_structs["Lista_aeropuertos_comercial"], 2, m)
    data_structs["REQ6"]=aeropuertos_m
    llegada=gr.indegree(data_structs["Grafo_comercial_distancia"], aepto_concurrente["ICAO"])
    salida=gr.outdegree(data_structs["Grafo_comercial_distancia"], aepto_concurrente["ICAO"])
    for aepto in lt.iterator(aeropuertos_m):
        camino = djk.pathTo(djk.Dijkstra(data_structs["Grafo_comercial_distancia"], aepto_concurrente["ICAO"]), aepto["ICAO"])
        icaos=lt.newList('ARRAY_LIST')
        secuencia_menor=lt.newList('ARRAY_LIST')
        for i in lt.iterator(camino):
            nodo_destino=me.getValue(mp.get(data_structs["aeropuertos"], str(i["vertexB"])))
            nodo_origen=me.getValue(mp.get(data_structs["aeropuertos"], str(i["vertexA"])))
            pareja=dict_req6(aepto, nodo_origen, nodo_destino)
            pareja["distancia"]+=i["weight"]
            lt.addLast(secuencia, pareja)
            if lt.isPresent(icaos, nodo_destino["ICAO"]) == 0:
                lt.addLast(secuencia_menor, nodo_origen)
                lt.addLast(icaos, nodo_destino["ICAO"])
            if lt.isPresent(icaos,nodo_origen["ICAO"]) == 0:
                lt.addLast(secuencia_menor, nodo_destino)
                lt.addLast(icaos, nodo_origen["ICAO"])
            pareja["total aeropuertos"]+=1
        
    global lista_coordenadas, req
    lt.addLast(lista_coordenadas, secuencia)
    req = 6
        
    return aepto_concurrente, salida, llegada, secuencia

def dict_req6(aepto, nodo1, nodo2):
    dict = {"Aeropuerto de prioridad": aepto["NOMBRE"], "total aeropuertos":0, "Aepto ida":nodo1, "Aepto llegada":nodo2, "Vuelo Ida": nodo1["ICAO"], "Vuelo Llegada": nodo2["ICAO"], "distancia":0}
    return dict


def req_7(data_structs, lat1, lat2, long1, long2):
    """
    Función que soluciona el requerimiento 7
    """
    grafo = data_structs["Grafo_Comercial_Tiempo"]
    vertices = gr.vertices(grafo)
    punto_1 = (lat1, long1)
    punto_2 = (lat2, long2)
    aeropuerto_origen = None
    aeropuerto_destino = None
    distancia_menor_origen = float("inf")
    distancia_menor_destino = float("inf")
    for vertice in lt.iterator(vertices):
        aeropuerto = me.getValue(mp.get(data_structs["aeropuertos"], vertice))
        punto_0=(aeropuerto["LATITUD"], aeropuerto["LONGITUD"])
        distancia_1 = haversine(punto_0, punto_1)
        distancia_2 = haversine(punto_0, punto_2)
        if distancia_1 < distancia_menor_origen and distancia_1 < 30:
            distancia_menor_origen = distancia_1
            aeropuerto_origen = aeropuerto
        if distancia_2 < distancia_menor_destino and distancia_2 < 30:
            distancia_menor_destino = distancia_2
            aeropuerto_destino = aeropuerto
    if aeropuerto_origen == None or aeropuerto_destino == None:
        return None
    search = djk.Dijkstra(grafo, aeropuerto_origen["ICAO"])#Camino minimo entre origen y todos los aeropuertos del grafo
    if not djk.hasPathTo(search, aeropuerto_destino["ICAO"]):
        return None
    #sacar el camno si hay aeropuertos que cumplen
    camino = djk.pathTo(search, aeropuerto_destino["ICAO"])
    tiempo_total = 0
    dist_total = 0
    num_aeropuertos = 1
    secuencia = lt.newList()
    llaves = ["ICAO", "NOMBRE", "CIUDAD", "PAIS"]
    for arco in lt.iterator(camino):
        arco_distancia = gr.getEdge(data_structs["Grafo_comercial_distancia"], arco["vertexA"], arco["vertexB"])
        num_aeropuertos += 1
        tiempo_total += arco["weight"]
        dist_total += arco_distancia["weight"]
        diccionario = {"origen": tabulate([filtrar_aeropuerto(me.getValue(mp.get(data_structs["aeropuertos"], arco["vertexA"])), llaves)], headers="keys", tablefmt="fancy_grid"), 
                           "destino": tabulate([filtrar_aeropuerto(me.getValue(mp.get(data_structs["aeropuertos"], arco["vertexB"])), llaves)], headers="keys", tablefmt="fancy_grid"), 
                           "distancia": arco_distancia["weight"],#arco de distancia
                           "tiempo": arco["weight"],
                           }
        lt.addLast(secuencia, diccionario)
        
        global lista_coordenadas, req
        lt.addLast(lista_coordenadas, secuencia)
        req = 7
        
        return tiempo_total, dist_total, num_aeropuertos, secuencia


def filtrar_aeropuerto(aeropuerto_importante, llaves):
    
    aeropuerto = {}
    for llave in llaves:
        aeropuerto[llave] = aeropuerto_importante[llave]
    return aeropuerto

def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    
    global lista_coordenadas
    lista = lista_coordenadas
    points = []
    mapa = folium.Map(zoom_start=6)
    for list in lt.iterator(lista):
        for vuelo in lt.iterator(list):
            if req == 1 or req == 2:
                folium.Marker([vuelo["LATITUD"], vuelo["LONGITUD"]], popup=vuelo["NOMBRE"]).add_to(mapa)
                point = [vuelo["LATITUD"], vuelo["LONGITUD"]]
                points.append(point)
                folium.Marker(point, popup=vuelo["NOMBRE"]).add_to(mapa)
                folium.PolyLine(points, color="red").add_to(mapa)
            if req == 5:
                for vuelos in lt.iterator(data_structs["Lista_aeropuertos_militar"]):
                    if vuelo["origen"] == vuelos["ICAO"]:
                        folium.Marker([vuelos["LATITUD"], vuelos["LONGITUD"]], popup=vuelos["NOMBRE"]).add_to(mapa)
                        point = [vuelos["LATITUD"], vuelos["LONGITUD"]]
                        points.append(point)
                        folium.Marker(point, popup=vuelos["NOMBRE"]).add_to(mapa)
                        folium.PolyLine(points, color="red").add_to(mapa)
            elif req == 6:
                folium.Marker([vuelo["Aepto ida"]["LATITUD"], vuelo["Aepto ida"]["LONGITUD"]], popup=vuelo["Aepto ida"]["NOMBRE"]).add_to(mapa)
                folium.Marker([vuelo["Aepto llegada"]["LATITUD"], vuelo["Aepto llegada"]["LONGITUD"]], popup=vuelo["Aepto llegada"]["NOMBRE"]).add_to(mapa)
            else:
                folium.Marker([vuelo["Nodo_origen"]["LATITUD"], vuelo["Nodo_origen"]["LONGITUD"]], popup=vuelo["Nodo_origen"]["NOMBRE"]).add_to(mapa)
                point = [vuelo["Nodo_origen"]["LATITUD"], vuelo["Nodo_origen"]["LONGITUD"]]
                points.append(point)
                folium.Marker(point, popup=vuelo["Nodo_origen"]["NOMBRE"]).add_to(mapa)
                folium.PolyLine(points, color="red").add_to(mapa)

    mapa.save("mapa.html")
    webbrowser.open("mapa.html")
    lista_coordenadas = lt.newList(datastructure="ARRAY_LIST")

    return mapa


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

# Funciones de ordenamiento

def cmp_mayor_menor(key1, key2):
    if key1 == key2:
        return 0
    elif key1 > key2:
        return -1
    else:
        return 1



def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass
