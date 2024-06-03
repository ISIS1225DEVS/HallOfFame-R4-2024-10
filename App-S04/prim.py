import New_Functions as nf
import grafos as gr
import hash_table_lp as ht
import math

def minDistance(lista, dist, mstSet):
    min_val = math.inf
    min_index = None
    for v in nf.iterator(lista):
        if dist[v] < min_val and not mstSet[v]:
            min_val = dist[v]
            min_index = v
    return min_index

def primMST(grafo, start_vertex):
    dist_total=0
    lista = gr.vertices(grafo)
    dist = {}
    mstSet = {}
    parent = {}

    for v in nf.iterator(lista):
        dist[v] = float('inf')
        mstSet[v] = False
        parent[v] = None

    dist[start_vertex] = 0
    parent[start_vertex] = start_vertex

    for count in range(gr.numVertices(grafo)):
        u = minDistance(lista, dist, mstSet)
        mstSet[u] = True

        vecinos = gr.adjacents(grafo, u)
        for v in nf.iterator(vecinos):
            peso = gr.weight(grafo, u, v)
            if not mstSet[v] and peso < dist[v]:
                dist[v] = peso
                parent[v] = u

    mst = gr.newGraph(gr.numVertices(grafo), grafo['directed'])
    for v in nf.iterator(lista):
        gr.insertVertex(mst, v)
        if dist[v] != float('inf'):
            dist_total+= dist[v]
    for v in nf.iterator(lista):
        if parent[v] is not None and parent[v] != v:
            gr.addEdge(mst, parent[v], v, dist[v])

    return mst, dist_total #retorna grafo y ditancia total

#el mst no puede ser la tupla anterior
def recorridoMST(MST, origen, destino): #lista con el recorrido y el peso
    distancia = 0
    recorrido = nf.newList()
    actual = destino
    final = False
    while final == False:
        #ubi, item = ht.get_value(MST[0]['vertices'], actual)
        item = gr.findNodeReverso(MST, actual)
        nf.addLast(recorrido, actual)
        actual = gr.other(item, actual)
        distancia += gr.weight_node(item)
        if actual == origen:
            nf.addLast(recorrido, origen)
            final = True
    return nf.inversa(recorrido), distancia

def adjacentEdgesPrim(MST, origen):
    v = nf.newList()
    vertices = ht.keySet(MST['vertices'])
    for i in vertices['elements']:
        if i != origen:
            valor = (ht.get_value(MST['vertices'], i))[1]
            if nf.is_empty(valor) == False:
                nf.addLast(v, i)          
    return v

"""
a = gr.newGraph(10, False)
gr.insertVertex(a, "Bogota")
gr.insertVertex(a, "Cartagena")
gr.insertVertex(a, "Balu")
gr.insertVertex(a, "Bali")
gr.insertVertex(a, "Juan")
gr.insertVertex(a, "Maria")
gr.insertVertex(a, "Julian")
gr.addEdge(a, "Bogota", "Balu", 2)
gr.addEdge(a, "Bogota", "Bali", 3)
gr.addEdge(a, "Bogota", "Cartagena", 4)
gr.addEdge(a, "Bogota", "Maria", 100)
gr.addEdge(a, "Cartagena", "Juan", 1)
gr.addEdge(a, "Juan", "Maria", 1)
b = primMST(a,'Bogota')"""