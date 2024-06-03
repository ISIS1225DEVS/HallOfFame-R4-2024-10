import New_Functions as nf
import random

# Funciones de ordenamiento:

def SelectionSort(lista, criterio):
    if lista['type'] == "ARRAY_LIST":
        pos1 = 0
        counter = 1
        while counter < nf.get_size(lista):
            minimum = pos1  
            pos2 = pos1 + 1
        while (pos2 < nf.get_size(lista)-1):
            if not criterio(int(lista['elements'][pos2]) , int(lista['elements'][minimum])):
                minimum = pos2 
            pos2 += 1
        lista['elements'][pos2], lista['elements'][minimum] = lista['elements'][minimum], lista['elements'][pos2]
        pos1 += 1
        counter += 1
    elif lista['type'] == "SINGLE_LINKED":
        current = lista['first']
        while current != None:
            minimum = current
            next_node = current['next']
            while next_node != None:
                if not criterio(next_node['info'] , minimum['info']):
                    minimum = next_node
                next_node = next_node['next']
            current['info'], minimum['info'] = minimum['info'], current['info']
            if current['next'] == None:
                ultimo = current
            current = current['next']
        lista['last'] = ultimo
    return lista

def InsertionSort(lista,criterio):
    if lista['type'] == "ARRAY_LIST":    
        for i in range(1,nf.get_size(lista)):
            key= lista["elements"][i]
            j= i-1
            while j>=0 and criterio(lista["elements"][j],key):
                lista["elements"][j+1]=lista["elements"][j]
                j=j-1
            lista["elements"][j+1]= key
    elif lista['type'] == "SINGLE_LINKED":
        for i in range(1,nf.get_size(lista)):
            key= nf.getElement(lista, i)
            j= i-1            
            while j>=0 and criterio(nf.getElement(lista, j),key):
                nf.exchange(lista, j+1, j)
                j=j-1
            nf.changeInfo(lista, j+1, key)
    return lista

def ShellSort(lista,criterio):
    if lista['type'] == "ARRAY_LIST":
        mitad= nf.get_size(lista)//2
        while mitad>0:
            for i in range(mitad,nf.get_size(lista)):
                key= lista["elements"][i]
                j= i
                while j>= mitad and criterio(lista["elements"][j-mitad] , key):
                    lista["elements"][j]=lista["elements"][j-mitad]
                    j=j-mitad
                lista["elements"][j]= key
            mitad= mitad//2
    elif lista['type'] == "SINGLE_LINKED":
        mitad= nf.get_size(lista)//2
        while mitad>0:
            for i in range(mitad,nf.get_size(lista)):
                key= nf.getElement(lista, i)
                j= i
                while j>= mitad and criterio(nf.getElement(lista, j-mitad),key):
                    nf.exchange(lista, j,j-mitad)
                    j=j-mitad
                nf.changeInfo(lista, j, key)
            mitad= mitad//2
            
    return lista

def MergeSort(lista, criterio):
    if lista['type'] == "ARRAY_LIST" or lista['type'] == "SINGLE_LINKED":
        size = nf.get_size(lista)
        if size > 1:
            medio = size // 2
            leftlist = nf.subList(lista, 0, medio)  
            rightlist = nf.subList(lista, medio, size - medio)  

            MergeSort(leftlist, criterio)
            MergeSort(rightlist, criterio)
            i = j = k = 0  
            leftelements = nf.get_size(leftlist)
            rightelements = nf.get_size(rightlist)

            while (i < leftelements) and (j < rightelements):  
                elemento1 = nf.getElement(leftlist, i)  
                elemento2 = nf.getElement(rightlist, j)  
                if not criterio(elemento2, elemento1): 
                    nf.changeInfo(lista, k, elemento2)
                    j += 1
                else: 
                    nf.changeInfo(lista, k, elemento1)
                    i += 1
                k += 1

            while i < leftelements:
                nf.changeInfo(lista, k, nf.getElement(leftlist, i))
                i += 1
                k += 1

            while j < rightelements:
                nf.changeInfo(lista, k, nf.getElement(rightlist, j))
                j += 1
                k += 1

    return lista

def is_sorted(lista, criterio, size):
    if lista['type'] == "ARRAY_LIST":
        for pos in range(0, size - 1):
            if criterio(lista['elements'][pos], lista['elements'][pos + 1]):
                return False
        return True
    elif lista['type'] == "SINGLE_LINKED":
        actual = lista['first']
        while (actual != None) and (actual['next'] != None):
            if criterio(actual['info'], actual['next']['info']):
                return False
            actual = actual['next']
            if actual['next'] == None:
                final = actual
        lista['last'] = final
        return True

def BogoSort(lista, criterio):
    size = nf.get_size(lista)
    if lista['type'] == "ARRAY_LIST":
        while is_sorted(lista, criterio, size) != True:
            random.shuffle(lista['elements'])
    elif lista['type'] == "SINGLE_LINKED":
        while is_sorted(lista,criterio, size) != True:
          for pos in range(1,size):
            random_pos = random.randint(0,size-1)
            nf.exchange(lista,pos,random_pos)   
    return lista

def QuickSort(lista, criterio):
    size = nf.get_size(lista)
    if size <= 1:
        return lista
    
    if lista['type'] == "ARRAY_LIST":
        pivot_index = size // 2
        pivot = lista['elements'][pivot_index]
        start = nf.newList()
        middle = nf.newList()
        end = nf.newList()
        
        for i in range(size):
            element = nf.getElement(lista, i)
            if criterio(element, pivot):
                nf.addLast(start, element)
            elif criterio(pivot, element):
                nf.addLast(end, element)
            else:
                nf.addLast(middle, element)    
                
    elif lista['type'] == "SINGLE_LINKED":
        pivot_index = nf.get_size(lista) // 2
        pivot = nf.getElement(lista, pivot_index)
        start = nf.newList("SINGLE_LINKED")
        middle = nf.newList("SINGLE_LINKED")
        end = nf.newList("SINGLE_LINKED")
        
        current = lista['first']
        while current is not None:
            if current['info'] != pivot:
                if not criterio(current['info'], pivot):
                    nf.addLast(start, current['info'])
                elif criterio(current['info'], pivot):
                    nf.addLast(end, current['info'])
            else:
                nf.addLast(middle, current['info'])
            next_node = current['next']
            current = next_node
        
    sorted_start = QuickSort(start, criterio)
    sorted_end = QuickSort(end, criterio)

    concatenated = nf.concatenate(sorted_start, middle)
    concatenated = nf.concatenate(concatenated, sorted_end)
    
    return concatenated

#FALTA CORREGIR
def HeapSort(lista,criterio):
    
    def heapify(arr, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and criterio(arr[l], arr[largest]):
            largest = l

        if r < n and criterio(arr[r], arr[largest]):
            largest = r

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i] 
            heapify(arr, n, largest)

    n = nf.get_size(lista)

    if lista['type'] == "ARRAY_LIST":
        for i in range(n // 2 - 1, -1, -1):
            heapify(lista["elements"], n, i)

        for i in range(n - 1, 0, -1):
            lista["elements"][i], lista["elements"][0] = lista["elements"][0], lista["elements"][i] 
            heapify(lista["elements"], i, 0)

    elif lista['type'] == "SINGLE_LINKED":
        for i in range(n // 2 - 1, -1, -1):
            heapify_linked(lista, i, criterio)
            
        for i in range(n - 1, 0, -1):
            last_element = nf.getElement(lista, i)
            first_element = nf.getElement(lista, 0)
            nf.changeInfo(lista, i, first_element)
            nf.changeInfo(lista, 0, last_element)
            heapify_linked(lista, i, criterio)

    return lista

def heapify_linked(lista, i, criterio):
    current = nf.getElement(lista, i)

    if current is not None:
        next_node = current.get('next', None)
        
        if next_node is not None:
            left = next_node
            right = next_node.get('next', None)
        else:
            left = None
            right = None

        if left is not None and 'info' in left and criterio(left['info'], current['info']):
            largest = left
        else:
            largest = current

        if right is not None and 'info' in right and criterio(right['info'], largest['info']):
            largest = right

        if largest != current:
            nf.exchange(lista, i, i + 1)  

            heapify_linked(lista, i + 1, criterio)  

def TimSort(lista, criterio):
    n = nf.get_size(lista)
   
    if lista['type'] == "ARRAY_LIST":
        def insertionSort(arr, left, right):
            for i in range(left + 1, right + 1):
                temp = arr[i]
                j = i - 1
                while j >= left and criterio(arr[j], temp):
                    arr[j + 1] = arr[j]
                    j -= 1
                arr[j + 1] = temp

        def merge(arr, l, m, r):
            len1 = m - l + 1
            len2 = r - m
            left = [arr[l + i] for i in range(len1)]
            right = [arr[m + 1 + i] for i in range(len2)]

            i, j, k = 0, 0, l
            while i < len1 and j < len2:
                if criterio(left[i], right[j]):
                    arr[k] = left[i]
                    i += 1
                else:
                    arr[k] = right[j]
                    j += 1
                k += 1

            while i < len1:
                arr[k] = left[i]
                k += 1
                i += 1

            while j < len2:
                arr[k] = right[j]
                k += 1
                j += 1

        RUN = 32
        for i in range(0, n, RUN):
            insertionSort(lista["elements"], i, min(i + RUN - 1, n - 1))
        size = RUN
        while size < n:
            for left in range(0, n, 2 * size):
                mid = left + size - 1
                right = min(left + 2 * size - 1, n - 1)
                if mid < right:
                    merge(lista["elements"], left, mid, right)
            size *= 2
    elif lista['type'] == "SINGLE_LINKED":
        def insertionSort(chain, left, right):
            current = nf.getElement(chain, left)
            for i in range(left + 1, right + 1):
                temp = nf.getElement(chain, i)
                j = i - 1
                while j >= left and criterio(nf.getElement(chain, j), temp):
                    nf.changeInfo(chain, j + 1, nf.getElement(chain, j))
                    j -= 1
                nf.changeInfo(chain, j + 1, temp)

        def merge(chain, l, m, r):
            left_size = m - l + 1
            right_size = r - m
            left_chain = nf.subList(chain, l, left_size)
            right_chain = nf.subList(chain, m + 1, right_size)

            i, j, k = 0, 0, l
            while i < left_size and j < right_size:
                if criterio(nf.getElement(left_chain, i), nf.getElement(right_chain, j)):
                    nf.changeInfo(chain, k, nf.getElement(left_chain, i))
                    i += 1
                else:
                    nf.changeInfo(chain, k, nf.getElement(right_chain, j))
                    j += 1
                k += 1

            while i < left_size:
                nf.changeInfo(chain, k, nf.getElement(left_chain, i))
                i += 1
                k += 1

            while j < right_size:
                nf.changeInfo(chain, k, nf.getElement(right_chain, j))
                j += 1
                k += 1

        RUN = 32
        for i in range(0, n, RUN):
            insertionSort(lista, i, min(i + RUN - 1, n - 1))
        
        size = RUN
        while size < n:
            for left in range(0, n, 2 * size):
                mid = left + size - 1
                right = min(left + 2 * size - 1, n - 1)
                if mid < right:
                    merge(lista, left, mid, right)
            size *= 2

    return lista

def ShellSort_tupla(lista,criterio):
    if lista['type'] == "ARRAY_LIST":
        mitad= nf.get_size(lista)//2
        while mitad>0:
            for i in range(mitad,nf.get_size(lista)):
                key= lista["elements"][i]
                j= i
                while j>= mitad and criterio(lista["elements"][j-mitad] , key):
                    lista["elements"][j]=lista["elements"][j-mitad]
                    j=j-mitad
                lista["elements"][j]= key
            mitad= mitad//2
    return lista


# Funciones utilizadas para comparar elementos dentro de una lista:

def comparacion_diccionarios(dict_a,dict_b):
    return dict_a[1]<= dict_b[1]

def comparacion_numeros(a, b):
    if a['conteo'] < b['conteo']:
        return True
    elif a['conteo'] == b['conteo']:
        if a['ciudad'] > b['ciudad']:
            return True
        else:
            return False
    else:
        return False
    

def conteo_nombres_ciudad(a, b):
    if a['conteo'] < b['conteo']:
        return True
    elif a['conteo'] == b['conteo']:
        return a['city'] > b['city']

def fecha_empresa(a,b):
    if a['published_at']>b['published_at']:
        return True
    elif a['published_at']==b['published_at']:
        return a['company_name']>b['company_name']

def fecha_empresa_req_1(a,b):
    return a['published_at']<b['published_at']
        
def fecha_pais(a,b): #se usa en reto 2
    if a['published_at']>b['published_at']:
        return True
    elif a['published_at']==b['published_at']:
        return a['country_code']>b['country_code']

def organizar_ciudad(a, b):
    if a['total_ofertas']<b['total_ofertas']:
        return True
    elif a['total_ofertas']==b['total_ofertas']:
        if a['salario']<b['salario']:
            return True
        elif a['salario']==b['salario']:
            return a['nombre']<b['nombre']
        
#para probar si sirven los sorts: diccionario(array) y chain(single_linked)
        
def mayor_menor(a, b):
    return a > b

def mayor_menor_published(a, b):
    return a["published_at"] > b["published_at"]

def mayor_menor_p(a, b):
    return a['id'] > b['id']
    