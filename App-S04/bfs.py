import hash_table_lp as ht
import grafos as gr
import New_Functions as nf
from collections import deque

def bfs_route(grafo, origen): #retorna lista con el path completo desde un origen
    queue = nf.newList()
    visited = nf.newList()
    nf.addLast(visited, origen)
    nf.addLast(queue, origen)
    valor = True
    while valor == True: #infinitamente
        vesinos = gr.adjacents(grafo, origen)
        for i in vesinos['elements']: #agrega los vecinos al queue
            if nf.isPresent(visited, i) == None:
                nf.addLast(queue, i)
                nf.addLast(visited,i)
        if nf.get_size(vesinos) == 0 or nf.get_size(queue) == 0: #final
            if ht.get_value(grafo['vertices'], origen) == None:
                return None
            return visited
        origen = nf.remove_first(queue)  
    return visited

def hasPathTo(grafo, origen, llegada):
    queue = nf.newList()
    visited = nf.newList()
    nf.addLast(visited, origen)
    nf.addLast(queue, origen)
    valor = True
    while valor == True: #infinitamente
        vesinos = gr.adjacents(grafo, origen)
        for i in vesinos['elements']: #agrega los vecinos al queue
            if not nf.isPresent(visited, i):
                if i == llegada:
                    return True
                nf.addLast(queue, i)
                nf.addLast(visited,i)
        if nf.get_size(vesinos)== 0 or nf.get_size(queue) == 0: #final
            return False
        origen = nf.remove_first(queue)  

def pathTo(grafo, origen, llegada):
    queue = nf.newList()
    visited = nf.newList()
    nf.addLast(visited, origen)
    nf.addLast(queue, origen)
    caminos = ht.hash_table()
    lista_origen = nf.newList()
    nf.addLast(lista_origen, origen)
    ht.put(caminos, origen, lista_origen)
    valor = True
    while valor == True: #infinitamente
        vesinos = gr.adjacents(grafo, origen)
        for i in vesinos['elements']: #agrega los vecinos al queue
            if nf.isPresent(visited, i) == None:
                nf.addLast(queue, i)
                nf.addLast(visited,i)
                camino = (ht.get_value(caminos, origen))[1]
                camino = nf.copiarLista(camino)
                nf.addLast(camino, i)
                ht.put(caminos, i, camino)
                if i == llegada:
                    return camino
        if nf.get_size(vesinos) == 0 or nf.get_size(queue) == 0: #final
            if ht.get_value(grafo['vertices'], origen) == None:
                return None
        origen = nf.remove_first(queue)  
    return visited  

"""
def pathTodfs(grafo, origen, llegada):
    queue = nf.newList()
    visited = nf.newList()
    nf.addLast(visited, origen)
    nf.addLast(queue, origen)
    caminos = ht.hash_table()
    lista_origen = nf.newList()
    nf.addLast(lista_origen, origen)
    ht.put(caminos, origen, lista_origen)
    valor = True
    while valor == True:
        vesinos = gr.adjacents(grafo, origen)
        vesinos_acutal = []
        for i in vesinos['elements']:
            if nf.isPresent(visited,i) == None:
                nf.addLast(queue, i)
                vesinos_acutal.append(i)
        anterior = origen
        origen, queue = nf.remove_last(queue)
        nf.addLast(visited,origen)
        camino = (ht.get_value(caminos, anterior))[1]
        camino = nf.copiarLista(camino)
        nf.addLast(camino, origen)
        ht.put(caminos, origen, camino)
        if origen == llegada:
            print(camino)
            return camino
        if nf.get_size(vesinos) == 0 or nf.get_size(queue) == 0: #final
            if ht.get_value(grafo['vertices'], origen) == None:
                valor = False
                return None
            
            
def dfs(grafo, origen, llegada):
    queue = nf.newList()
    visited = nf.newList()
    nf.addLast(visited, origen)
    nf.addLast(queue, origen)
    camino = nf.newList()
    lista_origen = nf.newList()
    nf.addLast(camino, origen)
    valor = True
    while valor == True:
        vesinos = gr.adjacents(grafo, origen)
        vesinos_acutal = []
        for i in vesinos['elements']:
            if nf.isPresent(visited,i) == None:
                nf.addLast(queue, i)
                vesinos_acutal.append(i)
        if vesinos_acutal == []:
            camino = nf.newList()
"""
#funciones de dfs

def Dfs(graph, source):
        search = {
                  'source': source,
                  'visited': None,
                  }

        search['visited'] = ht.hash_table(gr.numVertices(graph))
        ht.put(search['visited'], source, {'marked': True, 'edgeTo': None})
        dfsVertex(search, graph, source)
        return search


def dfsVertex(search, graph, vertex):
        adjlst = gr.adjacents(graph, vertex)
        for w in nf.iterator(adjlst):
            visited = ht.get_value(search['visited'], w)
            if visited is None:
                ht.put(search['visited'],
                        w, {'marked': True, 'edgeTo': vertex})
                dfsVertex(search, graph, w)
        return search


def hasPathTod(search, vertex):
        element = (ht.get_value(search['visited'], vertex))[1]
        if element and element['marked'] is True:
            return True
        return False


def pathTod(search, vertex):
    if hasPathTod(search, vertex) is False:
        return None
    path = nf.newList()
    while vertex != search['source']:
        nf.addLast(path, vertex)
        vertex = (ht.get_value(search['visited'], vertex)[1]['edgeTo'])
    nf.addLast(path, search['source'])
    path = nf.inversa(path)
    return path

"""
a = gr.newGraph(10, True)
gr.insertVertex(a, "Bogota")
gr.insertVertex(a, "Cartagena")
gr.insertVertex(a, "Balu")
gr.insertVertex(a, "Bali")
gr.insertVertex(a, "Juan")
gr.insertVertex(a, "Maria")
gr.insertVertex(a, "Julian")
gr.addEdge(a, "Bogota", "Balu", 2)
gr.addEdge(a, "Balu", "Bali", 3)
gr.addEdge(a, "Bogota", "Juan", 2)
gr.addEdge(a, "Juan", "Bali")
d = Dfs(a, "Bogota")
print(pathTod(d, "Bali"))
print(pathTo(a, "Bogota", "Bali"))"""