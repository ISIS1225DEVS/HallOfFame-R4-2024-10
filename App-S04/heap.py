import New_Functions as nf
import hash_table_lp as ht

def newIndex(cmpfunction):
    indexheap = {'elements': None,
                 'qpMap': None,
                 'size': 0,
                 'cmpfunction': cmpfunction}
    indexheap['elements'] = nf.newList(cmpfunction=cmpfunction)
    indexheap['qpMap'] = ht.hash_table(17, 0.5)
    return indexheap

def is_empty(list):
    return nf.is_empty(list)

def delMin(list):
    if (list['size'] > 0):
        minIdx = nf.getElement(list['elements'], 0)
        exchange(list, 0, list['size']-1)
        list['size'] -= 1
        sink(list, 1)
        ht.remove(list['qpMap'], minIdx['key'])
        return minIdx['key']
    return None

def sink(list, pos):
    size = list['size']
    while ((2*pos <= size)):
        j = 2*pos
        if (j < size):
            if greater(nf.getElement(list['elements'], j),
                nf.getElement(list['elements'], (j+1))):
                j += 1
        if (not greater(nf.getElement(list['elements'], pos), nf.getElement(list['elements'], j))):
                break
        exchange(list, pos, j)
        
def greater(parent, element):
    return parent['index'] > element['index']

def exchange(list, i, j):
    element_i = nf.getElement(list['elements'], i)
    element_j = nf.getElement(list['elements'], j)
    nf.changeInfo(list['elements'], i, element_j)
    ht.put(list['qpMap'], element_i['key'], j)
    nf.changeInfo(list['elements'], j, element_i)
    ht.put(list['qpMap'], element_j['key'], i)
    
def contains(hash, key):
    return  ht.get_value(hash['qpMap'], key)

def decreaseKey(list, key, newindex):
    val = ht.get_value(list['qpMap'], key)
    elem = nf.getElement(list['elements'], val[1])
    elem['index'] = newindex
    nf.changeInfo(list['elements'], val[1], elem)
    swim(list, val[1])
    return list

def insert(iheap, key, index):
    if not ht.get_value(iheap['qpMap'], key):
        iheap['size'] += 1
        nf.addLast(iheap['elements'], {'key': key, 'index': index})
        ht.put(iheap['qpMap'], key, 0)
        swim(iheap, iheap['size'])
    return iheap

def swim(list, pos):
    while (pos > 1):
        posparent = int((pos/2))
        poselement = int(pos)
        parent = nf.getElement(list['elements'], posparent)
        element = nf.getElement(list['elements'], poselement)
        if greater(list, parent, element):
            exchange(list, posparent, poselement)
        pos = (pos//2)