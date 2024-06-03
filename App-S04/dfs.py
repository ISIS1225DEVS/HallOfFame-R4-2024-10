import New_Functions as nf
import hash_table_lp as ht
import grafos as gr

def dfs_route(graph, node):
    stack = nf.newList()
    visited = nf.newList()
    nf.addLast(visited, node)
    nf.addLast(stack, node)
    loop = True
    while loop == True:
        neighbors = gr.adjacents(graph, node)
        for i in neighbors['elements']:
            if nf.isPresent(visited, i) == None:
                nf.addLast(stack, i)
                nf.addLast(visited, i)
        if nf.get_size(neighbors) == 0 or nf.get_size(stack) == 0:
            if ht.get_value(graph['vertices'], node) == None:
                return None
            return visited
        node = nf.remove_last(stack)  
    return visited

def hasPathTo(graph, node, destination):
    stack = nf.newList()
    visited = nf.newList()
    nf.addLast(visited, node)
    nf.addLast(stack, node)
    loop = True
    while loop == True:
        neighbors = gr.adjacents(graph, node)
        for i in neighbors['elements']:
            if not nf.isPresent(visited, i):
                if i == destination:
                    return True
                nf.addLast(stack, i)
                nf.addLast(visited, i)
        if nf.get_size(neighbors)== 0 or nf.get_size(stack) == 0:
            return False
        node = nf.remove_last(stack)

def backtrace(parent, start, end):
    path = [end]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path

def PathTo(graph, node, destination):
    if hasPathTo(graph, node, destination) is False:
        return None
    else:
        parent = {}
        stack = []
        stack.append(node)
        while stack != []:
            node = stack.pop(len(stack)-1)
            if node == destination:
                return backtrace(parent, node, destination)
            neighbors = gr.adjacents(graph, node)
            for adjacent in neighbors['elements']:
                if node not in stack:
                    parent[adjacent] = node
                    stack.append(adjacent)

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
gr.addEdge(a, "Bali", "Cartagena", 10)
gr.addEdge(a, "Cartagena", "Maria", 100)
gr.addEdge(a, "Bogota", "Juan", 10)

print(dfs_route(a,"Bogota"))