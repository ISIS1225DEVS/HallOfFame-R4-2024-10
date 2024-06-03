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
import math
import folium
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

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Algoritmos de ordenamiento, por defecto se ha seleccionado Merge Sort
sort_algorithm = merg

# Construccion de modelos

def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    analyzer = {
        'airports': None,
        'best_airports': None,
        'commercial': None,
        'merchandise': None,
        'military': None
    }

    # Tabla de hash para almacenar los aeropuertos
    analyzer['airports'] = mp.newMap(numelements=430,
                                     maptype='CHAINING',
                                     loadfactor=5)
    # Árbol que contiene los mejores aeropuertos según el tipo de vuelo
    analyzer['best_airports'] = om.newMap(omaptype='RBT',
                                          cmpfunction=compareTreeKeys)
    # Grafo que contiene los vuelos comerciales
    analyzer['commercial'] = gr.newGraph(datastructure='ADJ_LIST',
                                      directed=True,
                                      size=100,
                                      cmpfunction=compareGraphKeys)
    # Grafo que contiene los vuelos de carga
    analyzer['merchandise'] = gr.newGraph(datastructure='ADJ_LIST',
                                      directed=True,
                                      size=100,
                                      cmpfunction=compareGraphKeys)
    # Grafo que contiene los vuelos militares
    analyzer['military'] = gr.newGraph(datastructure='ADJ_LIST',
                                      directed=True,
                                      size=100,
                                      cmpfunction=compareGraphKeys)
    
    return analyzer
    

# Funciones para agregar informacion al modelo

def add_map(analyzer, data_structure, key, data):
    """
    Función para agregar nuevos elementos al mapa
    """
    data_structure.put(analyzer, key, data)

def add_vertex(analyzer, data):
    """
    Función para agregar nuevos vertices al grafo
    """
    if not gr.containsVertex(analyzer, data):
        gr.insertVertex(analyzer, data)

def add_edge(analyzer, origin, destination, weight):
    """
    Adiciona un arco entre dos aeropuertos
    """
    gr.addEdge(analyzer, origin, destination, weight)


# Funciones para creacion de datos

def new_airport(analyzer, data):
    """
    Crea una nueva estructura para modelar los datos
    """
    data['LATITUD'] = data['LATITUD'].replace(',', '.')
    data['LONGITUD'] = data['LONGITUD'].replace(',', '.')
    data['ALTITUD'] = data['ALTITUD'].replace(',', '.')

    add_map(analyzer['airports'], mp, data['ICAO'], data)

def new_flight(analyzer, type, data, weight):
    """
    Crea una nueva estructura para modelar los datos
    """
    # Obtener el aeropuerto de origen de la tabla de hash
    origin_airport = me.getValue(get_entry(analyzer['airports'], mp, data['ORIGEN']))
    # Obtener el aeropuerto de destino de la tabla de hash
    destination_airport = me.getValue(get_entry(analyzer['airports'], mp, data['DESTINO']))

    if type == 'AVIACION_COMERCIAL':
        flights = analyzer['commercial']

    elif type == 'AVIACION_CARGA':
        flights = analyzer['merchandise']

    else:
        flights = analyzer['military']

    # Añadir los vertices correspondientes a los aeropuertos
    add_vertex(flights, origin_airport['ICAO'])
    add_vertex(flights, destination_airport['ICAO'])

    if weight == 'time':
        weight = int(data['TIEMPO_VUELO'])
    else:
        weight = haversine(origin_airport, destination_airport)
    # Añadir arco entre los dos aeropuertos
    add_edge(flights, origin_airport['ICAO'], destination_airport['ICAO'], weight)


# Funciones de consulta

def get_data(analyzer, id):
    """
    Retorna un dato por su ID.
    """
    return lt.getElement(analyzer, id)

def get_entry(analyzer, data_structure, key):
    """
    Retorna una entrada a partir de su llave
    """
    return data_structure.get(analyzer, key)

def get_sublist(catalog, pos, numelem):
    """
    Retorna una sublista de una lista dada.
    """
    return lt.subList(catalog, pos, numelem)

def data_size(analyzer, data_structure):
    """
    Retorna el tamaño de la lista de datos.
    """
    return data_structure.size(analyzer)

def totalFlights(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer)


# Funciones de requerimientos

def req_1(analyzer, origin, destination, map):
    """
    Función que soluciona el requerimiento 1
    """
    commercial = analyzer["commercial"]
    airports = analyzer["airports"]
    best_airports = me.getValue(get_entry(analyzer['best_airports'], om, 'commercial'))
    origin_airport = None, 100000
    destination_airport = None, 100000

    for airport in lt.iterator(best_airports):
        # Hallar el aeropuerto mas cercano a las coordenadas
        distance = haversine(airport, origin)
        if distance < origin_airport[1]:
            origin_airport = airport, distance

        distance = haversine(airport, destination)
        if distance < destination_airport[1]:
            destination_airport = airport, distance

    if origin_airport[1] > 30 or destination_airport[1] > 30:
        return (origin_airport[1], destination_airport[1]), (origin_airport[0], destination_airport[0]), None
        
    estructura = djk.Dijkstra(commercial,origin_airport[0]["ICAO"])
    path = djk.pathTo(estructura,destination_airport[0]["ICAO"])

    # Verificar si hay un camino entre los dos aeropuertos
    if not djk.hasPathTo(estructura, destination_airport[0]['ICAO']):
        return None, (origin_airport[0], destination_airport[0]), None
    else:
        # Hallar el camino hasta el aeropuerto
        path = djk.pathTo(estructura, destination_airport[0]['ICAO'])
    
    flights_queue = qu.newQueue()
    total_distance = origin_airport[1] + destination_airport[1]
    total_time = djk.distTo(estructura, destination_airport[0]['ICAO'])
    total_airports = data_size(path, st) + 1

    # Ejecucion del requerimiento 8
    req_8_lst = lt.newList()
    lt.addLast(req_8_lst, origin_airport[0])
    lt.addLast(req_8_lst, destination_airport[0])

    while not st.isEmpty(path):
        flight = st.pop(path)

        airport_1 = me.getValue(get_entry(airports, mp, flight['vertexA']))
        airport_2 = me.getValue(get_entry(airports, mp, flight['vertexB']))
        # Sumar la distancia del trayecto a la suma total de distancias
        total_distance += haversine(airport_1, airport_2)

        # Agregar aeropuerto intermedio a la cola
        if airport_1['ICAO'] != origin_airport[0]['ICAO']:
            qu.enqueue(flights_queue, airport_1)

    # Ejecucion del requerimiento 8
    if map:
        req_8(req_8_lst)

    return flights_queue,(origin_airport[0],destination_airport[0]),(total_distance,total_airports,total_time)

def req_2(analyzer, origin, destination, map):
    """
    Función que soluciona el requerimiento 7
    """
    # Tabla de hash de aeropuertos
    airports = analyzer['airports']
    # Grafo de vuelos comerciales
    commercial = analyzer['commercial']
    # Lista de aeropuertos con mayor concurrecia comercial
    best_airports = me.getValue(get_entry(analyzer['best_airports'], om, 'commercial'))

    # Establecer aeropuertos de origen y destino
    origin_airport = None, 1000
    destination_airport = None, 100000

    for airport in lt.iterator(best_airports):
        distance = haversine(airport, origin)
        if distance < origin_airport[1]:
            origin_airport = airport, distance

        distance = haversine(airport, destination)
        if distance < destination_airport[1]:
            destination_airport = airport, distance

    if origin_airport[1] > 30 or destination_airport[1] > 30:
        return (origin_airport[1], destination_airport[1]), (origin_airport[0], destination_airport[0]), None

    searching_structure = bfs.BreathFirstSearch(commercial, origin_airport[0]['ICAO'])

    if not bfs.hasPathTo(searching_structure, destination_airport[0]['ICAO']):
        print("No hay ruta entre los aeropuertos")
        return None, (origin_airport[0], destination_airport[0]), None
    else:
        path = bfs.pathTo(searching_structure, destination_airport[0]['ICAO'])
        

    total_distance = origin_airport[1] + destination_airport[1]
    total_airports = data_size(path, st) 
    flights_queue = qu.newQueue()

    req_8_lst = lt.newList()
    lt.addLast(req_8_lst, origin_airport[0])
    lt.addLast(req_8_lst, destination_airport[0])

    i = lt.size(path)
    
    
    while i>1:
        vertexA = lt.getElement(path, i)
        vertexB = lt.getElement(path, i-1)
        

        airport_1 = me.getValue(get_entry(airports, mp, vertexA))
        airport_2 = me.getValue(get_entry(airports, mp, vertexB))

        total_distance += haversine(airport_1, airport_2)
        
        if airport_1['ICAO'] != origin_airport[0]['ICAO']:
            qu.enqueue(flights_queue, airport_1)
            lt.addLast(req_8_lst, airport_1)

        i -= 1

    if map:
        req_8(req_8_lst)

    return flights_queue, (origin_airport[0], destination_airport[0]), (total_distance, total_airports)


def req_3(analyzer, map):
    """
    Función que soluciona el requerimiento 3
    """
    # Tabla de hash de aeropuertos
    airports = analyzer['airports']
    # Lista de aeropuertos con mayor concurrecia comercial
    best_airports = analyzer['best_airports']
    # Grafo de vuelos comerciales
    commercial = analyzer['commercial']

    important_arirport = lt.firstElement(me.getValue(get_entry(best_airports, mp, 'commercial')))
    commercial_coverage = djk.Dijkstra(commercial, important_arirport['ICAO'])

    flights = lt.newList()
    total_distance = 0

    # Ejecucion del requerimiento 8
    req_8_lst = lt.newList()
    lt.addLast(req_8_lst, important_arirport)

    for airport in lt.iterator(mp.keySet(prim.PrimMST(commercial, important_arirport['ICAO'])['edgeTo'])):

        if djk.hasPathTo(commercial_coverage, airport):
            # Ejecucion del requerimiento 8
            lt.addLast(req_8_lst, me.getValue(get_entry(airports, mp, airport)))

            # Hallar camino
            path = djk.pathTo(commercial_coverage, airport)
            distance = djk.distTo(commercial_coverage, airport)

            flights_queue = qu.newQueue()

            while not st.isEmpty(path):
                flight = st.pop(path)
                # Sumar la distancia del trayecto a la suma total de distancias
                total_distance += distance

                # Crear estructura para modelar los datos
                flight_structure = {
                    'ORIGEN': me.getValue(get_entry(airports, mp, flight['vertexA'])),
                    'DESTINO': me.getValue(get_entry(airports, mp, flight['vertexB'])),
                    'DISTANCIA': distance
                }
                qu.enqueue(flights_queue, flight_structure)

            lt.addLast(flights, flights_queue)

    total_flights = data_size(flights, lt)

    # Ejecucion del requerimiento 8
    if map:
        req_8(req_8_lst)

    return flights, important_arirport, (total_flights, total_distance)


def req_4(analyzer, map):
    """
    Función que soluciona el requerimiento 4
    """
    airports = analyzer["airports"]
    best_airports = analyzer["best_airports"]
    carga = analyzer["merchandise"]

    important_arirport = lt.firstElement(me.getValue(get_entry(best_airports, mp, 'merchandise')))
    merchandise_coverage = djk.Dijkstra(carga, important_arirport['ICAO'])

    flights = lt.newList()
    total_distance = 0

    # Ejecucion del requerimiento 8
    req_8_lst = lt.newList()
    lt.addLast(req_8_lst, important_arirport)

    for airport in lt.iterator(mp.keySet(prim.PrimMST(carga, important_arirport['ICAO'])['edgeTo'])):

        if djk.hasPathTo(merchandise_coverage, airport):
            # Ejecucion del requerimiento 8
            lt.addLast(req_8_lst, me.getValue(get_entry(airports, mp, airport)))

            # Hallar camino
            path = djk.pathTo(merchandise_coverage, airport)
            distance = djk.distTo(merchandise_coverage, airport)

            flights_queue = qu.newQueue()

            while not st.isEmpty(path):
                flight = st.pop(path)
                # Sumar la distancia del trayecto a la suma total de distancias
                total_distance += distance

                # Crear estructura para modelar los datos
                flight_structure = {
                    'ORIGEN': me.getValue(get_entry(airports, mp, flight['vertexA'])),
                    'DESTINO': me.getValue(get_entry(airports, mp, flight['vertexB'])),
                    'DISTANCIA': distance
                }
                qu.enqueue(flights_queue, flight_structure)

            lt.addLast(flights, flights_queue)

    total_flights = data_size(flights, lt)

    # Ejecucion del requerimiento 8
    if map:
        req_8(req_8_lst)

    return flights, important_arirport, total_flights, total_distance



def req_5(analyzer, map):
    """
    Función que soluciona el requerimiento 5
    """
        # Tabla de hash de aeropuertos
    airports = analyzer['airports']
    # Lista de aeropuertos con mayor concurrecia comercial
    best_airports = analyzer['best_airports']
    # Grafo de vuelos comerciales
    military = analyzer['military']

    important_arirport = lt.firstElement(me.getValue(get_entry(best_airports, mp, 'military')))
    military_coverage = djk.Dijkstra(military, important_arirport['ICAO'])

    flights = lt.newList()
    total_distance = 0

    # Ejecucion del requerimiento 8
    req_8_lst = lt.newList()
    lt.addLast(req_8_lst, important_arirport)

    for airport in lt.iterator(mp.keySet(prim.PrimMST(military, important_arirport['ICAO'])['edgeTo'])):

        if djk.hasPathTo(military_coverage, airport):
            # Ejecucion del requerimiento 8
            lt.addLast(req_8_lst, me.getValue(get_entry(airports, mp, airport)))

            # Hallar camino
            path = djk.pathTo(military_coverage, airport)
            distance = djk.distTo(military_coverage, airport)

            flights_queue = qu.newQueue()

            while not st.isEmpty(path):
                flight = st.pop(path)
                # Sumar la distancia del trayecto a la suma total de distancias
                total_distance += distance

                # Crear estructura para modelar los datos
                flight_structure = {
                    'ORIGEN': me.getValue(get_entry(airports, mp, flight['vertexA'])),
                    'DESTINO': me.getValue(get_entry(airports, mp, flight['vertexB'])),
                    'DISTANCIA': distance
                    
                }
                qu.enqueue(flights_queue, flight_structure)

            lt.addLast(flights, flights_queue)

    total_flights = data_size(flights, lt)

    # Ejecucion del requerimiento 8
    if map:
        req_8(req_8_lst)

    return flights, important_arirport, (total_flights, total_distance)


def req_6(analyzer, num_airports, map):
    """
    Función que soluciona el requerimiento 6
    """
    # Tabla de hash de aeropuertos
    airports = analyzer['airports']
    # Lista de aeropuertos con mayor concurrecia comercial
    best_airports = me.getValue(get_entry(analyzer['best_airports'], om, 'commercial'))

    colombian_airports = lt.newList()
    answer = lt.newList()

    for airport in lt.iterator(best_airports):
        # Encontrar los aeropuertos colombianos
        if airport['PAIS'].upper() == 'COLOMBIA':
            lt.addLast(colombian_airports, airport)

    # Extraer el aeropuerto con mayor concurrencia
    important_airport = lt.removeFirst(colombian_airports)
    # Verificar que la lista sea menor o igual al tamaño recibido por parametro
    if data_size(colombian_airports, lt) > num_airports:    
        colombian_airports = get_sublist(colombian_airports, 1, num_airports)

    # Calcular los caminos de costo mínimo
    military_coverage = djk.Dijkstra(analyzer['military'], important_airport['ICAO'])

    # Recorrer los n aeropuertos que se desean cubrir
    for airport in lt.iterator(colombian_airports):
        # Hallar el camino hasta el aeropuerto
        path = djk.pathTo(military_coverage, airport['ICAO'])

        airports_queue = qu.newQueue()
        flights_queue = qu.newQueue()

        if path is None:
            lt.addLast(answer, { 'DISTANCE': 0 })
            
        else:
            while not st.isEmpty(path):
                flight = st.pop(path)

                # Obtener los datos del aeropuerto ubicado en el vertice A
                airport_structure = me.getValue(get_entry(airports, mp, flight['vertexA']))
                qu.enqueue(airports_queue, airport_structure)

                # Crear estructura para modelar los datos
                flight_structure = {
                    'ORIGEN': flight['vertexA'],
                    'DESTINO': flight['vertexB']
                }
                qu.enqueue(flights_queue, flight_structure)

            # Crear estructura para modelar los datos
            airport_coverage = {
                'AIRPORTS': airports_queue,
                'FLIGHTS': flights_queue,
                'DISTANCE': djk.distTo(military_coverage, airport['ICAO'])
            }
            lt.addLast(answer, airport_coverage)

    # Volver a añadir el aeropuerto con mayor concurrencia a la lista
    lt.addFirst(colombian_airports, important_airport)

    # Ejecucion del requerimiento 8
    if map:
        req_8(colombian_airports)

    return answer, colombian_airports


def req_7(analyzer, origin, destination, map):
    """
    Función que soluciona el requerimiento 7
    """
    # Tabla de hash de aeropuertos
    airports = analyzer['airports']
    # Grafo de vuelos comerciales
    commercial = analyzer['commercial']
    # Lista de aeropuertos con mayor concurrecia comercial
    best_airports = me.getValue(get_entry(analyzer['best_airports'], om, 'commercial'))

    # Establecer aeropuertos de origen y destino
    origin_airport = None, 100000
    destination_airport = None, 100000

    for airport in lt.iterator(best_airports):
        # Hallar el aeropuerto mas cercano a las coordenadas
        distance = haversine(airport, origin)
        if distance < origin_airport[1]:
            origin_airport = airport, distance

        distance = haversine(airport, destination)
        if distance < destination_airport[1]:
            destination_airport = airport, distance

    # Si no hay un aeropuerto menor a los 30 Km, no se ejecuta la busqueda
    if origin_airport[1] > 30 or destination_airport[1] > 30:
        return (origin_airport[1], destination_airport[1]), (origin_airport[0], destination_airport[0]), None

    searching_structure = djk.Dijkstra(commercial, origin_airport[0]['ICAO'])

    # Verificar si hay un camino entre los dos aeropuertos
    if not djk.hasPathTo(searching_structure, destination_airport[0]['ICAO']):
        return None, (origin_airport[0], destination_airport[0]), None
    else:
        # Hallar el camino hasta el aeropuerto
        path = djk.pathTo(searching_structure, destination_airport[0]['ICAO'])

    # Iniciar variables para guardar los datos que pide el requerimiento
    total_distance = origin_airport[1] + destination_airport[1]
    total_time = djk.distTo(searching_structure, destination_airport[0]['ICAO'])
    total_airports = data_size(path, st) + 1
    flights_queue = qu.newQueue()

    # Ejecucion del requerimiento 8
    req_8_lst = lt.newList()
    lt.addLast(req_8_lst, origin_airport[0])
    lt.addLast(req_8_lst, destination_airport[0])

    while not st.isEmpty(path):
        flight = st.pop(path)

        airport_1 = me.getValue(get_entry(airports, mp, flight['vertexA']))
        airport_2 = me.getValue(get_entry(airports, mp, flight['vertexB']))
        # Sumar la distancia del trayecto a la suma total de distancias
        total_distance += haversine(airport_1, airport_2)

        # Agregar aeropuerto intermedio a la cola
        if airport_1['ICAO'] != origin_airport[0]['ICAO']:
            qu.enqueue(flights_queue, airport_1)
            lt.addLast(req_8_lst, airport_1)

    # Ejecucion del requerimiento 8
    if map:
        req_8(req_8_lst)

    return flights_queue, (origin_airport[0], destination_airport[0]), (total_time, total_distance, total_airports)


def req_8(airports):
    """
    Función que soluciona el requerimiento 8
    """
    # Crear mapa
    map = folium.Map()

    for airport in lt.iterator(airports):
        # Obtener las coordenadas como una tupla (latitud, longitud)
        coordenates = (airport["LATITUD"],airport["LONGITUD"])
        # Mensaje que se mostrara al hacer click sobre un marcador
        message = airport["NOMBRE"] + ' - ' + airport['ICAO']

        # Añadir marcador al mapa
        folium.Marker(location=coordenates,
                      tooltip=airport['CIUDAD'],
                      popup=message).add_to(map)
        
    # Guardar mapa para poder visualizarlo
    map.save("mapa_req_8.html")


# Funciones de comparación

def compareGraphKeys(key_1, entry):
    """
    Compara dos llaves
    """
    key_2 = entry['key']
    if (key_1 == key_2):
        return 0
    elif (key_1 > key_2):
        return 1
    else:
        return -1
    
def compareTreeKeys(key_1, key_2):
    """
    Función encargada de comparar dos llaves
    """
    if (key_1 == key_2):
        return 0
    elif (key_1 > key_2):
        return 1
    else:
        return -1


# Funciones de ordenamiento

def sort_airports(airport_1, airport_2):
    """
    Función encargada de comparar la cantidad de vuelos de dos aeropuertos
    """
    if airport_1['CONCURRENCIA'] > airport_2['CONCURRENCIA']:
        return True
    elif airport_1['CONCURRENCIA'] == airport_2['CONCURRENCIA']:
        if airport_1['ICAO'] < airport_2['ICAO']:
            return True
    else:
        return False

def select_sort_algorithm(algorithm):
    """
    Permite seleccionar el algoritmo de ordenamiento.

    Args:
        algorithm (int): opcion de algoritmo de ordenamiento, las opciones son:
            1: Selection Sort
            2: Insertion Sort
            3: Shell Sort
            4: Merge Sort
            5: Quick Sort

    Returns:
        list: sort_algorithm (sort) la instancia del ordenamiento y
        msg (str) el texto que describe la configuracion del ordenamiento
    """
    sort_algorithm = None
    msg = None

    # opcion 1: Selection Sort
    if algorithm == 1:
        sort_algorithm = se
        msg = "Selection Sort"
    
    # opcion 2: Insertion Sort
    elif algorithm == 2:
        sort_algorithm = ins
        msg = "Insertion Sort"

    # opcion 3: Shell Sort
    elif algorithm == 3: 
        sort_algorithm = sa
        msg = "Shell Sort"

    # opcion 4: Merge Sort
    elif algorithm == 4:
        sort_algorithm = merg
        msg = "Merge Sort"

    # opcion 5: Quick Sort
    elif algorithm == 5:
        sort_algorithm = quk
        msg = "Quick Sort"

    return sort_algorithm, msg

def sort(analyzer, sort_criteria):
    """
    Función encargada de ordenar la lista con los datos
    """
    sorted_analyzer = sort_algorithm.sort(analyzer, sort_criteria)
    analyzer = sorted_analyzer

    return analyzer


# Funciones adicionales

def haversine(airport_1, airport_2):
    # Convertir grados a radianes
    latitude_1 = math.radians(float(airport_1['LATITUD']))
    longitude_1 = math.radians(float(airport_1['LONGITUD']))

    latitude_2 = math.radians(float(airport_2['LATITUD']))
    longitude_2 = math.radians(float(airport_2['LONGITUD']))

    # Diferencia en latitud y longitud
    delta_lat = latitude_2 - latitude_1
    delta_lon = longitude_2 - longitude_1

    # Aplicar la fórmula haversine
    a = math.sin(delta_lat / 2)**2 + math.cos(latitude_1) * math.cos(latitude_2) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    # Multiplicar por el radio de la Tierra en kilómetros
    distance = 6371.0 * c

    return distance

def airport_flights(analyzer, type):
    """
    Retorna el número de vuelos que salen y llegan de un aeropuerto
    """
    # Obtener los codigos de los aeropuertos
    ICAO_codes = gr.vertices(analyzer[type])
    # Inicializar la lista para ordenar los aeropuertos
    airports_lst = lt.newList('ARRAY_LIST')

    for ICAO in lt.iterator(ICAO_codes):
        # Obtener el diccionario con los datos del aeropuerto
        airport = me.getValue(get_entry(analyzer['airports'], mp, ICAO))
        # Crear estructura para modelar los datos
        airport_flights = {
            'NOMBRE': airport['NOMBRE'],
            'CIUDAD': airport['CIUDAD'],
            'PAIS': airport['PAIS'],
            'ICAO': airport['ICAO'],
            'LATITUD': airport['LATITUD'],
            'LONGITUD': airport['LONGITUD'],
            'ALTITUD': airport['ALTITUD']
        }
        # Agregar la concurrencia (grado) del aeropuerto (vertice)
        airport_flights['CONCURRENCIA'] = gr.indegree(analyzer[type], ICAO) + gr.outdegree(analyzer[type], ICAO)
        # Añadir a la lista de mejores aeropuertos
        lt.addLast(airports_lst, airport_flights)

    # Ordenar los aeropuertos, de mayor a menor, por la concurrencia
    sort(airports_lst, sort_airports)
    # Agregar al árbol "best_airports"
    add_map(analyzer['best_airports'], om, type, airports_lst)