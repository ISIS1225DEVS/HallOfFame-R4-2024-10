import pyvis
from pyvis.network import Network
from DISClib.ADT import list as lt
from DISClib.ADT import graph as gra
from DISClib.DataStructures import mapentry as me # Puede que se use
import json

#* Por fgutep y Grupo 3. Comentado por ChatGPT

def makeGraphFile(DiscLibGraph, FileName='OutputGraph.html', ShowWeight=True):
    """
    High-level function to generate a visualization of a graph from DISClib.
    
    Args:
        DiscLibGraph: The DISClib graph object to visualize.
        FileName (str): The name of the output HTML file that will display the graph.
        ShowWeight (bool): If True, display weights on the edges in the graph visualization.
        
    This function initializes the visualization, adds all nodes and edges to the network,
    and then saves the visualization to an HTML file.
    """
    net = initialize_visualization()
    addAllNodes(net, DiscLibGraph)
    addAllEdges(net, DiscLibGraph, showW=ShowWeight)
    saveFile(net, FileName)

def addSingleNode(net, DiscLibGraph, vertex, showW=True):
    """
    Adds a single node and its adjacent edges to the network visualization.
    
    Args:
        net: The Pyvis network object.
        DiscLibGraph: The DISClib graph object.
        vertex: The vertex to add to the network.
        showW (bool): If True, display weights on the edges.
        
    Raises:
        Exception: If the vertex does not exist in the graph.
        
    Returns:
        net: The updated Pyvis network object with the node and edges added.
        
    This function first checks if the vertex exists in the graph, then adds it as a node,
    and adds all its adjacent edges to the network visualization.
    """
    if gra.containsVertex(DiscLibGraph, vertex):
        net.add_node(str(vertex), label=str(vertex))
        adjacents = gra.adjacentEdges(DiscLibGraph, vertex)
        for edge in lt.iterator(adjacents):
            if showW:
                net.add_edge(edge['vertexA'], edge['vertexB'], weight=edge['weight'], title=f"Weight:{edge['weight']}")
            else:
                net.add_edge(edge['vertexA'], edge['vertexB'], weight=edge['weight'])
    else:
        raise Exception(f"No existe el vertice {vertex}")
    return net

def saveFile(net, FileName='OutputGraph.html'):
    """
    Saves the Pyvis network graph to an HTML file.
    
    Args:
        net: The Pyvis network object.
        FileName (str): The filename to save the HTML graph visualization.
        
    This function attempts to save the network graph to a file. It enables physics
    simulation by default which makes nodes interactively arrange themselves.
    """
    try:
        net.toggle_physics(True)
        net.save_graph(FileName)
    except Exception as e:
        print(f"Caught an exception: {e}")

def addAllNodes(net, DiscLibGraph):
    """
    Adds all nodes from a DISClib graph to the Pyvis network.
    
    Args:
        net: The Pyvis network object.
        DiscLibGraph: The DISClib graph object.
        
    Returns:
        net: The updated Pyvis network object with all nodes added.
        
    Iterates through all vertices in the DISClib graph and adds them as nodes
    to the network visualization.
    """
    for vertex in lt.iterator(gra.vertices(DiscLibGraph)):
        net.add_node(str(vertex), label=str(vertex))
    return net

def addAllEdges(net, DiscLibGraph, showW=True):
    """
    Adds all edges from a DISClib graph to the Pyvis network.
    
    Args:
        net: The Pyvis network object.
        DiscLibGraph: The DISClib graph object.
        showW (bool): If True, display weights on the edges.
        
    Returns:
        net: The updated Pyvis network object with all edges added.
        
    Iterates through all edges in the DISClib graph and adds them to the network visualization.
    If 'showW' is True, it also displays the weight of each edge.
    """
    for edge in lt.iterator(gra.edges(DiscLibGraph)):
        if showW:
            net.add_edge(edge['vertexA'], edge['vertexB'], weight=edge['weight'], title=f"Weight:{edge['weight']}")
        else:
            net.add_edge(edge['vertexA'], edge['vertexB'], weight=edge['weight'])
    return net

def initialize_visualization():
    """
    Initializes a new Pyvis network with specific visualization settings.
    
    Returns:
        net: A Pyvis network object with configured settings.
        
    Configures the network visualization with a specified height, width,
    background color, and font color for improved aesthetics.
    """
    net = Network(height="1080px", width="100%", bgcolor="#222222", font_color="white")
    return net
