import New_Functions as nf
import grafos as gr
import copy
import math


def minDistance(lista:list, dist:list, sptSet:list):

        min = math.inf
        # Search not nearest vertex not in the
        # shortest path tree
        min_index=None

        for v in nf.iterator(lista):
            if dist[v] < min and sptSet[v] == False:
                min = dist[v]
                min_index = v
 
        return min_index
 
def dijkstra(grafo, src):

    lista= gr.vertices(grafo)
    dist={}
    sptSet={}
    path={}
    for v in nf.iterator(lista):
        dist[v]= float('inf')
        sptSet[v]= False
        path[v]=[]
    dist[src]=0
    path[src].append(src)
    
    for cout in range(gr.numVertices(grafo)):

        u = minDistance(lista, dist, sptSet)

        sptSet[u] = True

        vecinos = gr.adjacents(grafo, u)
        for v in nf.iterator(vecinos):
            act = dist[u] + gr.weight(grafo, u,v)
            if (gr.weight(grafo,u,v) >= 0 and
                sptSet[v] == False and
                dist[v] > act):
                dist[v] = act
                path[v]= path[u].copy()
                path[v].append(v)

    return dist, path #retorna dos diccionarios donde la llave es el vertice, en dist el valor es la distancia entre src y el vertice, y path es el camino minimo hasta el vertice 

def hasPathTo(d: tuple, destino):
    return d[1][destino]!=[]

def pathTo(d: tuple, destino):
    return d[0][destino],d[1][destino] #retorna tupla 0 es tamaño:float, 1 es ruta:list