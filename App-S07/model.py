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
from datetime import datetime as dt
import time
from datetime import timezone
from DISClib.Utils import error as error
from math import radians, cos, sin, asin, sqrt
#import bridge as brie ##! Maricada de grafos visuales



"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def newCatalog():
    """ Inicia el catalogo
    flights: Lista con todos los aeropuertos
    map_flights: Hash Map para guardar la información de cada uno de los vuelos
    map_airports: Hash Map para guardar la información de cada uno de los aeropuertos
    graph_distance: Grafo para representar las rutas con costo de distancia entre aeropuertos
    graph_time: Grafo para representar las rutas con costo de tiempo entre aeropuertos
    graph_escalas: Grafo para representar las rutas con costo 1 entre aeropuertos
    map_type: Hash Map (llave: tipo vuelo, valor: un graph_escalas, graph_time y un graph_distance)
    airport_conc: Hash Map (llave: aeropuerto, valor: cantidad de vuelos entrantes y salientes de ese aeropuerto)
    concurrencia_airp: Ordered Map (llave: cantidad de vuelos entrantes y salientes de los determiandos aeropuertos, 
        valor: lista de aeropuertos que cumplen la cantidad)
    """
    catalog={
        "flights":None,
        "map_flights":None,
        "map_airports":None,
        "graph_distance":None,
        "graph_time":None,
        "graph_escalas":None,
        "map_types":None,
        "airport_conc":None,
        "concurrencia_airp":None
    }
    
    catalog["flights"] = lt.newList("ARRAY_LIST")
    catalog["map_flights"] = mp.newMap(numelements=200,
                                     maptype="PROBING",
                                     loadfactor=0.5
                                     )
    catalog["map_airports"] = mp.newMap(numelements=1500,
                                     maptype="PROBING",
                                     loadfactor=0.5
                                     )
    catalog["graph_distance"] = gr.newGraph(datastructure="ADJ_LIST",
                                            directed=True,
                                            size=500,
                                            cmpfunction=compareAirportIds
                                            )
    catalog["graph_time"] = gr.newGraph(datastructure="ADJ_LIST",
                                        directed=True,
                                        size=500,
                                        cmpfunction=compareAirportIds
                                        )
    catalog["graph_escalas"] = gr.newGraph(datastructure="ADJ_LIST",
                                        directed=True,
                                        size=500,
                                        cmpfunction=compareAirportIds
                                        )
    catalog["map_types"] = mp.newMap(numelements=3,
                                     maptype="PROBING",
                                     loadfactor=0.5
                                     )
    catalog["airport_conc"] = mp.newMap(numelements=220,
                                       maptype="PROBING",
                                       loadfactor=0.5)
    catalog["concurrencia_airp"] = om.newMap(omaptype="RBT")
    
    return catalog

#########################################
# Funciones para agregar informacion al modelo  
#########################################

def templist(filename):
    """
    Creación de una lista temporal
    """
    temporallist = lt.newList(datastructure="ARRAY_LIST",filename=filename, delimiter=";")
    return temporallist

def createkeysmaptypes(catalog):
    mapa = catalog["map_types"]
    ##* Hash Map por tipo de vuelo
    estructura = {
        "graph_distance":None,
        "graph_time":None,
        "graph_escalas":None,
        "airport_conc":None,
        "concurrencia_airp":None
    }
    estructura["graph_distance"] = gr.newGraph(datastructure="ADJ_LIST",
                                        directed=True,
                                        size=500,
                                        cmpfunction=compareAirportIds
                                        )
    estructura["graph_time"] = gr.newGraph(datastructure="ADJ_LIST",
                                        directed=True,
                                        size=500,
                                        cmpfunction=compareAirportIds
                                        )
    estructura["graph_escalas"] = gr.newGraph(datastructure="ADJ_LIST",
                                        directed=True,
                                        size=500,
                                        cmpfunction=compareAirportIds
                                        )
    estructura["airport_conc"] = mp.newMap(numelements=220,
                                       maptype="PROBING",
                                       loadfactor=0.5)
    estructura["concurrencia_airp"] = om.newMap(omaptype="RBT")
    estructura1 = {
        "graph_distance":None,
        "graph_time":None,
        "graph_escalas":None,
        "airport_conc":None,
        "concurrencia_airp":None
    }
    estructura1["graph_distance"] = gr.newGraph(datastructure="ADJ_LIST",
                                        directed=True,
                                        size=500,
                                        cmpfunction=compareAirportIds
                                        )
    estructura1["graph_time"] = gr.newGraph(datastructure="ADJ_LIST",
                                        directed=True,
                                        size=500,
                                        cmpfunction=compareAirportIds
                                        )
    estructura1["graph_escalas"] = gr.newGraph(datastructure="ADJ_LIST",
                                        directed=True,
                                        size=500,
                                        cmpfunction=compareAirportIds
                                        )
    estructura1["airport_conc"] = mp.newMap(numelements=220,
                                       maptype="PROBING",
                                       loadfactor=0.5)
    estructura1["concurrencia_airp"] = om.newMap(omaptype="RBT")
    estructura2 = {
        "graph_distance":None,
        "graph_time":None,
        "graph_escalas":None,
        "airport_conc":None,
        "concurrencia_airp":None
    }
    estructura2["graph_distance"] = gr.newGraph(datastructure="ADJ_LIST",
                                        directed=True,
                                        size=500,
                                        cmpfunction=compareAirportIds
                                        )
    estructura2["graph_time"] = gr.newGraph(datastructure="ADJ_LIST",
                                        directed=True,
                                        size=500,
                                        cmpfunction=compareAirportIds
                                        )
    estructura2["graph_escalas"] = gr.newGraph(datastructure="ADJ_LIST",
                                        directed=True,
                                        size=500,
                                        cmpfunction=compareAirportIds
                                        )
    estructura2["airport_conc"] = mp.newMap(numelements=220,
                                       maptype="PROBING",
                                       loadfactor=0.5)
    estructura2["concurrencia_airp"] = om.newMap(omaptype="RBT")
    #* Meter los grafos para todos los tipos de vuelo (See if Trouble)
    mp.put(mapa,"AVIACION_CARGA",estructura)
    mp.put(mapa,"AVIACION_COMERCIAL",estructura1)
    mp.put(mapa,"MILITAR",estructura2)

def add_nodes(catalog, airports_list):
    """
    Adiciona un aeropuerto como un vertice de los grafos
    """
    for value in lt.iterator(airports_list):
        airport = value["ICAO"]
        if not gr.containsVertex(catalog['graph_distance'], airport):
            gr.insertVertex(catalog['graph_distance'], airport)
        if not gr.containsVertex(catalog['graph_time'], airport):
            gr.insertVertex(catalog['graph_time'], airport)
        if not gr.containsVertex(catalog['graph_escalas'], airport):
            gr.insertVertex(catalog['graph_escalas'], airport)
        entrycarga = mp.get(catalog["map_types"],"AVIACION_CARGA")
        valuecarga = me.getValue(entrycarga)
        if not gr.containsVertex(valuecarga["graph_distance"], airport):
            gr.insertVertex(valuecarga["graph_distance"], airport)
        if not gr.containsVertex(valuecarga["graph_time"], airport):
            gr.insertVertex(valuecarga["graph_time"], airport)
        if not gr.containsVertex(valuecarga["graph_escalas"], airport):
            gr.insertVertex(valuecarga["graph_escalas"], airport)
        entrycomercial = mp.get(catalog["map_types"],"AVIACION_COMERCIAL")
        valuecomercial = me.getValue(entrycomercial)
        if not gr.containsVertex(valuecomercial["graph_distance"], airport):
            gr.insertVertex(valuecomercial["graph_distance"], airport)
        if not gr.containsVertex(valuecomercial["graph_time"], airport):
            gr.insertVertex(valuecomercial["graph_time"], airport)
        if not gr.containsVertex(valuecomercial["graph_escalas"], airport):
            gr.insertVertex(valuecomercial["graph_escalas"], airport)
        entrymilitar = mp.get(catalog["map_types"],"MILITAR")
        valuemilitar = me.getValue(entrymilitar)
        if not gr.containsVertex(valuemilitar["graph_distance"], airport):
            gr.insertVertex(valuemilitar["graph_distance"], airport)
        if not gr.containsVertex(valuemilitar["graph_time"], airport):
            gr.insertVertex(valuemilitar["graph_time"], airport)
        if not gr.containsVertex(valuemilitar["graph_escalas"], airport):
            gr.insertVertex(valuemilitar["graph_escalas"], airport)
            
        mp.put(catalog["map_airports"],airport,value)


    return catalog


def add_edges_distance(catalog, flights_list):
    ##* Para el grafo de nivel 1
    distanceGraph = catalog['graph_distance']
    
    ##* -------------Generales--------------
    airportsMap = catalog['map_airports']
    mapTypes = catalog['map_types'] ## Acceder a el HM con los tipos#
    # ---------------------------------------
    
    ##* Para los grafos de nivel 3 (por tipo: CARGA)
    cargoType = me.getValue(mp.get(mapTypes, 'AVIACION_CARGA')) # hay: 'AVIACION_CARGA', 'MILITAR', 'AVIACION_COMERCIAL'
    cargodistanceGraph = cargoType['graph_distance'] # Sacar el valor, el valor es un dic {'graph_distance', 'graph_time', 'graph_escalas'}
    ##* Para los grafos de nivel 3 (por tipo: MILITAR)
    militarType = me.getValue(mp.get(mapTypes, 'MILITAR')) # hay: 'AVIACION_CARGA', 'MILITAR', 'AVIACION_COMERCIAL'
    militardistanceGraph = militarType['graph_distance'] # Sacar el valor, el valor es un dic {'graph_distance', 'graph_time', 'graph_escalas'}
    ##* Para los grafos de nivel 3 (por tipo: AVIACION_COMERCIAL)
    commType = me.getValue(mp.get(mapTypes, 'AVIACION_COMERCIAL')) # hay: 'AVIACION_CARGA', 'MILITAR', 'AVIACION_COMERCIAL'
    comercialdistanceGraph = commType['graph_distance'] # Sacar el valor, el valor es un dic {'graph_distance', 'graph_time', 'graph_escalas'}
     
    for value in lt.iterator(flights_list): 
        #* Para el grafo de nivel 1
        origen = value['ORIGEN']
        origenValue = me.getValue(mp.get(airportsMap, origen))
        origenLat = origenValue['LATITUD']
        origenLong = origenValue['LONGITUD']
        origenPoint = (origenLat, origenLong)
        destino = value['DESTINO']
        destinoValue = me.getValue(mp.get(airportsMap, destino))
        destinoLat = destinoValue['LATITUD']
        destinoLong = destinoValue['LONGITUD']
        destinoPoint = (destinoLat, destinoLong)
        distance = HaversineDistance(origenPoint, destinoPoint)
        gr.addEdge(distanceGraph, origen, destino, distance)
        
        #! MUxx para segregar por vuelos
        valueType = value['TIPO_VUELO']  # hay: 'AVIACION_CARGA', 'MILITAR', 'AVIACION_COMERCIAL'
        if valueType == 'AVIACION_CARGA':
            # Pegelo
            gr.addEdge(cargodistanceGraph, origen, destino, distance)
        elif valueType == 'MILITAR':
            # Pegelo
            gr.addEdge(militardistanceGraph, origen, destino, distance)
        elif valueType == 'AVIACION_COMERCIAL':
            # Pegelo
            gr.addEdge(comercialdistanceGraph, origen, destino, distance)
    
    #! Tempo / Quitar
    #brie.makeGraphFile(distanceGraph, "mainDistanceGraph.html", True)
    #brie.makeGraphFile(cargodistanceGraph, "cargoDistanceGraph.html", True)
    #brie.makeGraphFile(militardistanceGraph, "militarDistanceGraph.html", True)
    #brie.makeGraphFile(comercialdistanceGraph, "commercialDistanceGraph.html", True)

    return catalog

def add_edges_time_y_escalas(catalog, flights_list):
    for value in lt.iterator(flights_list):
        origin = value["ORIGEN"]
        destination = value["DESTINO"]
        #parte time
        add_edges_time(catalog, value)
        #parte escalas
        add_edges_escalas(catalog, value)
        #parte HashMap vuelos
        flight = origin + "-" + destination
        mp.put(catalog["map_flights"],flight,value)
    #brie.makeGraphFile(valuemilitar["graph_time"], "timeMilitarGraph.html", True)
    return catalog

def add_edges_time(catalog, value):
    mapatipo =catalog["map_types"]
    origin = value["ORIGEN"]
    destination = value["DESTINO"]
    cost = int(value["TIEMPO_VUELO"])
    addRoutes(catalog["graph_time"],origin,destination,cost)
    if value["TIPO_VUELO"] == "AVIACION_CARGA":
        entrycarga = mp.get(mapatipo,"AVIACION_CARGA")
        valuecarga = me.getValue(entrycarga)
        addRoutes(valuecarga["graph_time"],origin,destination,cost)
    elif value["TIPO_VUELO"] == "AVIACION_COMERCIAL":
        entrycomercial = mp.get(mapatipo,"AVIACION_COMERCIAL")
        valuecomercial = me.getValue(entrycomercial)
        addRoutes(valuecomercial["graph_time"],origin,destination,cost)
    elif value["TIPO_VUELO"] == "MILITAR":
        entrymilitar = mp.get(mapatipo,"MILITAR")
        valuemilitar = me.getValue(entrymilitar)
        addRoutes(valuemilitar["graph_time"],origin,destination,cost)
    
def add_edges_escalas(catalog, value):
    tipo_mapas= catalog["map_types"]
    origen= value["ORIGEN"]
    destino= value["DESTINO"]
    costo= 1 #Grafico dirigido sin peso
    addRoutes(catalog["graph_escalas"], origen, destino, costo)
    if value["TIPO_VUELO"] == "AVIACION_CARGA":
        entrycarga = mp.get(tipo_mapas,"AVIACION_CARGA")
        valuecarga = me.getValue(entrycarga)
        addRoutes(valuecarga["graph_escalas"], origen, destino, costo)
    elif value["TIPO_VUELO"] == "MILITAR":
        entrymilitar = mp.get(tipo_mapas,"MILITAR")
        value_militar = me.getValue(entrymilitar)
        addRoutes(value_militar["graph_escalas"], origen, destino, costo)
    elif value["TIPO_VUELO"] == "AVIACION_COMERCIAL":
        entrycomercial = mp.get(tipo_mapas,"AVIACION_COMERCIAL")
        value_comercial = me.getValue(entrycomercial)
        addRoutes(value_comercial["graph_escalas"], origen, destino, costo)

  
def addRoutes(graph, origin, destination, Cost):
    edge = gr.getEdge(graph, origin, destination)
    if edge is None:
        gr.addEdge(graph, origin, destination, Cost)
    return graph

def hashmap_concurrencia(catalog, flight_list):
    cantidad_aero = catalog["airport_conc"]
    aeropuertos_cantidad = catalog["concurrencia_airp"]
    mapatipo = catalog["map_types"]
    #Almacenamiento temporal/conteo
    entrycomercial = mp.get(mapatipo,"AVIACION_COMERCIAL")
    value_comercial = me.getValue(entrycomercial)
    cantidad_repetidosC = value_comercial["airport_conc"] #comercial llave aeropuerto, valor cantidad
    aeropuertos_cantidadC = value_comercial["concurrencia_airp"] #comercial llave cantidad, valor lista aeruertos
    entrycarga = mp.get(mapatipo,"AVIACION_CARGA")
    value_carga = me.getValue(entrycarga)
    cantidad_repetidosCA = value_carga["airport_conc"] #carga llave aeropuerto, valor cantidad
    aeropuertos_cantidadCA = value_carga["concurrencia_airp"] #carga llave cantidad, valor lista aeruertos
    entrymilitar = mp.get(mapatipo,"MILITAR")
    value_militar = me.getValue(entrymilitar)
    cantidad_repetidosM = value_militar["airport_conc"] #militar llave aeropuerto, valor cantidad
    aeropuertos_cantidadM = value_militar["concurrencia_airp"] #militar llave cantidad, valor lista aeruertos
    
    #! Método de Felipe [Para hacer un mapa contador]
    """
    fill_mapa_contador(catalog,cantidad_aero)
    fill_mapa_contador(value_comercial,cantidad_repetidosC)
    fill_mapa_contador(value_carga,cantidad_repetidosCA)
    fill_mapa_contador(value_militar,cantidad_repetidosM)
    """
    for value in lt.iterator(flight_list):
        origen= value["ORIGEN"] #icao
        destino= value["DESTINO"] #icao
        #extrae la cantidad de vuelos que le llegan a un aeropuerto sin importar el tipo de vuelo
        #Tiene en cuenta entradas y salidas
        add_conteo_concurrencia(cantidad_aero,origen,destino)
        #Extrae la cantidad de veces que se repite un aeropuerto con su respectivo tipo de vuelo
        if value["TIPO_VUELO"] == "AVIACION_COMERCIAL":
            add_conteo_concurrencia(cantidad_repetidosC,origen,destino)
        elif value["TIPO_VUELO"] == "AVIACION_CARGA":
            add_conteo_concurrencia(cantidad_repetidosCA,origen,destino) 
        elif value["TIPO_VUELO"] == "MILITAR":
            add_conteo_concurrencia(cantidad_repetidosM,origen,destino)
    
    switch_conteo_concurrencia(aeropuertos_cantidad,cantidad_aero) #general
    switch_conteo_concurrencia(aeropuertos_cantidadC,cantidad_repetidosC) #comercial
    switch_conteo_concurrencia(aeropuertos_cantidadCA,cantidad_repetidosCA) #carga
    switch_conteo_concurrencia(aeropuertos_cantidadM,cantidad_repetidosM) #militar

def add_conteo_concurrencia(mapa, origen, destino):
    #para origen
    if mp.contains(mapa, origen):
        entry = mp.get(mapa, origen)
        datoO = me.getValue(entry)
    else:
        datoO = 0
    datoO = datoO + 1
    mp.put(mapa,origen,datoO)
    #para destino
    if mp.contains(mapa, destino):
        entry = mp.get(mapa, destino)
        datoD = me.getValue(entry)
    else:
        datoD = 0
    datoD = datoD + 1
    mp.put(mapa,destino,datoD)

def fill_mapa_contador(valortipo, mapacontador):
    layoverGraph = valortipo['graph_escalas'] # Acceder al grafo de escalas dentro de comercial
    vertexes = gr.vertices(layoverGraph) # Sacar la lista de vértices
    for vertex in lt.iterator(vertexes): # Iterar la lista de vértices
        #deg = gr.degree(layoverGraph, vertex) # Scar el grado de cada vértice
        indeg = gr.indegree(layoverGraph, vertex)
        outdeg = gr.outdegree(layoverGraph, vertex)
        deg = indeg + outdeg
        mp.put(mapacontador, vertex, deg)

def switch_conteo_concurrencia(mapa, conteo_concurrencia):
    airports = mp.keySet(conteo_concurrencia)
    airports = merg.sort(airports,CompareForConcurrencyHigh)
    for key in lt.iterator(airports):
        value = me.getValue(mp.get(conteo_concurrencia,key)) #del mapa de conteo concurrencia
        newkey = value #para el nuevo mapa
        airport = key
        if mp.contains(mapa,newkey):
            lista_airports = me.getValue(mp.get(mapa,newkey))
        else:
            lista_airports = lt.newList(datastructure="ARRAY_LIST")
            om.put(mapa,newkey,lista_airports)
        existe = False
        for code in lt.iterator(lista_airports):
            if code == airport:
                existe = True
        if not existe:
            lt.addLast(lista_airports,airport)

#*########################################
#*######## Funciones de cálculo
#*########################################

def infocarga(catalog):
    cantidad_aeropuertos = mp.size(catalog["map_airports"])
    cantidad_vuelos = mp.size(catalog["map_flights"])
    #* COMERCIAL
    comercial = me.getValue(mp.get(catalog["map_types"],"AVIACION_COMERCIAL"))
    conc_comercial = comercial["concurrencia_airp"] # llave cantidad, valor lista aeropuertos
    mayorC, menorC = getStatsConc(conc_comercial,5)
    #mayorC, menorC = getFirst5andLast5Concurrencia(conc_comercial)
    mayorC = get_airport_info(catalog,mayorC)
    menorC = get_airport_info(catalog,menorC)
    
    #* CARGA
    carga = me.getValue(mp.get(catalog["map_types"],"AVIACION_CARGA"))
    conc_carga = carga["concurrencia_airp"]
    mayorCA, menorCA = getStatsConc(conc_carga,5)
    #mayorCA, menorCA = getFirst5andLast5Concurrencia(conc_carga)
    mayorCA = get_airport_info(catalog,mayorCA)
    menorCA = get_airport_info(catalog,menorCA)
    
    #* MILITAR
    militar = me.getValue(mp.get(catalog["map_types"],"MILITAR"))
    conc_militar = militar["concurrencia_airp"]
    mayorM, menorM = getStatsConc(conc_militar,5)
    #mayorM, menorM = getFirst5andLast5Concurrencia(conc_militar)
    mayorM = get_airport_info(catalog,mayorM)
    menorM = get_airport_info(catalog,menorM)
    
    return [cantidad_aeropuertos, cantidad_vuelos, mayorC, menorC, mayorCA, menorCA, mayorM, menorM]

def getFirst5andLast5Concurrencia(concurrencyMap):
    mayor = lt.newList(datastructure="ARRAY_LIST")
    menor = lt.newList(datastructure="ARRAY_LIST")
    concurrencyMap_keys = om.keySet(concurrencyMap)
    concurrencyMap_keys = merg.sort(concurrencyMap_keys,CompareForConcurrencyHigh)
    i=lt.size(concurrencyMap_keys)
    while lt.size(mayor) < 5:
        mayorvalue = me.getValue(om.get(concurrencyMap,lt.getElement(concurrencyMap_keys,i)))
        mayorvalue = merg.sort(mayorvalue,CompareForConcurrencyHigh)
        for valuemayor in lt.iterator(mayorvalue):
            if lt.size(mayor) < 5:
                lt.addLast(mayor,valuemayor)
        i=i-1
    i=0
    while lt.size(menor) < 5:
        menorvalue = me.getValue(om.get(concurrencyMap,lt.getElement(concurrencyMap_keys,i)))
        menorvalue = merg.sort(menorvalue,CompareForConcurrencyHigh)
        for valuemenor in lt.iterator(menorvalue):
            if lt.size(menor) < 5:
                lt.addLast(menor,valuemenor)
        i=i+1
    return mayor, menor

def getInRadious(catalog, Point, Rad = 30):
    mapAirports = catalog['map_airports']
    '''Busca si hay / el mejor Aeropuerto en el radio (Default 30Km) y si lo hay si lo regresa'''
    BestContender = None
    Airports = mp.valueSet(mapAirports)
    for Airport in lt.iterator(Airports):
        latitud = Airport['LATITUD']
        longitud = Airport['LONGITUD']
        AirportCoords = georaphicTuple((latitud, longitud))
        distance = HaversineDistance(Point, AirportCoords)
        if distance <= float(Rad):
            BestContender = (Airport['ICAO'], distance)

    return BestContender
        
    
def HaversineDistance(PointA:tuple, PointB:tuple):
    '''Se le madna una tupla (latitud, longitud) para puntoA y para puntoB. 
    Retorna: Valor (int) para distancia entre A y B.'''

    PointA = georaphicTuple(PointA)
    PointB = georaphicTuple(PointB)

    lat1 = float(PointA[0])
    lat2 = float(PointB[0])
    lon1 = float(PointA[1])
    lon2 = float(PointB[1])

    lat1 = radians(lat1)
    lat2 = radians(lat2)
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    diflon = lon2 - lon1
    diflat = lat2 - lat1
    a = sin(diflat / 2)**2 + cos(lat1) * cos(lat2) * sin(diflon / 2)**2
    c = 2 * asin(sqrt(a))
    
    r = 6371  
    disto =  c * r  
    return disto

def georaphicTuple(tup: tuple) -> tuple:
    '''Recibe una tupla con lat, long en el formato que sea 
    y lo regresa en un formato de tupla (float, float)'''
    try:
        lat_str, lon_str = str(tup[0]), str(tup[1])
        if ',' in lat_str:
            lat = float(lat_str.replace(',', '.'))
            lon = float(lon_str.replace(',', '.'))
        else:
            lat = float(lat_str)
            lon = float(lon_str)
    except ValueError:
        raise ValueError("Que mamada es esto wey, esto no es un número")
    
    return (lat, lon)

#*########################################
#*######## Funciones de consulta
#*########################################

def req_1(catalog, origin:tuple, destination:tuple):
    """
    Find a route between two tourist destinations using user-input latitudes and longitudes, approximate to the nearest airport 
    within 30 km, and return the total distance, execution time, number of airports visited, and the route sequence.
    """
    
    originQuery = georaphicTuple((origin)) #* Garantiza que sea leido como float-tupla
    destinationQuery = georaphicTuple((destination)) #* Garantiza que sea leido como float-tupla
    bestOrigin = getInRadious(catalog, originQuery, 30) #* Retorna tup (ICAO, Distancia hasta)
    bestDestination = getInRadious(catalog, destinationQuery, 30) #* Retorna tup (ICAO, Distancia hasta)
    #* Usamos Dikjtra para poder saber la distancia (camino mas corto)
    valCom = me.getValue(mp.get(catalog['map_types'], 'AVIACION_COMERCIAL')) ## Acceder al mapa de comercial
    distanceGraph = valCom['graph_distance'] ## Acceder al grafo de comercial
    #* Paso 1) Se calculan todas las distancias usando Dijktra desde el aeropuerto de Origen (es obligatorio)
    busqueda = djk.Dijkstra(distanceGraph, bestOrigin[0]) ## Se hace la búsqueda de origen hacia todo los nodos.
    #* Paso 2) Se pide la distancia entre el origen (busqueda ya hecha) y el aeropuerto de destino 
    flightDistance = djk.distTo(busqueda, bestDestination[0]) #* (Recordar que bestxx es tupla y que el ICAO también es key del grafo)
    #distHastaDestino = HaversineDistance(bestDestination[1], destination) #! Se me habia olvidado esto, pero es super importante
    totalDistance = sum([bestOrigin[1], flightDistance, bestDestination[1]]) ## Usar la funcion suma para calcular distTot
    #* Paso 3) Sacar el camino (todo aeropuerto intermedio) desde AeroOrigen hasta AeroDestino
    pilaRecorrido = djk.pathTo(busqueda, bestDestination[0]) # Retorna una pila 
    stackIterable = nodeListFromStack(pilaRecorrido)
    #* Ahora, tenemos que sacar la info por el identificador por cada elemento en el stack
    mapaAirports = catalog['map_airports']
    valuesList = lt.newList('ARRAY_LIST')
    for idi in lt.iterator(stackIterable):
        value = me.getValue(mp.get(mapaAirports, idi))
        lt.addLast(valuesList, value)
        
    #* paso 3.1) Sacar el tamaño de la pila (número de aeropuertos visitados)
    numAeropuertos = st.size(pilaRecorrido)
    
    OriginaInfo = me.getValue(mp.get(catalog['map_airports'], bestOrigin[0])) 
    DestInfo = me.getValue(mp.get(catalog['map_airports'], bestDestination[0]))    
   
    return [totalDistance, OriginaInfo, DestInfo, valuesList, numAeropuertos] # Distancia Total, numero de aeropuertos visitados y Lista de Dics con info de todos escalas involucradas 


def req_2(catalog, origin:tuple, destination:tuple):
    """
    Función que soluciona el requerimiento 2
    """
    originQuery = georaphicTuple((origin)) #* Garantiza que sea leido como float-tupla
    destinationQuery = georaphicTuple((destination)) #* Garantiza que sea leido como float-tupla
    bestOrigin = getInRadious(catalog, originQuery, 30) #* Retorna tup (ICAO, Distancia hasta)
    bestDestination = getInRadious(catalog, destinationQuery, 30) #* Retorna tup (ICAO, Distancia hasta)
    valCom = me.getValue(mp.get(catalog['map_types'], 'AVIACION_COMERCIAL')) ## Acceder al mapa de comercial
    layoverGraph = valCom['graph_escalas'] ## Acceder al grafo de escalas dentro de comercial
    #* Normalmente se usaría BFS, pero nosotros somos extra pilobos e hicimos un mapa de escalas con todos los edges = 1
    # Así que hacemos Dijkstra y mamey
    busqueda = djk.Dijkstra(layoverGraph, bestOrigin[0]) ## Se hace la búsqueda de origen hacia todo los nodos.
    layoverNo = djk.distTo(busqueda, bestDestination[0]) #* (Recordar que bestxx es tupla y que el ICAO también es key del grafo)
    solvingPathStack = djk.pathTo(busqueda, bestDestination[0])
    stackIterable = nodeListFromStack(solvingPathStack)
    #* Ahora, tenemos que sacar la info por el identificador por cada elemento en el stack
    mapaAirports = catalog['map_airports']
    valuesList = lt.newList('ARRAY_LIST')
    for idi in lt.iterator(stackIterable):
        value = me.getValue(mp.get(mapaAirports, idi))
        lt.addLast(valuesList, value)
    # Calcular las distancias
    flightDistance = djk.distTo(busqueda, bestDestination[0]) #* (Recordar que bestxx es tupla y que el ICAO también es key del grafo)
    totalDistance = sum([bestOrigin[1], flightDistance, bestDestination[1]]) ## Usar la funcion suma para calcular distTot
    # Se suman las distancias ya calculadas por las funciones 'best'
    #* Sacar información aeropuerto origen y destino
    OriginInfo = me.getValue(mp.get(mapaAirports, bestOrigin[0]))
    DestinoInfo = me.getValue(mp.get(mapaAirports, bestDestination[0]))
    return [layoverNo, OriginInfo, DestinoInfo, valuesList ,totalDistance] #* NumeroDeEscalas, OriginInfo, DestinoInfo,  Dics con info de escalas involucradas, distancia total



def req_3(catalog):
    # Parte 1 - Sacar mayor concurrencia -
    #* Método de un mapa contador no-ordenado por concurrencia
    valCom = me.getValue(mp.get(catalog['map_types'], 'AVIACION_COMERCIAL')) # Acceder al mapa de comercial
    layoverGraph = valCom['graph_escalas'] # Acceder al grafo de escalas dentro de comercial
    vertexes = gr.vertices(layoverGraph) # Sacar la lista de vértices
    mapaContador = mp.newMap() # Iniciar mapa contador
    for vertex in lt.iterator(vertexes): # Iterar la lista de vértices
        deg = gr.degree(layoverGraph, vertex) # Scar el grado de cada vértice
        mp.put(mapaContador, vertex, deg)
    
    #* Sacar el máximo de concurrencia (llave ICAO)
    keySet = mp.keySet(mapaContador)
    Top = float('-inf')
    TopKey = None
    for key in lt.iterator(keySet):
        value = float(me.getValue(mp.get(mapaContador, key)))
        if value > Top:
            TopKey = key
            Top = value
        elif (value == Top) and (key != TopKey):
            Top = value
            if str(TopKey)> str(key):
                TopKey = TopKey
                Top = value
            else:
                TopKey = key
                Top = value
    #*  - - - Para este punto 'TopKey' contendrá el ICAO de mayor concurrencia y por orden alabético. - - - 
    mapaAirports = catalog['map_airports']
    TopKeyInfo = me.getValue(mp.get(mapaAirports, TopKey)) #- Sacar información del más concurrido
    
    #* Parte 2 - Encontrar menor distancia desde el ICAO encontrado a todos sus edges -
    distanceGraph = valCom['graph_distance'] ## Acceder al grafo de DISTANCIA comercial
    
    
    menorDistanciaBusqueda = prim.PrimMST(distanceGraph, TopKey) ## Se hace la búsqueda PRIM de origen hacia todo los nodos.
    peso = prim.weightMST(distanceGraph, menorDistanciaBusqueda) ##* Se calcula el peso, sin esto NO crea MST
    #* Acá ya se tiene el MST de distancia.
    
    #* Ahora, sacar el tiempo para todas
    distanceGraph = valCom['graph_distance'] ## Acceder al grafo de DISTANCIA comercial
    timeGraph = valCom['graph_time'] ## Acceder al grafo de TIEMPO comercial

    # Dado que no siempre mejor distancia = mejor tiempo, y que nos piden mejor DISTANCIA, sacar los tiempos para esas distancias
    sumlist = [] # Lista para sumar distancias
    listaTrayectos = lt.newList('ARRAY_LIST') # Lista de retorno con toda la info de los trayectos
    for connected in lt.iterator(menorDistanciaBusqueda['mst']):
        Va = connected['vertexA']
        Vb = connected['vertexB']
        Time = gr.getEdge(timeGraph, Va, Vb)['weight']
        sumlist.append(connected['weight']) # !Lo agregamos a la lista de suma
        dicPE = {'ORIGEN': Va, 'DESTINO': Vb, 'DISTANCIA': connected['weight'], 'TIEMPO': Time}
        lt.addLast(listaTrayectos, dicPE)
    totalDistance = sum(sumlist) # Sumamos La lista
    numTotal = lt.size(listaTrayectos)
    return [TopKeyInfo, Top, totalDistance, numTotal, listaTrayectos]


def req_4(catalog):
    """
    Función que soluciona el requerimiento 4
    """
    mapa_tipos = catalog["map_types"]
    mapa_airport = catalog["map_airports"]
    mapa_flights = catalog["map_flights"]
    conc_carga = me.getValue(mp.get(mapa_tipos,"AVIACION_CARGA"))["concurrencia_airp"]
    distance_graph = me.getValue(mp.get(mapa_tipos,"AVIACION_CARGA"))["graph_distance"]
    time_graph = me.getValue(mp.get(mapa_tipos,"AVIACION_CARGA"))["graph_time"]
    topconc, lastconc = getStatsConc(conc_carga,1) #topconc tiene (cantidad concurrencia, ICAO aeropuerto)
    topconc = lt.getElement(topconc,1)
    
    infoTopconc = me.getValue(mp.get(mapa_airport,topconc[1]))
    infoTopconc["CONCURRENCIA"] = topconc[0]
    
    moreAirp_lessDist = prim.PrimMST(distance_graph,topconc[1])
    total_distance = prim.weightMST(distance_graph, moreAirp_lessDist)
    
    mst = moreAirp_lessDist["mst"]
    NumTrayectos = 0
    sequenceInfo = lt.newList(datastructure="ARRAY_LIST")
    for trayecto in lt.iterator(mst):
        verticeA = trayecto["vertexA"]
        verticeB = trayecto["vertexB"]
        if verticeA == topconc[1]:
            NumTrayectos = NumTrayectos + 1
        dic = {"TRAYECTO":str(verticeA)+"-"+str(verticeB)}
        keeper = ['ICAO', 'NOMBRE', 'CIUDAD', 'PAIS']
        dic["ORIGEN"] = me.getValue(mp.get(mapa_airport,verticeA))
        dic["DESTINO"] = me.getValue(mp.get(mapa_airport,verticeB))
        dic["DISTANCIA"] = gr.getEdge(distance_graph,verticeA,verticeB)["weight"]
        dic["TIEMPO"] = gr.getEdge(time_graph,verticeA,verticeB)["weight"]
        dic["TIPO_AERONAVE"] = me.getValue(mp.get(mapa_flights,str(verticeA)+"-"+str(verticeB)))["TIPO_AERONAVE"]
        
        dic["ORIGEN"] = DicKeepOnly(keeper, dic["ORIGEN"])["elements"]
        dic["DESTINO"] = DicKeepOnly(keeper, dic["DESTINO"])["elements"]
        lt.addLast(sequenceInfo,dic)
    
    return [infoTopconc, total_distance, NumTrayectos, sequenceInfo]
    
    


def req_5(catalog):
    """
    Función que soluciona el requerimiento 5
    """
    #Tablas y grafos a usar
    concurrencias_tabla= catalog["concurrencia_airp"]
    aeropuertos_tabla= catalog["map_airports"]
    militar = me.getValue(mp.get(catalog['map_types'], 'MILITAR')) #Accede de una vez a la categoria militar
    distance_militar= militar["graph_distance"]        
    tiempo_militar= militar["graph_time"]
    vuelos_flight= catalog["map_flights"]
    #Keyset para extraer la mayor concurrencia
    lista_llaves= mp.keySet(concurrencias_tabla)
    #Contador max, busca la concurrencia mas alta de la tabla
    max= 0 #retorno
    for cantidad in lt.iterator(lista_llaves):
        if cantidad > max:
            max= cantidad
    #Extrae la lista de concurrencia de la tabla, key= concurrencia, value= lista (aeropuertos)
    aeropuerto_s= mp.get(concurrencias_tabla, max)      
    aeropuerto_s= (me.getValue(aeropuerto_s))["elements"] #element crimen tratado de ginebra, accede a la lista
    #Si es una lista retorna por orden ICAO el primero
    if isinstance(aeropuerto_s, list):
        aeropuerto= get_icao(aeropuerto_s)
    #Sacar el search y el peso del mst(red)
    red_recorrido= prim.PrimMST(distance_militar, aeropuerto)    
    peso_red= prim.weightMST(distance_militar, red_recorrido) #Necesita ejecutarse para generar el MST, hptas.
    #Genera nueva lista para almacenar cada trayecto
    trayectos_lista= lt.newList("ARRAY_LIST")
    for info in lt.iterator(red_recorrido["mst"]):
        aeropuerto_origen= info["vertexA"]
        aeropuerto_destino= info["vertexB"]
        llave_tabla= aeropuerto_origen +"-"+ aeropuerto_destino #Creacion de key para preguntar en tabla flights
        dict={
        "aeropuerto_origin": me.getValue(mp.get(aeropuertos_tabla, aeropuerto_origen)), #Extrae los aeropuertos y su info
        "aeropuerto_destino": me.getValue(mp.get(aeropuertos_tabla, aeropuerto_destino)),
        "distancia": info["weight"], #Extrae peso/distancia
        "tiempo": (gr.getEdge(tiempo_militar, aeropuerto_origen, aeropuerto_destino))["weight"],  #getEdges para sacar el tiempo entre los grafos
        "tipo_aeronave": (me.getValue((mp.get(vuelos_flight, llave_tabla))))["TIPO_AERONAVE"] #Saca el tipo de aeronaves del HM de vuelos
        }
        lt.addLast(trayectos_lista, dict)
    cantidad_trayectos= lt.size(trayectos_lista)
    aeropuerto= me.getValue(mp.get(aeropuertos_tabla, aeropuerto))
    return [aeropuerto, peso_red, cantidad_trayectos, trayectos_lista]


    
def req_6(catalog, M:int):
    #* Parte 1 - Sacar contar concurrencia
    #* Método para hacer un mapa contador ordenado basado en el grado de un vértice 
    valCom = me.getValue(mp.get(catalog['map_types'], 'AVIACION_COMERCIAL')) # Acceder al mapa de comercial
    layoverGraph = valCom['graph_escalas'] # Acceder al grafo de escalas dentro de comercial
    vertexes = gr.vertices(layoverGraph) # Sacar la lista de vértices
    mapaContador_ORDENADO = om.newMap(cmpfunction= compareConcurrency) # Iniciar mapa contador ordenado
    for vertex in lt.iterator(vertexes): # Iterar la lista de vértices
        degIncom = gr.indegree(layoverGraph, vertex)
        degOut = gr.outdegree(layoverGraph, vertex)
        deg  = degIncom + degOut 

        om.put(mapaContador_ORDENADO, (deg, vertex), deg) # Agregar al mapa de acuerdo a una tupla apra poder ordenar por grado

    #* Parte 2, Sacar top N Concurrencias
    listaTopM = lt.newList('DOUBLE_LINKED') # Lista de los M más concurridos (Tuplas)
    listaTopKeys = lt.newList('DOUBLE_LINKED') #Lista de los M más concurridos (sólo llaves)
    for i in range(0, M):
        MKey = OmPopMaxCounter(mapaContador_ORDENADO) # Uso del método creado Pop para un mapa ordenado max counter
        icao = MKey[1] #Sacar el ICAO de la tupla
        AirportMap = catalog['map_airports'] # Acceder el mapa de aeropuertos
        info = me.getValue(om.get(AirportMap, icao)) # Sacar la información asociada al aeropuerto
        pais = info['PAIS'] # Confirmar que el país ...
        if pais == "Colombia": # ... Sea Colombia
            lt.addLast(listaTopM, MKey) # Agregar a la lista de top M (Tuplas)
            lt.addLast(listaTopKeys, icao) # Agregar a la lista de llaves
        else:
            None # No hacer nada
    mayorConcurrencia = lt.firstElement(listaTopKeys) # Sacar el de más concurrencia (primero en orden)
    lt.removeFirst(listaTopKeys) #Eliminar el de más concurrencia para iterar de manera más fácil
    CuentaMayorConc = lt.firstElement(listaTopKeys) # Sacar llave más concurrente
    #* Sacar info estadística
    mayorConcInfo = me.getValue(om.get(AirportMap, mayorConcurrencia)) # Sacar info del de mayor concurrencia
    MayorConCDegree = gr.degree(layoverGraph, mayorConcurrencia) #Sacar el degree del de mayor concurrencia
    distanceGraph = valCom['graph_distance'] ## Acceder al grafo de comercial de distancia
    #* Paso 3 - Dijkstra
    Search = djk.Dijkstra(distanceGraph, mayorConcurrencia) #* Hacer la búsqueda de Dijkstra desde el más concurrente hacia TODO
    Prioridades = lt.newList("ARRAY_LIST")
    #* Usar la lista de importantes anteriores para sacar info necesaria
    for important in lt.iterator(listaTopKeys):
        #* Sacar las distancias desde el más importante al resto de importantes
        distance = djk.distTo(Search, important) # distancia
        PathTo = djk.pathTo(Search, important) # Lista de camino
        CantAeropuetos = lt.size(PathTo) #Número de aeropuertos
        # Sacar los ICAOs de Origen y Destino
        listaAeropuertosIncluidos = lt.newList('ARRAY_LIST') #sub-Lista de aeropuertos que incluye
        vuelosIncluidos = lt.newList('ARRAY_LIST') # Vuelos que incluye
        for flight in lt.iterator(PathTo):
            vertexA = flight['vertexA'] #Sacar vértices
            vertexB = flight['vertexB']
            strVuelo = str("Vuelo: ") + str(vertexA) + str("-") + str(vertexB) #Crear str de vuelos
            lt.addLast(listaAeropuertosIncluidos, vertexA) # Agregar aeropuerto A
            lt.addLast(listaAeropuertosIncluidos, vertexB) # Agregar aeropuerto B
            lt.addLast(vuelosIncluidos, strVuelo) # Agregar lista de vuelos incluidos
            
        for aeroporto in lt.iterator(listaAeropuertosIncluidos): #Iterar por los aeropuertos incluidos
            AirportMap = catalog['map_airports'] # Acceder al mapa de aeropuertos
            aeroporto = me.getValue(om.get(AirportMap, aeroporto)) # Sacar info por ICAO
            
        # Diccionario para empaquetar toda esta madre
        dic = {"Total": CantAeropuetos, "AeropuertosIncluidos": listaAeropuertosIncluidos, "VuelosIncluidos": vuelosIncluidos, 
               "Distancia": distance}   
        # Agregar todo a la lista de retorno
        lt.addLast(Prioridades, dic)
        # Retornar todo lo pedido
    return [mayorConcInfo, MayorConCDegree, Prioridades]


def req_7(catalog, origen, destino):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Revisar funcionamiento
    airportsmap = catalog["map_airports"]
    originQuery = georaphicTuple((origen)) #* Garantiza que sea leido como float-tupla
    destinationQuery = georaphicTuple((destino)) #* Garantiza que sea leido como float-tupla
    bestOrigin = getInRadious(catalog, originQuery, 30) #* Retorna tup (ICAO, Distancia hasta)
    bestDestination = getInRadious(catalog, destinationQuery, 30) #* Retorna tup (ICAO, Distancia hasta)
    #* Usamos Dikjtra para poder saber la distancia (camino mas corto en tiempo)
    valCom = me.getValue(mp.get(catalog['map_types'], 'AVIACION_COMERCIAL')) ## Acceder al mapa de comercial
    distanceGraph = valCom['graph_distance'] ## Acceder al grafo de comercial de distancia
    distanceTime = valCom['graph_time'] ## Acceder al grafo de comercial de tiempo
    #* Paso 1) Se calculan todas las distancias usando Dijktra desde el aeropuerto de Origen (es obligatorio)
    busqueda = djk.Dijkstra(distanceTime, bestOrigin[0]) ## Se hace la búsqueda de origen hacia todo los nodos.
    #* Paso 2) Se pide la distancia entre el origen (busqueda ya hecha) y el aeropuerto de destino 
    flightTime = djk.distTo(busqueda, bestDestination[0]) #* (Recordar que bestxx es tupla y que el ICAO también es key del grafo)
    #* Paso 3) Sacar el camino (todo aeropuerto intermedio) desde AeroOrigen hasta AeroDestino
    pilaRecorrido = djk.pathTo(busqueda, bestDestination[0]) # Retorna una pila 
    #* paso 3.1) Sacar el tamaño de la pila (número de aeropuertos visitados)
    numAeropuertos = st.size(pilaRecorrido)
    #* Paso 4) Sacar la secuencia de aeropuertos que componen el camino encontrado
    listaRecorrido = nodeListFromStack(pilaRecorrido)
    flightDistance = bestOrigin[1] + bestDestination[1]
    infotrayectos = lt.newList(datastructure="ARRAY_LIST")
    for item in lt.iterator(pilaRecorrido):
        verticeA = item["vertexA"]
        verticeB = item["vertexB"]
        tiempo_trayecto = item["weight"]
        distancia_trayecto = gr.getEdge(distanceGraph,verticeA,verticeB)
        flightDistance = flightDistance + distancia_trayecto["weight"]
        lt.addLast(infotrayectos,{verticeA+"-"+verticeB:str("\nTiempo trayecto: \n"+str(tiempo_trayecto)+"\nDistancia trayecto: \n"+str(distancia_trayecto["weight"]))})
        
    listainfo = lt.newList(datastructure="ARRAY_LIST")
    for value in lt.iterator(listaRecorrido):
        informacion = me.getValue(mp.get(airportsmap,value))
        lt.addLast(listainfo,informacion)
    return [flightTime, flightDistance, numAeropuertos, listainfo, infotrayectos]


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass

#*####################################################################################
#*##########################Funciones utilizadas para comparar elementos
#*####################################################################################

def compareAirportIds(airport, tuplakeyvalue):
    """
    Función encargada de comparar dos datos
    """
    airportcode = tuplakeyvalue["key"]
    if airport == airportcode:
        return 0
    elif airport > airportcode:
        return 1
    else:
        return -1

def compareDistance(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora del valor de distancia de las rutas
    pass    

def compareTime(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora del valor de tiempo de las rutas
    pass

#*####################################################################################
#*##########################Funciones de ordenamiento
#*####################################################################################

def CompareAirportsCode(airport1, airport2):
    if airport1 == airport2:
        return None
    elif airport1 > airport2:
        return True
    elif airport1 < airport2  :
        return False

def CompareForConcurrencyHigh(value1, value2):
    """Compara los valores y despues del sort queda: elements: menor, .... , mayor
    ej: elements: 1,2,3,4,5
    """
    if value1 == value2:
        return None
    elif value1 < value2:
        return True
    elif value1 > value2  :
        return False

def CompareForConcurrencyLow(value1, value2):
    """Compara los valores y despues del sort queda: elements: mayor, .... , menor
    ej: elements: 5,4,3,2,1
    """
    if value1 == value2:
        return None
    elif value1 > value2:
        return True
    elif value1 < value2  :
        return False

def CompareDatesISO8601(Dic1, Dic2): 
    date1 = Dic1['published_at']
    date2 = Dic2['published_at']
    date1 = dt.fromisoformat(date1)
    date2 = dt.fromisoformat(date2)
    if date1 == date2:
        return None
    elif date1 > date2:
        return True
    elif date1 < date2  :
        return False

def Datesort(lista):
    listaord = merg.sort(lista, CompareDatesISO8601)
    return listaord

# No tocar hay muertos :)
def compareConcurrency(val1, val2):
    deg1, deg2 = float(val1[0]), float(val2[0])
    if deg1 == deg2:
        return 0
    if deg1 < deg2:
        return -1
    else:
        return 1

def OmPopMaxCounter(OMap):
    Mk = om.maxKey(OMap)
    om.deleteMax(OMap)
    
    return Mk

#*####################################################################################
#*##########################Funciones Tabulate
#*####################################################################################
def declutterLoad3(sortedlist, Head):
    keep = []
    if Head:
        HeadSublist = lt.subList(sortedlist, 1, 3)
        Heads = DicKeepOnly(keep, HeadSublist)
    elif not Head:
        Tmin = lt.size(sortedlist) - 2
        TailsSublist = lt.subList(sortedlist, Tmin, 3)
        Tails = DicKeepOnly(keep, TailsSublist)
    if Head:
        return Heads['elements']
    else:
        return Tails['elements']
    
def declutterLoad5(sortedlist, Head, keep):
    if Head:
        HeadSublist = lt.subList(sortedlist, 1, 5)
        Heads = DicKeepOnly(keep, HeadSublist)
    elif not Head:
        Tmin = lt.size(sortedlist) - 4
        TailsSublist = lt.subList(sortedlist, Tmin, 5)
        Tails = DicKeepOnly(keep, TailsSublist)
    if Head:
        return Heads['elements']
    else:
        return Tails['elements']

def declutterLoad_N(sortedlist, Head, keep, N):
    """
    Head=False -> Primeras N | Head=True -> Ultimas N
    """
    if Head:
        HeadSublist = lt.subList(sortedlist, 1, N)
        Heads = DicKeepOnly(keep, HeadSublist)
    elif not Head:
        Tmin = lt.size(sortedlist) - N
        TailsSublist = lt.subList(sortedlist, Tmin, N)
        Tails = DicKeepOnly(keep, TailsSublist)
    if Head:
        return Heads['elements']
    else:
        return Tails['elements']
    
def DicKeepOnly(keep, lista):
    kept = lt.newList("ARRAY_LIST")
    listTypes = ['ARRAY_LIST', 'SINGLE_LINKED', 'DOUBLE_LINKED']
    try:
        typelista = lista['type'] 
    except:
        typelista = None
    
    if typelista not in listTypes:
        #* Asumimos que no es una lista sino un valor único
        try:
            dic = {}
            for key in keep:
                dic[key] =  lista[key]
            lt.addLast(kept, dic)
        except:
            raise ValueError(f'oh no, tu {lista} es una mierda que no soporta esta función')
    else:
        for element in lt.iterator(lista):
            dic = {}
            for key in keep:
                dic[key] =  element[key]
            lt.addLast(kept, dic)
    
    return kept

def nodeListFromStack(stack)-> dict:
    '''Recibe un stack con objetos {VertexA: <>, VertexB: <>} y regresa una lista iterable'''
    Keys = mp.newMap() #* Esto es un truquito para hacer consultas en O(1) Aunque un tris overkill
    for item in lt.iterator(stack):
        if item != None:
            pa = item['vertexA']
            isIn = mp.contains(Keys, pa)
            if not isIn:
                mp.put(Keys, pa, pa)
            pb = item['vertexB']
            isIn = mp.contains(Keys, pb)
            if not isIn:
                mp.put(Keys, pb, pb)
    stackIterable = mp.keySet(Keys) #* Retornar una lista con las llaves de las cuales se necesita información   
    return stackIterable

def copy(datastruture):
    newdatastruture = datastruture.copy()
    return newdatastruture

def timeIs():
    return time.time()

def deltaTime(start, end, seconds= False, do_print=False):
    time = end-start
    if seconds:
        if do_print:
            print(f"El tiempo fue de {time} segundos")
        return time
    else:
        time = time*1000
        if do_print:
            print(f"El tiempo fue de {time} mili-segundos")
        return time
    
    
def get_icao(lista):
    # Comparar lexicognosequemondamente aeropuertos y extraer el primero.
    primer= lista[0]
    for value in lista:
        if value < primer:
            primer = value
    
    return primer

def get_airport_info(catalog, listaICAOs):
    mapaAirports = catalog["map_airports"]
    listaInfoICAOs = lt.newList(datastructure="ARRAY_LIST")
    for conc, ICAO in lt.iterator(listaICAOs):
        Info_ICAO = me.getValue(mp.get(mapaAirports, ICAO))
        Info_ICAO["CONCURRENCIA"] = conc
        lt.addLast(listaInfoICAOs,Info_ICAO)
    return listaInfoICAOs

def getStatsConc(mapaContador_ORDENADO, N:int):
    """mapaContador_ORDENADO: Ordered mapa del conteo, N: cantidad de elementos a sacar
    return: lista de Top N elementos en concurrencia y lista de Last N elementos en concurrencia
    """
    concurrencyMap_keys = om.keySet(mapaContador_ORDENADO)
    concurrencyMap_keys = merg.sort(concurrencyMap_keys,CompareForConcurrencyHigh)
    listaTopN = lt.newList('DOUBLE_LINKED')
    listaLastN = lt.newList('DOUBLE_LINKED')
    i=lt.size(concurrencyMap_keys)
    while lt.size(listaTopN) < N:
        mayorkey = me.getKey(om.get(mapaContador_ORDENADO,lt.getElement(concurrencyMap_keys,i)))
        mayorvalue = me.getValue(om.get(mapaContador_ORDENADO,lt.getElement(concurrencyMap_keys,i)))
        mayorvalue = merg.sort(mayorvalue,CompareForConcurrencyHigh)
        for valuemayor in lt.iterator(mayorvalue):
            if lt.size(listaTopN) < N:
                lt.addLast(listaTopN,(mayorkey,valuemayor))
        i=i-1
    i=0
    while lt.size(listaLastN) < N:
        menorkey = me.getKey(om.get(mapaContador_ORDENADO,lt.getElement(concurrencyMap_keys,i)))
        menorvalue = me.getValue(om.get(mapaContador_ORDENADO,lt.getElement(concurrencyMap_keys,i)))
        menorvalue = merg.sort(menorvalue,CompareForConcurrencyHigh)
        for valuemenor in lt.iterator(menorvalue):
            if lt.size(listaLastN) < N:
                lt.addLast(listaLastN,(menorkey,valuemenor))
        i=i+1
    
    return listaTopN, listaLastN