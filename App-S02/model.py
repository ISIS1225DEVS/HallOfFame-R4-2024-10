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

import math
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
from DISClib.Algorithms.Graphs import dijsktra_tuple as djkt
from DISClib.Algorithms.Graphs import bellmanford as bf
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Graphs import prim_tuple
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
assert cf
import folium
from folium.plugins import MarkerCluster
from folium.plugins import AntPath
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
        "flights": None, #va a ser una HashTable, donde las llaves van a ser un string donde está el ICAO-ICAO, siendo el primer ICAO el origen y el segundo ICAO el destino.
        #como valor va a tener un array_list con toda la información de los vuelos que tienen dicho trayecto.
        "airports_by_distance": None, #va a ser el grafo más general, donde los vértices serán los aeropuertos, y los arcos los trayectos que hay entre los aeropuertos. 
        #Su peso va a ser la distancia en kilómetros
        "airpots_by_time": None, #va a ser el grafo más general, donde los vértices serán los aeropuertos, y los arcos los trayectos que hay entre los aeropuertos. 
        #Su peso va a ser el tiempo del trayecto
        
        #los que están abajo es lo mismo que los de arriba, solo que únicamente van a estar los vuelos de cada tipo en particular. Note que en todos van a estar los mismos vértices.
        #es decir, que el tamaño de los grafos va a ser el mismo, lo único que va a cambiar son los arcos.
        "comercial_by_distance": None,
        "comercial_by_time": None,
        "militar_by_distance": None,
        "militar_by_time": None,
        "charge_by_distance": None,
        "charge_by_time": None,
        
        "airports": None, #este es el array con la info de todos los aeropuertos
        "airports_id": None,
        
        "airports_mayor_ocurrencia": None
        
    }
    
    data_structs["flights"] = mp.newMap(numelements= 4000, maptype="PROBING", loadfactor=0.6)
    data_structs["airports_by_distance"] = gr.newGraph(datastructure="ADJ_LIST", directed=True, size=2000)
    data_structs["airports_by_time"] = gr.newGraph(datastructure="ADJ_LIST", directed=True, size=2000)
    data_structs["comercial_by_distance"] = gr.newGraph(datastructure="ADJ_LIST", directed=True, size=2000)
    data_structs["comercial_by_time"] = gr.newGraph(datastructure="ADJ_LIST", directed=True, size=2000)
    data_structs["militar_by_distance"] = gr.newGraph(datastructure="ADJ_LIST", directed=True, size=2000)
    data_structs["militar_by_time"] = gr.newGraph(datastructure="ADJ_LIST", directed=True, size=2000)
    data_structs["charge_by_distance"] = gr.newGraph(datastructure="ADJ_LIST", directed=True, size=2000)
    data_structs["charge_by_time"] = gr.newGraph(datastructure="ADJ_LIST", directed=True, size=2000)
    data_structs["airports"] = lt.newList(datastructure="ARRAY_LIST")
    data_structs["airports_id"] = mp.newMap(numelements= 4000, maptype="PROBING", loadfactor=0.6)
    data_structs["airports_mayor_ocurrencia"] = mp.newMap(numelements= 2000, maptype="PROBING", loadfactor=0.6)
    
    return data_structs
    

# Funciones para agregar informacion al modelo

def add_airport(data_structs, data):
    airport_id = data["ICAO"]
    gr.insertVertex(data_structs["airports_by_distance"], airport_id)
    gr.insertVertex(data_structs["airports_by_time"], airport_id)
    gr.insertVertex(data_structs["comercial_by_distance"], airport_id)
    gr.insertVertex(data_structs["comercial_by_time"], airport_id)
    gr.insertVertex(data_structs["militar_by_distance"], airport_id)
    gr.insertVertex(data_structs["militar_by_time"], airport_id)
    gr.insertVertex(data_structs["charge_by_distance"], airport_id)
    gr.insertVertex(data_structs["charge_by_time"], airport_id)
    lt.addLast(data_structs["airports"], data)
    mp.put(data_structs["airports_id"], airport_id, data)
    
   
    

def add_flight(data_structs, data):
    origen = data["ORIGEN"]
    destino = data["DESTINO"]
    distancia = calculo_distancia_haversine(data_structs, origen, destino)
    
    key = origen + "-" + destino
    entry = mp.get(data_structs["flights"], key)
    if entry is None:
        lista = lt.newList(datastructure="ARRAY_LIST")
        lt.addLast(lista, data)
        mp.put(data_structs["flights"], key, lista)
    else:
        lista_anterior = me.getValue(entry)
        lt.addLast(lista_anterior, data)
        mp.put(data_structs["flights"], key, lista_anterior)
        
    #este también va a agregar los arcos:
    
    gr.addEdge(data_structs["airports_by_distance"], origen, destino, float(distancia))
    gr.addEdge(data_structs["airports_by_time"], origen, destino, float(data["TIEMPO_VUELO"]))
    
    #en caso de hacerlo con tuplas:
    #gr.addEdge(data_structs["airports_by_distance"], origen, destino, (distancia, data["TIEMPO_VUELO"]))
    
    if data["TIPO_VUELO"] == "AVIACION_CARGA":
        gr.addEdge(data_structs["charge_by_distance"], origen, destino, float(distancia))
        gr.addEdge(data_structs["charge_by_time"], origen, destino, float(data["TIEMPO_VUELO"]))
        
        #gr.addEdge(data_structs["charge_by_distance"], origen, destino, (distancia, data["TIEMPO_VUELO"]))
        
    elif data["TIPO_VUELO"] == "MILITAR":
        gr.addEdge(data_structs["militar_by_distance"], origen, destino, float(distancia))
        gr.addEdge(data_structs["militar_by_time"], origen, destino, float(data["TIEMPO_VUELO"]))
        
        #gr.addEdge(data_structs["militar_by_distance"], origen, destino, (distancia, data["TIEMPO_VUELO"]))
        
    elif data["TIPO_VUELO"] == "AVIACION_COMERCIAL":
        gr.addEdge(data_structs["comercial_by_distance"], origen, destino, float(distancia))
        gr.addEdge(data_structs["comercial_by_time"], origen, destino, int(data["TIEMPO_VUELO"]))
        
        #gr.addEdge(data_structs["comercial_by_distance"], origen, destino, (distancia, data["TIEMPO_VUELO"]))
        
def encontrar_minimo(lat, lon, aeropuertos, distancia_min: bool):
    """
    ATENCION: ponen True en distancia_min si necesitan que el aeropuerto se encuentr
    a menos ed 30km. Ponen False si quieren directamente el aeropuerto más cercano
    sin importar si se encuentra a menos de 30km (podría estar a 40 km o a una distancia mayor a 30)
    Gente, hice esta función para que pongan unas coordenadas, y les 
    digan el aeropuerto que se encuentra a menos de 30km desde dicha
    coordenada, y que sea el de menor distancia.
    
    Retorna None si no hay un aeropuerto que esté a menos de 30km.
    Retorna el ICAO,distancia del aeropuerto en caso en que haya un aeropuerto. (una tupla)
    """
    lista_ordenada = lt.newList(datastructure="ARRAY_LIST")
    for x in lt.iterator(aeropuertos):
        
        latitud_aeropuerto = float(x["LATITUD"].replace(",", "."))
        longitud_aeropuerto = float(x["LONGITUD"].replace(",", "."))
        distancia = calculo_distancia_haversine_posiciones(lat, latitud_aeropuerto, lon, longitud_aeropuerto)
        if distancia_min == True:
            if distancia <= 30:
                lt.addLast(lista_ordenada, {"ICAO": x["ICAO"], "distancia": distancia})
        else:
            lt.addLast(lista_ordenada, {"ICAO": x["ICAO"], "distancia": distancia})
    
    if lt.size(lista_ordenada) == 0:
        return None
    else:
        sa.sort(lista_ordenada, cmp_aeropuerto_minimo)
        nombre_aeropuerto = lt.lastElement(lista_ordenada)["ICAO"]
        distancia_aeropuerto = lt.lastElement(lista_ordenada)["distancia"]
        return nombre_aeropuerto, distancia_aeropuerto
    
def cmp_aeropuerto_minimo(data1, data2):
    distancia1 = float(data1["distancia"])
    distancia2 = float(data2["distancia"])
    
    if distancia1 < distancia2:
        return False
    else:
        return True
    

    
def calculo_distancia_haversine(data_structs, origen, destino):
    """ 
    Esta función es para calcular la distancia entre un aeropuerto de 
    origen, y una de destino.
    """
    aeropuertos_id = data_structs["airports_id"]
    info_1 = me.getValue(mp.get(aeropuertos_id, origen))
    info_2 = me.getValue(mp.get(aeropuertos_id, destino))
    
    lat_1 = math.radians(float(info_1["LATITUD"].replace(",", ".")))
    lat_2 = math.radians(float(info_2["LATITUD"].replace(",", ".")))
    lon_1 = math.radians(float(info_1["LONGITUD"].replace(",", ".")))
    lon_2 = math.radians(float(info_2["LONGITUD"].replace(",", ".")))
    
    primer_termino = math.sin((lat_2 - lat_1) / 2)**2 + math.cos(lat_1) * math.cos(lat_2) * math.sin((lon_2 - lon_1) / 2)**2
    segundo_termino = 2 * math.atan2(math.sqrt(primer_termino), math.sqrt(1 - primer_termino))
    
    return 6371.0 * segundo_termino

def calculo_distancia_haversine_posiciones(lat_1, lat_2, lon_1, lon_2):
    lat_1 = str(lat_1)
    lat_2 = str(lat_2)
    lon_1 = str(lon_1)
    lon_2 = str(lon_2)
    lat_1 = math.radians(float(lat_1.replace(",", ".")))
    lat_2 = math.radians(float(lat_2.replace(",", ".")))
    lon_1 = math.radians(float(lon_1.replace(",", ".")))
    lon_2 = math.radians(float(lon_2.replace(",", ".")))
    primer_termino = math.sin((lat_2 - lat_1) / 2)**2 + math.cos(lat_1) * math.cos(lat_2) * math.sin((lon_2 - lon_1) / 2)**2
    segundo_termino = 2 * math.atan2(math.sqrt(primer_termino), math.sqrt(1 - primer_termino))
    
    return 6371.0 * segundo_termino

#l = calculo_distancia_haversine_posiciones("12133218",6312,"7813",137892)
#print(l)
def graf_size(data_structs):
    grafo = data_structs["airports_by_distance"]
    cantidad_aeropuertos = gr.numVertices(grafo)
    cantidad_vuelos = gr.numEdges(grafo)
    return cantidad_aeropuertos, cantidad_vuelos

def mostrar_info(control):
    aeropuertos = control["model"]["airports"]
    militares = control["model"]["militar_by_distance"]
    carga = control["model"]["charge_by_distance"]
    comercial = control["model"]["comercial_by_distance"]
    
    cantidad_militares = lt.newList("ARRAY_LIST")
    cantidad_carga = lt.newList("ARRAY_LIST")
    cantidad_comercial = lt.newList("ARRAY_LIST")
    
    for aero in lt.iterator(aeropuertos):
        id_a = aero["ICAO"]
        can_militares = float(gr.indegree(militares, id_a) + gr.outdegree(militares, id_a))
        can_carga = float(gr.indegree(carga, id_a) + gr.outdegree(carga, id_a))
        can_comercial = float(gr.indegree(comercial, id_a) + gr.outdegree(comercial, id_a))
        
        if can_militares != 0:
            lt.addLast(cantidad_militares, {"nombre": id_a, "cantidad": can_militares})
        if can_carga != 0:
            lt.addLast(cantidad_carga, {"nombre": id_a, "cantidad": can_carga})
        if can_comercial != 0:
            lt.addLast(cantidad_comercial, {"nombre": id_a, "cantidad": can_comercial})
        
    sa.sort(cantidad_militares, cmp_mayor_concurrencia)
    sa.sort(cantidad_comercial, cmp_mayor_concurrencia)
    sa.sort(cantidad_carga, cmp_mayor_concurrencia)
    
    añadir = control["model"]["airports_mayor_ocurrencia"]
    mp.put(añadir, "comercial", cantidad_comercial)
    mp.put(añadir, "carga", cantidad_carga)
    mp.put(añadir, "militar", cantidad_militares)
    
      
    return cantidad_militares, cantidad_comercial, cantidad_carga

def cmp_mayor_concurrencia(data1, data2):
    cantidad1 = float(data1["cantidad"])
    cantidad2 = float(data2["cantidad"])
    nombre1 = data1["nombre"]
    nombre2 = data2["nombre"]
    if cantidad1 < cantidad2:
        return False
    elif cantidad1 == cantidad2:
        if nombre1 < nombre2:
            return True
        else:
            return False
    else:
        return True
    
       

# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass


# Funciones de consulta

def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


def req_1(data_structs, latitud_origen, longitud_origen, latitud_destino, longitud_destino):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    aeropuertos_comerciales_distance = data_structs["comercial_by_distance"]
    #print(aeropuertos_comerciales_distance)
    aeropuertos_comerciales_time = data_structs["comercial_by_time"]
    aeropuertos = data_structs["airports"]

    #print(aeropuertoss)
    
    cantidad_aeropuerto_visitados = 0
    lista_aeropuertos = lt.newList("ARRAY_LIST")
    tiempo_trayecto = 0
    tiempo_entre_trayectos = lt.newList("ARRAY_LIST")
    distancia_trayecto = 0
    
    if(encontrar_minimo(latitud_origen, longitud_origen, aeropuertos, True) == None or encontrar_minimo(latitud_destino, longitud_destino, aeropuertos, True) == None):
        ae_origen = None
        ae_destino = None
    else:
        ae_origen = encontrar_minimo(latitud_origen, longitud_origen, aeropuertos, True)[0]
        ae_destino = encontrar_minimo(latitud_destino, longitud_destino, aeropuertos, True)[0]
    #print(ae_destino)
    #print(ae_origen)
    if ae_origen == None or ae_destino == None:
        ae_mas_cercano = encontrar_minimo(latitud_origen, longitud_origen, aeropuertos, False)[0]
        distancia_mas_cercano = encontrar_minimo(latitud_origen, longitud_origen, aeropuertos, False)[1]
        return  ae_mas_cercano, distancia_mas_cercano, None, None, None, None, False, None
    else:
        search = bfs.BreathFirstSearch(aeropuertos_comerciales_distance, ae_origen)
        camino = bfs.pathTo(search, ae_destino)
        if camino != None:
            cantidad_aeropuerto_visitados = camino["size"]
            #print(camino) #que putassssss
            for x in lt.iterator(camino):
                lt.addFirst(lista_aeropuertos, x)
            #print(gr.getEdge(aeropuertos_comerciales_distance, "SKBO", "SKOT"))
            #print(lista_aeropuertos)   
            for i in range(1, lt.size(lista_aeropuertos)):
                vertice_a = lt.getElement(lista_aeropuertos, i)
                vertice_b =  lt.getElement(lista_aeropuertos, i + 1)
                #print(vertice_a)
                #print(vertice_b)
                arco_distancia = gr.getEdge(aeropuertos_comerciales_distance, vertice_a, vertice_b)
                distancia = float(arco_distancia["weight"])
                distancia_trayecto += distancia
                arco_tiempo = gr.getEdge(aeropuertos_comerciales_time, vertice_a, vertice_b)
                tiempo = float(arco_tiempo["weight"])
                tiempo_trayecto += tiempo
                lt.addLast(tiempo_entre_trayectos, {vertice_a + "-" + vertice_b : tiempo})
        else:
            ae_mas_cercano = encontrar_minimo(latitud_origen, longitud_origen, aeropuertos, False)[0]
            distancia_mas_cercano = encontrar_minimo(latitud_origen, longitud_origen, aeropuertos, False)[1]
            return ae_mas_cercano, distancia_mas_cercano, None, None, None, None, None, None
        #print(tiempo_trayecto)
        #print(distancia_trayecto)
        
        #notese que lista_aeropuertos tiene todos los vértices (incluyendo el orien y destino, entonces tengo que quitarle el primero y el último)
        bono_req1(lista_aeropuertos, data_structs)
        return ae_origen, ae_destino, lista_aeropuertos, cantidad_aeropuerto_visitados, tiempo_entre_trayectos, distancia_trayecto, True, tiempo_trayecto

def bono_req1(lst, data_structs):            
    lista_con_id = lst

    airports_id = data_structs["airports_id"]
    
    
    mapa = folium.Map(location=[19.9449799, 50.0646501], zoom_start=4)

    for x in lt.iterator(lista_con_id):
        value = me.getValue(mp.get(airports_id, x))
        longitude = float(value["LONGITUD"].replace(",", "."))
        latitude = float(value["LATITUD"].replace(",", "."))
        
        folium.Marker([latitude, longitude], popup=value).add_to(mapa)

    for i in range(1, lt.size(lst)):
        
        vertice_a = lt.getElement(lst, i)
        value_a = me.getValue(mp.get(airports_id, vertice_a))
        coordenada1 = [float(value_a["LATITUD"].replace(",", ".")), float(value_a["LONGITUD"].replace(",", "."))]
        vertice_b =  lt.getElement(lst, i + 1)
        value_b = me.getValue(mp.get(airports_id, vertice_b))
        coordenada2 = [float(value_b["LATITUD"].replace(",", ".")), float(value_b["LONGITUD"].replace(",", "."))]
        
        AntPath(
                locations=[coordenada1, coordenada2],
                color='blue',
                weight=2.5,
                opacity=1
                ).add_to(mapa)
    
        #mapa.add_child(mc)
        
    mapa.save("mapa.html")
            

def req_2(data_structs, latitud_origen, longitud_origen, latitud_destino, longitud_destino):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    gr_aeropuertos_comerciales_distance = data_structs["comercial_by_distance"]
    gr_aeropuertos_comerciales_time = data_structs["comercial_by_time"]
    lst_aeropuertos = data_structs["airports"]
    
    cantidad_aeropuerto_visitados = 0
    lista_aeropuertos = lt.newList("ARRAY_LIST")
    tiempo_entre_trayectos = lt.newList("ARRAY_LIST")
    distancia_trayecto = 0
    tiempo_trayecto_total = 0
    
    if(encontrar_minimo(latitud_origen, longitud_origen, lst_aeropuertos, True) == None or encontrar_minimo(latitud_destino, longitud_destino, lst_aeropuertos, True) == None):
        ae_origen = None
        ae_destino = None
    else:
        ae_origen = encontrar_minimo(latitud_origen, longitud_origen, lst_aeropuertos, True)[0]
        ae_destino = encontrar_minimo(latitud_destino, longitud_destino, lst_aeropuertos, True)[0]
        
    if ae_origen == None or ae_destino == None:
        ae_mas_cercano = encontrar_minimo(latitud_origen, longitud_origen, lst_aeropuertos, False)[0]
        distancia_mas_cercano = encontrar_minimo(latitud_origen, longitud_origen, lst_aeropuertos, False)[1]
        return  ae_mas_cercano, distancia_mas_cercano, None, None, None, None, False, None
    else:
        search = bfs.BreathFirstSearch(gr_aeropuertos_comerciales_distance, ae_origen)
        camino = bfs.pathTo(search, ae_destino)
        if camino != None:
            cantidad_aeropuerto_visitados = camino["size"]
            for x in lt.iterator(camino):
                lt.addFirst(lista_aeropuertos, x)
            for i in range(1, lt.size(lista_aeropuertos)):
                vertice_a = lt.getElement(lista_aeropuertos, i)
                vertice_b =  lt.getElement(lista_aeropuertos, i + 1)
                #print(vertice_a)
                #print(vertice_b)
                arco_distancia = gr.getEdge(gr_aeropuertos_comerciales_distance, vertice_a, vertice_b)
                distancia = float(arco_distancia["weight"])
                distancia_trayecto += distancia
                arco_tiempo = gr.getEdge(gr_aeropuertos_comerciales_time, vertice_a, vertice_b)
                tiempo = float(arco_tiempo["weight"])
                lt.addLast(tiempo_entre_trayectos, {vertice_a + "-" + vertice_b : tiempo})
                tiempo_trayecto_total += tiempo
        else:
            ae_mas_cercano = encontrar_minimo(latitud_origen, longitud_origen, lst_aeropuertos, False)[0]
            distancia_mas_cercano = encontrar_minimo(latitud_origen, longitud_origen, lst_aeropuertos, False)[1]
            return ae_mas_cercano, distancia_mas_cercano, None, None, None, None, None, None
        bono_req2(lista_aeropuertos, data_structs)
        return ae_origen, ae_destino, lista_aeropuertos, cantidad_aeropuerto_visitados, tiempo_entre_trayectos, distancia_trayecto, True, tiempo_trayecto_total

def bono_req2(lst, data_structs):            
    lista_con_id = lst

    airports_id = data_structs["airports_id"]
    
    
    mapa = folium.Map(location=[19.9449799, 50.0646501], zoom_start=4)

    for x in lt.iterator(lista_con_id):
        value = me.getValue(mp.get(airports_id, x))
        longitude = float(value["LONGITUD"].replace(",", "."))
        latitude = float(value["LATITUD"].replace(",", "."))
        
        folium.Marker([latitude, longitude], popup=value).add_to(mapa)

    for i in range(1, lt.size(lst)):
        
        vertice_a = lt.getElement(lst, i)
        value_a = me.getValue(mp.get(airports_id, vertice_a))
        coordenada1 = [float(value_a["LATITUD"].replace(",", ".")), float(value_a["LONGITUD"].replace(",", "."))]
        vertice_b =  lt.getElement(lst, i + 1)
        value_b = me.getValue(mp.get(airports_id, vertice_b))
        coordenada2 = [float(value_b["LATITUD"].replace(",", ".")), float(value_b["LONGITUD"].replace(",", "."))]
        
        AntPath(
                locations=[coordenada1, coordenada2],
                color='blue',
                weight=2.5,
                opacity=1
                ).add_to(mapa)
    
        #mapa.add_child(mc)
        
    mapa.save("mapa.html")
        

def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    ocurrencia = data_structs["airports_mayor_ocurrencia"]
    grafo_comercial_distancia = data_structs["comercial_by_distance"]
    grafo_comercial_tiempos = data_structs["comercial_by_time"]
    
    flights = data_structs["flights"]
    
    lst_comercial = me.getValue(mp.get(ocurrencia, "comercial"))
    primer_elemento = lt.firstElement(lst_comercial)["nombre"]
    cantidad_ocurrencias = lt.firstElement(lst_comercial)["cantidad"]
    
    search = prim.PrimMST(graph=grafo_comercial_distancia, origin=primer_elemento)
    table_edge_to = search["edgeTo"] #es una hashTable
    lista_aeropuertos_a_los_que_hay_camino = mp.keySet(table_edge_to) 
    lst = lt.newList("ARRAY_LIST")

    for x in lt.iterator(lista_aeropuertos_a_los_que_hay_camino):
        lt.addLast(lst, x)
        
    nuevo_grafo_a_partir_del_mst = gr.newGraph(datastructure="ADJ_LIST", directed=True, size=1000)
    for y in lt.iterator(lst):
        value = me.getValue(mp.get(table_edge_to, y))
        key_a = value["vertexA"]
        key_b = value["vertexB"]
        weight_asc = value["weight"]
        if gr.containsVertex(nuevo_grafo_a_partir_del_mst, key_a) == False:
            gr.insertVertex(nuevo_grafo_a_partir_del_mst, key_a)
        if gr.containsVertex(nuevo_grafo_a_partir_del_mst, key_b) == False:
            gr.insertVertex(nuevo_grafo_a_partir_del_mst, key_b)
        
        if gr.getEdge(grafo_comercial_tiempos, key_a, key_b):
            gr.addEdge(nuevo_grafo_a_partir_del_mst, key_a, key_b, weight_asc)
    
    #Recorrido desde el aereopuerto_de_mayor concurrencia hasta todas sus posibles conexiones
    
    search_2 = bfs.BreathFirstSearch(nuevo_grafo_a_partir_del_mst, primer_elemento)
    respuesta = lt.newList("ARRAY_LIST")
    for destiny in lt.iterator(lst):
        if destiny != primer_elemento:
            distancia = 0
            distancia_trayecto = 0
            tiempo = 0
            tiempo_trayecto = 0
            camino = bfs.pathTo(search_2, destiny)
            lst_aero = lt.newList("ARRAY_LIST")
            aeronaves_str = ""
            check_aeronaves = mp.newMap(maptype="PROBING")
            for y in lt.iterator(camino):
                lt.addFirst(lst_aero, y)
            for i in range(1, lt.size(lst_aero)):
                vertice_a = lt.getElement(lst_aero, i)
                vertice_b =  lt.getElement(lst_aero, i + 1)
                arco_distancia = gr.getEdge(nuevo_grafo_a_partir_del_mst, vertice_a, vertice_b)
                distancia = float(arco_distancia["weight"])
                
                distancia_trayecto += distancia
                arco_tiempo = gr.getEdge(grafo_comercial_tiempos, vertice_a, vertice_b)
                tiempo = float(arco_tiempo["weight"])
                tiempo_trayecto += tiempo
                
                key_flight = str(vertice_a) + "-" + str(vertice_b)
                aeronave = me.getValue(mp.get(flights, key_flight))["elements"][0]["TIPO_AERONAVE"]
                
                if mp.contains(check_aeronaves, aeronave) == False:
                    aeronaves_str = aeronaves_str + " - " + aeronave
                    mp.put(check_aeronaves, aeronave, aeronave)
                
            lt.addLast(respuesta, 
                    {"aeropuerto origen": primer_elemento, 
                        "aeropuerto destino": destiny, 
                        "distancia recorrida": distancia_trayecto,
                        "tiempo trayecto": tiempo_trayecto,
                        "aeronaves": aeronaves_str})
    bono_req3(respuesta, data_structs)
    cantidad_tr = lt.size(respuesta)
    return primer_elemento, cantidad_ocurrencias, cantidad_tr, respuesta  

def bono_req3(lst, data_structs):            
    lista_con_id = lst

    airports_id = data_structs["airports_id"]
    
    
    mapa = folium.Map(location=[19.9449799, 50.0646501], zoom_start=4)

    for x in lt.iterator(lista_con_id):
        aeropuerto_i = x["aeropuerto destino"]
        
        value = me.getValue(mp.get(airports_id, aeropuerto_i))
        longitude = float(value["LONGITUD"].replace(",", "."))
        latitude = float(value["LATITUD"].replace(",", "."))
        
        folium.Marker([latitude, longitude], popup=value).add_to(mapa)
    value_origin = me.getValue(mp.get(airports_id, "SKBO"))
    longitude_origin = float(value_origin["LONGITUD"].replace(",", "."))
    latitude_origin = float(value_origin["LATITUD"].replace(",", "."))
        
    folium.Marker([latitude_origin, longitude_origin], popup=value).add_to(mapa)
    
    
    for i in lt.iterator(lst):
        
        vertice_a = i["aeropuerto origen"]
        value_a = me.getValue(mp.get(airports_id, vertice_a))
        coordenada1 = [float(value_a["LATITUD"].replace(",", ".")), float(value_a["LONGITUD"].replace(",", "."))]
        vertice_b =  i["aeropuerto destino"]
        value_b = me.getValue(mp.get(airports_id, vertice_b))
        coordenada2 = [float(value_b["LATITUD"].replace(",", ".")), float(value_b["LONGITUD"].replace(",", "."))]
        
        AntPath(
                locations=[coordenada1, coordenada2],
                color='blue',
                weight=2.5,
                opacity=1
                ).add_to(mapa)
    
        #mapa.add_child(mc)
        
    mapa.save("mapa.html")   


def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    distancia_total_trayectos = 0
    ocurrencia = data_structs["airports_mayor_ocurrencia"]
    
    grafo_carga_distancia = data_structs["charge_by_distance"]
    grafo_carga_tiempos = data_structs["charge_by_time"]
    
    flights = data_structs["flights"]
    
    lst_carga = me.getValue(mp.get(ocurrencia, "carga"))
    primer_elemento = lt.firstElement(lst_carga)["nombre"]
    cantidad_ocurrencias = lt.firstElement(lst_carga)["cantidad"]
    #print(primer_elemento)
    
    search = prim.PrimMST(graph=grafo_carga_distancia, origin=primer_elemento)
    distancia_total_trayectos = prim.weightMST(grafo_carga_distancia, search)
    #minimun = prim.prim(grafo_carga_distancia, search, primer_elemento)
    #print(minimun)
    
    
    
    table_edge_to = search["edgeTo"] #es una hashTable
    #print(table_edge_to)
    lista_aeropuertos_a_los_que_hay_camino = mp.keySet(table_edge_to) 
    #print(lista_aeropuertos_a_los_que_hay_camino)
    lst = lt.newList("ARRAY_LIST")

    for x in lt.iterator(lista_aeropuertos_a_los_que_hay_camino):
        lt.addLast(lst, x)
        
    #print(lst)
    
    nuevo_grafo_a_partir_del_mst = gr.newGraph(datastructure="ADJ_LIST", directed=True, size=1000)
    for y in lt.iterator(lst):
        value = me.getValue(mp.get(table_edge_to, y))
        key_a = value["vertexA"]
        key_b = value["vertexB"]
        weight_asc = value["weight"]
        if gr.containsVertex(nuevo_grafo_a_partir_del_mst, key_a) == False:
            gr.insertVertex(nuevo_grafo_a_partir_del_mst, key_a)
        if gr.containsVertex(nuevo_grafo_a_partir_del_mst, key_b) == False:
            gr.insertVertex(nuevo_grafo_a_partir_del_mst, key_b)
        
        if gr.getEdge(grafo_carga_tiempos, key_a, key_b):
            gr.addEdge(nuevo_grafo_a_partir_del_mst, key_a, key_b, weight_asc)
        # if gr.getEdge(grafo_carga_tiempos, key_b, key_a):
        #     gr.addEdge(nuevo_grafo_a_partir_del_mst, key_b, key_a, weight_asc)

    #print(nuevo_grafo_a_partir_del_mst)
    
    #ahora voy a hacer el recorrido desde el aeropuerto_de_mayor concurrencia hasta todas sus posibles conexiones
    
    search_2 = bfs.BreathFirstSearch(nuevo_grafo_a_partir_del_mst, primer_elemento)
    respuesta = lt.newList("ARRAY_LIST")
    for destiny in lt.iterator(lst):
        if destiny != primer_elemento:
            distancia = 0
            distancia_trayecto = 0
            tiempo = 0
            tiempo_trayecto = 0
            camino = bfs.pathTo(search_2, destiny)
            #print("entro1")
            #if(camino != None):
            #print("entro")
            lst_aero = lt.newList("ARRAY_LIST")
            aeronaves_str = ""
            check_aeronaves = mp.newMap(maptype="PROBING")
            for y in lt.iterator(camino):
                lt.addFirst(lst_aero, y)
            for i in range(1, lt.size(lst_aero)):
                vertice_a = lt.getElement(lst_aero, i)
                vertice_b =  lt.getElement(lst_aero, i + 1)
                arco_distancia = gr.getEdge(nuevo_grafo_a_partir_del_mst, vertice_a, vertice_b)
                distancia = float(arco_distancia["weight"])
                
                distancia_trayecto += distancia
                arco_tiempo = gr.getEdge(grafo_carga_tiempos, vertice_a, vertice_b)
                tiempo = float(arco_tiempo["weight"])
                tiempo_trayecto += tiempo
                
                key_flight = str(vertice_a) + "-" + str(vertice_b)
                aeronave = me.getValue(mp.get(flights, key_flight))["elements"][0]["TIPO_AERONAVE"]

                if mp.contains(check_aeronaves, aeronave) == False:
                    aeronaves_str = aeronaves_str + " - " + aeronave
                    mp.put(check_aeronaves, aeronave, aeronave)
                
            lt.addLast(respuesta, 
                    {"aeropuerto origen": primer_elemento, 
                        "aeropuerto destino": destiny, 
                        "distancia recorrida": distancia_trayecto,
                        "tiempo trayecto": tiempo_trayecto,
                        "aeronaves": aeronaves_str})
    bono_req4(respuesta, data_structs)
    cantidad_tr = lt.size(respuesta)
    return primer_elemento, cantidad_ocurrencias, cantidad_tr, respuesta, distancia_total_trayectos      
        
def bono_req4(lst, data_structs):            
    lista_con_id = lst

    airports_id = data_structs["airports_id"]
    
    
    mapa = folium.Map(location=[19.9449799, 50.0646501], zoom_start=4)

    for x in lt.iterator(lista_con_id):
        aeropuerto_i = x["aeropuerto destino"]
        
        value = me.getValue(mp.get(airports_id, aeropuerto_i))
        longitude = float(value["LONGITUD"].replace(",", "."))
        latitude = float(value["LATITUD"].replace(",", "."))
        
        folium.Marker([latitude, longitude], popup=value).add_to(mapa)
    value_origin = me.getValue(mp.get(airports_id, "SKBO"))
    longitude_origin = float(value_origin["LONGITUD"].replace(",", "."))
    latitude_origin = float(value_origin["LATITUD"].replace(",", "."))
        
    folium.Marker([latitude_origin, longitude_origin], popup=value).add_to(mapa)
    
    
    for i in lt.iterator(lst):
        
        vertice_a = i["aeropuerto origen"]
        value_a = me.getValue(mp.get(airports_id, vertice_a))
        coordenada1 = [float(value_a["LATITUD"].replace(",", ".")), float(value_a["LONGITUD"].replace(",", "."))]
        vertice_b =  i["aeropuerto destino"]
        value_b = me.getValue(mp.get(airports_id, vertice_b))
        coordenada2 = [float(value_b["LATITUD"].replace(",", ".")), float(value_b["LONGITUD"].replace(",", "."))]
        
        AntPath(
                locations=[coordenada1, coordenada2],
                color='blue',
                weight=2.5,
                opacity=1
                ).add_to(mapa)
    
        #mapa.add_child(mc)
        
    mapa.save("mapa.html")            

def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    ocurrencia = data_structs["airports_mayor_ocurrencia"]
    grafo_militar_distancia = data_structs["militar_by_distance"]
    grafo_militar_tiempos = data_structs["militar_by_time"]
    
    flights = data_structs["flights"]
    
    lst_militar = me.getValue(mp.get(ocurrencia, "militar"))
    primer_elemento = lt.firstElement(lst_militar)["nombre"]
    cantidad_ocurrencias = lt.firstElement(lst_militar)["cantidad"]
    
    search = prim.PrimMST(graph=grafo_militar_distancia, origin=primer_elemento)
    distancia_total_trayectos = prim.weightMST(grafo_militar_distancia, search)
    
    table_edge_to = search["edgeTo"] 
    lista_aeropuertos_a_los_que_hay_camino = mp.keySet(table_edge_to) 
    lst = lt.newList("ARRAY_LIST")

    for x in lt.iterator(lista_aeropuertos_a_los_que_hay_camino):
        lt.addLast(lst, x)
    
    nuevo_grafo_a_partir_del_mst = gr.newGraph(datastructure="ADJ_LIST", directed=True, size=1000)
    
    for y in lt.iterator(lst):
        value = me.getValue(mp.get(table_edge_to, y))
        key_a = value["vertexA"]
        key_b = value["vertexB"]
        weight_asc = value["weight"]
        if gr.containsVertex(nuevo_grafo_a_partir_del_mst, key_a) == False:
            gr.insertVertex(nuevo_grafo_a_partir_del_mst, key_a)
        if gr.containsVertex(nuevo_grafo_a_partir_del_mst, key_b) == False:
            gr.insertVertex(nuevo_grafo_a_partir_del_mst, key_b)
        
        if gr.getEdge(grafo_militar_tiempos, key_a, key_b):
            gr.addEdge(nuevo_grafo_a_partir_del_mst, key_a, key_b, weight_asc)
    
    #recorrido desde el aeropuerto mayor concurrencia hasta todas sus posibles conexiones
    
    search_2 = bfs.BreathFirstSearch(nuevo_grafo_a_partir_del_mst, primer_elemento)
    respuesta = lt.newList("ARRAY_LIST")
    for destiny in lt.iterator(lst):
        if destiny != primer_elemento:
            distancia = 0
            distancia_trayecto = 0
            tiempo = 0
            tiempo_trayecto = 0
            camino = bfs.pathTo(search_2, destiny)
            lst_aero = lt.newList("ARRAY_LIST")
            aeronaves_str = ""
            check_aeronaves = mp.newMap(maptype="PROBING")
            for y in lt.iterator(camino):
                lt.addFirst(lst_aero, y)
            for i in range(1, lt.size(lst_aero)):
                vertice_a = lt.getElement(lst_aero, i)
                vertice_b =  lt.getElement(lst_aero, i + 1)
                arco_distancia = gr.getEdge(nuevo_grafo_a_partir_del_mst, vertice_a, vertice_b)
                distancia = float(arco_distancia["weight"])
                
                distancia_trayecto += distancia
                arco_tiempo = gr.getEdge(grafo_militar_tiempos, vertice_a, vertice_b)
                tiempo = float(arco_tiempo["weight"])
                tiempo_trayecto += tiempo
                
                key_flight = str(vertice_a) + "-" + str(vertice_b)
                aeronave = me.getValue(mp.get(flights, key_flight))["elements"][0]["TIPO_AERONAVE"]

                if mp.contains(check_aeronaves, aeronave) == False:
                    aeronaves_str = aeronaves_str + " - " + aeronave
                    mp.put(check_aeronaves, aeronave, aeronave)
                
            lt.addLast(respuesta, 
                    {"aeropuerto origen": primer_elemento, 
                        "aeropuerto destino": destiny, 
                        "distancia recorrida": distancia_trayecto,
                        "tiempo trayecto": tiempo_trayecto,
                        "aeronaves": aeronaves_str})
    bono_req5(respuesta, data_structs)
    cantidad_tr = lt.size(respuesta)
    return primer_elemento, cantidad_ocurrencias, cantidad_tr, respuesta, distancia_total_trayectos     

def bono_req5(lst, data_structs):            
    lista_con_id = lst

    airports_id = data_structs["airports_id"]
    
    
    mapa = folium.Map(location=[19.9449799, 50.0646501], zoom_start=4)

    for x in lt.iterator(lista_con_id):
        aeropuerto_i = x["aeropuerto destino"]
        
        value = me.getValue(mp.get(airports_id, aeropuerto_i))
        longitude = float(value["LONGITUD"].replace(",", "."))
        latitude = float(value["LATITUD"].replace(",", "."))
        
        folium.Marker([latitude, longitude], popup=value).add_to(mapa)
    value_origin = me.getValue(mp.get(airports_id, "SKAP"))
    longitude_origin = float(value_origin["LONGITUD"].replace(",", "."))
    latitude_origin = float(value_origin["LATITUD"].replace(",", "."))
        
    folium.Marker([latitude_origin, longitude_origin], popup=value).add_to(mapa)
    
    
    for i in lt.iterator(lst):
        
        vertice_a = i["aeropuerto origen"]
        value_a = me.getValue(mp.get(airports_id, vertice_a))
        coordenada1 = [float(value_a["LATITUD"].replace(",", ".")), float(value_a["LONGITUD"].replace(",", "."))]
        vertice_b =  i["aeropuerto destino"]
        value_b = me.getValue(mp.get(airports_id, vertice_b))
        coordenada2 = [float(value_b["LATITUD"].replace(",", ".")), float(value_b["LONGITUD"].replace(",", "."))]
        
        AntPath(
                locations=[coordenada1, coordenada2],
                color='blue',
                weight=2.5,
                opacity=1
                ).add_to(mapa)
    
        #mapa.add_child(mc)
        
    mapa.save("mapa.html")       


def req_6(data_structs, M):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    ocurrencia = data_structs["airports_mayor_ocurrencia"]
    gr_aeropuertos_comerciales_distance = data_structs["comercial_by_distance"]
    grafo_comercial_tiempos = data_structs["charge_by_time"]
    gr_aeropuertos_comerciales_time = data_structs["comercial_by_time"]
    lst_aeropuertos = data_structs["airports"]
    
    lst_comercial = me.getValue(mp.get(ocurrencia, "comercial"))
    lst_comercial_colombia = lt.newList('ARRAY_LIST')
    
    for elem in lt.iterator(lst_comercial):
        icao = elem["nombre"]
        airports_id = data_structs["airports_id"]
        pais = me.getValue(mp.get(airports_id, icao))['PAIS']
        if pais == "Colombia":
            lt.addLast(lst_comercial_colombia, elem)
            
    primer_elemento = lt.firstElement(lst_comercial_colombia)["nombre"] #Aereopuerto con mayor concurrencia comercial
    if lt.size(lst_comercial_colombia) > M:
        lst_M = lt.subList(lst_comercial_colombia, 2, M-1) #Lista aereopuertos mas importantes del pais (Sin el más importante)
    else:
        lst_M = lst_comercial_colombia
        lt.removeFirst(lst_M)
    cantidad_ocurrencias = lt.firstElement(lst_comercial_colombia)["cantidad"] #Valor de concurrencia comercial (total vuelos saliendo y llegando)
    ae_origen = primer_elemento
    lst_retornar = lt.newList('ARRAY_LIST')
    
    for elem in lt.iterator(lst_M):
        cantidad_aeropuerto_visitados = 0 #Total de aereopuertos del camino
        lista_aeropuertos = lt.newList("ARRAY_LIST") #Los aereopuertos incluidos en el camino
        tiempo_entre_trayectos = lt.newList("ARRAY_LIST")
        distancia_trayecto = 0 #distancia en km del camino
        distancia_entre_trayectos = lt.newList('ARRAY_LIST')
        resultado = None
        
        
        ae_destino = elem["nombre"]
        #print(ae_destino)
        search = djk.Dijkstra(gr_aeropuertos_comerciales_distance, ae_origen)
        #print(search)
        camino = djk.pathTo(search, ae_destino)
        if camino != None:
            #print(camino)
            cantidad_aeropuerto_visitados = camino["size"]
            for paso in lt.iterator(camino):
                lt.addFirst(lista_aeropuertos, paso)
            #print(lista_aeropuertos)
            if lt.size(lista_aeropuertos) > 1:
                for i in range(lt.size(lista_aeropuertos)):
                    vertice_a = lt.getElement(lista_aeropuertos, i)['vertexA']
                    vertice_b =  lt.getElement(lista_aeropuertos, i)['vertexB']
                    arco_distancia = gr.getEdge(gr_aeropuertos_comerciales_distance, vertice_a, vertice_b)
                    distancia = float(arco_distancia["weight"])
                    distancia_trayecto += distancia
                    lt.addFirst(distancia_entre_trayectos, {vertice_a + "-" + vertice_b : distancia})
                    arco_tiempo = gr.getEdge(gr_aeropuertos_comerciales_time, vertice_a, vertice_b)
                    tiempo = float(arco_tiempo["weight"])
                    lt.addFirst(tiempo_entre_trayectos, {vertice_a + "-" + vertice_b : tiempo})
            else:
                vertice_a = lt.firstElement(camino)['vertexA']
                vertice_b = lt.firstElement(camino)['vertexB']
                arco_distancia = gr.getEdge(gr_aeropuertos_comerciales_distance, vertice_a, vertice_b)
                distancia = float(arco_distancia["weight"])
                distancia_trayecto += distancia     
                arco_tiempo = gr.getEdge(gr_aeropuertos_comerciales_time, vertice_a, vertice_b)
                tiempo = float(arco_tiempo["weight"])
                lt.addLast(tiempo_entre_trayectos, {vertice_a + "-" + vertice_b : tiempo})
                
                
            resultado = ae_origen, ae_destino, lista_aeropuertos, cantidad_aeropuerto_visitados, tiempo_entre_trayectos, distancia_trayecto
            lt.addLast(lst_retornar, resultado)
    bono_req6(lst_retornar, data_structs)
    return primer_elemento, cantidad_ocurrencias, lst_retornar
    
def bono_req6(lst, data_structs):            
    lista_con_id = lst
    #print(lst)
    airports_id = data_structs["airports_id"]
    
    
    mapa = folium.Map(location=[19.9449799, 50.0646501], zoom_start=4)

    for x in lt.iterator(lst):
        #print(x)
        id_vertice_a = x[0]
        id_vertice_b = x[1]
        value_a = me.getValue(mp.get(airports_id, id_vertice_a))
        longitude_a = float(value_a["LONGITUD"].replace(",", "."))
        latitude_a = float(value_a["LATITUD"].replace(",", "."))
        folium.Marker([latitude_a, longitude_a], popup=value_a).add_to(mapa)
        
        value_b = me.getValue(mp.get(airports_id, id_vertice_b))
        longitude_b = float(value_b["LONGITUD"].replace(",", "."))
        latitude_b = float(value_b["LATITUD"].replace(",", "."))
        
        folium.Marker([latitude_b, longitude_b], popup=value_b).add_to(mapa)
        
        coordenada1 = [latitude_a, longitude_a]
        coordenada2 = [latitude_b, longitude_b]
        
        AntPath(
                locations=[coordenada1, coordenada2],
                color='blue',
                weight=2.5,
                opacity=1
                ).add_to(mapa)
    
        #mapa.add_child(mc)
        
    mapa.save("mapa.html")
        
    


def req_7(data_structs, latitud_origen, longitud_origen, latitud_destino, longitud_destino):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    gr_comerciales_distance = data_structs["comercial_by_distance"]
    gr_comerciales_time = data_structs["comercial_by_time"]
    lst_aeropuertos = data_structs["airports"]
    
    cantidad_aeropuerto_visitados = 0
    respuesta = lt.newList("ARRAY_LIST")
    tiempo_entre_trayectos = lt.newList("ARRAY_LIST")
    distancia_entre_trayectos = lt.newList('ARRAY_LIST')
    tiempo_total = 0
    distancia_trayecto = 0
    
    if(encontrar_minimo(latitud_origen, longitud_origen, lst_aeropuertos, True) == None or encontrar_minimo(latitud_destino, longitud_destino, lst_aeropuertos, True) == None):
        ae_origen = None
        ae_destino = None
    else:
        ae_origen = encontrar_minimo(latitud_origen, longitud_origen, lst_aeropuertos, True)[0]
        ae_destino = encontrar_minimo(latitud_destino, longitud_destino, lst_aeropuertos, True)[0]
        
    if ae_origen == None or ae_destino == None:
        ae_mas_cercano, distancia_mas_cercano = encontrar_minimo(latitud_origen, longitud_origen, lst_aeropuertos, False)
        return  ae_mas_cercano, distancia_mas_cercano, None, None, None, None, False, None, None
    else:
        search = djk.Dijkstra(gr_comerciales_time, ae_origen)
        camino = djk.pathTo(search, ae_destino)
        if camino != None:
            cantidad_aeropuerto_visitados = camino["size"]
            for paso in lt.iterator(camino):
                lt.addFirst(respuesta, paso)
            #print(respuesta)
            if lt.size(respuesta) > 1:
                for i in range(lt.size(respuesta)):
                    vertice_a = lt.getElement(respuesta, i)['vertexA']
                    vertice_b =  lt.getElement(respuesta, i)['vertexB']
                    arco_distancia = gr.getEdge(gr_comerciales_distance, vertice_a, vertice_b)
                    distancia = float(arco_distancia["weight"])
                    distancia_trayecto += distancia
                    lt.addFirst(distancia_entre_trayectos, {vertice_a + "-" + vertice_b : distancia})
                    arco_tiempo = gr.getEdge(gr_comerciales_time, vertice_a, vertice_b)
                    tiempo = float(arco_tiempo["weight"])
                    tiempo_total += tiempo
                    lt.addFirst(tiempo_entre_trayectos, {vertice_a + "-" + vertice_b : tiempo})
            else:
                vertice_a = lt.firstElement(camino)['vertexA']
                vertice_b = lt.firstElement(camino)['vertexB']
                arco_distancia = gr.getEdge(gr_comerciales_distance, vertice_a, vertice_b)
                distancia = float(arco_distancia["weight"])
                distancia_trayecto += distancia    
                lt.addFirst(distancia_entre_trayectos, {vertice_a + "-" + vertice_b : distancia}) 
                arco_tiempo = gr.getEdge(gr_comerciales_time, vertice_a, vertice_b)
                tiempo = float(arco_tiempo["weight"])
                tiempo_total += tiempo
                lt.addFirst(tiempo_entre_trayectos, {vertice_a + "-" + vertice_b : tiempo})           
        else:
            ae_mas_cercano, distancia_mas_cercano = encontrar_minimo(latitud_origen, longitud_origen, lst_aeropuertos, False)
            return ae_mas_cercano, distancia_mas_cercano, None, None, None, None, None, None, None
        bono_req7(data_structs, respuesta)
        return ae_origen, ae_destino, tiempo_entre_trayectos, distancia_trayecto, cantidad_aeropuerto_visitados, respuesta, True, tiempo_total, distancia_entre_trayectos

def bono_req7(data_structs, lst):          
    lista_con_id = lst
    #print(lista_con_id)
    airports_id = data_structs["airports_id"]

    
    mapa = folium.Map(location=[19.9449799, 50.0646501], zoom_start=4)

    for x in lt.iterator(lista_con_id):
        vertice_a = x["vertexA"]
        vertice_b = x["vertexB"]
        
        
        value_a = me.getValue(mp.get(airports_id, vertice_a))
        longitude_a = float(value_a["LONGITUD"].replace(",", "."))
        latitude_a = float(value_a["LATITUD"].replace(",", "."))
        folium.Marker([latitude_a, longitude_a], popup=value_a).add_to(mapa)
        
        value_b = me.getValue(mp.get(airports_id, vertice_b))
        longitude_b = float(value_b["LONGITUD"].replace(",", "."))
        latitude_b = float(value_b["LATITUD"].replace(",", "."))
        
        folium.Marker([latitude_b, longitude_b], popup=value_b).add_to(mapa)
        
        coordenada1 = [latitude_a, longitude_a]
        coordenada2 = [latitude_b, longitude_b]
        
        AntPath(
                locations=[coordenada1, coordenada2],
                color='blue',
                weight=2.5,
                opacity=1
                ).add_to(mapa)
    
        #mapa.add_child(mc)
        
    mapa.save("mapa.html")
        



def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def bono_tuplas(data_structs):
    """
    Funcion que implementa los grafos con tuplas
    
    """
    ae_origen = 'SCAR'
    ae_destino = 'SKOT'
    vuelos_hash = data_structs["flights"]
    comerciales_distance = data_structs["comercial_by_distance"]
    comerciales_time = data_structs["comercial_by_time"]
    vuelos = mp.keySet(vuelos_hash)
    grafo_tuplas = gr.newGraph(datastructure="ADJ_LIST", directed=True, size=1000)
    grafo_comp = gr.newGraph(datastructure="ADJ_LIST", directed=True, size=1000)
     
    for y in lt.iterator(vuelos):
        key_a, key_b = y.split('-')
        weight_tiemp = gr.getEdge(comerciales_time, key_a, key_b)
        weight_dist = gr.getEdge(comerciales_distance, key_a, key_b)
        
        if weight_tiemp != None and weight_dist != None:
            weight_tupla = (float(weight_dist['weight']), float(weight_tiemp['weight']))
        elif weight_tiemp == None and weight_dist != None:
            weight_tupla = (float(weight_dist['weight']), 0)
        else:
            weight_tupla = None
        
        if gr.containsVertex(grafo_tuplas, key_a) == False:
            gr.insertVertex(grafo_tuplas, key_a)
        if gr.containsVertex(grafo_tuplas, key_b) == False:
            gr.insertVertex(grafo_tuplas, key_b)
        if weight_tupla != None:
            gr.addEdge(grafo_tuplas, key_a, key_b, weight_tupla)
                                
        if gr.containsVertex(grafo_comp, key_a) == False:
            gr.insertVertex(grafo_comp, key_a)   
        if gr.containsVertex(grafo_comp, key_b) == False:
            gr.insertVertex(grafo_comp, key_b)
        if weight_dist != None:
            gr.addEdge(grafo_comp, key_a, key_b, float(weight_dist['weight']))
    
    #DIJSKTRA
    
    search_t = djkt.Dijkstra(grafo_tuplas, ae_origen, firstWeight= True)
    camino_t = djk.pathTo(search_t, ae_destino)
    search = djk.Dijkstra(grafo_comp, ae_origen)
    camino = djk.pathTo(search, ae_destino)
    
    cantidad_aeropuerto_visitados_t = 0
    cantidad_aeropuerto_visitados = 0
    
    distancia_entre_trayectos_t = lt.newList('ARRAY_LIST')
    distancia_entre_trayectos = lt.newList('ARRAY_LIST')
    
    distancia_trayecto_t = 0
    distancia_trayecto = 0
    
    respuesta_t = lt.newList('ARRAY_LIST')
    respuesta = lt.newList('ARRAY_LIST')
    
    if camino_t != None:
            cantidad_aeropuerto_visitados_t = camino_t["size"]
            for paso in lt.iterator(camino_t):
                lt.addFirst(respuesta_t, paso)
            if lt.size(respuesta_t) > 1:
                for i in range(lt.size(respuesta_t)):
                    vertice_a = lt.getElement(respuesta_t, i)['vertexA']
                    vertice_b =  lt.getElement(respuesta_t, i)['vertexB']
                    arco_distancia = gr.getEdge(comerciales_distance, vertice_a, vertice_b)
                    distancia = float(arco_distancia["weight"])
                    distancia_trayecto_t += distancia
                    lt.addFirst(distancia_entre_trayectos_t, {vertice_a + "-" + vertice_b : distancia})
            else:
                vertice_a = lt.firstElement(camino_t)['vertexA']
                vertice_b = lt.firstElement(camino_t)['vertexB']
                arco_distancia = gr.getEdge(comerciales_distance, vertice_a, vertice_b)
                distancia = float(arco_distancia["weight"])
                distancia_trayecto_t += distancia 
                lt.addFirst(distancia_entre_trayectos_t, {vertice_a + "-" + vertice_b : distancia})
                    
    if camino != None:
            cantidad_aeropuerto_visitados = camino["size"]
            for paso in lt.iterator(camino):
                lt.addFirst(respuesta, paso)
            if lt.size(respuesta) > 1:
                for i in range(lt.size(respuesta)):
                    vertice_a = lt.getElement(respuesta, i)['vertexA']
                    vertice_b =  lt.getElement(respuesta, i)['vertexB']
                    arco_distancia = gr.getEdge(comerciales_distance, vertice_a, vertice_b)
                    distancia = float(arco_distancia["weight"])
                    distancia_trayecto += distancia
                    lt.addFirst(distancia_entre_trayectos, {vertice_a + "-" + vertice_b : distancia})
            else:
                vertice_a = lt.firstElement(camino)['vertexA']
                vertice_b = lt.firstElement(camino)['vertexB']
                arco_distancia = gr.getEdge(comerciales_distance, vertice_a, vertice_b)
                distancia = float(arco_distancia["weight"])
                distancia_trayecto += distancia   
                lt.addFirst(distancia_entre_trayectos, {vertice_a + "-" + vertice_b : distancia})
    
    #Prim
    
    search_t = prim_tuple.PrimMST(graph=grafo_tuplas, origin=ae_origen, firstWeight=True)
    table_edge_t = search_t["edgeTo"] 
    lista_aeropuertos_t = mp.keySet(table_edge_t) 
    lst_tuple = lt.newList("ARRAY_LIST")

    for x in lt.iterator(lista_aeropuertos_t):
        lt.addLast(lst_tuple, x)

    search = prim.PrimMST(graph=grafo_comp, origin=ae_origen)
    table_edge_to = search["edgeTo"] 
    lista_aeropuertos_a_los_que_hay_camino = mp.keySet(table_edge_to) 
    lst = lt.newList("ARRAY_LIST")

    for w in lt.iterator(lista_aeropuertos_a_los_que_hay_camino):
        lt.addLast(lst, w) 

                
    return camino_t, cantidad_aeropuerto_visitados_t, distancia_entre_trayectos_t, camino, cantidad_aeropuerto_visitados, distancia_entre_trayectos, lst_tuple, lst
    

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

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
    pass


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass

def convertir_bool(a):
    if a == "True":
        return True
    else:
        return False