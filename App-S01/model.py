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

from haversine import haversine, Unit
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
from DISClib.ADT import stack
import copy
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


def new_data_structs():
    data_struct={
    "airport_map": None,
    "graph_time" : None,
    "flights" : None,
    "graph_distance": None,
    "lista_comercial": None,
    "grafo_comercial_busqueda": None
    }
    data_struct["airport_map"]=mp.newMap(numelements=450)
    data_struct['graph_time']=mp.newMap(numelements=5)
    data_stucts_aux(data_struct['graph_time'],False)
    data_struct['flights']=mp.newMap(numelements=5)
    data_stucts_aux(data_struct['flights'],True)
    data_struct['graph_distance']=mp.newMap(numelements=5)
    data_stucts_aux(data_struct['graph_distance'],False)
    data_struct['lista_comercial'] = lt.newList('ARRAY_LIST')
    return data_struct
# Funciones para agregar informacion al modelo
def data_stucts_aux(data_struct,bool):
    if bool:
        mp.put(data_struct,'AVIACION_CARGA',mp.newMap(numelements=450))
        mp.put(data_struct,'MILITAR',mp.newMap(numelements=450))
        mp.put(data_struct,'AVIACION_COMERCIAL',mp.newMap(numelements=450))
    else:
        mp.put(data_struct,'AVIACION_CARGA',gr.newGraph(directed=True,size=450))
        mp.put(data_struct,'MILITAR',gr.newGraph(directed=True,size=450))
        mp.put(data_struct,'AVIACION_COMERCIAL',gr.newGraph(directed=True,size=450))
    
    
def add_data_airpot(data_structs, data):
    data['LATITUD']=data['LATITUD'].replace(",",".")
    data['LONGITUD']=data['LONGITUD'].replace(",",".")
    gr.insertVertex(me.getValue(mp.get(data_structs["graph_time"],'AVIACION_CARGA')),data['ICAO'])
    gr.insertVertex(me.getValue(mp.get(data_structs["graph_time"],'MILITAR')),data['ICAO'])
    gr.insertVertex(me.getValue(mp.get(data_structs["graph_time"],'AVIACION_COMERCIAL')),data['ICAO'])
    
    gr.insertVertex(me.getValue(mp.get(data_structs["graph_distance"],'AVIACION_CARGA')),data['ICAO'])
    gr.insertVertex(me.getValue(mp.get(data_structs["graph_distance"],'MILITAR')),data['ICAO'])
    gr.insertVertex(me.getValue(mp.get(data_structs["graph_distance"],'AVIACION_COMERCIAL')),data['ICAO'])
    
    mp.put(data_structs['airport_map'],data['ICAO'],data)
    
def add_data_flight(data_structs, data):
    tipo=data['TIPO_VUELO']
    start=data['ORIGEN']
    end=data['DESTINO']
    mp.put(me.getValue(mp.get(data_structs["flights"],tipo)),(start+end),data)
    start=me.getValue(mp.get(data_structs['airport_map'],start))
    end=me.getValue(mp.get(data_structs['airport_map'],end))
    dist=haversine((float(start['LATITUD']),float(start['LONGITUD'])), (float(end['LATITUD']),float(end['LONGITUD'])), unit='km')
    gr.addEdge(me.getValue(mp.get(data_structs["graph_distance"],tipo)),start['ICAO'],end['ICAO'],dist)
    gr.addEdge(me.getValue(mp.get(data_structs["graph_time"],tipo)),start['ICAO'],end['ICAO'],float(data['TIEMPO_VUELO']))
# Funciones para creacion de datos
def tabulador(data_structs):
    grafo=gr.vertices(me.getValue(mp.get(data_structs['graph_time'],'AVIACION_CARGA')))
    for aeropuerto in lt.iterator(grafo):
        frecuencia=lt.size(gr.adjacentEdges(me.getValue(mp.get(data_structs['graph_time'],'AVIACION_CARGA')),aeropuerto))
        me.getValue(mp.get(data_structs['airport_map'],aeropuerto))['Frecuencia Carga']=int(frecuencia)
        frecuencia=lt.size(gr.adjacentEdges(me.getValue(mp.get(data_structs['graph_time'],'AVIACION_COMERCIAL')),aeropuerto))
        me.getValue(mp.get(data_structs['airport_map'],aeropuerto))['Frecuencia Comercial']=int(frecuencia)
        frecuencia=lt.size(gr.adjacentEdges(me.getValue(mp.get(data_structs['graph_time'],'MILITAR')),aeropuerto))
        me.getValue(mp.get(data_structs['airport_map'],aeropuerto))['Frecuencia Militar']=int(frecuencia)
    carga=tabuladoraux(data_structs['airport_map'],'Frecuencia Carga')
    comercial=tabuladoraux(data_structs['airport_map'],'Frecuencia Comercial')
    militar=tabuladoraux(data_structs['airport_map'],'Frecuencia Militar')
    return carga,comercial,militar



    
def distancia(model,lati,long):
    aeropuertos=model['airport_map']
    mini=10000000
    minim=None
    for aeropuerto in lt.iterator(mp.keySet(aeropuertos)):
         dist=haversine((float(me.getValue(mp.get(aeropuertos,aeropuerto))['LATITUD']),float(me.getValue(mp.get(aeropuertos,aeropuerto))['LONGITUD'])), (lati,long), unit='km')
         if dist<=mini:
             mini=dist
             minim=aeropuerto
    return minim,float(mini)

def lista_in_data_struct(data_structs):
    data_structs['lista_comercial'] = lista_de_importancia_comercial(data_structs)
    data_structs['lista_carga'] = lista_de_importancia_carga(data_structs)
    
def carga_datos_req4(data_structs):
    grafo_busqueda_carga(data_structs)
    lista_de_importancia_carga(data_structs)
def carga_datos_req6(data_structs):
    grafo_busqueda(data_structs)
    lista_de_importancia_comercial(data_structs)
    

def lista_de_importancia_comercial(data_structs, n = 50):
    grafo = gr.vertices(me.getValue(mp.get(data_structs['graph_time'],'AVIACION_COMERCIAL')))
    numero = mp.size(data_structs['airport_map'])
    for aeropuerto in lt.iterator(grafo):
        frecuencia=lt.size(gr.adjacents(me.getValue(mp.get(data_structs['graph_time'],'AVIACION_COMERCIAL')),aeropuerto))
        me.getValue(mp.get(data_structs['airport_map'],aeropuerto))['Frecuencia Comercial']=int(frecuencia)
    lista = maximo(data_structs['airport_map'],'Frecuencia Comercial',numero)
    return lista

def maximo (lista, crit,n= 10, param=['NOMBRE','ICAO', 'CIUDAD']):
    res=lt.newList()
    maxs=lt.newList()
    maxi=0
    maxim=None
    visitados=mp.newMap(numelements=(n*2)+1)
    if len(lista)> 10:
        for i in range(1,n+1):
            for element in lt.iterator(mp.valueSet(lista)):
                if element[crit]>=maxi and not mp.contains(visitados,element['ICAO']):
                    maxi=element[crit]
                    maxim=element
            mp.put(visitados,maxim['ICAO'],None)
            lt.addLast(maxs,maxim)
            maxi=0
        for dato in lt.iterator(maxs):
            dic = {}
            for i in param:
                dic[i] = dato[i]
            dic['Frecuencia']=dato[crit]
            lt.addLast(res, dic)
    return res
    
def grafo_busqueda(data_structs):
    lista = data_structs['lista_comercial']
    mayor = lt.firstElement(lista)
    ICAO = mayor['ICAO']
    mapa = data_structs['graph_distance']
    grafo = me.getValue(mp.get(mapa,'AVIACION_COMERCIAL'))
    data_structs['grafo_comercial_busqueda'] = djk.Dijkstra(grafo, ICAO)

def req_6_intento (data_structs, n, bool=True):
    
    paths= lt.newList()
    grafo = data_structs['grafo_comercial_busqueda']
    lista = data_structs['lista_comercial']
    mayor = lt.getElement(lista, 0)
    if bool == True:
        for poss in range (1, n+1):
            element = lt.getElement(lista, poss+1)
            if djk.hasPathTo(grafo, element['ICAO']):
                path = djk.pathTo(grafo,element['ICAO'])
                lista_a = path_to_list(path, data_structs)
                peso = djk.distTo(grafo, element['ICAO'])
                tupla = element,lista_a, peso
                lt.addLast(paths, tupla)
    else: 
        n = lt.size(lista)
        for poss in range (2, n+1):
            element = lt.getElement(lista, poss)
            if djk.hasPathTo(grafo, element['ICAO']):
                path = djk.pathTo(grafo,element['ICAO'])
                lista_a = path_to_list(path, data_structs)
                peso = djk.distTo(grafo, element['ICAO'])
                tupla = element,lista_a, peso
                lt.addLast(paths, tupla)
    return paths, mayor


def path_to_list (path, data_structs):
    if path is not None:
        mapa= data_structs['airport_map']
        lista = lt.newList()
        lista_areopuerto= lt.newList()
        pathlen = stack.size(path)
        while (not stack.isEmpty(path)):
            icao = stack.pop(path)['vertexB']
            lt.addLast(lista,icao )
        for icao in  lt.iterator(lista):
            airport = me.getValue(mp.get(mapa,icao))
            airport = tabulador_sin_criterio(airport)
            lt.addLast(lista_areopuerto, airport)
    return lista_areopuerto


def tabulador_sin_criterio(airport, param = ['NOMBRE','ICAO', 'CIUDAD',"Frecuencia Comercial" ]):
    dic = {}
    for i in param:
        dic[i] = airport[i]
        if i == "Frecuencia Comercial":
            dic['Frecuencia'] =dic[i]
    return dic
        
            
            
            
            
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


def req_1(data_structs):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    pass


def req_2(data_structs):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    pass


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    n = 0
    res = req_6_intento(data_structs, n, False)
    return res


def grafo_busqueda_carga(data_structs):
    lista = data_structs['lista_carga']
    mayor = lt.firstElement(lista)
    ICAO = mayor['ICAO']
    mapa = data_structs['graph_distance']
    grafo = me.getValue(mp.get(mapa,'AVIACION_CARGA'))
    data_structs['grafo_carga_busqueda'] = djk.Dijkstra(grafo, ICAO)
    
def lista_de_importancia_carga(data_structs, n = 50):
    grafo = gr.vertices(me.getValue(mp.get(data_structs['graph_time'],'AVIACION_CARGA')))
    numero = mp.size(data_structs['airport_map'])
    for aeropuerto in lt.iterator(grafo):
        frecuencia=lt.size(gr.adjacents(me.getValue(mp.get(data_structs['graph_time'],'AVIACION_CARGA')),aeropuerto))
        me.getValue(mp.get(data_structs['airport_map'],aeropuerto))['Frecuencia Comercial']=int(frecuencia)
    lista = maximo(data_structs['airport_map'],'Frecuencia Carga',numero)
    return lista


def req_4(data_structs, n, bool=False):
    paths= lt.newList()
    grafo = data_structs['grafo_carga_busqueda']
    lista = data_structs['lista_carga']
    mayor = lt.getElement(lista, 0)
    if bool == True:
        for poss in range (1, n+1):
            element = lt.getElement(lista, poss+1)
            if djk.hasPathTo(grafo, element['ICAO']):
                path = djk.pathTo(grafo,element['ICAO'])
                lista_a = path_to_list(path, data_structs)
                peso = djk.distTo(grafo, element['ICAO'])
                tupla = element,lista_a, peso
                lt.addLast(paths, tupla)
    else: 
        n = lt.size(lista)
        for poss in range (2, n+1):
            element = lt.getElement(lista, poss)
            if djk.hasPathTo(grafo, element['ICAO']):
                path = djk.pathTo(grafo,element['ICAO'])
                lista_a = path_to_list(path, data_structs)
                peso = djk.distTo(grafo, element['ICAO'])
                tupla = element,lista_a, peso
                lt.addLast(paths, tupla)
    return paths, mayor


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(data_structs):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    pass


def req_7(data_structs,inicio,final):
    origen,distorigen=distancia(data_structs,inicio[0],inicio[1])
    destino,distdestino=distancia(data_structs,final[0],final[1])
    distorigen=float(distorigen)
    distdestino=float(distdestino)
    estruct=me.getValue(mp.get(data_structs['graph_time'],'AVIACION_COMERCIAL'))
    estruct2=me.getValue(mp.get(data_structs['graph_distance'],'AVIACION_COMERCIAL'))
    if distdestino>30 or distorigen>30:
        return (origen,destino,distorigen,distdestino)
    else:
        grafo = djk.Dijkstra(estruct,origen)
        tiempo=djk.distTo(grafo,destino)
        me.getValue(mp.get(data_structs['airport_map'],origen))
        camino=djk.pathTo(grafo,destino)
        caminoc=djk.pathTo(grafo,destino)
        dist=0
        arptoa=st.pop(caminoc)
        while not st.isEmpty(caminoc):
            arptob = st.pop(caminoc)
            dist+=gr.getEdge(estruct2,arptoa,arptob)
            arptoa=arptob
        dist+=distdestino
        dist+=distorigen
        st.push
        camino=path_to_list(camino,data_structs)
        camino=req_7aux(camino)
        tupla=camino,tiempo,dist,origen,destino,lt.size(camino),origen,destino
        return tupla
def req_7aux(lista,param=['NOMBRE','ICAO', 'CIUDAD']):
        retorno=lt.newList(datastructure='ARRAY_LIST')
        for dato in lt.iterator(lista):
            dic = {}
            for i in param:
                dic[i] = dato[i]
            lt.addLast(retorno, dic)
        return retorno


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

def tabuladoraux(lista,crit,param=['NOMBRE','ICAO', 'CIUDAD'],n=5):
    res=lt.newList()
    mins=lt.newList()
    maxs=lt.newList()
    maxi=0
    mini=999
    maxim=None
    minim=None
    visitados=mp.newMap(numelements=(n*2)+1)
    if len(lista)> 10:
        for i in range(1,n+1):
            for element in lt.iterator(mp.valueSet(lista)):
                if element[crit]>=maxi and not mp.contains(visitados,element['ICAO']):
                    maxi=element[crit]
                    maxim=element
                if element[crit]<=mini and not mp.contains(visitados,element['ICAO']) and element[crit]>0:
                    mini=element[crit]
                    minim=element
            mp.put(visitados,maxim['ICAO'],None)
            mp.put(visitados,minim['ICAO'],None)
            lt.addLast(mins,minim)
            lt.addLast(maxs,maxim)
            maxi=0
            mini=999
        for dato in lt.iterator(maxs):
            dic = {}
            for i in param:
                dic[i] = dato[i]
            dic['Frecuencia']=dato[crit]
            lt.addLast(res, dic)
        for dato in lt.iterator(mins):
            dic = {}
            for i in param:
                dic[i] = dato[i]
            dic['Frecuencia']=dato[crit]
            lt.addLast(res, dic)
    return res
            
                    