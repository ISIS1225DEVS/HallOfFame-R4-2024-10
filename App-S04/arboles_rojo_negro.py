import New_Functions as nf

red = 0
black = 1
neutral = 2

def create_vacio(color=red):
    return {'info': {'root': None, 'left':None, 'right': None, 'color': color}, 'size': 0}

def create(elem, color=red):
    bst = {'info': {'root': elem, 'left':create_vacio(neutral), 'right': create_vacio(neutral), 'color': color}, 'size': 1}
    return bst

def tamanio(bst):
    if bst['info']['root'] == None:
        return 0
    else:
        return bst['size']   

def is_empty(bst):
    return bst['info']['root'] == None

def isRed(bst):
    base = False
    if bst != None:
        if  bst['info']['color'] == 0:
            base = True
    return base

def getValue(node):
    return node['valor']

def getKey(node):
    return node['key']

def rotateLeft(rbt):
    x = rbt['info']['right']
    rbt['info']['right'] = x['info']['left']
    x['info']['left'] = rbt
    x['info']['color'] = x['info']['left']['info']['color']
    x['info']['left']['color'] = red
    x['size'] = rbt['size']
    rbt['size'] = tamanio(rbt['info']['left']) + tamanio(rbt['info']['right']) + 1
    return x

def rotateRight(rbt):
    x = rbt['info']['left']
    rbt['info']['left'] = x['info']['right']
    x['info']['right'] = rbt
    x['info']['color'] = x['info']['right']['info']['color']
    x['info']['right']['color'] = red
    x['size'] = rbt['size']
    rbt['size'] = tamanio(rbt['info']['left']) + tamanio(rbt['info']['right']) + 1
    return x

def flipColorNode(bst):
    root = bst['info']
    if root['color'] == 0:
        root['color'] == 1
    else:
        root['color'] == 0
    pass

def flipColors(bst):
    flipColorNode(bst)
    flipColorNode(bst['info']['left'])
    flipColorNode(bst['info']['right'])
    

def add(bst, elem, inicial=1): # poner 0 en inicial cuando es el primero de todos
    if bst['info']['root'] == None:
        bst = create(elem, red)
        return bst
    
    if (isRed(bst['info']['right'])):
            bst = rotateLeft(bst) 
    if (isRed(bst['info']['left']) and (isRed(bst['info']['left']['info']['left']))):
            bst = rotateRight(bst)
    if (isRed(bst['info']['left']) and (isRed(bst['info']['right']))):
            flipColors(bst)
        
        
    if bst['info']['root']['key'] == elem['key']: 
        bst['info']['root'] == elem
    elif bst['info']['root']['key'] > elem['key']:
        bst['info']['left'] = add(bst['info']['left'], elem)
    elif elem["key"] > bst['info']['root']["key"]:
        bst['info']['right'] = add(bst['info']['right'], elem)
    
    leftsize = tamanio(bst['info']['left'])
    rightsize = tamanio(bst['info']['right'])
    bst['size'] = 1 + leftsize + rightsize
        
    if (isRed(bst['info']['right'])):
            bst = rotateLeft(bst) 
    if (isRed(bst['info']['left']) and (isRed(bst['info']['left']['info']['left']))):
            bst = rotateRight(bst)    
    if (isRed(bst['info']['left']) and (isRed(bst['info']['right']))):
            flipColors(bst)
    
    #se va a crear un problema con el size
    return bst
    
def get(bst, key):
    root = bst['info']['root']
    node = None
    if root != None:
        if root['key'] != None:
            if root['key'] == key:
                node = root
            elif root['key'] > key:
                node = get(bst['info']['left'], key)
            elif root['key'] < key:
                node = get(bst['info']['right'], key)
    return node #node esta en la forma {"key": blahh, "valor": blahhh}

def getValue(node):
    return node['valor']

def getKey(node):
    return node['key']

def minKey(bst):
    min = None
    if (bst['info']['root']['key'] is not None):
        if (bst['info']['left']['info']['root'] is None):
            min = bst['info']['root']
        else:
            min = minKey(bst['info']['left'])
    return min #esto da ['key] y ['value']

def maxKey(bst):
    max = None
    if (bst['info']['root']['key'] is not None):
        if (bst['info']['right']['info']['root'] is None):
            max = bst['info']['root']
        else:
            max = maxKey(bst['info']['right'])
    return max #lo mismo que con el max

def preorder(bst):
    def preorden(bst, l):
        if is_empty(bst):
            return
        else:
            l.append(bst['info']['root'])
            preorden(bst['info']['left'], l)
            preorden(bst['info']['right'], l)
    l = []
    preorden(bst, l)
    return l

def inorder(bst):
    #lista con todos los elementos
    #no esta terminado
    def inorden(bst, l):
        if is_empty(bst):
            return []
        else: 
            inorden(bst['info']['left'], l)
            l.append(bst['info']['root'])
            inorden(bst['info']['right'], l)
    l=[]
    inorden(bst, l)
    return l

def keys_range(bst, key_low, key_high, lista, cmpfunction):  
    if bst['info']['root']!= None:
        complo = cmpfunction(key_low, bst['info']['root']['key'])
        comphi = cmpfunction(key_high, bst['info']['root']['key'])

        if (complo < 0):
            keys_range(bst['info']['left'], key_low, key_high, lista, cmpfunction)
        if ((complo < 0) and (comphi > 0)):
            nf.addLast(lista, bst['info']['root']['key'])
        if (comphi > 0):
            keys_range(bst['info']['right'], key_low, key_high, lista, cmpfunction)
    return lista

def values_range(bst, key_low, key_high, lista, cmpfunction):  
    if bst['info']['root']!= None:
        complo = cmpfunction(key_low, bst['info']['root']['key'])
        comphi = cmpfunction(key_high, bst['info']['root']['key'])

        if (complo < 0):
            keys_range(bst['info']['left'], key_low, key_high, lista, cmpfunction)
        if ((complo <= 0) and (comphi >= 0)):
            nf.addLast(lista, bst['info']['root']['value'])
        if (comphi > 0):
            keys_range(bst['info']['right'], key_low, key_high, lista, cmpfunction)
    return lista

def keys(bst, key_lo, key_high, cmpfunction):
    lista= nf.newList()
    if not is_empty(bst):
        keys_range(bst, key_lo, key_high, lista, cmpfunction)
    return lista

def values(bst, key_lo, key_high, cmpfunction):
    lista= nf.newList()
    if not is_empty(bst):
        values_range(bst, key_lo, key_high, lista, cmpfunction)
    return lista

def posorder(bst):
    def posorden(bst, l):
        if is_empty(bst):
            return []
        else:
            posorden(bst['info']['left'], l)
            posorden(bst['info']['right'], l)
            l.append(bst['info']['root'])
    l = []
    posorden(bst, l)
    return l

def create_node(key, value):
    return {'key': key, 'value': value}
    
#casos de prueba  
"""
bst = create_vacio()

bst = add(bst, {'key': 10, "value": "a"})
bst = add(bst, {'key': 8, "value": "c"})
bst = add(bst, {'key': 7, "value": "d"})
bst = add(bst, {'key': 6, "value": "e"})
bst = add(bst, {'key': 5, "value": "f"})
bst = add(bst, {'key': 200, "value": "a"})
bst = add(bst, {'key': 300, "value": "b"})
bst = add(bst, {'key': 400, "value": "c"})
bst = add(bst, {'key': 500, "value": "d"})
bst = add(bst, {'key': 600, "value": "e"})
bst = add(bst, {'key': 750, "value": "f"})
bst = add(bst, {'key': 9, "value": "b"})
print(bst)"""