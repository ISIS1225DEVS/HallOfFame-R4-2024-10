import hash_table_lp as ht
import New_Functions as nf


def newGraph(size, directed=False, cmpfunction=None):
    graph = {'vertices': None,
             'edges': 0,
             'directed': directed,
             'guide_directed': None,
             'cmpfunction': cmpfunction
    }
    graph['vertices'] = ht.hash_table(size, 0.5)
    if directed:
        graph['guide_directed'] = ht.hash_table(size, 0.5)
    return graph
    
def newNode(vertexa, vertexb, peso, peso2=None):
    #peso2 por si se hace el reto complicado - eliminable
    return {"vertexA": vertexa, "vertexB": vertexb, "peso": peso}

def findNode(graph, vertexA, vertexB): #NO FUNCIONA, porfa cuentemente si lo necesitan y lo cambio :)
    list1 = (ht.get_value(graph['vertices'], vertexA)[1])
    for i in list1['elements']:
        if (i['vertexA'] == vertexA and i['vertexB'] == vertexB) or (i['vertexB'] == vertexA and i['vertexA'] == vertexB):
            return i
    return None

def findNodeReverso(graph, vertexA):
    list1 = (ht.get_value(graph['vertices'], vertexA)[1])
    for i in list1['elements']:
        if i['vertexB'] == vertexA:
            return i
    return None
            

def weight(graph, vertexA, vertexB):
    #node = findNode(graph, vertexA, vertexB)
    lista = (ht.get_value(graph['vertices'], vertexA)[1])
    for i in lista["elements"]:
        if i["vertexB"] == vertexB:
            return i["peso"]
    return None

def weight_node(node):
    return node['peso']

def containsVertex(graph, vertex):
    return ht.get_value(graph['vertices'], vertex)

def insertVertex(graph, vertex):
    edges = nf.newList()
    ht.put(graph['vertices'], vertex, edges)
    if (graph['directed']) == True:
        ht.put(graph['guide_directed'], vertex, 0)
    return graph
    
def both(edge, vertexA, vertexB): #funcion other y either combinada en una
    if edge['vertexA'] == vertexA and edge['vertexB'] == vertexB:
        return True
    else:
        return False
    
def either(edge):
    return edge['vertexA']

def other(edge, vertex):
    if vertex == edge['vertexA']:
        return edge['vertexB']
    elif vertex == edge['vertexB']:
        return edge['vertexA']
    else:
        return None
    
def getEdge(graph, vertexA, vertexB):
    element = ht.get_value(graph['vertices'], vertexA)
    if element is None:
        return None
    lst = element[1] #revisar que es esto -> después de crear addEdge
    for edge in nf.iterator(lst):
        if both(edge, vertexA, vertexB) == True:
            return edge

def fijarPeso(graph, vertexA, vertexB, weight): #NO FUNCIONA, porfa cuentemente si lo necesitan y lo cambio :)
    node = findNode(graph, vertexA, vertexB)
    node['peso'] = weight
    return node

def fijarPesoNode(node, weight): #no se usa
    value = node
    value['peso'] == weight
    return value
'''
def addEdge(graph, vertexA, vertexB, peso=0):
  if vertexA != vertexB:
    valora = ht.get_value(graph['vertices'], vertexA)
    valorb = ht.get_value(graph['vertices'], vertexB)
    if valora == None:
        insertVertex(graph, vertexA)
    if valorb == None:
        insertVertex(graph, vertexB)
    if graph['directed'] != True:
        eje = newNode(vertexB, vertexA, peso)
        nf.addLast(valorb[1], eje)
    eje = newNode(vertexA, vertexB, peso)
    nf.addLast(valora[1], eje)
    graph['edges'] += 1
    return graph
'''
def addEdge(graph, vertexA, vertexB, peso=0):
    valora = ht.get_value(graph['vertices'], vertexA)
    valorb = ht.get_value(graph['vertices'], vertexB)
    if valora == None:
        insertVertex(graph, vertexA)
    if valorb == None:
        insertVertex(graph, vertexB)
    edge = getEdge(graph, vertexA, vertexB)
    if vertexA != vertexB:
     if edge is None:
        eje = newNode(vertexA, vertexB, peso) #misma cosa que edge, solo que para no confundir el de busqueda
        #y el que cambia los valores
        nf.addLast(valora[1], eje)
        if graph['directed'] == False:
            dif_eje = newNode(vertexA, vertexB, peso)
            nf.addLast(valorb[1], dif_eje)
        graph['edges'] += 1
    return graph

def numVertices(graph):
    return ht.getSize(graph['vertices'])

def numEdges(graph):
    return (graph['edges'])

def adjacents(graph, vertex):
    lst = (ht.get_value(graph['vertices'], vertex))
    lstresp = nf.newList()
    if lst != None:
        for edge in nf.iterator(lst[1]):
            nf.addLast(lstresp, edge['vertexB'])
    return lstresp

def adjacentEdges(graph, vertex):
    element = ht.get_value(graph['vertices'], vertex)
    if element is not None:
        return element[1]

def sizeEdges(graph, vertex):
    size = adjacentEdges(graph, vertex)
    if size is not None:
        size = size['size']
        return size
    return 0

def vertices(graph):
    lstmap = ht.keySet(graph['vertices'])
    return lstmap   

def directedToUndirected(graph): #combierte un grafo dirigido en no dirigido

    undirectedGraph = newGraph(numVertices(graph), False)
    verticesList = vertices(graph)
    for vertex in nf.iterator(verticesList):
        insertVertex(undirectedGraph, vertex)
    
    for vertexA in nf.iterator(verticesList):
        adjEdges = adjacentEdges(graph, vertexA)
        for edge in nf.iterator(adjEdges):
            vertexB = edge['vertexB']
            peso = edge['peso']
            if getEdge(undirectedGraph, vertexA, vertexB) is None:  
                addEdge(undirectedGraph, vertexA, vertexB, peso)
    
    return undirectedGraph


def pesoRecorrido(grafo, lista): #retorna el peso de un recorrido especifico
    peso = 0
    for i in range(0, nf.get_size(lista)-1):
        nodo = findNode(grafo, lista['elements'][i], lista['elements'][i+1])
        peso += weight_node(nodo)
    return peso
    
"""
a = newGraph(10, True)
insertVertex(a, "Bogota")
insertVertex(a, "Cartagena")
insertVertex(a, "Balu")
insertVertex(a, "Bali")
insertVertex(a, "Juan")
insertVertex(a, "Maria")
insertVertex(a, "Julian")
addEdge(a, "Bogota", "Balu", 2)
addEdge(a, "Bogota", "Bali", 3)
addEdge(a, "Bogota", "Cartagena", 10)
addEdge(a, "Bogota", "Maria", 100)
addEdge(a, "Cartagena", "Juan", 10)
addEdge(a, "Juan", "Maria", 1)
print(directedToUndirected(a))"""