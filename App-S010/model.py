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

from haversine import haversine,Unit
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
    data_structs={}
    #mapas con los datos
    data_structs["map_aeropuertos"]= mp.newMap(numelements=109, maptype="CHAINING", loadfactor=4)
    data_structs["map_vuelos"]= mp.newMap(numelements=757, maptype="CHAINING", loadfactor=4)
    #grafos
    data_structs["comercial_dist"]= gr.newGraph(datastructure="ADJ_LIST", directed=True)
    data_structs["comercial_time"]= gr.newGraph(datastructure="ADJ_LIST", directed=True)
    
    data_structs["carga_dist"]= gr.newGraph(datastructure="ADJ_LIST", directed=True)
    data_structs["carga_time"]= gr.newGraph(datastructure="ADJ_LIST", directed=True)
    
    data_structs["militar_dist"]= gr.newGraph(datastructure="ADJ_LIST", directed=True)
    data_structs["militar_time"]= gr.newGraph(datastructure="ADJ_LIST", directed=True)
    #Listas de concurrencia para cada areopuerto
    data_structs["conc_comercial"]=lt.newList("ARRAY_LIST")
    data_structs["conc_carga"]=lt.newList("ARRAY_LIST")
    data_structs["conc_militar"]=lt.newList("ARRAY_LIST")

    return data_structs

# Funciones para agregar informacion al modelo

def add_data(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    pass


def add_map_aeropuertos(data_structs, aerop):
    """
    Función para agregar areopuertos al mapa
    """
    #Modificar latitud y longitud para que luego se puedan usar para calcular la distancia
    latitud=str(aerop["LATITUD"])
    longitud=aerop["LONGITUD"]
    aerop["LATITUD"]=float(latitud.replace(",","."))
    aerop["LONGITUD"]= float(longitud.replace(",","."))

    mp.put(data_structs["map_aeropuertos"],aerop["ICAO"], aerop)
    
    add_areopuertos_grafos(data_structs,aerop["ICAO"])
    
    return data_structs

def add_map_vuelos(data_structs, vuelo):
    """
    Función para agregar vuelos al mapa
    """
    origen=str(vuelo["ORIGEN"])
    destino=str(vuelo["DESTINO"])
    tipo=str(vuelo["TIPO_VUELO"])

    key="{0};{1};{2}".format(origen,destino,tipo)
    
    mp.put(data_structs["map_vuelos"],key,vuelo)
    return data_structs

def add_areopuertos_grafos(data_structs,ICAO):
    """
    Función para agregar los vértices a los grafos
    """
    gr.insertVertex(data_structs["comercial_dist"],ICAO)
    gr.insertVertex(data_structs["comercial_time"],ICAO)
    
    gr.insertVertex(data_structs["carga_dist"],ICAO)
    gr.insertVertex(data_structs["carga_time"],ICAO)
    
    gr.insertVertex(data_structs["militar_dist"],ICAO)
    gr.insertVertex(data_structs["militar_time"],ICAO)


def terminar_carga_datos(data_structs):

    add_vuelos_grafos(data_structs)

    add_concurrencia_aerop(data_structs)

    data_structs["conc_comercial"]= sort_concurrencia(data_structs["conc_comercial"])
    data_structs["conc_carga"]=sort_concurrencia(data_structs["conc_carga"])
    data_structs["conc_militar"]=sort_concurrencia(data_structs["conc_militar"])

    first_comercial,last_comercial, first_carga,last_carga,first_militar,last_militar=imprimir_carga_datos(data_structs)
    return first_comercial,last_comercial, first_carga,last_carga,first_militar,last_militar,data_structs

def add_vuelos_grafos(data_structs):
    """
    Función para agregar los arcos a los grafos
    """
    lst_vuelos=mp.keySet(data_structs["map_vuelos"])
    for key in lt.iterator(lst_vuelos):
        vuelo=me.getValue(mp.get(data_structs["map_vuelos"],key))
        origen=vuelo["ORIGEN"]
        destino=vuelo["DESTINO"]
        tiempo= int(vuelo["TIEMPO_VUELO"])

        #encontrar los areopuertos de origen y destino
        aero_origen=me.getValue(mp.get(data_structs["map_aeropuertos"],origen))
        aero_destino=me.getValue(mp.get(data_structs["map_aeropuertos"],destino))
        #usando sus latitudes y longitudes calcular la distancia
        salida=(float(aero_origen["LATITUD"]), float(aero_origen["LONGITUD"]))
        llegada=(float(aero_destino["LATITUD"]), float(aero_destino["LONGITUD"]))

        distancia=haversine(salida,llegada)
    
        if vuelo["TIPO_VUELO"]=="AVIACION_COMERCIAL":
            gr.addEdge(data_structs["comercial_dist"],origen,destino,distancia)
            gr.addEdge(data_structs["comercial_time"],origen,destino,tiempo)
        elif vuelo["TIPO_VUELO"]=="AVIACION_CARGA":
            gr.addEdge(data_structs["carga_dist"],origen,destino,distancia)
            gr.addEdge(data_structs["carga_time"],origen,destino,tiempo)
        elif vuelo["TIPO_VUELO"]=="MILITAR":
            gr.addEdge(data_structs["militar_dist"],origen,destino,distancia)
            gr.addEdge(data_structs["militar_time"],origen,destino,tiempo)
    return data_structs

def add_concurrencia_aerop(data_structs):
    """
    Función para crear las lista de concurrencia de los areopuertos
    """
    lst_aerop=mp.keySet(data_structs["map_aeropuertos"])
  
    for aerop in lt.iterator(lst_aerop):
        airport=me.getValue(mp.get(data_structs["map_aeropuertos"],aerop))

        in_comercial=gr.indegree(data_structs["comercial_time"],aerop)
        out_comercial=gr.outdegree(data_structs["comercial_time"],aerop)

        in_carga=gr.indegree(data_structs["carga_time"],aerop)
        out_carga=gr.outdegree(data_structs["carga_time"],aerop)

        in_militar=gr.indegree(data_structs["militar_time"],aerop)
        out_militar=gr.outdegree(data_structs["militar_time"],aerop)

        conc_comercial={"aerop":airport, "conc": int(in_comercial+out_comercial)}
        conc_carga={"aerop":airport, "conc": int(in_carga+out_carga)}
        conc_militar={"aerop":airport, "conc": int(in_militar+out_militar)}

        lt.addLast(data_structs["conc_comercial"],conc_comercial)
        lt.addLast(data_structs["conc_carga"],conc_carga)
        lt.addLast(data_structs["conc_militar"],conc_militar)
    return data_structs

def imprimir_carga_datos(data_structs):

    com=lt.size(data_structs["conc_comercial"])
    first_comercial=lt.subList(data_structs["conc_comercial"],1,5)
    last_comercial=lt.subList(data_structs["conc_comercial"],com-4,5)

    car=lt.size(data_structs["conc_carga"])
    first_carga=lt.subList(data_structs["conc_carga"],1,5)
    last_carga=lt.subList(data_structs["conc_carga"],car-4,5)

    mili=lt.size(data_structs["conc_militar"])
    first_militar=lt.subList(data_structs["conc_militar"],1,5)
    last_militar=lt.subList(data_structs["conc_militar"],mili-4,5)

    return first_comercial,last_comercial, first_carga,last_carga,first_militar,last_militar

# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass

def new_vuelo(origen,ciudad_origen, destino,ciudad_destino, tipo_aeronave,
              trafico, tipo_vuelo,tiempo_vuelo):
    """
    Crea una nuevo vuelo
    """
    #TODO: Crear la función para estructurar los datos
    vuelo={"ORIGEN":origen,"CIUDAD_ORIGEN":ciudad_origen, "DESTINO":destino,
           "CIUDAD_DESTINO":ciudad_destino,"TIPO_AERONAVE": tipo_aeronave,
              "TRAFICO":trafico,"TIPO_VUELO":tipo_vuelo,"TIEMPO_VUELO":tiempo_vuelo}
    return vuelo

def new_aeropuerto(nombre,ciudad,pais,ICAO,latitud,longitud,altitud):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    
    aeropuerto={"NOMBRE":nombre,"CIUDAD":ciudad, "PAIS":pais, "ICAO":ICAO,
                "LATITUD":latitud,"LONGITUD":longitud,"ALTITUD":altitud}
    return aeropuerto


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

def aeropuerto_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    return mp.size(data_structs["map_aeropuertos"])

def vuelos_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    return mp.size(data_structs["map_vuelos"])


def get_distancia_aerop_30km(data_structs,latitud,longitud):
    """
    Funcion que encuentra el areopuerto más cercano en un rango de 30 km. Si no lo encuentra,
    retorna el areopuerto más cercano. 

    input:
        data_structs:estructura de datos
        latitud:float
        lonigud:float
    return:
        aerop_encontrado=si se ha encontrado un aeropuerto en el rango
        ans= ICAO de el areopuerto más cercano
        dist_ans: distancia entre el aeropuerto y la ubicación dada por el usuario
    """
    #TODO: Crear la función para obtener un dato de una lista
    arop_encontrado=True
    ans=""
    dist_ans=100000
    

    aerop_lst=mp.keySet(data_structs["map_aeropuertos"])
    loc_1=(latitud,longitud)
    menor_dist=100000
    areop_cercano=""
   
    for aerop in lt.iterator(aerop_lst):
        airport=me.getValue(mp.get(data_structs["map_aeropuertos"],aerop))
        loc_2=(airport["LATITUD"],airport["LONGITUD"])

        dist=abs(haversine(loc_1,loc_2))
        if dist<=30:
            if dist_ans>dist:
                dist_ans=dist
                ans=airport["ICAO"]
        else:
            if menor_dist>dist:
                menor_dist=dist
                areop_cercano=airport["ICAO"]
    if dist_ans==100000:
        arop_encontrado=False
        ans=areop_cercano
        dist_ans=menor_dist
    
    return arop_encontrado,ans,dist_ans


def req_1(data_structs,o_latitud,o_longitud,d_latitud,d_longitud):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
      
    no_airports=0
    result=lt.newList("ARRAY_LIST")
    dist_vuelos=0
    time_total=0
    

    o_encontrado,o_ICAO,o_dist=get_distancia_aerop_30km(data_structs,o_latitud,o_longitud)
    d_encontrado,d_ICAO,d_dist=get_distancia_aerop_30km(data_structs,d_latitud,d_longitud)

    if o_encontrado and d_encontrado:
        caminos=dfs.DepthFirstSearch(data_structs["comercial_dist"],o_ICAO)
        
        if dfs.hasPathTo(caminos,d_ICAO):
            path=dfs.pathTo(caminos,d_ICAO)
            
            no_airports= st.size(path)
            while st.size(path) > 0:
                aerop=st.pop(path)
                
                airport=me.getValue(mp.get(data_structs["map_aeropuertos"],aerop))
                lt.addLast(result,airport)
                
                if st.top(path):
                    dist=gr.getEdge(data_structs["comercial_dist"],aerop,st.top(path))["weight"]
                    dist_vuelos+=dist

                    time=gr.getEdge(data_structs["comercial_time"],aerop,st.top(path))["weight"]
                    time_total+=time
        else:
            lt.addLast(result,"Busqueda fallida. No existe una ruta entre los dos destinos.Aeropuertos encontrados:")
            lt.addLast(result, str(o_ICAO)+", "+str(round(o_dist,2))+" km del punto de ORIGEN")
            lt.addLast(result,str(d_ICAO)+", "+str(round(d_dist,2))+" km del punto de DESTINO")
    else:
        lt.addLast(result,"Busqueda fallida.")
        lt.addLast(result,"Aeropuerto más cercano al ORIGEN: "+str(o_ICAO)+", "+str(round(o_dist,2))+" km")
        lt.addLast(result,"Aeropuerto más cercano al DESTINO: "+str(d_ICAO)+", "+str(round(d_dist,2))+" km")

    return result,no_airports,time_total,dist_vuelos,o_dist,d_dist

def req_2(data_structs,o_latitud,o_longitud,d_latitud,d_longitud):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
      
    no_airports=0
    result=lt.newList("ARRAY_LIST")
    dist_vuelos=0
    time_total=0
    

    o_encontrado,o_ICAO,o_dist=get_distancia_aerop_30km(data_structs,o_latitud,o_longitud)
    d_encontrado,d_ICAO,d_dist=get_distancia_aerop_30km(data_structs,d_latitud,d_longitud)

    if o_encontrado and d_encontrado:
        caminos=bfs.BreathFirstSearch(data_structs["comercial_dist"],o_ICAO)
        
        if bfs.hasPathTo(caminos,d_ICAO):
            path=bfs.pathTo(caminos,d_ICAO)
            
            no_airports= st.size(path)
            while st.size(path) > 0:
                aerop=st.pop(path)
                
                airport=me.getValue(mp.get(data_structs["map_aeropuertos"],aerop))
                lt.addLast(result,airport)
                
                if st.top(path):
                    dist=gr.getEdge(data_structs["comercial_dist"],aerop,st.top(path))["weight"]
                    dist_vuelos+=dist

                    time=gr.getEdge(data_structs["comercial_time"],aerop,st.top(path))["weight"]
                    time_total+=time
        else:
            lt.addLast(result,"Busqueda fallida. No existe una ruta entre los dos destinos.Aeropuertos encontrados:")
            lt.addLast(result, str(o_ICAO)+", "+str(round(o_dist,2))+" km del punto de ORIGEN")
            lt.addLast(result,str(d_ICAO)+", "+str(round(d_dist,2))+" km del punto de DESTINO")
    else:
        lt.addLast(result,"Busqueda fallida.")
        lt.addLast(result,"Aeropuerto más cercano al ORIGEN: "+str(o_ICAO)+", "+str(round(o_dist,2))+" km")
        lt.addLast(result,"Aeropuerto más cercano al DESTINO: "+str(d_ICAO)+", "+str(round(d_dist,2))+" km")

    return result,no_airports,time_total,dist_vuelos,o_dist,d_dist

def req_3(data_structs):
    """
    Determinar la red de trayectos comerciales de cobertura máxima desde el aeropuerto con mayor concurrencia.
    """
    # TODO: Realizar el requerimiento 3
    aeropuertos_base = mp.keySet(data_structs["map_aeropuertos"])
    
    # entregables
    aerop_mayor_concurrencia = lt.getElement(data_structs["conc_comercial"], 1)
    dijkstra_mayor_conc = djk.Dijkstra(data_structs["comercial_dist"], aerop_mayor_concurrencia["aerop"]["ICAO"])
    dist_trayectos = 0
    trayectos_posibles = 0
    encontrados = lt.newList("ARRAY_LIST") 
    
    for aeropuerto in lt.iterator(aeropuertos_base):
        if djk.hasPathTo(dijkstra_mayor_conc, aeropuerto) and aeropuerto is not aerop_mayor_concurrencia["aerop"]["ICAO"]:
            
            camino_ar = djk.pathTo(dijkstra_mayor_conc, aeropuerto)  # retorna una pila de arcos
            distancia = 0
            tiempo = 0
            
            tamanio_pila = st.size(camino_ar)
            for i in range(tamanio_pila):
                edge = st.pop(camino_ar)
                distancia += edge["weight"]
                tiempo += gr.getEdge(data_structs["comercial_time"], edge["vertexA"], edge["vertexB"])["weight"]
                
            trayectos_posibles += 1
            dist_trayectos += distancia
            
            lt.addLast(encontrados, {"origen": aerop_mayor_concurrencia["aerop"], "destino": me.getValue(mp.get(data_structs["map_aeropuertos"], aeropuerto)), 
                                     "distancia": distancia, "tiempo": tiempo})
    
    return aerop_mayor_concurrencia, dist_trayectos, trayectos_posibles, encontrados
    


def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    #Importante ={"aerop":[info aerop],"concurrencia":int}
    importante= lt.getElement(data_structs["conc_carga"],1)
    dist_total=0
    no_trayectos=0
    results=lt.newList("ARRAY_LIST")

    caminos=djk.Dijkstra(data_structs["carga_dist"], importante["aerop"]["ICAO"])

    lst_aerop=mp.keySet(data_structs["map_aeropuertos"])
    
    for icao in lt.iterator(lst_aerop):
        #si no es el areopuerto origen y si existe un camino
        if (icao !=importante["aerop"]["ICAO"]) and (djk.hasPathTo(caminos,icao)):
            
            origen=importante["aerop"]
            destino=me.getValue(mp.get(data_structs["map_aeropuertos"],icao))
            tipo_avion=lt.newList("ARRAY_LIST")
            dist_viaje=0
            time_viaje=0

            path=djk.pathTo(caminos,icao)
                
            while st.size(path) > 0:
                aerop=st.pop(path)
                #aerop es el arco {vertexA,vertexB,weight}
                
                key="{0};{1};{2}".format(aerop["vertexA"],aerop["vertexB"],"AVIACION_CARGA")
                avion=me.getValue(mp.get(data_structs["map_vuelos"],key))
                lt.addLast(tipo_avion,avion["TIPO_AERONAVE"])
                
                dist_viaje+=aerop["weight"]
        
                time=gr.getEdge(data_structs["carga_time"],aerop["vertexA"],aerop["vertexB"])["weight"]
                time_viaje+=time
                
            dist_total+=dist_viaje
            no_trayectos+=1 

            camino={"origen":origen,"destino":destino,"tipo_avion":tipo_avion,"distancia":dist_viaje,"tiempo":time_viaje}
            lt.addLast(results,camino)
    results=sort_results_req4(results)
    return results,importante,dist_total,no_trayectos 

def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    #Se extraen los datos
    concurrency_list = data_structs['conc_militar']
    flights = data_structs['map_vuelos']
    airports = data_structs['map_aeropuertos']
    
    #Se obtiene el aereopuerto más importante
    most_important = lt.getElement(concurrency_list, 1)
    most_important_info = mp.get(airports, most_important['aerop']['ICAO'])
    most_important_info["Conc"] = most_important["conc"]
    
    #Se extraen y recorren grafos
    graph = data_structs['militar_time']
    graph2 = data_structs['militar_dist']
    search = djk.Dijkstra(graph, most_important['aerop']["ICAO"])

    #Se inician variables
    total_distance = 0
    total_routes = 0
    route_list = lt.newList('SINGLE_LINKED')
    
    #Se iteran los vertices
    vertices = gr.vertices(graph)
    for vertex in lt.iterator(vertices):
        if djk.hasPathTo(search, vertex):
            path = djk.pathTo(search, vertex)
            path_distance = 0
            #Se extrae información para agregarla a lista
            while not lt.isEmpty(path):
                edge = lt.removeFirst(path)
                if edge['vertexA'] == most_important['aerop']["ICAO"]:
                    total_routes += 1
                path_distance += gr.getEdge(graph2,edge['vertexA'],edge['vertexB'])['weight']
                edge_id = f"{edge['vertexA']};{edge['vertexB']};MILITAR"
                flight_data = mp.get(flights, edge_id)
                origin_airport = mp.get(airports, edge['vertexA'])['value']
                destination_airport = mp.get(airports, edge['vertexB'])['value']
                lt.addLast(route_list, {
                    'origin': edge['vertexA'],
                    'origin_name': origin_airport['NOMBRE'],
                    'origin_city': origin_airport['CIUDAD'],
                    'origin_country': origin_airport['PAIS'],
                    'destination': edge['vertexB'],
                    'destination_name': destination_airport['NOMBRE'],
                    'destination_city': destination_airport['CIUDAD'],
                    'destination_country': destination_airport['PAIS'],
                    'weight': gr.getEdge(graph2,edge['vertexA'],edge['vertexB']),
                    'tiempo': flight_data['value']['TIEMPO_VUELO'],
                    'aircraft': flight_data['value']['TIPO_AERONAVE']
                })
            #Se agrega a las sumas
            total_distance += path_distance

    return most_important['aerop']["ICAO"], most_important_info, total_distance, total_routes, route_list

def req_6(data_structs,M):
    """
    Función que soluciona el requerimiento 6
    """
    #Se extrae de la carga de datos
    airports = data_structs['map_aeropuertos']
    concurrency_list = data_structs['conc_comercial']
    
    #se saca el aereopuerto con mayor concurrencia
    top_airports = lt.newList(datastructure='SINGLE_LINKED')
    for i in range(int(M)+1):
        lt.addLast(top_airports, concurrency_list['elements'][i])
    most_important = lt.getElement(top_airports, 1)
    most_important_info = mp.get(airports, most_important['aerop']['ICAO'])
    most_important_info["Conc"] = most_important["conc"]

    #Se extraen y recorren grafos
    graph = data_structs['comercial_time']
    graph2 = data_structs['comercial_dist']
    search = djk.Dijkstra(graph, most_important['aerop']['ICAO'])
    paths_info = lt.newList('SINGLE_LINKED')

    #Se iteran los aereopuertos y se sacan los caminos a esos aereopuertos desde el mayor aereopuerto
    for item in lt.iterator(top_airports):
        airport_code = item['aerop']['ICAO']
        airport_info = mp.get(airports, airport_code)['value']
        if airport_code != most_important['aerop']['ICAO']:
            if djk.hasPathTo(search, airport_code):
                path = djk.pathTo(search, airport_code)
                if path:
                    path_distance = 0
                    airports_in_path = lt.newList('SINGLE_LINKED')
                    flights_in_path = lt.newList('SINGLE_LINKED')
                    
                    #Se extrae la info y se mete a una lista
                    while not lt.isEmpty(path):
                        edge = lt.removeFirst(path)
                        path_distance += gr.getEdge(graph2,edge['vertexA'],edge['vertexB'])['weight']
                        origin_airport = mp.get(airports, edge['vertexA'])['value']
                        destination_airport = mp.get(airports, edge['vertexB'])['value']
                        lt.addLast(airports_in_path, origin_airport)
                        lt.addLast(airports_in_path, destination_airport)
                        lt.addLast(flights_in_path, {'source': edge['vertexA'], 'destination': edge['vertexB']})
                    lt.addLast(paths_info, {
                        'airport_code': airport_code,
                        'airport_info': airport_info,
                        'total_airports': lt.size(airports_in_path),
                        'airports': airports_in_path,
                        'flights': flights_in_path,
                        'distance': path_distance
                    })

    return most_important_info, paths_info


def req_7(data_structs, origen_lat, origen_lon, destino_lat, destino_lon):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    
    distancia = 0
    tiempo = 0
    num_aerop_camino = 0
    camino_final = lt.newList("ARRAY_LIST")
    lista_aeropuertos = data_structs['map_aeropuertos']
    error_str = ""
    success = True
    
    
    origen_tof, origen_icao, origen_dist = get_distancia_aerop_30km(data_structs, origen_lat, origen_lon)
    destino_tof, destino_icao, destino_dist = get_distancia_aerop_30km(data_structs, destino_lat, destino_lon)
    
    if (origen_tof and destino_tof):
        aeropuerto_origen = me.getValue(mp.get(data_structs["map_aeropuertos"], origen_icao)) 
        aeropuerto_destino = me.getValue(mp.get(data_structs["map_aeropuertos"], destino_icao))
        
        caminos = djk.Dijkstra(data_structs['comercial_time'], origen_icao) 
        if djk.hasPathTo(caminos, destino_icao):
            pathto = djk.pathTo(caminos, destino_icao)
            
            while st.size(pathto) > 0:
                edge = st.pop(pathto)
                tiempo += edge["weight"]
                distancia += gr.getEdge(data_structs["comercial_dist"], edge["vertexA"], edge["vertexB"])["weight"]
                num_aerop_camino += 1
                
                aerop_i = mp.get(lista_aeropuertos, edge['vertexA'])['value']
                
                aeropuerto_info = {"icao": aerop_i["ICAO"], "nombre" : aerop_i["NOMBRE"], "ciudad": aerop_i["CIUDAD"], "pais": aerop_i["PAIS"]}
                lt.addLast(camino_final, aeropuerto_info)
    else:
        error_str, x1 ,x2,x3,x4,x5 = req_1(data_structs, origen_lat, origen_lon, destino_lat, destino_lon)
        success = False
    
    return distancia, tiempo, num_aerop_camino, camino_final, error_str, success, aeropuerto_origen, aeropuerto_destino


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

def sort_concurrencia(list):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    merg.sort(list,evalconc)
    return list

def evalconc(aerop_1, aerop_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        aerop1 (dict): {aerop:str, conc:int}
        aerop2 (dict): {aerop:str, conc:int}

    Returns:
        bool: compara las fechas y determina si conc1 < conc2
    """
    
    if aerop_1["conc"]>aerop_2["conc"]:
        return True
    elif aerop_1["conc"]<aerop_2["conc"]: 
        return False
    else:
        if aerop_1["aerop"]["ICAO"]<aerop_2["aerop"]["ICAO"]:
            return True
        else:
            return False


def sort_results_req4(list):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    merg.sort(list,evalReq4)
    return list

def evalReq4(camino_1, camino_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    if camino_1["destino"]["ICAO"]<camino_2["destino"]["ICAO"]:
        return True
    else:
        return False


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass
