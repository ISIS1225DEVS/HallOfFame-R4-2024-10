import New_Functions as nf
#casi iguales a las funciones de arrays
 
def create():
    return nf.newList()

def remove_stack(list):
    location = nf.get_size(list)
    list = nf.delete(list, location)
    return list

def dequeue(list):
    nf.delete(list, 1)

def add(list, info):
    nf.addLast(list, info)

def delete_last(lista):
    size = nf.get_size(lista)
    if not nf.is_empty(lista):
        lista = nf.delete(lista, size)
    return lista

def pop(lista):
    size = nf.get_size(lista)
    value = nf.getElement(lista, size-1)
    delete_last(lista)
    return value

def enqueue(lista, elem): #queue
    nf.addLast(lista, elem)
    return lista

def push(lista, elem):
    nf.addLast(lista, elem)
    return lista