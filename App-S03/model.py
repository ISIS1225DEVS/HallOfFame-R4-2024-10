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
import math
assert cf
from tabulate import tabulate

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
    catalog= {"airports": None,
              "airports_importance":None,
              "flights" : None
              }

  
    catalog['airports'] = mp.newMap(numelements=108, maptype="CHAINING", loadfactor=4)
    catalog["airports_importance"] = mp.newMap(numelements=6, maptype="PROBING", loadfactor=0.5)
    catalog["flights"] = mp.newMap(numelements=755, maptype="CHAINING", loadfactor=4)
    
    
    catalog["comercialDistancia"] = gr.newGraph("ADJ_LIST", directed=True, size=428)
    catalog["cargaDistancia"] = gr.newGraph("ADJ_LIST", directed=True, size=428)
    catalog["militarDistancia"] = gr.newGraph("ADJ_LIST", directed=True, size=428)
    catalog["comercialTiempo"] = gr.newGraph("ADJ_LIST", directed=True, size=428)
    catalog["cargaTiempo"] = gr.newGraph("ADJ_LIST", directed=True, size=428)
    catalog["militarTiempo"] = gr.newGraph("ADJ_LIST", directed=True, size=428)
    """
    catalog["comercialDistancia"] = gr.newGraph("ADJ_LIST", directed=False, size=428)
    catalog["cargaDistancia"] = gr.newGraph("ADJ_LIST", directed=False, size=428)
    catalog["militarDistancia"] = gr.newGraph("ADJ_LIST", directed=False, size=428)
    catalog["comercialTiempo"] = gr.newGraph("ADJ_LIST", directed=False, size=428)
    catalog["cargaTiempo"] = gr.newGraph("ADJ_LIST", directed=False, size=428)
    catalog["militarTiempo"] = gr.newGraph("ADJ_LIST", directed=False, size=428)
    """
    
    
    
    return catalog

def cmpFunctionConcurrencia(airport1, airport2):
    if airport1 > airport2:
        return 1
    elif airport1 < airport2:
        return -1
    else:
        return 0

# Funciones para agregar informacion al modelo

def add_data(data_structs,part, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    if part == "airport":
        data["concurrencia_comercial"] = 0
        data["concurrencia_carga"] = 0
        data["concurrencia_militar"] = 0
        
        existsAirport = om.contains(data_structs["airports"], data["ICAO"])
        if not existsAirport:                                    #Com,Car,Mil
            om.put(data_structs["airports"], data["ICAO"], data)
       
        
        gr.insertVertex(data_structs["comercialDistancia"], data["ICAO"])
        gr.insertVertex(data_structs["cargaDistancia"], data["ICAO"])
        gr.insertVertex(data_structs["militarDistancia"], data["ICAO"])
        gr.insertVertex(data_structs["comercialTiempo"], data["ICAO"])
        gr.insertVertex(data_structs["cargaTiempo"], data["ICAO"])
        gr.insertVertex(data_structs["militarTiempo"], data["ICAO"])
        
    if part == "flight":
        if not mp.contains(data_structs["flights"], f"{data['ORIGEN']}_{data['DESTINO']}_{data['TIPO_VUELO']}"):
            mp.put(data_structs["flights"], f"{data['ORIGEN']}_{data['DESTINO']}_{data['TIPO_VUELO']}", data)
        
        
        origen = me.getValue(mp.get(data_structs["airports"],data["ORIGEN"]))
        destino = me.getValue(mp.get(data_structs["airports"],data["DESTINO"]))
        lat1 = float(origen["LATITUD"])
        lat2 = float(destino["LATITUD"])
        long1 = float(origen["LONGITUD"])
        long2 = float(destino["LONGITUD"])
        distance = coversine(lat1,lat2, long1, long2)
        
        if data["TIPO_VUELO"] == "AVIACION_CARGA":
            
            me.getValue(mp.get(data_structs["airports"],data["ORIGEN"]))["concurrencia_carga"] += 1
            me.getValue(mp.get(data_structs["airports"],data["DESTINO"]))["concurrencia_carga"] += 1 
            """
            tupla = me.getValue(mp.get(data_structs["airports"],data["ORIGEN"]))
            mp.put(data_structs["airports"],data["ORIGEN"], (tupla[0], tupla[1] ,tupla[2] + 1, tupla[3]))
            tupla = me.getValue(mp.get(data_structs["airports"],data["DESTINO"]))
            mp.put(data_structs["airports"],data["DESTINO"], (tupla[0], tupla[1] , tupla[2] + 1, tupla[3]))
            """
            
            gr.addEdge(data_structs["cargaDistancia"],data["ORIGEN"], data["DESTINO"], distance)
            gr.addEdge(data_structs["cargaTiempo"],data["ORIGEN"], data["DESTINO"], float(data["TIEMPO_VUELO"]))
            
        elif data["TIPO_VUELO"] == "AVIACION_COMERCIAL":
            me.getValue(mp.get(data_structs["airports"],data["ORIGEN"]))["concurrencia_comercial"] += 1
            me.getValue(mp.get(data_structs["airports"],data["DESTINO"]))["concurrencia_comercial"] += 1 
            """
            tupla = me.getValue(mp.get(data_structs["airports"],data["ORIGEN"]))
            mp.put(data_structs["airports"],data["ORIGEN"], (tupla[0], tupla[1]+1 ,tupla[2], tupla[3]))
            tupla = me.getValue(mp.get(data_structs["airports"],data["DESTINO"]))
            mp.put(data_structs["airports"],data["DESTINO"], (tupla[0], tupla[1]+1, tupla[2], tupla[3]))
            """
            
            gr.addEdge(data_structs["comercialDistancia"],data["ORIGEN"], data["DESTINO"], distance)
            gr.addEdge(data_structs["comercialTiempo"],data["ORIGEN"], data["DESTINO"], float(data["TIEMPO_VUELO"]))
            
        else:
            
            me.getValue(mp.get(data_structs["airports"],data["ORIGEN"]))["concurrencia_militar"] += 1
            me.getValue(mp.get(data_structs["airports"],data["DESTINO"]))["concurrencia_militar"] += 1 
            """
            tupla = me.getValue(mp.get(data_structs["airports"],data["ORIGEN"]))
            mp.put(data_structs["airports"],data["ORIGEN"], (tupla[0], tupla[1] ,tupla[2], tupla[3]+1))
            tupla = me.getValue(mp.get(data_structs["airports"],data["DESTINO"]))
            mp.put(data_structs["airports"],data["DESTINO"], (tupla[0], tupla[1], tupla[2], tupla[3]+1))
            """
            
            gr.addEdge(data_structs["militarDistancia"],data["ORIGEN"], data["DESTINO"], distance)
            gr.addEdge(data_structs["militarTiempo"],data["ORIGEN"], data["DESTINO"], float(data["TIEMPO_VUELO"]))
    
    
def coversine(lat1,lat2, long1, long2):
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    long1 = math.radians(long1)
    long2 = math.radians(long2)
    
    a = (math.sin((lat2-lat1)/2))**2 + math.cos(lat1)*math.cos(lat2)*((math.sin((long2-long1)/2))**2)
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = 6371 * c
    return d

def getSortedList(data_structs):
    aeropuertos_mas_concurridos_militar = lt.newList("ARRAY_LIST")
    aeropuertos_mas_concurridos_carga = lt.newList("ARRAY_LIST")
    aeropuertos_mas_concurridos_comercial = lt.newList("ARRAY_LIST")
    
    for airport in lt.iterator(mp.valueSet(data_structs["airports"])):
        if airport["concurrencia_carga"] != 0:
            lt.addLast(aeropuertos_mas_concurridos_carga, airport)
        if airport["concurrencia_comercial"] != 0:
            lt.addLast(aeropuertos_mas_concurridos_comercial, airport)
        if airport["concurrencia_militar"] != 0:  
            lt.addLast(aeropuertos_mas_concurridos_militar, airport)
            
    merg.sort(aeropuertos_mas_concurridos_carga, sort_critCM)
    merg.sort(aeropuertos_mas_concurridos_comercial, sort_critCoM)
    merg.sort(aeropuertos_mas_concurridos_militar, sort_critMM)
    
    primerosCo = lt.subList(aeropuertos_mas_concurridos_comercial, 1, 5)
    ultimosCo = lt.subList(aeropuertos_mas_concurridos_comercial, lt.size(aeropuertos_mas_concurridos_comercial)-5,5)
    
    primerosCa = lt.subList(aeropuertos_mas_concurridos_carga, 1, 5)
    ultimosCa = lt.subList(aeropuertos_mas_concurridos_carga, lt.size(aeropuertos_mas_concurridos_carga)-5,5)
    
    primerosM = lt.subList(aeropuertos_mas_concurridos_militar, 1, 5)
    ultimosM = lt.subList(aeropuertos_mas_concurridos_militar, lt.size(aeropuertos_mas_concurridos_militar)-5,5)
    
    total_vuelos = lt.size(gr.edges(data_structs["comercialDistancia"])) + lt.size(gr.edges(data_structs["cargaDistancia"])) +lt.size(gr.edges(data_structs["militarDistancia"]))
    return primerosCo, ultimosCo, primerosCa, ultimosCa, primerosM, ultimosM, lt.size(mp.keySet(data_structs["airports"])), total_vuelos
        
def sort_critCM(airport1, airport2):
    if airport1["concurrencia_carga"] > airport2["concurrencia_carga"]:
        return True
    elif airport1["concurrencia_carga"] < airport2["concurrencia_carga"]:
        return False
    else:
        return True
def sort_critCoM(airport1, airport2):
    if airport1["concurrencia_comercial"] > airport2["concurrencia_comercial"]:
        return True
    elif airport1["concurrencia_comercial"] < airport2["concurrencia_comercial"]:
        return False
    else:
        return True
    
def sort_critMM(airport1, airport2):
    if airport1["concurrencia_militar"] > airport2["concurrencia_militar"]:
        return True
    elif airport1["concurrencia_militar"] < airport2["concurrencia_militar"]:
        return False
    else:
        return True
"""
def importanceAirports(data_structs):
    mp.put(data_structs["airports_importance"], "militar", om.newMap(omaptype="RBT", cmpfunction=cmpFunctionConcurrencia))
    mp.put(data_structs["airports_importance"], "carga", om.newMap(omaptype="RBT", cmpfunction=cmpFunctionConcurrencia))
    mp.put(data_structs["airports_importance"], "comercial", om.newMap(omaptype="RBT", cmpfunction=cmpFunctionConcurrencia))
    
    for key in lt.iterator(mp.keySet(data_structs["airports"])):
        existsFrequency = om.contains(me.getValue(mp.get(data_structs["airports_importance"], "militar")),me.getValue(mp.get(data_structs["airports"], key))[3])
        if not existsFrequency:
            om.put(me.getValue(mp.get(data_structs["airports_importance"], "militar")),me.getValue(mp.get(data_structs["airports"], key))[3], lt.newList("ARRAY_LIST") )
    
        lt.addLast(me.getValue(om.get(me.getValue(mp.get(data_structs["airports_importance"], "militar")),me.getValue(mp.get(data_structs["airports"], key))[3])),me.getValue(mp.get(data_structs["airports"], key))[0])

        existsFrequency = om.contains(me.getValue(mp.get(data_structs["airports_importance"], "carga")),me.getValue(mp.get(data_structs["airports"], key))[2])
        if not existsFrequency:
            om.put(me.getValue(mp.get(data_structs["airports_importance"], "carga")),me.getValue(mp.get(data_structs["airports"], key))[2], lt.newList("ARRAY_LIST") )
    
        lt.addLast(me.getValue(om.get(me.getValue(mp.get(data_structs["airports_importance"], "carga")),me.getValue(mp.get(data_structs["airports"], key))[2])),me.getValue(mp.get(data_structs["airports"], key))[0])

        existsFrequency = om.contains(me.getValue(mp.get(data_structs["airports_importance"], "comercial")),me.getValue(mp.get(data_structs["airports"], key))[1])
        if not existsFrequency:
            om.put(me.getValue(mp.get(data_structs["airports_importance"], "comercial")),me.getValue(mp.get(data_structs["airports"], key))[1], lt.newList("ARRAY_LIST") )
    
        lt.addLast(me.getValue(om.get(me.getValue(mp.get(data_structs["airports_importance"], "comercial")),me.getValue(mp.get(data_structs["airports"], key))[1])),me.getValue(mp.get(data_structs["airports"], key))[0])

    concurridosMilitar = om.values(me.getValue(mp.get(data_structs["airports_importance"], "militar")), me.getValue(mp.get(data_structs["airports_importance"], "militar"))["root"], om.maxKey(me.getValue(mp.get(data_structs["airports_importance"], "militar"))))
    concurridosCarga = om.values(me.getValue(mp.get(data_structs["airports_importance"], "carga")), me.getValue(mp.get(data_structs["airports_importance"], "carga"))["root"], om.maxKey(me.getValue(mp.get(data_structs["airports_importance"], "carga"))))
    concurridosComercial = om.values(me.getValue(mp.get(data_structs["airports_importance"], "comercial")), me.getValue(mp.get(data_structs["airports_importance"], "comercial"))["root"], om.maxKey(me.getValue(mp.get(data_structs["airports_importance"], "comercial"))))
    total_militar= lt.newList("ARRAY_LIST")
    total_carga = lt.newList("ARRAY_LIST")
    total_comercial = lt.newList("ARRAY_LIST")
    
    for value in lt.iterator(concurridosMilitar):
        for offer in lt.iterator(value):
            lt.addLast(total_militar, offer)
    for value in lt.iterator(concurridosCarga):
        for offer in lt.iterator(value):
            lt.addLast(total_carga, offer)
    for value in lt.iterator(concurridosComercial):
        for offer in lt.iterator(value):
            lt.addLast(total_comercial, offer)
            
        
    
    maximo = om.maxKey(me.getValue(mp.get(data_structs["airports_importance"], "comercial")))
    minimo  = om.minKey(me.getValue(mp.get(data_structs["airports_importance"], "comercial")))
    variabel = 0
    
# Funciones para creacion de datos
"""
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
    distance1 = None
    origen = None
    distance2 = None
    destino = None
    
    for airport in lt.iterator(mp.valueSet(data_structs["airports"])):
        distance_i = coversine(latitud_origen, float(airport["LATITUD"]), longitud_origen, float(airport["LONGITUD"]))
        distance_ii = coversine(latitud_destino, float(airport["LATITUD"]), longitud_destino, float(airport["LONGITUD"]))
        
        if distance1 == None:
            distance1 = distance_i
            origen = airport["ICAO"]
        
        if distance_i < distance1:
            distance1 = distance_i
            origen = airport["ICAO"]
            
        if distance2 == None:
            distance2 = distance_ii
            destino = airport["ICAO"]
        
        if distance_ii < distance2:
            distance2 = distance_ii
            destino = airport["ICAO"]
    
    
    if distance1 > 30:
        return False, distance1, distance2, origen, destino, False, False
    
    if distance2 > 30:
        return False, distance1, distance2, origen, destino, False, False
    
    
    search = bfs.BreathFirstSearch(data_structs["comercialDistancia"], origen)
    vertex = bfs.bfsVertex(search, data_structs["comercialDistancia"], origen)
    
    camino = bfs.pathTo(search, destino)
    if camino == None:
        return False, False, False, False, origen, destino, False
    
    vertices = lt.newList("ARRAY_LIST")
    for i in range(st.size(camino)):
        tope = st.pop(camino)
        lt.addLast(vertices, tope)
    
    conteo = 1
    kilometros_camino = 0
    trayectory_time = 0
    trayectories_times = lt.newList("ARRAY_LIST")
    lt.addLast(trayectories_times, 0)
    for airport in lt.iterator(vertices):
        if conteo < lt.size(vertices):
            edgeD = gr.getEdge(data_structs["comercialDistancia"], airport, lt.getElement(vertices, conteo+1))
            edgeT = gr.getEdge(data_structs["comercialTiempo"], airport, lt.getElement(vertices, conteo+1))
            
            
            kilometros_camino += float(edgeD["weight"])
            trayectory_time += float(edgeT["weight"])
            lt.addLast(trayectories_times, float(edgeT["weight"]))
        conteo +=1
    
    
    trayectory_sequence = lt.newList("ARRAY_LIST")
    for airport in lt.iterator(vertices):
        lt.addLast(trayectory_sequence, me.getValue(mp.get(data_structs["airports"], airport)))
    
    variable = 0
    return kilometros_camino, distance1, distance2, lt.size(vertices), trayectory_time, trayectory_sequence, trayectories_times

    
    
            
    


def req_2(data_structs, latitud_origen, longitud_origen, latitud_destino, longitud_destino):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    distance1 = None
    origen = None
    distance2 = None
    destino = None
    
    #Conversion de coordenadas
    for airport in lt.iterator(mp.valueSet(data_structs["airports"])):
        distance_i = coversine(latitud_origen, float(airport["LATITUD"]), longitud_origen, float(airport["LONGITUD"]))
        distance_ii = coversine(latitud_destino, float(airport["LATITUD"]), longitud_destino, float(airport["LONGITUD"]))
        
        if distance1 == None:
            distance1 = distance_i
            origen = airport["ICAO"]
        
        if distance_i < distance1:
            distance1 = distance_i
            origen = airport["ICAO"]
            
        if distance2 == None:
            distance2 = distance_ii
            destino = airport["ICAO"]
        
        if distance_ii < distance2:
            distance2 = distance_ii
            destino = airport["ICAO"]
    
    
    if distance1 > 30:
        return False, distance1, distance2, origen, destino, False
    
    if distance2 > 30:
        return False, distance1, distance2, origen, destino, False
    
    
    search = bfs.BreathFirstSearch(data_structs["comercialDistancia"], origen)
    vertex = bfs.bfsVertex(search, data_structs["comercialDistancia"], origen)
    
    
    
    camino = bfs.pathTo(search, destino)
    if camino == None:
        return False, False, False, False, origen, destino

    
    vertices = lt.newList("ARRAY_LIST")
    for i in range(st.size(camino)):
        tope = st.pop(camino)
        lt.addLast(vertices, tope)
    
    conteo = 1
    kilometros_camino = 0
    trayectory_time = 0
    for airport in lt.iterator(vertices):
        if conteo < lt.size(vertices):
            #Retorna los arcos
            edgeD = gr.getEdge(data_structs["comercialDistancia"], airport, lt.getElement(vertices, conteo+1))
            edgeT = gr.getEdge(data_structs["comercialTiempo"], airport, lt.getElement(vertices, conteo+1))
            
            
            kilometros_camino += float(edgeD["weight"])
            trayectory_time += float(edgeT["weight"])
        conteo +=1
    
    
    trayectory_sequence = lt.newList("ARRAY_LIST")
    for airport in lt.iterator(vertices):
     
        
        lt.addLast(trayectory_sequence, me.getValue(mp.get(data_structs["airports"], airport)))
    
    variable = 0
    return kilometros_camino, distance1, distance2, lt.size(vertices), trayectory_time, trayectory_sequence


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    lista_bono= lt.newList("ARRAY_LIST")
    grafo= data_structs["comercialDistancia"]
    mapa=data_structs["airports"] 
    valor=mp.valueSet(mapa)
    ICAO,mayor=mayor_concurrencia(valor)
    busqueda= prim.PrimMST(grafo,ICAO)
    costo_total= prim.weightMST(grafo,busqueda)
    
    #else:
    contador=0    
        #respuesta="nooooo"
    for aeropuerto in lt.iterator(mp.keySet(data_structs["airports"])):
        lista_caminos= lt.newList("ARRAY_LIST")
        if hasPathToMST(busqueda, aeropuerto):
            camino = pathToMST(busqueda, aeropuerto,ICAO)
            suma=0
            if camino != False:
                contador += 1
                pathlen = st.size(camino)
                print('El camino desde ',ICAO," hasta", aeropuerto,"es de longitud:", str(pathlen), "\n")
                while (not st.isEmpty(camino)):
                    stop = st.pop(camino)
                    lt.addLast(lista_caminos,stop)
                lista_aero=[]
                for i in lt.iterator(lista_caminos):
                    
                    ICAO_origen= i["vertexA"]
                    info_origen= me.getValue(mp.get(mapa,ICAO_origen))
                    ICAO_destino= i["vertexB"]
                    info_destino= me.getValue(mp.get(mapa,ICAO_destino))
                    i["Nombre_origen"]=info_origen["NOMBRE"]
                    i["Pais_origen"]= info_origen["PAIS"]
                    i["Ciudad_origen"]= info_origen["CIUDAD"]
                    i["Pais_destino"]= info_destino["PAIS"]
                    i["Nombre_destino"]= info_destino["NOMBRE"]
                    i["Ciudad_destino"]= info_destino["CIUDAD"]
                    suma += i["weight"]
                    lista_aero.append(ICAO_origen)
                lista_aero.append(aeropuerto)
                        #print(info_origen,info_destino)
                lt.addLast(lista_bono,lista_aero)
                print("la distancia total del camino es: ",suma,"km" "\n")   
                imprimir=[]
                headers= ["Origen", "Nombre Origen","Pais O","Ciudad O","Destino", "Nombre Destino","Pais D","Ciudad D","distancia",]
    
                llaves=["vertexA","Nombre_origen","Pais_origen","Ciudad_origen","vertexB","Nombre_destino","Pais_destino","Ciudad_destino","weight"]
                    #elemento1=lt.lastElement(lista_imp)
                for j in lt.iterator(lista_caminos):
                    provisional=[]
                    for k in llaves:
                        provisional.append(j[k])
                    imprimir.append(provisional)
                print(tabulate(imprimir,headers=headers),"\n")
    
            else:
                print('No hay camino')
                
    
 
    return contador,costo_total, lista_bono




def mayor_concurrencia(lista):
    mayor=0
    ICAO= None
    for aeropuerto in lt.iterator(lista):
        if aeropuerto["concurrencia_comercial"]> mayor:
            mayor= aeropuerto["concurrencia_comercial"]
            ICAO = aeropuerto["ICAO"]
        if aeropuerto["concurrencia_comercial"] != 0 and aeropuerto["concurrencia_comercial"] == mayor:
            if aeropuerto["ICAO"] > ICAO:
                mayor= aeropuerto["concurrencia_comercial"]
                ICAO = aeropuerto["ICAO"]
    return ICAO, mayor

def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    airports = gr.vertices(data_structs["cargaDistancia"])
    
    maximo = None
    airportMC = None
    iguales =lt.newList("ARRAY_LIST")
    for airport in lt.iterator(airports):
        if maximo == None:
            maximo = gr.indegree(data_structs["cargaDistancia"], airport) + gr.outdegree(data_structs["cargaDistancia"], airport)
            airportMC = airport
        
        maximo_i = gr.indegree(data_structs["cargaDistancia"], airport) + gr.outdegree(data_structs["cargaDistancia"], airport)
        
        
        if maximo_i > maximo:
            iguales = lt.newList("ARRAY_LIST")
            maximo = maximo_i
            airportMC = airport
            lt.addLast(iguales, airport)
            
        elif maximo_i == maximo:
            lt.addLast(iguales, airport)
    
    if lt.size(iguales) > 1:
        merg.sort(iguales, sort_critAlfabeticamente)
        airportMC = lt.getElement(iguales, 1)
    trayectos = lt.newList("ARRAY_LIST")
    searchi = prim.PrimMST(data_structs["cargaTiempo"], airportMC)
    searchii = prim.PrimMST(data_structs["cargaDistancia"], airportMC)
    
    for airport in lt.iterator(mp.keySet(data_structs["airports"])):
        if hasPathToMST(searchii, airport):
            path = pathToMST(searchii, airport, airportMC)
            if path != False:
                lt.addLast(trayectos, path)
    
    paths = lt.newList("ARRAY_LIST")
    for path in lt.iterator(trayectos):
        lstProvisional = lt.newList("ARRAY_LIST")
        lstProvisional2 = lt.newList("ARRAY_LIST")
        conteo = 1
       
        for arco in lt.iterator(path):
            if conteo == 1:
                lt.addLast(lstProvisional, arco["vertexB"])
                lt.addLast(lstProvisional, arco["vertexA"])
            else:
                lt.addLast(lstProvisional, arco["vertexA"])
            
            conteo += 1
                
        for i in range(lt.size(lstProvisional), 0, -1):
            lt.addLast(lstProvisional2, lt.getElement(lstProvisional,i))
        
        if not lt.isEmpty(lstProvisional2):
            lt.addLast(paths, lstProvisional2)
    
    distancia_total_trayectos = 0
    trayectos = lt.newList("ARRAY_LIST")
    
    for path in lt.iterator(paths):
        
        trayectory_time = 0
        kilometros_camino = 0
        tipo_aeronave = lt.newList("ARRAY_LIST")
        conteo = 1
        for airport in lt.iterator(path):
            
            if conteo < lt.size(path):
                
                flight_info = me.getValue(mp.get(data_structs["flights"], f"{airport}_{lt.getElement(path, conteo+1)}_AVIACION_CARGA"))
                edgeD = gr.getEdge(data_structs["cargaDistancia"], airport, lt.getElement(path, conteo+1))
                edgeT = gr.getEdge(data_structs["cargaTiempo"], airport, lt.getElement(path, conteo+1))
                lt.addLast(tipo_aeronave, flight_info["TIPO_AERONAVE"])
            
                kilometros_camino += float(edgeD["weight"])
                trayectory_time += float(edgeT["weight"])
            conteo += 1
        lt.addLast(path, str(kilometros_camino))
        
            
        distancia_total_trayectos += kilometros_camino
        
        trayecto = (lt.getElement(path, 1), lt.getElement(path, lt.size(path)-1), trayectory_time, kilometros_camino, tipo_aeronave)
        
        lt.addLast(trayectos, trayecto)
    
    merg.sort(trayectos, sort_crit_trayectos)
    merg.sort(paths, sort_crit_paths)
    return trayectos, paths, airportMC, distancia_total_trayectos, prim.weightMST(data_structs["cargaDistancia"], searchii), lt.size(paths)
    total_distancia = prim.weightMST(data_structs["cargaTiempo"], searchii)
    total_tiempo = prim.weightMST(data_structs["cargaDistancia"], searchi)
    
    
    

"""
    print(airportMC, maximo)
    print(lt.size(iguales))
    
    if lt.size(iguales) > 1:
        merg.sort(iguales, sort_critAlfabeticamente)
        airportMC = lt.getElement(iguales, 1)
    
    search = djk.Dijkstra(data_structs["cargaDistancia"], airportMC)
    trayectos = lt.newList("ARRAY_LIST")
    
    for airport in lt.iterator(mp.keySet(data_structs["airports"])):
        if djk.hasPathTo(search, airport):
            lt.addLast(trayectos, djk.pathTo(search, airport))


        
        
    
        
    
    
    paths = lt.newList("ARRAY_LIST")
    for path in lt.iterator(trayectos):
        lstProvisional = lt.newList("ARRAY_LIST")
        lstProvisional2 = lt.newList("ARRAY_LIST")
        conteo = 1
       
        for arco in lt.iterator(path):
            if conteo == 1:
                lt.addLast(lstProvisional, arco["vertexB"])
                lt.addLast(lstProvisional, arco["vertexA"])
            else:
                lt.addLast(lstProvisional, arco["vertexA"])
            
            conteo += 1
                
        for i in range(lt.size(lstProvisional), 0, -1):
            lt.addLast(lstProvisional2, lt.getElement(lstProvisional,i))
        
        if not lt.isEmpty(lstProvisional2):
            lt.addLast(paths, lstProvisional2)
    
    distancia_total_trayectos = 0
    trayectos = lt.newList("ARRAY_LIST")
    
    for path in lt.iterator(paths):
        
        trayectory_time = 0
        kilometros_camino = 0
        tipo_aeronave = lt.newList("ARRAY_LIST")
        conteo = 1
        for airport in lt.iterator(path):
            
            if conteo < lt.size(path):
                
                flight_info = me.getValue(mp.get(data_structs["flights"], f"{airport}_{lt.getElement(path, conteo+1)}_AVIACION_CARGA"))
                edgeD = gr.getEdge(data_structs["cargaDistancia"], airport, lt.getElement(path, conteo+1))
                edgeT = gr.getEdge(data_structs["cargaTiempo"], airport, lt.getElement(path, conteo+1))
                lt.addLast(tipo_aeronave, flight_info["TIPO_AERONAVE"])
            
                kilometros_camino += float(edgeD["weight"])
                trayectory_time += float(edgeT["weight"])
            conteo += 1
        
        
            
        distancia_total_trayectos += kilometros_camino
        
        trayecto = (lt.getElement(path, 1), lt.getElement(path, lt.size(path)), trayectory_time, kilometros_camino, tipo_aeronave)
        
        lt.addLast(trayectos, trayecto)
    
    return trayectos, paths, airportMC, distancia_total_trayectos
        
        
    variable = 0
    """
    
def sort_crit_trayectos(trayecto1, trayecto2):
    if trayecto1[3] > trayecto2[3]:
        return True
    elif trayecto1[3] < trayecto2[3]:
        return  False
    else:
        return True
def sort_crit_paths(path1, path2):
    if float(lt.getElement(path1, lt.size(path1))) > float(lt.getElement(path2, lt.size(path2))):
        return True
    elif float(lt.getElement(path1, lt.size(path1))) < float(lt.getElement(path2, lt.size(path2))):
        return False
    else:
        return True
    
def sort_critAlfabeticamente(airport1, airport2):
    if airport1 < airport2:
        return True
    elif airport1 > airport2:
        return False
    else:
        return True
    

def pathToMST(search, destino, source):
    puntoB = mp.get(search["edgeTo"], destino)
    if puntoB == None:
        return False
    else:
        
        nombreB = me.getValue(puntoB)["vertexA"]
        camino = st.newStack()
        notfound = True
        while notfound == True:
            if puntoB == None:
                if nombreB == source:
                    notfound = False
                else:
                    notfound = None
            elif puntoB != None:
                st.push(camino, me.getValue(puntoB))
                puntoB = mp.get(search["edgeTo"], me.getValue(puntoB)["vertexA"])
                if puntoB != None:
                    nombreB = me.getValue(puntoB)["vertexA"]
        if notfound == None:
            return False
        else:
            return camino
    

def hasPathToMST(search, destino):
    if mp.get(search["edgeTo"], destino):
        return True
    else:
        return False
    

def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    mayor = 0
    nombre_mayor = ""
    trayectos_posibles = 0
    
    
    for airport in lt.iterator(mp.valueSet(data_structs["airports"])):
        if int(airport["concurrencia_militar"]) > int(mayor):
            mayor = airport["concurrencia_militar"]
            nombre_mayor = airport["ICAO"]
            
    
    search = prim.PrimMST(data_structs["militarTiempo"], nombre_mayor)
    #suma de kilometros por arcos
    kilometros_totales = prim.weightMST(data_structs["militarDistancia"], search)
    
    
    caminos = lt.newList("ARRAY_LIST")
    nombres_aeropuertos = lt.newList("ARRAY_LIST")
    trayectory_sequence = lt.newList("ARRAY_LIST")
    
    total_weights = lt.newList("ARRAY_LIST")
    
    
    for airport_search in lt.iterator(mp.keySet(data_structs["airports"])):
        
        #ES UN STACK
        camino = pathToMST(search, airport_search, nombre_mayor )
        
        
        #Guarda el camino desde el aeropuerto mayor a el aeropuerto de la iteracion
        if camino !=False:
            camino_actual = lt.newList("ARRAY_LIST")
            size_total = 0
            
            while not st.isEmpty(camino):
                tope = st.pop(camino)
                vertice_anadir = me.getValue(mp.get(data_structs["airports"], tope['vertexB']))
                lt.addLast(camino_actual, vertice_anadir)
                size_total += tope['weight']
                
            
            lt.addFirst(camino_actual, me.getValue(mp.get(data_structs["airports"], nombre_mayor)))
            lt.addLast(caminos, camino_actual)
            lt.addLast(total_weights, size_total)
            trayectos_posibles +=1
            
           
            
          
            
        """
        for camino in lt.iterator(caminos):
            trayectory = lt.newList("ARRAY_LIST")  
            for airport in lt.iterator(camino):
                airport_info = me.getValue(mp.get(data_structs["airports"], airport))
                lt.addLast(trayectory, airport_info)
                
            lt.addLast(trayectory_sequence, trayectory)
            
        """       
        
    nombre_mayor = me.getValue(mp.get(data_structs["airports"], nombre_mayor))


    return nombre_mayor, kilometros_totales, nombres_aeropuertos, trayectos_posibles, caminos, total_weights
        
    
   
            
def pathToMST(search, destino, source):
    puntoB = mp.get(search["edgeTo"], destino)
    if puntoB == None:
        return False
    else:
        
        nombreB = me.getValue(puntoB)["vertexA"]
        camino = st.newStack()
        notfound = True
        while notfound == True:
            if puntoB == None:
                if nombreB == source:
                    notfound = False
                else:
                    notfound = None
            elif puntoB != None:
                st.push(camino, me.getValue(puntoB))
                puntoB = mp.get(search["edgeTo"], me.getValue(puntoB)["vertexA"])
                if puntoB != None:
                    nombreB = me.getValue(puntoB)["vertexA"]
        if notfound == None:
            return False
        else:
            return camino
    

def hasPathToMST(search, destino):
    if mp.get(search["edgeTo"], destino):
        return True
    else:
        return False 
    


def req_6(data_structs,M):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    lista_bono=lt.newList("ARRAY_LIST")
    grafo= data_structs["comercialDistancia"]
    mapa=data_structs["airports"]
    lista= mp.valueSet(mapa)
    mayor,ICAO,lista_final= mayor_concurrencia_req6(lista)
    info_mayor= mp.get(mapa,ICAO)
    valor=me.getValue(info_mayor)
    #lista_caminos=lt.newList("ARRAY_LIST")
    ordenada= merg.sort(lista_final,sort_crit_req6)
    lista_aeropuertos= lt.newList("ARRAY_LIST") 
    while lt.size(lista_aeropuertos)< M and not lt.isEmpty(ordenada):
        elemento = lt.removeFirst(ordenada)
        lt.addLast(lista_aeropuertos, elemento)
        
    if lt.size(lista_aeropuertos) <M:
        print("Hay menoooos:(")   
    #MST= prim.PrimMST(grafo,ICAO)
    algoritmo=djk.Dijkstra(grafo, ICAO)
    for element in lt.iterator(lista_aeropuertos):
        lista_imp=lt.newList("ARRAY_LIST")
        vertice= element["ICAO"]
        if djk.hasPathTo(algoritmo,vertice):
            camino= djk.pathTo(algoritmo,vertice)
            suma= 0
            if camino is not None:
                pathlen = st.size(camino)
                print('El camino desde ',ICAO," hasta", vertice,"es de longitud:", str(pathlen), "\n")
                while (not st.isEmpty(camino)):
                    stop = st.pop(camino)
                    lt.addLast(lista_imp,stop)
                lista_aero=[]
                for i in lt.iterator(lista_imp):
                    ICAO_origen= i["vertexA"]
                    info_origen= me.getValue(mp.get(mapa,ICAO_origen))
                    ICAO_destino= i["vertexB"]
                    info_destino= me.getValue(mp.get(mapa,ICAO_destino))
                    i["Nombre_origen"]=info_origen["NOMBRE"]
                    i["Pais_origen"]= info_origen["PAIS"]
                    i["Ciudad_origen"]= info_origen["CIUDAD"]
                    i["Pais_destino"]= info_destino["PAIS"]
                    i["Nombre_destino"]= info_destino["NOMBRE"]
                    i["Ciudad_destino"]= info_destino["CIUDAD"]
                    suma += i["weight"]
                    lista_aero.append(ICAO_origen)
                lista_aero.append(vertice)
                        #print(info_origen,info_destino)
                lt.addLast(lista_bono,lista_aero)
                        #print(info_origen,info_destino)
                print("la distancia total del camino es: ",suma,"km" "\n")   
                imprimir=[]
                headers= ["Origen", "Nombre Origen","Pais O","Ciudad O","Destino", "Nombre Destino","Pais D","Ciudad D","distancia",]
    
                llaves=["vertexA","Nombre_origen","Pais_origen","Ciudad_origen","vertexB","Nombre_destino","Pais_destino","Ciudad_destino","weight"]
                    #elemento1=lt.lastElement(lista_imp)
                for j in lt.iterator(lista_imp):
                    provisional=[]
                    for k in llaves:
                        provisional.append(j[k])
                    imprimir.append(provisional)
                print(tabulate(imprimir,headers=headers),"\n")
    
            else:
                print('No hay camino')
            #print(camino,"\n")

    
    return valor,suma,lista_bono  
        
def densidad(grafo):
    V = lt.size(gr.vertices(grafo))
    E = lt.size(gr.edges(grafo))
    densidad = E /((V)*(V-1))
    return V, E, densidad
    

def mayor_concurrencia_req6(lista):
    mayor=0
    ICAO= None
    lista_nueva= lt.newList("ARRAY_LIST")
    for aeropuerto in lt.iterator(lista):
        if aeropuerto["PAIS"] == "Colombia" and aeropuerto["concurrencia_comercial"] != 0:
            lt.addLast(lista_nueva,aeropuerto)

        if aeropuerto["PAIS"] == "Colombia" and aeropuerto["concurrencia_comercial"]> mayor:
            mayor= aeropuerto["concurrencia_comercial"]
            ICAO = aeropuerto["ICAO"]
        if aeropuerto["PAIS"] == "Colombia"and aeropuerto["concurrencia_comercial"] != 0 and aeropuerto["concurrencia_comercial"] == mayor:
            if aeropuerto["ICAO"] > ICAO:
                mayor= aeropuerto["concurrencia_comercial"]
                ICAO = aeropuerto["ICAO"]
    return mayor,ICAO,lista_nueva
def req_7(data_structs, latitud_origen, longitud_origen, latitud_destino, longitud_destino):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    distance1 = None
    origen = None
    distance2 = None
    destino = None
    
    for airport in lt.iterator(mp.valueSet(data_structs["airports"])):
        distance_i = coversine(latitud_origen, float(airport["LATITUD"]), longitud_origen, float(airport["LONGITUD"]))
        distance_ii = coversine(latitud_destino, float(airport["LATITUD"]), longitud_destino, float(airport["LONGITUD"]))
        
        if distance1 == None:
            distance1 = distance_i
            origen = airport["ICAO"]
        
        if distance_i < distance1:
            distance1 = distance_i
            origen = airport["ICAO"]
            
        if distance2 == None:
            distance2 = distance_ii
            destino = airport["ICAO"]
        
        if distance_ii < distance2:
            distance2 = distance_ii
            destino = airport["ICAO"]
    
    
    if distance1 > 30:
        return False, distance1, distance2, origen, destino
    
    if distance2 > 30:
        return False, distance1, distance2, origen, destino
    
    search = djk.Dijkstra(data_structs["comercialTiempo"], origen)
    
    
    if djk.hasPathTo(search, destino):
        camino = djk.pathTo(search, destino)
        conteo = 1
        lista_provisional = lt.newList("ARRAY_LIST")
        path = lt.newList("ARRAY_LIST")
        
        trayectory_time = 0
        path_distance = 0
        
        for edge in lt.iterator(camino):
            
            if conteo == 1:
                lt.addLast(lista_provisional, edge["vertexB"])
                lt.addLast(lista_provisional, edge["vertexA"])
            else:
                lt.addLast(lista_provisional, edge["vertexA"])
            conteo +=1
        for i in range(lt.size(lista_provisional), 0, -1):
            lt.addLast(path, lt.getElement(lista_provisional, i))
        
        airports_sequence = lt.newList("ARRAY_LIST")
        conteo = 1
        for airport in lt.iterator(path):
            if conteo < lt.size(path):
                
                #flight_info = me.getValue(mp.get(data_structs["flights"], f"{airport}_{lt.getElement(path, conteo+1)}_AVIACION_COMERCIAL"))
                
                edgeD = gr.getEdge(data_structs["comercialDistancia"], airport, lt.getElement(path, conteo+1))
                edgeT = gr.getEdge(data_structs["comercialTiempo"], airport, lt.getElement(path, conteo+1))
                
                edgeTbefore = gr.getEdge(data_structs["comercialTiempo"], lt.getElement(path, conteo-1), lt.getElement(path, conteo))
                #lt.addLast(airports_sequence, (me.getValue(mp.get(data_structs["airports"],airport)),edgeT["weight"]))
                
            
                path_distance += float(edgeD["weight"])
                trayectory_time += float(edgeT["weight"])
            if conteo != 1 and conteo != lt.size(path):
                lt.addLast(airports_sequence, (me.getValue(mp.get(data_structs["airports"],airport)),edgeTbefore["weight"]))
            elif conteo == 1:
                lt.addLast(airports_sequence, (me.getValue(mp.get(data_structs["airports"],airport)), 0))
            else:
                lt.addLast(airports_sequence, (me.getValue(mp.get(data_structs["airports"],airport)), edgeT["weight"]))
            conteo += 1
            
        return trayectory_time, path_distance, path_distance + distance1 +distance2, lt.size(path), airports_sequence
            
            
        
    else:
        return origen, False, False, False, destino


def req_8(data_structs):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    pass


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

# Funciones de ordenamiento


def sort_crit_req6(aeropuerto1, aeropuerto2):
    if aeropuerto1["concurrencia_comercial"] > aeropuerto2["concurrencia_comercial"]:
        return True
    elif aeropuerto1["concurrencia_comercial"] < aeropuerto2["concurrencia_comercial"]:
        return False
    else:
        if aeropuerto1["ICAO"] > aeropuerto2["ICAO"]:
            return True
        elif aeropuerto1["ICAO"] < aeropuerto2["ICAO"]:
            return False
        else: 
            return True
        

def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass
