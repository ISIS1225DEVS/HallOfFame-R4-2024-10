"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """
import time
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
from tabulate import tabulate
import traceback

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
   return controller.new_controller()


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control):
    carga,comercial,militar,cargaint,comercialint,militarint,aeropuertos, lista= controller.load_data(control)
    
    
    
    
    #size = aeropuertos["size"]
    
    #print(f"\nSe cargaron exitosamente {size} ofertas de trabajo")
    print(f"Se cargaron exitosamente {cargaint+militarint+comercialint} vuelos.\n Entre estos, {cargaint} vuelos de carga, {militarint} vuelos militares y {comercialint} vueloa comerciales.")
    print(f"Se cargaron exitosamente {aeropuertos} aeropuertos, entre estos:")
    print("\nLos 5 aeropuertos mas y menos concurridos en carga son los siguientes: ")
    print(tabulate(lt.iterator(carga), headers="keys"))
    print("\nLos 5 aeropuertos mas y menos concurridos comercialmente son los siguientes: ")
    print(tabulate(lt.iterator(comercial), headers="keys"))
    print("\nLos 5 aeropuertos mas y menos concurridos militarmente son los siguientes: ")
    print(tabulate(lt.iterator(militar), headers="keys"))
    #print(tabulate(lt.iterator(lista), headers="keys"))


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    pass


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(lista, mayor):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(lista,mayor):
    mayor_lt  = lt.newList()
    
    lt.addFirst(mayor_lt, mayor)
    print('El aeropuerto con mayor frecuencia es: ')
    print(tabulate(lt.iterator(mayor_lt), headers="keys"))
    print("---")
    print("---")
    print("---")
    
    
    for tupla in lt.iterator(lista):
        airport_destino, lista_destino, peso =  tupla
        
        lista_des = lt.newList()
        lt.addFirst(lista_destino, mayor)
        lt.addLast(lista_des, airport_destino)
        print ("La informacion del areopuerto destino es")
        print(tabulate(lt.iterator(lista_des), headers="keys"))
        print("--- ")
        print(" Las escalas para llegar a este areopuerto son: ")
        print(tabulate(lt.iterator(lista_destino), headers="keys"))
        if lt.size(lista_destino) - 1 > 1:
            print("Hay un total de "+str(lt.size(lista_destino) - 2)+ " escalas")
        else:
            print(" hay un vuelo directo")
        print("La distancia total es "+ str(round(peso, 1)) +" km")
        print(" Ya se termino el recorrido a este areopuerto")
        print("--- ")
        print("---")
        print("---")
        print("---")
        print("---")



def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(lista, mayor):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    mayor_lt  = lt.newList()
    
    lt.addFirst(mayor_lt, mayor)
    # TODO: Imprimir el resultado del requerimiento 6
    print('El areopuerto con mayor frecuencia es: ')
    print(tabulate(lt.iterator(mayor_lt), headers="keys"))
    print("---")
    print("---")
    print("---")
    
    
    for tupla in lt.iterator(lista):
        airport_destino, lista_destino, peso =  tupla
        
        lista_des = lt.newList()
        lt.addFirst(lista_destino, mayor)
        lt.addLast(lista_des, airport_destino)
        print ("La informacion del areopuerto destino es")
        print(tabulate(lt.iterator(lista_des), headers="keys"))
        print("--- ")
        print(" Las escalas para llegar a este areopuerto son: ")
        print(tabulate(lt.iterator(lista_destino), headers="keys"))
        if lt.size(lista_destino) - 1 > 1:
            print("Hay un total de "+str(lt.size(lista_destino) - 2)+ " escalas")
        else:
            print(" hay un vuelo directo")
        print("La distancia total es "+ str(round(peso, 1)) +" km")
        print(" Ya se termino el recorrido a este areopuerto")
        print("--- ")
        print("---")
        print("---")
        print("---")
        print("---")


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    pass


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            t1 = time.time()
            print("Cargando información de los archivos ....\n")
            load_data(control)
            t2 = time.time()
            
            tiempo = t2-t1
            print(f"\n\nEl tiempo de carga fue {tiempo:.3f} segundos")
        elif int(inputs) == 2:
            lati=float(input(("Ingrese la latitud de su lugar de orgien: ")))
            longi=float(input(("Ingrese la longitud de su lugar de orgien: ")))
            inicio=(lati,longi)
            lati=float(input(("Ingrese la latitud de su lugar de orgien: ")))
            longi=float(input(("Ingrese la longitud de su lugar de orgien: ")))
            final=(lati,longi)
            t1=time.time()
            retorno=controller.req_7(control,inicio,final)
            t2=time.time()
            if len(retorno) == 4:
                print("La distancia de las cordenadas ingresadas supera los 30 KM ")
                print(f"El aeropuerto mas cercano del origen es {retorno[0]} con un una distancia de {round(retorno[2])} KM. ")
                print(f"El aeropuerto mas cercano del destino es {retorno[1]} con un una distancia de {round(retorno[3])} KM . ")
            else:
                camino,tiempo,dist,origen,destino,escalas,origen,destino=retorno
                print(f"Su busqueda tardo {t2-t1} segundos")
                print(f"El aeropuerto mas cerca a su punto de partida es {origen} y el mas cercano a su destino es {destino}")
                print(f"El camino mas corto dura {tiempo} minutos y contando los trayectos a los aeropuertos recorre {round(dist)} KM ")
                print(f"Usted hara {escalas} escalas(s) ")
                print(f"Sus escalas seran las siguientes: ")
                print(tabulate(lt.iterator(camino), headers="keys"))

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            t1 = time.time()
            lista, mayor = controller.req_3(control)
            t2 = time.time()
            
            tiempo = t2-t1
            
            
            print_req_6(lista,mayor)
            print(f"\n\nEl tiempo de carga fue {tiempo:.3f} segundos")
            

        elif int(inputs) == 5:
            lista, mayor = controller.req_4(control)
            print_req_4(lista,mayor)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            n = int(input('Cuantos areopuertos quierres conectar con el areopuerto con mayor concurrencia comercial?: '))
            t1 = time.time()
            lista, mayor = controller.req_6(control, n)
            t2 = time.time()
            
            tiempo = t2-t1
            print_req_6(lista, mayor)
            print(f"\n\nEl tiempo de carga fue {tiempo:.3f} segundos")
            

        elif int(inputs) == 8:
            lati=float(input(("Ingrese la latitud de su lugar de orgien: ")))
            longi=float(input(("Ingrese la longitud de su lugar de orgien: ")))
            inicio=(lati,longi)
            lati=float(input(("Ingrese la latitud de su lugar de orgien: ")))
            longi=float(input(("Ingrese la longitud de su lugar de orgien: ")))
            final=(lati,longi)
            t1=time.time()
            retorno=controller.req_7(control,inicio,final)
            t2=time.time()
            if len(retorno) == 4:
                print("La distancia de las cordenadas ingresadas supera los 30 KM ")
                print(f"El aeropuerto mas cercano del origen es {retorno[0]} con un una distancia de {round(retorno[2])} KM. ")
                print(f"El aeropuerto mas cercano del destino es {retorno[1]} con un una distancia de {round(retorno[3])} KM . ")
                print(f"Su busqueda tardo {round((t2-t1)*1000)} milesimas")
            else:
                camino,tiempo,dist,origen,destino,escalas,origen,destino=retorno
                print(f"Su busqueda tardo {round((t2-t1)*1000)} milesimas")
                print(f"El aeropuerto mas cerca a su punto de partida es {origen} y el mas cercano a su destino es {destino}")
                print(f"El camino mas corto dura {tiempo} minutos y contando los trayectos a los aeropuertos recorre {round(dist)} KM ")
                print(f"Usted hara {escalas} escalas(s) ")
                print(f"Sus escalas seran las siguientes: ")
                print(tabulate(lt.iterator(camino), headers="keys"))


        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
            
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
