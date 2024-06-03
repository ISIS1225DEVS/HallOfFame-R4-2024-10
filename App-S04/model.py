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
assert cf
import New_Functions as nf
import hash_table_lp as ht
import scc as scc
import djk_2 as djk
import arboles_rojo_negro as arbol
import grafos as gr
import prim
import math
import bfs
import Sorts as srt
import math


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
    model = {"aeropuertos": ht.hash_table(800), #info de cada aeropuerto
             "aeropuertos_lista": nf.newList(), #lista con todos los aeropuertos
             "vuelos_km": gr.newGraph(800, True), #info todos los vuelos peso en kilometros
             "vuelos_comerciales_km": gr.newGraph(800, True), #info todos los vuelos comerciales peso en kilometros
             "vuelos_militares_km":gr.newGraph(800, True),
             "aeropuertos_lista": nf.newList(),
             "vuelos_carga_km":gr.newGraph(800, True),
             "vuelos_min": gr.newGraph(800, True), #info todos los vuelos peso en minutos
             "vuelos_comerciales_min": gr.newGraph(800, True), #info todos los vuelos comerciales peso en minutros
             "vuelos_militares_min":gr.newGraph(800, True),
             "vuelos_carga_min":gr.newGraph(800, True),
             "aeropuertos_imp": None, # lista de todos los aeropuertos por # de vuelos comerciales
             'conteo_aeropuertos_imp': None,
             'vuelos':ht.hash_table(5000),
             }
    return model

# Funciones para agregar informacion al modelo

def addAirport(data_structs, airport):
    """
    Función para agregar aeropuertos a los grafos
    """
    codigo= airport['ICAO']
    nf.addLast(data_structs['aeropuertos_lista'],airport)
    ht.put(data_structs['aeropuertos'],codigo,airport)
    gr.insertVertex(data_structs['vuelos_km'],codigo)
    gr.insertVertex(data_structs['vuelos_comerciales_km'],codigo)
    gr.insertVertex(data_structs['vuelos_militares_km'],codigo)
    gr.insertVertex(data_structs['vuelos_carga_km'],codigo)
    gr.insertVertex(data_structs['vuelos_min'],codigo)
    gr.insertVertex(data_structs['vuelos_comerciales_min'],codigo)
    gr.insertVertex(data_structs['vuelos_militares_min'],codigo)
    gr.insertVertex(data_structs['vuelos_carga_min'],codigo)

def addFlight(data_structs, flight):
    aeropuertos= flight['ORIGEN'] + '-' + flight['DESTINO']
    ht.put(data_structs['vuelos'],aeropuertos,flight)
    tipo_vuelo= flight['TIPO_VUELO']
    origen= ht.get_value(data_structs['aeropuertos'],flight['ORIGEN'])[1]
    destino= ht.get_value(data_structs['aeropuertos'],flight['DESTINO'])[1]
    distancia= distance(origen,destino)
    gr.addEdge(data_structs['vuelos_km'],flight['ORIGEN'],flight['DESTINO'],distancia)
    gr.addEdge(data_structs['vuelos_min'],flight['ORIGEN'],flight['DESTINO'],int(flight['TIEMPO_VUELO']))
    if tipo_vuelo== 'AVIACION_CARGA':
        gr.addEdge(data_structs['vuelos_carga_km'],flight['ORIGEN'],flight['DESTINO'],distancia)
        gr.addEdge(data_structs['vuelos_carga_min'],flight['ORIGEN'],flight['DESTINO'],int(flight['TIEMPO_VUELO']))
    elif tipo_vuelo== 'AVIACION_COMERCIAL':
        gr.addEdge(data_structs['vuelos_comerciales_km'],flight['ORIGEN'],flight['DESTINO'],distancia)
        gr.addEdge(data_structs['vuelos_comerciales_min'],flight['ORIGEN'],flight['DESTINO'],int(flight['TIEMPO_VUELO']))
    else:
        gr.addEdge(data_structs['vuelos_militares_km'],flight['ORIGEN'],flight['DESTINO'],distancia)
        gr.addEdge(data_structs['vuelos_militares_min'],flight['ORIGEN'],flight['DESTINO'],int(flight['TIEMPO_VUELO']))

def distance(origen,destino):
    lat1= float(origen['LATITUD'].replace(',','.'))
    lon1= float(origen['LONGITUD'].replace(',','.'))
    lat2= float(destino['LATITUD'].replace(',','.'))
    lon2= float(destino['LONGITUD'].replace(',','.'))
    distancia= haversine(lat1, lon1, lat2, lon2)
    return distancia

def organizarAeropuertos(data_structs):
    nuevo_grafo = gr.directedToUndirected(data_structs['vuelos_comerciales_km'])
    aeropuertos = gr.vertices(nuevo_grafo)
    num_vuelos = nf.newList()
    for i in aeropuertos['elements']:
        info = (ht.get_value(data_structs['aeropuertos'], i))[1]
        if info['PAIS'] == "Colombia":
            numero = gr.sizeEdges(nuevo_grafo, i)
            nf.addLast(num_vuelos, mejor_ciudad(i, numero))
    num_vuelos_organizado = srt.MergeSort(num_vuelos, srt.comparacion_numeros)
    aeropuertos_final = nf.newList()
    aeropuertos_valores = ht.hash_table(400, 0.5)
    for i in num_vuelos_organizado['elements']:
        nf.addLast(aeropuertos_final, i['ciudad'])
        ht.put(aeropuertos_valores, i['ciudad'], i['conteo'])
    data_structs['aeropuertos_imp'] = aeropuertos_final
    data_structs['conteo_aeropuertos_imp'] = aeropuertos_valores
    
#print de la carga
def organizarAeropuertosValor(data_structs, valor):
    if valor == "comercial":
        info = data_structs['vuelos_comerciales_km']
    elif valor == "militar":
        info = data_structs['vuelos_militares_km']
    else:
        info = data_structs['vuelos_carga_km']
    nuevo_grafo = gr.directedToUndirected(info)
    aeropuertos = gr.vertices(nuevo_grafo)
    num_vuelos = nf.newList()
    for i in aeropuertos['elements']:
        info = (ht.get_value(data_structs['aeropuertos'], i))[1]
        if info['PAIS'] == "Colombia":
            numero = gr.sizeEdges(nuevo_grafo, i)
            nf.addLast(num_vuelos, mejor_ciudad(i, numero))
    num_vuelos_organizado = srt.MergeSort(num_vuelos, srt.comparacion_numeros)
    aeropuertos_final = nf.newList()
    aeropuertos_valores = ht.hash_table(400, 0.5)
    for i in num_vuelos_organizado['elements']:
        nf.addLast(aeropuertos_final, i['ciudad'])
        ht.put(aeropuertos_valores, i['ciudad'], i['conteo'])
        
    para_tabular= []
    contador = 0
    for parada in aeropuertos_final['elements']:
        if contador < 5 or contador >= nf.get_size(aeropuertos_final)-5:
            aeropuerto= ht.get_value(data_structs['aeropuertos'],parada)[1]
            fila= []
            fila.append(parada)
            fila.append(aeropuerto['NOMBRE'])
            fila.append(aeropuerto['CIUDAD'])
            fila.append(aeropuerto['PAIS'])
            fila.append((ht.get_value(aeropuertos_valores, parada))[1])
            para_tabular.append(fila)
        contador += 1
            
    return para_tabular
    
    
# Funciones para creacion de datos

def haversine(lat1, lon1, lat2, lon2):
     
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
 
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0

    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
             math.cos(lat1) * math.cos(lat2))
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c

def mejor_ciudad(ciudad, numero):
    return {'ciudad': ciudad, 'conteo': numero}

def mayor_concurrencia(data_structs, criterio): #encuentra el aeropuerto de mayor concuerrencia militar, carga o comercial
    if criterio=="militar":
        grafo= data_structs['vuelos_militares_min']
    elif criterio=="carga":
        grafo= data_structs['vuelos_carga_km']
    else:
        grafo= data_structs['vuelos_comerciales_min']
    mayor= 0
    a= ''
    vertices= gr.vertices(grafo)
    grafo_nodirigido= gr.directedToUndirected(grafo)
    for vertice in nf.iterator(vertices):
        concurrencia= gr.sizeEdges(grafo_nodirigido, vertice)
        if concurrencia> mayor:
            mayor= concurrencia
            a= vertice
        elif concurrencia==mayor:
            if vertice<a:
                a=vertice
    return mayor, a, grafo_nodirigido  #retorna la concurrencia, el aeropuerto mas visitado, y el grafo no dirigido 
    
def encontrar_aeropuerto_cercano(control,coordenadas:tuple):
    lat1, lon1= coordenadas
    menor= math.inf
    a= ''
    for aeropuerto in nf.iterator(control['aeropuertos_lista']):
        lat2= float(aeropuerto['LATITUD'].replace(',','.'))
        lon2= float(aeropuerto['LONGITUD'].replace(',','.'))
        distancia= haversine(lat1,lon1,lat2,lon2)
        if distancia<menor:
            menor=distancia
            a= aeropuerto['ICAO']
    return menor, a

def sumar_distancia(grafo,aeropuertos:list):
    total=0
    i=0
    while i< len(aeropuertos)-1:
        a= aeropuertos[i]
        b= aeropuertos[i+1]
        distancia= gr.weight(grafo,a,b)
        total+=distancia
        i+=1
    return distancia

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
    return data_structs['size']


def req_1(data_structs, o1, o2, d1, d2):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    distance1, origen = encontrar_aeropuerto_cercano(data_structs, (o1, o2))
    distance2, destino = encontrar_aeropuerto_cercano(data_structs, (d1, d2))

    if distance1 > 30 or distance2 > 30:
        ao = ht.get_value(data_structs['aeropuertos'], origen)[1]['NOMBRE']
        ad = ht.get_value(data_structs['aeropuertos'], destino)[1]['NOMBRE']
        return distance1, ao, distance2, ad
    else:
        df = bfs.Dfs(data_structs['vuelos_comerciales_km'], origen)
        camino = bfs.pathTod(df, destino)
        distancia = gr.pesoRecorrido(data_structs['vuelos_comerciales_km'], camino) + distance1 + distance2
        tiempo = gr.pesoRecorrido(data_structs['vuelos_comerciales_min'], camino) #O(1)
        total_aeropuertos = nf.get_size(camino)
        para_tabular= []
        for parada in camino['elements']:
            aeropuerto= ht.get_value(data_structs['aeropuertos'],parada)[1]
            fila= []
            fila.append(parada)
            fila.append(aeropuerto['NOMBRE'])
            fila.append(aeropuerto['CIUDAD'])
            fila.append(aeropuerto['PAIS'])
            para_tabular.append(fila)
        headers = ['Identificador ICAO','Nombre', 'Ciudad','País', 'Tiempo']
        return tiempo, distancia, total_aeropuertos, para_tabular, headers
        

def req_2(data_structs, o1, o2, d1, d2):
    """
    Función que soluciona el requerimiento 2
    """
    distance1, origen= encontrar_aeropuerto_cercano(data_structs, (o1, o2)) #tupla: distancia, ICAO
    distance2, destino= encontrar_aeropuerto_cercano(data_structs, (d1, d2))
    
    if distance1>30 or distance2>30:
        ao= ht.get_value(data_structs['aeropuertos'],origen)[1]['NOMBRE']
        ad= ht.get_value(data_structs['aeropuertos'],destino)[1]['NOMBRE']
        return distance1, ao,  distance2, ad
    camino = bfs.pathTo(data_structs['vuelos_comerciales_km'], origen, destino)
    distancia = gr.pesoRecorrido(data_structs['vuelos_comerciales_km'], camino) + distance1 + distance2
    tiempo = gr.pesoRecorrido(data_structs['vuelos_comerciales_min'], camino)
    total_aeropuertos = nf.get_size(camino)
    para_tabular= []
    for parada in camino['elements']:
            aeropuerto= ht.get_value(data_structs['aeropuertos'],parada)[1]
            fila= []
            fila.append(parada)
            fila.append(aeropuerto['NOMBRE'])
            fila.append(aeropuerto['CIUDAD'])
            fila.append(aeropuerto['PAIS'])
            para_tabular.append(fila)
    headers = ['Identificador ICAO','Nombre', 'Ciudad','País', 'Tiempo']
    return tiempo, distancia, total_aeropuertos, para_tabular, headers
    


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    #concurrencia y grafo km
    conteo, aeropuerto_base, grafo_i = mayor_concurrencia(data_structs, "comercial") #falta agregar grafo [2]
    grafo = gr.directedToUndirected(data_structs['vuelos_comerciales_km'])

    #aeropuerto base
    info = (ht.get_value(data_structs['aeropuertos'], aeropuerto_base))[1]
    info_aeropuerto_base = nf.newList()
    nf.addLast(info_aeropuerto_base, info['ICAO'])
    nf.addLast(info_aeropuerto_base, info['NOMBRE'])
    nf.addLast(info_aeropuerto_base, info['CIUDAD'])
    nf.addLast(info_aeropuerto_base, info['PAIS'])
    toda_info = info['ICAO'], info['NOMBRE'], info['CIUDAD'], info['PAIS']
    nf.addLast(info_aeropuerto_base, conteo)
    
    mst, valor = prim.primMST(grafo, aeropuerto_base)
    #a que se refiere con total de trayectos???
    total_trayectos = gr.numEdges(mst)
    
    adjacent = prim.adjacentEdgesPrim(mst, aeropuerto_base)
    trayectos = nf.newList()
    for i in adjacent['elements']:
        nueva = nf.newList()
        recorrido, distancia = prim.recorridoMST(mst, aeropuerto_base, i)
        tiempo = gr.pesoRecorrido(data_structs['vuelos_comerciales_min'], recorrido)
        info2 = (ht.get_value(data_structs['aeropuertos'], i))[1]
        aeropuerto_final = info2['ICAO'], info2['NOMBRE'], info2['CIUDAD'], info2['PAIS']
        nf.addLast(nueva, toda_info)
        nf.addLast(nueva, aeropuerto_final)
        nf.addLast(nueva, distancia)
        nf.addLast(nueva, tiempo)
        nf.addLast(nueva, recorrido)
        nf.addLast(trayectos, nueva)
    
    #info de aeropuerto base, suma distancias, num_trayectos, lista de trayectos
    return info_aeropuerto_base, valor, total_trayectos, trayectos


def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    concurrencia, mostvisited, ugraph = mayor_concurrencia(data_structs, 'carga')
    graph = gr.directedToUndirected(data_structs['vuelos_carga_km'])

    info = (ht.get_value(data_structs['aeropuertos'], mostvisited))[1]
    info_mostvisited = nf.newList()
    nf.addLast(info_mostvisited, info['ICAO'])
    nf.addLast(info_mostvisited, info['NOMBRE'])
    nf.addLast(info_mostvisited, info['CIUDAD'])
    nf.addLast(info_mostvisited, info['PAIS'])
    toda_info = info['ICAO'], info['NOMBRE'], info['CIUDAD'], info['PAIS']
    nf.addLast(info_mostvisited, concurrencia)
    
    mst, valor = prim.primMST(graph, mostvisited)
    total_trayectos = gr.numEdges(mst)
    
    adjacent = prim.adjacentEdgesPrim(mst, mostvisited)
    trayectos = nf.newList()
    for i in adjacent['elements']:
        nueva = nf.newList()
        recorrido, distancia = prim.recorridoMST(mst, mostvisited, i)
        tiempo = gr.pesoRecorrido(data_structs['vuelos_carga_km'], recorrido)
        info2 = (ht.get_value(data_structs['aeropuertos'], i))[1]
        aeropuerto_final = info2['ICAO'], info2['NOMBRE'], info2['CIUDAD'], info2['PAIS']
        nf.addLast(nueva, toda_info)
        nf.addLast(nueva, aeropuerto_final)
        nf.addLast(nueva, distancia)
        nf.addLast(nueva, tiempo)
        nf.addLast(nueva, recorrido)
        nf.addLast(trayectos, nueva)
    
    return info_mostvisited, valor, total_trayectos, trayectos

def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    concurrencia, src, grafonodirigido = mayor_concurrencia(data_structs,'militar')
    mst, tiempo= prim.primMST(grafonodirigido,src)
    num_trayectos = gr.numEdges(mst)
    
    origen= ht.get_value(data_structs['aeropuertos'],src)[1]
    info= origen['ICAO'] + ', ' + origen['NOMBRE'] + ', ' + origen['CIUDAD'] + ', ' + origen['PAIS']
    vertices= prim.adjacentEdgesPrim(mst,src)
    
    distancia_total=0
    for vertice in nf.iterator(vertices):
        arcos= gr.adjacentEdges(mst,vertice)
        for arco in nf.iterator(arcos):
            peso= gr.weight(data_structs['vuelos_militares_km'],arco['vertexA'],arco['vertexB'])
            distancia_total+=peso
            
    distancia_total/=2
    
    para_tabular= []
    for aeropuerto in nf.iterator(vertices):
        trayecto, tiempo= prim.recorridoMST(mst,src,aeropuerto)
        distancia= gr.pesoRecorrido(data_structs['vuelos_militares_km'],trayecto)
        origen= trayecto['elements'][nf.get_size(trayecto)-2]
        llave= origen + '-' + aeropuerto
        vuelo= ht.get_value(data_structs['vuelos'],llave)[1]
        destino= ht.get_value(data_structs['aeropuertos'],aeropuerto)[1]
        infod= destino['ICAO'] + ', ' + destino['NOMBRE'] + ', ' + destino['CIUDAD'] + ', ' + destino['PAIS']
        fila= []
        fila.append(info)
        fila.append(infod)
        fila.append(trayecto['elements'])
        fila.append(distancia)
        fila.append(tiempo)
        fila.append(vuelo['TIPO_AERONAVE'])
        para_tabular.append(fila)
    headers = ['Aeropuerto de origen','Aeropuerto de destino', 'Trayecto','Distancia recorrida', 'Tiempo del trayecto', 'Tipo de aeronave']
    return info, concurrencia, distancia_total, num_trayectos, (para_tabular,headers)



def req_6(data_structs, numero):
    """
    Función que soluciona el requerimiento 6
    """
    #info aeropuerto base
    aeropuerto_base = nf.get_first(data_structs['aeropuertos_imp'])
    info_aeropuerto_base = nf.newList()
    info = (ht.get_value(data_structs['aeropuertos'], aeropuerto_base))[1]
    nf.addLast(info_aeropuerto_base, info['ICAO'])
    nf.addLast(info_aeropuerto_base, info['NOMBRE'])
    nf.addLast(info_aeropuerto_base, info['CIUDAD'])
    nf.addLast(info_aeropuerto_base, info['PAIS'])
    nf.addLast(info_aeropuerto_base,(ht.get_value(data_structs['conteo_aeropuertos_imp'], aeropuerto_base))[1])
    #información general -> ICAD, NOMBRE, CIUDAD, PAIS, CONTEO
    
    caminos = nf.newList()
    #información por aeropuerto -> num aeropuertos, lista aeropuertos, lista vuelos, distancia total
    #error en distancia total
    conteo = 0
    grafo = djk.dijkstra(data_structs['vuelos_comerciales_km'], aeropuerto_base)
    for aeropuerto in data_structs['aeropuertos_imp']['elements']:
        aeros = 0
        total = nf.newList()
        visitados = nf.newList()
        vuelos = nf.newList()
        anterior = aeropuerto_base
        if 1 <= conteo <= numero:
            path = djk.pathTo(grafo, aeropuerto)
            if path[0] != math.inf:
                for i in path[1]: # se puede tomar como O(1) porque siempre es O(2) o O(3)
                    aeros += 1
                    #info aeropuertos
                    info = (ht.get_value(data_structs['aeropuertos'], i))[1]
                    info = info['ICAO'] + ", " + info['NOMBRE'] + ", " + info['CIUDAD'] + ", " + info['PAIS']
                    nf.addLast(visitados, info)
                for i in path[1]: # se puede tomar como O(1)
                    if i != aeropuerto_base:
                        frase = anterior + " a " + i
                        nf.addLast(vuelos, frase)
                        anterior = i
                nf.addLast(total, aeros)
                nf.addLast(total, visitados)
                nf.addLast(total, vuelos)
                nf.addLast(total, path[0])
                nf.addLast(caminos, total)
                
        conteo += 1
    return info_aeropuerto_base, caminos


def req_7(data_structs,origen:tuple,destino:tuple):
    """
    Función que soluciona el requerimiento 7
    """
    aeropuerto_o= encontrar_aeropuerto_cercano(data_structs,origen) #tupla: distancia, ICAO
    aeropuerto_d= encontrar_aeropuerto_cercano(data_structs,destino)
    
    if aeropuerto_d[0]>30 or aeropuerto_o[0]>30:
        ao= ht.get_value(data_structs['aeropuertos'],aeropuerto_o[1])[1]['NOMBRE']
        ad= ht.get_value(data_structs['aeropuertos'],aeropuerto_d[1])[1]['NOMBRE']
        return aeropuerto_o[0], ao,  aeropuerto_d[0], ad
    else:
        alg_dikstra= djk.dijkstra(data_structs['vuelos_comerciales_min'],aeropuerto_o[1])
        tiempo_total, camino= djk.pathTo(alg_dikstra,aeropuerto_d[1])
        distancia = gr.pesoRecorrido(data_structs['vuelos_comerciales_km'],nf.convertir(camino))
        distancia_total= aeropuerto_o[0]+ distancia + aeropuerto_d[0]
        total_aeropuertos= len(camino)
        para_tabular= []
        for parada in camino:
            aeropuerto= ht.get_value(data_structs['aeropuertos'],parada)[1]
            fila= []
            fila.append(parada)
            fila.append(aeropuerto['NOMBRE'])
            fila.append(aeropuerto['CIUDAD'])
            fila.append(aeropuerto['PAIS'])
            para_tabular.append(fila)
        headers = ['Identificador ICAO','Nombre', 'Ciudad','País']
        return tiempo_total, distancia_total, total_aeropuertos, (para_tabular,headers), distancia

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
