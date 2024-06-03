import config
assert config
import hash_table_lp as ht
import grafos as gr
import New_Functions as nf
import stack_and_queue as sq

#temporal casi todo es disclib, espero mejorarlo para el reto

loadfactor= 0.5

#SCC
def KosarajuSCC(graph):
    """
    Implementa el algoritmo de Kosaraju
    para encontrar los componentes conectados
    de un grafo dirigido
    """
    scc = {
            'idscc': None,
            'marked': None,
            'grmarked': None,
            'components': 0
        }

    scc['idscc'] = ht.hash_table(gr.numVertices(graph), loadfactor,
                                cmpfunction=graph['cmpfunction'])

    scc['marked'] = ht.hash_table(gr.numVertices(graph), loadfactor,
                                cmpfunction=graph['cmpfunction'])
    scc['grmarked'] = ht.hash_table(gr.numVertices(graph), loadfactor,
                                    cmpfunction=graph['cmpfunction'])

    # Se calcula el grafo reverso de graph
    greverse = reverseGraph(graph)

    # Se calcula el DFO del reverso de graph
    dforeverse = DepthFirstOrderDFO(greverse)
    grevrevpost = dforeverse['reversepost']

    scc['components'] = 0
    while (not nf.is_empty(grevrevpost)):
        vert = sq.pop(grevrevpost)
        if not ht.get_value(scc['marked'], vert):
            scc['components'] += 1
            sccCount(graph, scc, vert)
    return scc

def sccCount(graph, scc, vert):
    """
    Este algoritmo cuenta el número de componentes conectados.
    Deja en idscc, el número del componente al que pertenece cada vértice
    """
    ht.put(scc['marked'], vert, True)
    ht.put(scc['idscc'], vert, scc['components'])
    lstadjacents = gr.adjacents(graph, vert)
    for adjvert in nf.iterator(lstadjacents):
        if not ht.get_value(scc['marked'], adjvert):
            sccCount(graph, scc, adjvert)
    return scc

def connectedComponents(scc):
    """
    Retorna el numero de componentes conectados
    """
    return scc['components']
    
def reverseGraph(graph):
    """
        Retornar el reverso del grafo graph
    """
    greverse = gr.newGraph(gr.numVertices(graph),directed=True,
                            cmpfunction=graph['cmpfunction'])

    lstvert = gr.vertices(graph)
    for vert in nf.iterator(lstvert):
        gr.insertVertex(greverse, vert)

    for vert in nf.iterator(lstvert):
        lstadj = gr.adjacents(graph, vert)
        for adj in nf.iterator(lstadj):
            gr.addEdge(greverse, adj, vert)
    return greverse


def comparenames(searchname, element):
    return (searchname == element['key'])

#dfo
def DepthFirstOrderDFO(graph):

    search = {
                'marked': None,
                'pre': None,
                'post': None,
                'reversepost': None
                }
    search['pre'] = sq.create()
    search['post'] = sq.create()
    search['reversepost'] = sq.create()
    search['marked'] = ht.hash_table(gr.numVertices(graph),loadfactor, graph['cmpfunction'])
    lstvert = gr.vertices(graph)
    for vertex in nf.iterator(lstvert):
        if ht.get_value(search['marked'], vertex) == None:
            dfsVertexDFO(graph, search, vertex)
    return search
        
def dfsVertexDFO(graph, search, vertex):
    sq.enqueue(search['pre'], vertex)
    ht.put(search['marked'], vertex, True)
    lstadjacents = gr.adjacents(graph, vertex)
    for adjvert in nf.iterator(lstadjacents):
        if not ht.get_value(search['marked'], adjvert):
            dfsVertexDFO(graph,search,adjvert)
    sq.enqueue(search['post'], vertex)
    sq.push(search['reversepost'], vertex)
    return search

#DFS