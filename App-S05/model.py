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
import math
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
from haversine import haversine as hvs
assert cf

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
    database = {"time_graph_com": None,
                "dist_graph_com": None,
                "time_graph_mil": None,
                "dist_graph_cargo": None,
                "airports_map": None,
                "military_tree":None,
                "commercial_tree": None,
                "cargo_tree": None,
                "edges_map": None
    }

    database["time_graph_com"] = gr.newGraph(directed=True, size=429)
    database["dist_graph_com"] = gr.newGraph(directed=True, size=429)
    database["time_graph_mil"] = gr.newGraph(directed=True, size=429)
    database["dist_graph_cargo"] = gr.newGraph(directed=True, size=429)
    database["airports_map"] = mp.newMap(maptype="CHAINING", loadfactor=4, numelements=429)
    database["military_tree"]= om.newMap(cmpfunction=compareCounts)
    database["commercial_tree"]= om.newMap(cmpfunction=compareCounts)
    database["cargo_tree"]= om.newMap(cmpfunction=compareCounts)

    #aca van los mapas no dirigidos
    database["time_nodirected_graph_com"] = gr.newGraph(directed=False, size=429)
    database["dist_nodirected_graph_com"] = gr.newGraph(directed=False, size=429)
    database["time_nodirected_graph_mil"] = gr.newGraph(directed=False, size=429)
    database["dist_nodirected_graph_mil"] = gr.newGraph(directed=False, size=429)
    database["time_nodirected_graph_cargo"] = gr.newGraph(directed=False, size=429)
    database["dist_nodirected_graph_cargo"] = gr.newGraph(directed=False, size=429)

    database["edges_map"] = mp.newMap(maptype="CHAINING", loadfactor=4)

    return database


# Funciones para agregar informacion al modelo

def load_data_airport(database, airport_input):
    """
    Función que carga la información dentro del modelo y las estructuras correspondientes.
    """
    add_info_airports_map(database, airport_input)

    return database

def load_connection(database, flight):
    """Función que carga las conexiones, en este caso vuelos, entre los aeropuertos. La función determina el 
    tipo de vuelo de la entrada y, dependiendo de esto, crea la conexión entre los dos aeropuertos involucrados
    en los grafos requeridos. Dadas las funcionalidades de los requerimientos, por cada tipo de vuelo hay dos grafos dirigidos,
    uno con pesos de distancia entre aeropuertos y otro con pesos de tiempo de vuelo entre aeropuertos. La función accede a esta
    información a través del método haversine y la información provista por el archivo, respectivamente. 

    Args:
        database (dict): Base de datos que contiene las estructuras del modelo
        flight (dict): Diccionario con la información de un vuelo entre dos aeropuertos 
        (una línea del csv 'flights').

    Returns:
        dict: Base de datos actualizada
    """
    vertexA = flight["ORIGEN"]
    vertexB = flight["DESTINO"]
    #determina vértices de origen y destino
    airports_map = database["airports_map"]
    mp.put(database["edges_map"], (vertexA, vertexB), flight["TIPO_AERONAVE"])
    #acceder al mapa con la información de los aeropuertos y al de los vuelos
    flight_type = flight["TIPO_VUELO"]
    #acceder a las coordenadas de cada aeropuerto para calcular la distancia entre ellos. 
    entryA = mp.get(airports_map, vertexA)
    dict_A = me.getValue(entryA)
    pos_A = (float(dict_A["LATITUD"]), float(dict_A["LONGITUD"])) # lat, lon

    entryB = mp.get(airports_map, vertexB)
    dict_B = me.getValue(entryB)
    pos_B = (float(dict_B["LATITUD"]), float(dict_B["LONGITUD"])) # lat, lon

    distance = hvs(pos_A, pos_B)
    #determina el tipo de vuelo
    #sin importar el tipo, el algoritmo sigue los siguientes pasos
        #1. accede a los grafos de distancia y tiempo del tipo
        #2. actualiza los contadores de concurrencia del tipo para ambos aeropuertos en la tabla de hash
        #3. revisa si los aeropuertos ya existen como vértices en los grafos
            #si no existen, crea los vértices, si existen, sigue sin hacer pasos extra.
        #4. Añade las conexiones a ambos grafos, indicando el peso correspondiente para cada uno. 
    if flight_type == "AVIACION_COMERCIAL":
        dist_graph = database["dist_graph_com"]
        time_graph = database["time_graph_com"]
        ##no dirigidos
        dist_nodirected_graph = database["dist_nodirected_graph_com"]
        time_nodirected_graph = database["time_nodirected_graph_com"]
        ##...

        dict_A["com_count"] += 1
        dict_B["com_count"] += 1
        
        if not gr.containsVertex(dist_graph, vertexA):
            gr.insertVertex(dist_graph, vertexA)
        if not gr.containsVertex(time_graph, vertexA):
            gr.insertVertex(time_graph, vertexA)
        if not gr.containsVertex(dist_graph, vertexB):
            gr.insertVertex(dist_graph, vertexB)
        if not gr.containsVertex(time_graph, vertexB):
            gr.insertVertex(time_graph, vertexB)
        gr.addEdge(time_graph, vertexA, vertexB, int(flight["TIEMPO_VUELO"]))
        gr.addEdge(dist_graph, vertexA, vertexB, distance)

        ##no dirigidios
        if not gr.containsVertex(dist_nodirected_graph, vertexA):
            gr.insertVertex(dist_nodirected_graph, vertexA)
        if not gr.containsVertex(time_nodirected_graph, vertexA):
            gr.insertVertex(time_nodirected_graph, vertexA)
        if not gr.containsVertex(dist_nodirected_graph, vertexB):
            gr.insertVertex(dist_nodirected_graph, vertexB)
        if not gr.containsVertex(time_nodirected_graph, vertexB):
            gr.insertVertex(time_nodirected_graph, vertexB)
        gr.addEdge(time_nodirected_graph, vertexA, vertexB, int(flight["TIEMPO_VUELO"]))
        gr.addEdge(dist_nodirected_graph, vertexA, vertexB, distance)
        ##...
    elif flight_type == "MILITAR":
        dist_graph = database["time_graph_mil"]

        ##no dirigidos
        dist_nodirected_graph = database["dist_nodirected_graph_mil"]
        time_nodirected_graph = database["time_nodirected_graph_mil"]
        ##...

        dict_A["mil_count"] += 1
        dict_B["mil_count"] += 1
        if not gr.containsVertex(dist_graph, vertexA):
            gr.insertVertex(dist_graph, vertexA)
        if not gr.containsVertex(dist_graph, vertexB):
            gr.insertVertex(dist_graph, vertexB)
        gr.addEdge(dist_graph, vertexA, vertexB, int(flight["TIEMPO_VUELO"]))

         ##no dirigidios
        if not gr.containsVertex(dist_nodirected_graph, vertexA):
            gr.insertVertex(dist_nodirected_graph, vertexA)
        if not gr.containsVertex(time_nodirected_graph, vertexA):
            gr.insertVertex(time_nodirected_graph, vertexA)
        if not gr.containsVertex(dist_nodirected_graph, vertexB):
            gr.insertVertex(dist_nodirected_graph, vertexB)
        if not gr.containsVertex(time_nodirected_graph, vertexB):
            gr.insertVertex(time_nodirected_graph, vertexB)
        gr.addEdge(time_nodirected_graph, vertexA, vertexB, int(flight["TIEMPO_VUELO"]))
        gr.addEdge(dist_nodirected_graph, vertexA, vertexB, distance)
        ##...


    else:
        dist_graph = database["dist_graph_cargo"]
        dict_A["cargo_count"] += 1
        dict_B["cargo_count"] += 1

        ##
        dist_nodirected_graph = database["dist_nodirected_graph_cargo"]
        time_nodirected_graph = database["time_nodirected_graph_cargo"]
        #...
        if not gr.containsVertex(dist_graph, vertexA):
            gr.insertVertex(dist_graph, vertexA)
        if not gr.containsVertex(dist_graph, vertexB):
            gr.insertVertex(dist_graph, vertexB)
        gr.addEdge(dist_graph, vertexA, vertexB, distance)

        ##no dirigidios
        if not gr.containsVertex(dist_nodirected_graph, vertexA):
            gr.insertVertex(dist_nodirected_graph, vertexA)
        if not gr.containsVertex(time_nodirected_graph, vertexA):
            gr.insertVertex(time_nodirected_graph, vertexA)
        if not gr.containsVertex(dist_nodirected_graph, vertexB):
            gr.insertVertex(dist_nodirected_graph, vertexB)
        if not gr.containsVertex(time_nodirected_graph, vertexB):
            gr.insertVertex(time_nodirected_graph, vertexB)
        gr.addEdge(time_nodirected_graph, vertexA, vertexB, int(flight["TIEMPO_VUELO"]))
        gr.addEdge(dist_nodirected_graph, vertexA, vertexB, distance)
        ##...
    return database


def add_info_airports_map(database, airport_dict):
    """
    Función para agregar elementos a la tabla de Hash que contiene los aeropuertos registrados en
    los archivos correspondientes. Las llaves son los identificadores únicos de cada aeropuerto y los
    valores los diccionarios que contienen la información correspondiente.
    
    Args:
        database: Base de Datos
        airport_dict: Diccionario con la información del aeropuerto
    
    Returns:
        dict: Base de datos actualizada
    """
    #convertir latitud y longitud a números
    airport_dict["LATITUD"] = float(airport_dict["LATITUD"].replace(',', '.'))
    airport_dict["LONGITUD"] = float(airport_dict["LONGITUD"].replace(',', '.'))
    #crear una tupla para acceder más fácil a las coordenadas de un aeropuerto
    airport_dict["coord"]=(airport_dict["LATITUD"], airport_dict["LONGITUD"])
    #crear contadores para las concurrencias de cada tipo de vuelo para el aeropuerto
    airport_dict["com_count"] = 0
    airport_dict["mil_count"] = 0
    airport_dict["cargo_count"] = 0
    mapa = database["airports_map"]
    #insertar en la tabla de hash.
    mp.put(mapa, airport_dict["ICAO"], airport_dict)
    return database

def analyzer(database):
    """Función que permite obtener la información necesaria para imprimir en pantalla
    al finalizar la carga de datos. 

    Args:
        database (dict): Base de Datos con las estructuras del modelo

    Returns:
        tuple: Contiene el número de aeropuertos y vuelos cargados, así como listas con 
        los aeropuertos con mayor y menor concurrencia para cada tipo de vuelo. 
    """
    #placeholders para el número de vuelos y aeropuertos
    str1 = ''
    str2 = ''
    #acceder a tabla de hash de aeropuertos
    airport_map = database["airports_map"]
    #acceder a los grafos de todos los tipos de vuelo
    graph1 = database["dist_graph_com"]
    graph2 = database["dist_graph_cargo"]
    graph3 = database["time_graph_mil"]
    #acceder a los árboles que ordenan aeropuertos por concurrencia de cada tipo de vuelo
    tree1 = database["commercial_tree"]
    tree2 = database["cargo_tree"]
    tree3 = database["military_tree"]
    #número total de aeropuertos
    total_vertices = mp.size(airport_map)
    #numero total de vuelos, suma de los vuelos entre todos los grafos/tipos de vuelo.
    total_edges = gr.numEdges(graph1)+gr.numEdges(graph2)+gr.numEdges(graph3)
    #obtener listas de los aeropuertos con mayor y menor conteo para cada tipo de vuelo
    most_com = get_most_count_tree(database, tree1, 5)
    least_com = get_least_count_tree(database,tree1, 5)
    most_cargo = get_most_count_tree(database,tree2, 5)
    least_cargo = get_least_count_tree(database,tree2, 5)
    most_mil = get_most_count_tree(database,tree3, 5)
    least_mil = get_least_count_tree(database,tree3, 5)
    
    str1 = "El número de aeropuertos cargados es: {0}".format(total_vertices)
    str2 = "El número de vuelos cargados es: {0}".format(total_edges)
    

    return str1, str2, most_com, least_com, most_cargo, least_cargo, most_mil, least_mil

def create_ordered_maps_airports (database):
    """Función que crea árboles binarios ordenados para los aeropuertos, tal que sean organizados
    por su conteo de cada una de las concurrencias posibles (comercial, carga y militar.)

    Args:
        database (dict): Base de Datos que contiene las estructuras del modelo
    """
    #acceder a la tabla de hash con la información de los aeropuertos y a los árboles vacíos.
    airports_map = database["airports_map"]
    commercial_tree = database["commercial_tree"]
    cargo_tree = database["cargo_tree"]
    military_tree = database["military_tree"]
    
    #obtener la lista de los diccionarios de los aeropuertos
    airports_lst = mp.valueSet(airports_map)
    
    #recorrer la lista de aeropuertos
    for airport in lt.iterator(airports_lst):
        #acceder a la información relevante del aeropuerto, conteos y código.
        airport_code = airport["ICAO"]
        com_count = airport["com_count"] 
        mil_count = airport["mil_count"] 
        cargo_count = airport["cargo_count"] 
        #para cada uno de los árboles, revisar si el conteo del aeropuerto para ese
        #tipo de vuelo ya existe
            #si ya existe, añadir el código del aeropuerto a la lista asociada a ese conteo
            #si no existe, crear una lista, añadir el código del aeropuerto a la lista, e insertar la lista en el mapa.
        if om.contains(commercial_tree, com_count):
            count_lst = me.getValue(om.get(commercial_tree, com_count))
            lt.addLast(count_lst, airport_code)
        else:
            count_lst = lt.newList("ARRAY_LIST")
            lt.addLast(count_lst, airport_code)
            om.put(commercial_tree, com_count, count_lst)
            
        if om.contains(cargo_tree, cargo_count):
            count_lst = me.getValue(om.get(cargo_tree, cargo_count))
            lt.addLast(count_lst, airport_code)
        else:
            count_lst = lt.newList("ARRAY_LIST")
            lt.addLast(count_lst, airport_code)
            om.put(cargo_tree, cargo_count, count_lst)
            
        if om.contains(military_tree, mil_count):
            count_lst = me.getValue(om.get(military_tree, mil_count))
            lt.addLast(count_lst, airport_code)
        else:
            count_lst = lt.newList("ARRAY_LIST")
            lt.addLast(count_lst, airport_code)
            om.put(military_tree, mil_count, count_lst)
    

# Funciones de consulta

def get_most_count_tree (database, tree, num):
    """Función que permite obtener los 'num' aeropuertos con mayor conteo de un
    tipo de vuelo.

    Args:
        database (dict): Base de datos que contiene las estructuras del modelo
        tree (Ordered Map): Árbol binario ordenado sobre el cual se quiere conseguir los valores con 
        mayor conteo
        num (int): Número de aeropuertos que se quieren retornar

    Returns:
        list: Lista nativa de python con los diccionarios de los 'num' aeropuertos con mayor conteo del árbol ingresado
    """
    #acceder a la tabla de hash que contiene la información de los aeropuertos
    airport_map = database['airports_map']
    #determinar máxima concurrencia para el tipo de vuelo
    max_key = om.maxKey(tree)
    response_lst = []
    #recorrer el árbol mientras haya menos de 'num' aeropuertos en la lista de entrega
    while len(response_lst)<num:
        #acceder a la lista de los aeropuertos con mayor conteo y ordenarla alfabéticamente
        count_lst = me.getValue(om.get(tree, max_key))
        count_lst = sort_airport_codes(count_lst)
        i = 1
        #recorrer la lista de aeropuertos del máximo conteo actual
        while len(response_lst)<num and i < lt.size(count_lst)+1:
            #acceder al código del aeropuerto
            airport_code = lt.getElement(count_lst, i)
            #acceder a la información del aeropuerto en la tabla de hash
            airport = me.getValue(mp.get(airport_map, airport_code))
            #insertar el aeropuerto en la lista de retorno
            response_lst.append(airport)
            i+=1
        #actualizar la llave máxima para recorrer el árbol
        max_key-=1
        max_key= om.floor(tree, max_key)
    return response_lst

def get_least_count_tree (database, tree, num):
    """Función que permite obtener los 'num' aeropuertos con menor concurrencia de un
    tipo de vuelo, tal que estos tengan por lo menos un vuelo de dicho tipo. Funcionamiento
    muy similar a la función 'get_most_count_tree', invirtiendo el orden del recorrido del árbol.

    Args:
        database (dict): Base de datos que contiene las estructuras del modelo
        tree (Ordered Map): Árbol binario ordenado sobre el cual se quiere conseguir los valores con 
        mayor conteo
        num (int): Número de aeropuertos que se quieren retornar

    Returns:
        list: Lista nativa de python con los diccionarios de los 'num' aeropuertos con mayor conteo del árbol ingresado
    """
    airport_map = database['airports_map']
    min_key = om.minKey(tree)
    if min_key== 0:
        new = min_key+1
        min_key=om.ceiling(tree, new)
    response_lst = []
    
    while len(response_lst)<num:
        count_lst = me.getValue(om.get(tree, min_key))
        count_lst = sort_airport_codes(count_lst)
        i = 1
        while len(response_lst)<num and i < lt.size(count_lst)+1:
            airport_code = lt.getElement(count_lst, i)
            airport = me.getValue(mp.get(airport_map, airport_code))
            response_lst.append(airport)
            i+=1
        min_key+=1
        min_key= om.ceiling(tree, min_key)
    return response_lst


def check_coordinates(coord_tuple, database):
    """Función que determina el aeropuerto registrado en la base de datos
    mas cercano a un par de coordenadas dado.

    Args:
        coord_tuple (tuple): Tupla de latitud y longitud en decimales, para la cual se quiere
        determinar el aeropuerto más cercano.
        database (dict): Base de datos que contiene las estructuras del modelo

    Returns:
        tuple: El aeropuerto de menor distancia a las coordenadas y esta distancia, en km.
    """
    #acceder a la lista de aeropuertos registrados en la base de datos.
    airports_map = database["airports_map"]
    airports_lst = mp.valueSet(airports_map)
    #placeholders para la información a guardar
    least_distance_airport = ""
    least_distance = 1000000000000
    #recorrer la lista de aeropuertos
    for airport in lt.iterator(airports_lst):
        #acceder al código y las coordenadas de cada aeropuerto
        airport_code = airport["ICAO"]
        airport_coord = airport["coord"]
        #determinar la distancia entre el aeropuerto y las coordenadas ingresadas y el aeropuerto
        #utiliza haversine
        dist = hvs(coord_tuple, airport_coord)
        #compara con la menor distancia actual y, en caso de ser menor, actualiza los datos.
        if dist <least_distance:
            least_distance_airport = airport_code
            least_distance = dist
    return least_distance_airport, least_distance



def req_1_2(database, origin, dest, req):
    """Función que resuelve los requerimientos 1 y 2. La función accede a los grafos con pesos de distancia y
    tiempo para vuelos comerciales, revisa que las coordenadas ingresadas para origen y destino sean válidas, y 
    devuelve el resultado dependiendo del requerimiento que se quiere resolver. 
        1. Para el req 1, la función utiliza el algoritmo 'dfs' para determinar si existe un camino posible entre los 
        puntos ingresados, accede a ese camino y genera un retorno adecuado para luego imprimir en pantalla.
        2. Para el req 2, los procedimientos son muy similares, solo se cambia al algoritmo 'bfs' para determinar el camino
        con menos escalas. 

    Args:
        database (dict): Base de datos con las estructuras del modelo
        origin (tuple): Tupla de coordenadas (lat, lon) del punto de origen
        dest (tuple): Tupla de coordenadas (lat, lon) del punto de destino
        req (int): Requerimiento que se quiere resolver, '1' o '2'

    Returns:
        tuple: Una tupla con la lista de trayectos que se deben tomar, la distancia y tiempo de vuelos totales
        del camino, el número total de aeropuertos vistados, y la información de los aeropuertos de origen y destino.
    """
    #acceder a los grafos necesarios
    commercial_graph_dist = database["dist_graph_com"]
    commercial_graph_time = database["time_graph_com"]
    #acceder a la tabla de hash con la info de los aeropuertos
    airports_map = database["airports_map"]
    #determinar los aeropuertos más cercanos y sus distancias a los puntos de origen y destino.
    origin_airport, origin_distance = check_coordinates(origin, database)
    destination_airport, dest_distance = check_coordinates(dest, database)
    #si la distancia a los aeropuertos tanto del origen como del destino es menor a 30 km, sigue con el proceso.
    if origin_distance <= 30 and dest_distance <= 30:
        #establece el algoritmo de búsqueda y la estructura de búsqueda dependiendo del requerimiento que se quiere resolver.
        if req == 1:
            search_algo = dfs
            search_graph_dist = dfs.DepthFirstSearch(commercial_graph_dist, origin_airport)
        elif req == 2:
            search_algo = bfs
            search_graph_dist = bfs.BreathFirstSearch(commercial_graph_dist, origin_airport)
        #revisar si existe un camino entre el aeropuerto de origen y el de destino
        path_exists = search_algo.hasPathTo(search_graph_dist, destination_airport)
        if path_exists == True: #hay camino
            #generar placeholders para la información que se debe retornar
            airports_list = lt.newList()
            total_dist = origin_distance+dest_distance
            total_time = 0
            #generar el camino entre origen y destino mediante el algoritmo pertinente.
            dist_path = search_algo.pathTo(search_graph_dist, destination_airport)
            #actualizar el número total de aeropuertos
            total_airports = st.size(dist_path)
            origin_airport_full = ""
            destination_airport_full = ""
            i = 1
            #recorrer el camino (solo trae los vértices)
            while i < st.size(dist_path):
                #acceder al aeropuerto de destino y al de origen
                org_airport = lt.getElement(dist_path, i+1)
                dest_airport = lt.getElement(dist_path, i)
                #acceder a los arcos entre los aeropuertos en ambos grafos
                dist_edge = gr.getEdge(commercial_graph_dist, org_airport, dest_airport)
                time_edge = gr.getEdge(commercial_graph_time, org_airport, dest_airport)
                #acceder a la distancia y al tiempo de vuelo
                flight_distance = dist_edge["weight"]
                flight_time = time_edge["weight"]
                #sumar el tiempo de vuelo y la distancia a los totales del camino
                total_dist+= flight_distance
                total_time+=flight_time
                
                #generar el diccionario para el camino
                airports_info= get_airports_info_req1_2(airports_map, org_airport, dest_airport,flight_distance, flight_time)
                
                #generar la información para el aeropuerto de origen y destino globales
                if org_airport == origin_airport:
                    origin_airport_full = "{0} ({1})".format(airports_info["NOMBRE ORIGEN"], org_airport)
                if dest_airport == destination_airport:
                    destination_airport_full = "{0} ({1})".format(airports_info["NOMBRE DESTINO"], dest_airport)
                #añadir el diccionario de la conexión a la lista de entrega
                lt.addFirst(airports_list, airports_info)
                i+=1
            return airports_list, total_dist, total_time, total_airports, origin_airport_full, destination_airport_full
        else:
            return -2, origin_airport, origin_distance, destination_airport, dest_distance
    else:
        return -1, origin_airport, origin_distance, destination_airport, dest_distance

def get_airports_info_req1_2(airports_map, org_airport, dest_airport, dist, time):
    """Función que genera un diccionario para representar un vuelo entre dos aeropuertos. 
    La función accede a la información de cada aeropuerto a través de su ICAO y genera un único 
    diccionario con la información necesaria. 

    Args:
        airports_map (tabla de hash): Tabla de hash de los aeropuertos por ICAO
        org_airport (str): ICAO del aeropuerto de origen del vuelo
        dest_airport (str): ICAO del aeropuerto de destino del vuelo
        dist (int): Distancia entre los aeropuertos
        time (int): Tiempo de vuelo

    Returns:
        dict: Diccionario con la información del vuelo entre los aeropuertos
    """
    #acceder a los diccionarios de los aeropuertos en la tabla de hash
    org_airport_dict = me.getValue(mp.get(airports_map, org_airport))
    dest_airport_dict = me.getValue(mp.get(airports_map, dest_airport))
    #crear el diccionario.
    airport_info = {"ICAO ORIGEN": org_airport,
                    "NOMBRE ORIGEN": org_airport_dict["NOMBRE"],
                    "CIUDAD ORIGEN": org_airport_dict["CIUDAD"],
                    "PAIS ORIGEN": org_airport_dict["PAIS"],
                    "ICAO DESTINO": dest_airport,
                    "NOMBRE DESTINO": dest_airport_dict["NOMBRE"],
                    "CIUDAD DESTINO": dest_airport_dict["CIUDAD"],
                    "PAIS DESTINO": dest_airport_dict["PAIS"],
                    "DISTANCIA (KM)": round(dist,2),
                    "TIEMPO DE VUELO (MINS)":time,
                    "org_coord": org_airport_dict["coord"],
                    "dest_coord": dest_airport_dict["coord"]}
    return airport_info

def req_3_4_5(database, req):
    """
    Función que soluciona el requerimiento 3, 4, 5. 
    Args:
        Database: el modelo con las estructuras de datos
        Req: cuál de los tres requerimientos se requiere resolver

    returns:
        Concurrency: Nivel de Concurrencia de un Aeropuerto
        Source_Airport: Diccionario del Aeropuero Base
        Total_Weight: Peso total del MST (Distancia o Tiempo)
        Other_Weight: El otro tipo de peso total del MST (Tiempo o Distancia)
        Airport_dicc_list: la lista de aeropuertos alcanzables en el mst
    """
    airports_map = database["airports_map"]
    airplanes_map = database["edges_map"]
    concurrecy, source_airport = find_most_concurrency_airport(database, req)
    ICAO_source = source_airport["ICAO"]

    selected_graph, other_graph = graph_selector(database, req)

    MST_tree = prim.PrimMST(selected_graph, ICAO_source)
    total_weight = prim.weightMST(selected_graph, MST_tree)
    cola = prim.edgesMST(selected_graph, MST_tree)
    marked_map = cola["marked"]
    edgeTo_map = cola["edgeTo"]
    vertices_list = mp.keySet(marked_map)
    total_other_weight = 0
    airport_dict_list = lt.newList("ARRAY_LIST")
    folium_connections = mp.newMap(400, maptype="PROBING")
    for airport in lt.iterator(vertices_list):
        if airport != ICAO_source:
            airport_info = me.getValue(mp.get(airports_map, airport))
            path_weight = 0
            path_other_weight = 0
            airplane_types = lt.newList()
            path_source = prim_path(edgeTo_map, ICAO_source, airport)
            i = 1
            while i < st.size(path_source):
                #acceder al aeropuerto de destino y al de origen
                org_airport = lt.getElement(path_source, i)
                dest_airport = lt.getElement(path_source, i+1)
                #acceder a los arcos entre los aeropuertos en ambos grafos
                edge = gr.getEdge(selected_graph, org_airport, dest_airport)
                other_edge = gr.getEdge(other_graph, org_airport, dest_airport)
                org_airport_info = me.getValue(mp.get(airports_map, org_airport))
                dest_airport_info = me.getValue(mp.get(airports_map, dest_airport))
                org_coord = org_airport_info["coord"]
                dest_coord = dest_airport_info["coord"]
                mp.put(folium_connections, (org_airport, dest_airport), (org_coord, dest_coord))
                #acceder a la distancia y al tiempo de vuelo
                edge_weight = edge["weight"]
                edge_other_weight = other_edge["weight"]
                #sumar el tiempo de vuelo y la distancia a los totales del camino
                path_weight+= edge_weight
                path_other_weight+=edge_other_weight
                total_other_weight += edge_other_weight
                airplane_type_entry = mp.get(airplanes_map, (org_airport, dest_airport))
                if airplane_type_entry == None:
                    airplane_type_entry = mp.get(airplanes_map, (dest_airport, org_airport))
                airplane_type = me.getValue(airplane_type_entry)
                if not lt.isPresent(airplane_types, airplane_type):
                    lt.addLast(airplane_types, airplane_type)
                i+=1
            airport_dict ={}
            airport_dict["NOMBRE"] = airport_info["NOMBRE"]
            airport_dict["ICAO"] = airport
            airport_dict["CIUDAD"] = airport_info["CIUDAD"]
            airport_dict["PAIS"] = airport_info["PAIS"]
            airport_dict["weight"] = path_weight
            airport_dict["other_weight"] = path_other_weight
            airport_dict["airplanes_list"] = airplane_types
            airport_dict["coord"] = airport_info["coord"]
            lt.addLast(airport_dict_list, airport_dict)
    connections_list = mp.valueSet(folium_connections)
    return concurrecy, source_airport, total_weight, total_other_weight, airport_dict_list, connections_list

def prim_path (prim_map, org_airport, dest_airport):
    encontrado = False
    path = lt.newList()
    lt.addFirst(path, dest_airport)
    while encontrado == False:
        edge = me.getValue(mp.get(prim_map, dest_airport))
        vertexA = edge["vertexA"]
        lt.addFirst(path, vertexA)
        if vertexA == org_airport:
            encontrado = True
        else:
            dest_airport = vertexA
    return path
    
def find_most_concurrency_airport(database, req):
    if req == "req3":
        tree = database["commercial_tree"]
    elif req == "req4":
        tree = database["cargo_tree"]
    else:
        tree = database["military_tree"]
    
    concurrency = om.maxKey(tree)
    list_max_key = om.get(tree, concurrency)
    list = me.getValue(list_max_key)

    sorted_lst = alphabetic_sort(list)

    airport_entry = mp.get(database["airports_map"], lt.getElement(sorted_lst, 1))
    concurrency_airport = me.getValue(airport_entry)

    return concurrency, concurrency_airport

def graph_selector(database, req):
    if req == "req3":
        graph1 = database["dist_nodirected_graph_com"]
        graph2 = database["time_nodirected_graph_com"]
    elif req == "req4":
        graph1 = database["dist_nodirected_graph_cargo"]
        graph2 = database["time_nodirected_graph_cargo"]
    else:
        graph1 = database["time_nodirected_graph_mil"]
        graph2 = database["dist_nodirected_graph_mil"]
    
    return graph1, graph2

def req_6(database, num):
    """Función que soluciona el requerimiento 6. 
    La función accede, a través de los árboles binarios ordenados generados en la carga, a los
    'num' aeropuertos con mayor concurrencia comercial, con lo cual se conoce el de mayor concurrencia.
    Para los otros aeropuertos, la función encuentra, usando el algoritmo de Dijkstra, la secuencia de 
    vuelos con la menor distancia para llegar del aeropuerto de mayor concurrencia a cada uno de los otros 
    aeropuertos. Para cada una de estas secuencias, la función determina los aeropuertos visitados, 
    así como los vuelos que se deben tomar. 

    Args:
        database (dict): Base de datos que contiene las estructuras del modelo
        num (int): Número de aeropuertos más concurridos que se quieren revisar. 

    Returns:
        tuple: Entrega una lista ADT con la información de los caminos para llegar a los 'num' 
        aeropuertos más importantes, así como la información sobre el aeropuerto de mayor concurrencia.
    """
    #acceder a las estructuras necesarias (tablas de hash, grafo y árbol binario ordenado)
    airports_com_tree = database["commercial_tree"]
    commercial_dist_graph = database["dist_graph_com"]
    airports_map = database["airports_map"]
    #determinar los 'num' aeropuertos con mayor concurrencia comercial en Colombia
    most_airports = get_most_count_tree_colombia(database, airports_com_tree, num+1)
    #determinar el aeropuerto de mayor concurrencia
    max_airport = most_airports[0]
    origin_airport = max_airport["ICAO"]
    #generar la estructura de búsqueda para el grafo. 
    search_graph = djk.Dijkstra(commercial_dist_graph, origin_airport)
    airports_dict_lst = lt.newList("ARRAY_LIST")
    #recorrer los aeropuertos más importantes, excluyendo el de mayor concurrencia.
    for i in range(1,num+1):
        #acceder a la información del aeropuerto
        airport = most_airports[i]
        destination_airport = airport["ICAO"]
        #crear listas para guardar la información, así como un diccionario para toda la información del aeropuerto
        airports_list = lt.newList()
        edges_list = lt.newList()
        path_dict = {}
        #verificar que haya camino entre el aeropuerto de mayor concurrencia y el aeropuerto actual del recorrido.
        if djk.hasPathTo(search_graph, destination_airport): #si hay camino
            
            #generar el camino entre los aeropuertos
            path = djk.pathTo(search_graph, destination_airport)
            #calcular la distancia entre los aeropuertos
            total_dist = djk.distTo(search_graph, destination_airport)
            #recorrer los arcos del camino para llegar al aeropuerto de destino
            for edge in lt.iterator(path):
                #declarar aeropuerto de destino y origen
                org_airport = edge["vertexA"]
                dest_airport = edge["vertexB"]
                #generar el diccionario que contiene la información del arco
                edge_info = get_airports_info_req1_2(airports_map, org_airport, dest_airport, 1, 1)
                #añadir el diccionario a la lista de arcos
                lt.addFirst(edges_list, edge_info)
                if dest_airport == destination_airport:
                    #si el aeropuerto de destino actual es el de destino global, añadir su info
                    #a la lista de aeropuertos. Simplifica el proceso de añadir esta información
                    #porque, añadir ambos generaría duplicados. 
                    dest_airport_info = get_single_airport_info(airports_map, dest_airport)
                    lt.addFirst(airports_list, dest_airport_info)
                #generar el diccionario con la info del aeropuerto de origen
                org_airport_info = get_single_airport_info(airports_map, org_airport)
                #añadir el diccionario del origen a la lista
                lt.addFirst(airports_list, org_airport_info)
            #actualizar el diccionario del aeropuerto con la información necesaria
            path_dict["ICAO"]=destination_airport
            path_dict["NOMBRE"]= airport["NOMBRE"]
            path_dict["concurrency"]=airport["com_count"]
            path_dict["airports_list"] = airports_list
            path_dict["edges_list"]=edges_list
            path_dict["total_dist"] = total_dist
            path_dict["total_airports"] = lt.size(path)+1
            #añadir el diccionario del aeropuerto a la lista que entregará el requerimiento
            lt.addLast(airports_dict_lst, path_dict)
        else: #no hay camino
            #se añade un -1 para generalizar el error e imprimir lo adecuado en consola. 
            lt.addLast(airports_dict_lst, -1)
    return airports_dict_lst, max_airport

def get_single_airport_info (airports_map, airport):
    """Función que permite generar un 'subdiccionario' de un
    aeropuerto; facilitar manejo de datos en req 6.

    Args:
        airports_map (tabla de hash): Tabla de Hash del ADT de Disclib con la info de 
        los aeropuertos registrados
        airport (str): ICAO del aeropuerto del cual se quiere conseguir su info

    Returns:
        dict: Diccionario con información filtrada del aeropuerto ingresado
    """
    airport_dict = me.getValue(mp.get(airports_map, airport))
    airport_info = {"ICAO": airport,
                    "NOMBRE": airport_dict["NOMBRE"],
                    "CIUDAD": airport_dict["CIUDAD"],
                    "PAIS": airport_dict["PAIS"],
                    "coord": airport_dict["coord"]}
    return airport_info

def get_most_count_tree_colombia (database, tree, num):
    """Función similar a 'get_most_count_tree', la cual añade un filtro para solo retornar
    aeropuertos dentro de Colombia
    
    Args:
        database (dict): Base de datos que contiene las estructuras del modelo
        tree (Ordered Map): Árbol binario ordenado sobre el cual se quiere conseguir los valores con 
        mayor conteo
        num (int): Número de aeropuertos que se quieren retornar

    Returns:
        list: Lista nativa de python con los diccionarios de los 'num' aeropuertos con mayor conteo del árbol ingresado
    """

    
    airport_map = database['airports_map']
    max_key = om.maxKey(tree)
    response_lst = []
    
    while len(response_lst)<num:
        count_lst = me.getValue(om.get(tree, max_key))
        count_lst = sort_airport_codes(count_lst)
        i = 1
        while len(response_lst)<num and i < lt.size(count_lst)+1:
            airport_code = lt.getElement(count_lst, i)
            airport = me.getValue(mp.get(airport_map, airport_code))
            if airport["PAIS"] == "Colombia":
                response_lst.append(airport)
            i+=1
        max_key-=1
        max_key= om.floor(tree, max_key)
    return response_lst

def req_7(database, origin, dest):
    """Función que soluciona el requerimiento 7. 
    La función utiliza el algoritmo de Dijkstra para encontrar el camino con el menor tiempo de vuelo entre dos puntos
    turísticos (solo usa vuelos comerciales), primero revisando que dichos puntos estén suficientemente cerca a un aeropuerto registrado
    Tiene una lógica similar a la función que resuelve los requerimientos 1 y 2 (req_1_2), contando con modificaciones
    para manejar adecuadamente el retorno del algoritmo de Dijkstra con respecto al camino entre dos aeropuertos. 

    Args:
        database (dict): Base de datos que contiene las estructuras del modelo
        origin (tuple): Tupla de coordenadas (lat, lon) del origen
        dest (tuple): Tupla de coordenadas (lat, lon) del destino

    Returns:
        tuple: Tupla con la lista de vuelos que se toman en el camino, la distancia y tiempo de vuelo total del camino,
        el número de aeropuertos visitados y la información de los aeropuertos de origen y destino globales. 
        
    """
    #acceder a los grafos pertinentes
    commercial_graph_dist = database["dist_graph_com"]
    commercial_graph_time = database["time_graph_com"]
    #acceder a la tabla de hash con la info de los aeropuertos
    airports_map = database["airports_map"]
    #determinar aeropuertos más cercanos a las coordenadas de origen y destino
    origin_airport, origin_distance = check_coordinates(origin, database)
    destination_airport, dest_distance = check_coordinates(dest, database)
    
    if origin_distance <= 30 and dest_distance <= 30:#hay aeropuertos a menos de 30 km tanto del destino como del origen.
        #inicializar la estructura de búsqueda sobre el grafo con pesos de tiempo
        search_algo = djk
        search_graph_dist = search_algo.Dijkstra(commercial_graph_time, origin_airport)
        path_exists = search_algo.hasPathTo(search_graph_dist, destination_airport)
        if path_exists == True: #hay camino entre origen y destino
            #generar variables y listas para guardar la info
            airports_list = lt.newList()
            total_dist = origin_distance+dest_distance
            total_time = 0
            #generar el camino entre los dos aeropuertos, pila de disclib
            dist_path = search_algo.pathTo(search_graph_dist, destination_airport)
            #usando el tamaño de la pila, dar el total de aeropuertos. 
            total_airports = st.size(dist_path)+1
            origin_airport_full = ""
            destination_airport_full = ""
            
            #recorrer la lista de vuelos
            for edge in lt.iterator(dist_path):
                #declarar aeropuertos de origen y destino
                org_airport = edge["vertexA"]
                dest_airport = edge["vertexB"]
                flight_time = edge["weight"]
                #acceder a la conexión en el grafo de distancia (dijkstra se hace sobre el de tiempo)
                dist_edge = gr.getEdge(commercial_graph_dist, org_airport, dest_airport)
                #determinar distancia entre aeropuertos
                flight_distance = dist_edge["weight"]
                #sumar distancia y tiempo a los globales
                total_time += flight_time
                total_dist+= flight_distance
                #generar el diccionario con la información del vuelo entre aeropuertos.
                airports_info = get_airports_info_req1_2(airports_map, org_airport, dest_airport, flight_distance, flight_time)
                #generar la información para los aeropuertos de origen y destino globales si se cumple que el de origen/destino actual
                #es el de origen/destino global
                if org_airport == origin_airport:
                    origin_airport_full = "{0} ({1})".format(airports_info["NOMBRE ORIGEN"], org_airport)
                if dest_airport == destination_airport:
                    destination_airport_full = "{0} ({1})".format(airports_info["NOMBRE DESTINO"], dest_airport)
                #añadir la información del vuelo a la lista de retorno.
                lt.addFirst(airports_list, airports_info)
                    
            return airports_list, total_dist, total_time, total_airports, origin_airport_full, destination_airport_full     
        else:
            return -2, origin_airport, origin_distance, destination_airport, dest_distance
    else:
        return -1, origin_airport, origin_distance, destination_airport, dest_distance

# Funciones utilizadas para comparar elementos dentro de una lista

def compareCounts(count_1, count_2):
    """
    Compara los dos conteos ingresados
    """
    if (count_1 == count_2):
        return 0
    elif (count_1 > count_2):
        return 1
    else:
        return -1

# Funciones de ordenamiento

sort_algorithm = merg
def sort_by_airport_codes(code_1, code_2):
    """sortCriteria criterio de ordenamiento para sort_airport_codes

    Args:
        code_1
        code_2

    Returns:
        type: bool
    """
    return code_1<code_2

def alphabetic_comparison(word1, word2):
    """sortCriteria criterio de ordenamiento para alphabetic_sort

    Args:
        word1
        word2

    Returns:
        type: bool
    """
    return word1 < word2


def sort_airport_codes(codes_lst):
    """
    Función encargada de ordenar la lista con los datos
    """
    ordered_lst = sort_algorithm.sort(codes_lst, sort_by_airport_codes)
    return ordered_lst

def alphabetic_sort(lst):
    """Función encargada de ordenar una lista de cadenas, alfabéticamente."""
    ordered_lst =  sort_algorithm.sort(lst, alphabetic_comparison)
    return ordered_lst
