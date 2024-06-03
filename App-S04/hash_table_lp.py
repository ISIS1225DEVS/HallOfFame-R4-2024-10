import random as rd
import math
import New_Functions as nf

def hashfun(ht, key):
    #buscar la función mad
    h = hash(key)
    a = ht['scale']
    b = ht['shift']
    p = ht['prime']
    m = ht['capacity']
    value = int((abs(a*h + b) % p) % m) + 1
    return value

def hash_table(capacity=17, loadfactor=0.5, cmpfunction=None):
    capacity = nextPrime(capacity//loadfactor)
    scale = rd.randint(1, 109345120)
    shift = rd.randint(0, 109345120)
    return {'capacity': capacity, 
            'keys': [None]*capacity,
            'limitfactor': loadfactor,
            'size': 0,
            'load': 0,
            'prime': 109345121,
            'scale': scale,
            'shift': shift,
            'cmpfunction': cmpfunction}
    
def is_empty(ht):
    for i in ht['keys']:
        if i != None:
            return False
    return True

def put(ht, key, value):
    #O(1) linear acotado -> significa que hay unas situaciones donde puede ser más
    #agregar cuando ya existe la llave
    if ht['load'] > ht['limitfactor']:
        resize(ht)
    pos = hashfun(ht, key)-1
    while ht['keys'][pos] != None and ht['keys'][pos] != '__EMPTY__': 
        pos = (pos + 1) % ht['capacity']
    ht['keys'][pos] = (key, value)
    ht['size'] += 1
    ht['load'] = ht['size']/ht['capacity']
    return ht
    
def resize(ht):
    #O(i)
    """ expands the hash table with new capacity"""
    ht["capacity"] = nextPrime(2*ht['capacity'])
    llaves = ht["keys"]
    ht["keys"] = [None]*ht["capacity"]
    ht["size"] = 0
    ht["load"] = 0
    for elem in llaves:
        if elem != None:
            pos = hashfun(ht, elem[0])-1
            while ht['keys'][pos] != None and ht['keys'][pos] != '__EMPTY__': 
                pos = (pos + 1) % ht['capacity']
            ht["keys"][pos] = elem
            ht['size'] += 1
            ht['load'] = ht['size']/ht['capacity']
    return ht

def get_value(ht, key): #retorna tupla
    pos = find_key(ht, key)
    if pos == None:
        rta = None
    else:
        rta = ht['keys'][pos]
    return rta

def remove(ht, key):
    #elimina la key del mapa
    pos = find_key(ht, key)
    if pos is not None:
        ht['keys'][pos] = None
        ht['size'] -= 1

def find_key_ignorar(ht, key):
    #encuentra la posición de una key
    pos = hashfun(ht, key) - 1
    if ht['keys'][pos] == None or ht['keys'][pos] == '__EMPTY__' :
        return None

    else:
      while ht['keys'][pos][0] != key:
          pos = (pos + 1) % ht['capacity']
          if ht['keys'][pos][0] == None:
                    return None
    return pos

def keySet(ht):
    lista_keys = nf.newList()
    for pos in range(len(ht['keys'])):
        if (ht['keys'][pos] is not None and ht['keys'][pos] != '__EMPTY__'):
            nf.addLast(lista_keys, ht['keys'][pos][0])
    return lista_keys


def find_key(ht,key):
    pos = hashfun(ht, key) - 1
    if ht['keys'][pos] == None:
        return None
    elif ht['keys'][pos][0] == None:
        return None
    elif ht['keys'][pos][0] == key:
        return pos
    else:
        while (ht['keys'][pos][0] != None) and ht['keys'][pos][0] != key: 
            pos = (pos + 1) % ht['capacity']
            if ht['keys'][pos] == None:
                return None
        return pos
    
        
def isAvailable(table, pos):
    #if a slot is available
    entry = table['keys'][pos]
    if (entry is None or entry == '__EMPTY__'):
         return True
    return False
     

def contains(ht, key): #no usar, hay error, getValue puede ser usada como
    pos = find_key(ht, key)
    if pos != None:
        return pos
    else:
        return None

def valueSet(ht):
    lista_values = nf.newList()
    for pos in range(0, len(ht['keys'])):
        if (ht['keys'][pos] is not None and ht['keys'][pos] != '__EMPTY__'):
            nf.addLast(lista_values, ht['keys'][pos][1])
    return lista_values

def getSize(ht):
    return ht['size']



"""PRIMOS"""
def nextPrime(N):
    if (N <= 1):
        return 2
    prime = int(N)
    found = False
    while(not found):
        prime = prime + 1
        if(isPrime(prime) is True):
            found = True
    return int(prime)

def isPrime(n):
    if(n <= 1):
        return False
    if(n <= 3):
        return True

    if(n % 2 == 0 or n % 3 == 0):
        return False

    for i in range(5, int(math.sqrt(n) + 1), 6):
        if(n % i == 0 or n % (i + 2) == 0):
            return False
    return True
    

h = hash_table(5, 0.5)
for i in range(10):
    put(h, i, i)