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
    """
        Se crea una instancia del controlador
    """
    control=controller.new_controller()
    return control


def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Ejecutar Requerimiento 7")
    print("8- Ejecutar Requerimiento 8")
    print("9- Salir")


def load_data(control):
    """
    Carga los datos
    """
    aeropuertos, vuelos=controller.load_data(control)
    return aeropuertos, vuelos
    
    
def primerosyult3(lista, n=3):
    if lt.size(lista)>n*2:
        tresprimeros=lt.subList(lista, 1, n)
        tresultimos=lt.subList(lista, lt.size(lista)-n+1, n)
        for oferta in lt.iterator(tresultimos):
            lt.addLast(tresprimeros,oferta)
    else: 
        tresprimeros=lista
    return tresprimeros

def titulos(headers, lista_ofertas):
    """
    Función que imprime los títulos de las ofertas de trabajo
    """
    lista_headers=lt.newList('ARRAY_LIST')
    for oferta in lt.iterator(lista_ofertas):
        copiaoferta={}
        for header in headers: 
            copiaoferta[header]=oferta[header]
        lt.addLast(lista_headers,copiaoferta)
        
    return lista_headers


def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    punto_origen_lat=float(input("Ingrese el punto de origen (lat): "))
    punto_destino_lat=float(input("Ingrese el punto de destino (lat): "))
    punto_origen_long=float(input("Ingrese el punto de origen (long): "))
    punto_destino_long=float(input("Ingrese el punto de destino (long): "))
    delta, distancia, numero_vuelos, secuencia, tiempo_del_trayecto=controller.req_1(control, punto_origen_lat, punto_origen_long, punto_destino_lat, punto_destino_long)
    if distancia is not None:
        print("El tiempo es: ", delta, "ms")
        print("La distancia es: ", distancia, "km")
        print("El número de aeropuertos visitados es: " + str(numero_vuelos))
        titulos1=["ICAO", "NOMBRE", "CIUDAD", "PAIS"]
        print("La secuencia de aeropuertos es:")
        print(tabulate(lt.iterator(titulos(titulos1, secuencia)), headers="keys", tablefmt="fancy_grid"))
        print("El tiempo del trayecto es: ", tiempo_del_trayecto, "minutos")
    else:
        print("No hay una ruta directa entre los puntos seleccionados")

def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    punto_origen_lat=float(input("Ingrese el punto de origen (lat): "))
    punto_destino_lat=float(input("Ingrese el punto de destino (lat): "))
    punto_origen_long=float(input("Ingrese el punto de origen (long): "))
    punto_destino_long=float(input("Ingrese el punto de destino (long): "))
    delta, distancia, numero_vuelos, secuencia, tiempo_del_trayecto=controller.req_2(control, punto_origen_lat, punto_origen_long, punto_destino_lat, punto_destino_long)
    if distancia is not None:
        print("El tiempo es: ", delta, "ms")
        print("La distancia es: ", distancia, "km")
        print("El número de aeropuertos visitados es: " + str(numero_vuelos))
        titulos1=["ICAO", "NOMBRE", "CIUDAD", "PAIS"]
        print("La secuencia de aeropuertos es:")
        print(tabulate(lt.iterator(titulos(titulos1, secuencia)), headers="keys", tablefmt="fancy_grid"))
        print("El tiempo del trayecto es: ", tiempo_del_trayecto, "minutos")
    else:
        print("No hay una ruta entre los puntos seleccionados")
    
    

def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    delta, aepto_concurrente, distancia, num_trayectos_posibles, salida,llegada, secuencia=controller.req_3(control)
    print("El tiempo es: ", delta, "ms")
    print("El aeropuerto con mayor concurrencia es: ", aepto_concurrente["NOMBRE"],"su ICAO es ", aepto_concurrente["ICAO"], '\n', 'y esta ubicado en ', aepto_concurrente["CIUDAD"],",", aepto_concurrente["PAIS"] ,"con ", salida, "vuelos de salida y ", llegada, "vuelos de llegada")
    print("La distancia es: ", distancia, "km")
    print("El número de trayectos posibles es: ", num_trayectos_posibles)
    titulos1=["ICAO", "NOMBRE", "CIUDAD", "PAIS"]
    print("La secuencia de aeropuertos es:")
    lista_auxiliar=lt.newList('ARRAY_LIST')
    for nodo in lt.iterator(secuencia):
        dict=nodo.copy()
        lista_nodo_origen = lt.newList('ARRAY_LIST')
        lt.addLast(lista_nodo_origen, dict["Nodo_origen"])
        dict["Nodo_origen"]=tabulate(lt.iterator(titulos(titulos1, lista_nodo_origen)), headers="keys", tablefmt="fancy_grid")
        lista_nodo_destino = lt.newList('ARRAY_LIST')
        lt.addLast(lista_nodo_destino, dict["Nodo_destino"])
        dict["Nodo_destino"]=tabulate(lt.iterator(titulos(titulos1, lista_nodo_destino)), headers="keys", tablefmt="fancy_grid")
        lt.addLast(lista_auxiliar, dict)
    print(tabulate(lt.iterator(lista_auxiliar), headers="keys", tablefmt="fancy_grid"))
    


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    delta, aepto_concurrente, distancia, num_trayectos_posibles, salida, llegada, secuencia=controller.req_3(control)
    print("El tiempo es: ", delta, "ms")
    print("El aeropuerto con mayor concurrencia es: ", aepto_concurrente["NOMBRE"],"su ICAO es ", aepto_concurrente["ICAO"], '\n', 'y esta ubicado en ', aepto_concurrente["CIUDAD"],",", aepto_concurrente["PAIS"] ,"con ", salida, "vuelos de salida y ", llegada, "vuelos de llegada")
    print("La distancia es: ", distancia, "km")
    print("El número de trayectos posibles es: ", num_trayectos_posibles)
    titulos1=["ICAO", "NOMBRE", "CIUDAD", "PAIS"]
    print("La secuencia de aeropuertos es:")
    lista_auxiliar=lt.newList('ARRAY_LIST')
    for nodo in lt.iterator(secuencia):
        dict=nodo.copy()
        lista_nodo_origen = lt.newList('ARRAY_LIST')
        lt.addLast(lista_nodo_origen, dict["Nodo_origen"])
        dict["Nodo_origen"]=tabulate(lt.iterator(titulos(titulos1, lista_nodo_origen)), headers="keys", tablefmt="fancy_grid")
        lista_nodo_destino = lt.newList('ARRAY_LIST')
        lt.addLast(lista_nodo_destino, dict["Nodo_destino"])
        dict["Nodo_destino"]=tabulate(lt.iterator(titulos(titulos1, lista_nodo_destino)), headers="keys", tablefmt="fancy_grid")
        lt.addLast(lista_auxiliar, dict)
    print(tabulate(lt.iterator(lista_auxiliar), headers="keys", tablefmt="fancy_grid"))

def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    lat1 = float(input("Ingrese la latitud del aeropuerto de origen: "))
    long1 = float(input("Ingrese la longitud del aeropuerto de origen: "))
    lat2 = float(input("Ingrese la latitud del aeropuerto de destino: "))
    long2 = float(input("Ingrese la longitud del aeropuerto de destino: "))
    delta, tiempo_total, dist_total, num_aeropuertos, secuencia = controller.req_7(control, lat1, lat2, long1, long2)
    print("El tiempo de ejecución del requerimiento fue: ", delta, "\n")
    print("El camino encontado fue: ")
    print(tabulate(lt.iterator(secuencia), headers="keys", tablefmt="fancy_grid"), "\n")
    print("El tiempo total del trayecto fue: ", tiempo_total)
    print("La distancia total del trayecto fue: ", dist_total, "\n")
    print("El número de aeropuertos es: ", num_aeropuertos, "\n")


def print_req_6(control):
    
    
    m=int(input("Ingrese la cantidad de aeropuertos mas importantes que desea cubrir: "))
    delta, aepto_concurrente,salida,llegada, secuencia=controller.req_6(control, m)
    print(f"El tiempo es: {delta} ms")
    print(f"El aeropuerto con mayor concurrencia es: {aepto_concurrente['NOMBRE']} su ICAO es {aepto_concurrente['ICAO']}")
    print(f"y esta ubicado en {aepto_concurrente['CIUDAD']}, {aepto_concurrente['PAIS']} con {salida} vuelos de salida y {llegada} vuelos de llegada\n")
    
    lista_auxiliar=lt.newList('ARRAY_LIST')
    lista_aeptos=["NOMBRE", "ICAO", "CIUDAD", "PAIS"]
    for nodo in lt.iterator(secuencia):
        dict=nodo.copy()
        lista_nodo = lt.newList('ARRAY_LIST')
        lt.addLast(lista_nodo, dict["Aepto ida"])
        dict["Aepto ida"]=tabulate(lt.iterator(titulos(lista_aeptos, lista_nodo)), headers="keys", tablefmt="fancy_grid")
        lista_nodo2 = lt.newList('ARRAY_LIST')
        lt.addLast(lista_nodo2, dict["Aepto llegada"])
        dict["Aepto llegada"]=tabulate(lt.iterator(titulos(lista_aeptos, lista_nodo2)), headers="keys", tablefmt="fancy_grid")
        lt.addLast(lista_auxiliar, dict)
    print(tabulate(lt.iterator(lista_auxiliar), headers="keys", tablefmt="fancy_grid"))


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    tiempo_total,aeropuerto_importante, dist_total, num_trayectos_total, trayectos = controller.req_5(control)
    
        
    print("El tiempo total fue: ", tiempo_total, '\n')
    print("El aeropuerto más importante con concurrencia militar encontrado es: ")
    print(tabulate([aeropuerto_importante], headers="keys", tablefmt="fancy_grid"), "\n")
    print("La distancia total fue: ", dist_total, " kms", '\n')
    print("El numero total de trayectos fue: ", num_trayectos_total, '\n')
    print("Los trayectos encontrados fueron: ")
    print(tabulate(lt.iterator(trayectos), headers="keys", tablefmt="fancy_grid"))


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    mapa, delta = controller.req_8(control)
    print("El tiempo de ejecución del requerimiento fue: ", delta, "ms")
    print("El mapa que tiene todas las ofertas esta en el siguente enlace: " + str(mapa))

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
        if int(inputs) == 0:
            # Se crea el controlador asociado a la vista
            control = new_controller()
            print("Cargando información de los archivos ....\n")
            aeropuertos, vuelos= load_data(control)
            print("El total de aeropuertos cargados es: ", str(aeropuertos))
            print("El total de vuelos cargados es: ", str(vuelos))
            titulos_1=["NOMBRE", "ICAO", "CIUDAD", "CONCURRENCIA_Comercial"]
            titulos_2=["NOMBRE", "ICAO", "CIUDAD", "CONCURRENCIA_Carga"]
            titulos_3=["NOMBRE", "ICAO", "CIUDAD", "CONCURRENCIA_Militar"]
            print("Los tres aeropuertos con mayor concurrencia comercial son: ")
            print(tabulate(lt.iterator(titulos(titulos_1, primerosyult3(control["model"]["Lista_aeropuertos_comercial"], 5))), headers="keys", tablefmt="fancy_grid"))
            print("Los tres aeropuertos con mayor concurrencia de carga son: ")
            print(tabulate(lt.iterator(titulos(titulos_2, primerosyult3(control["model"]["Lista_aeropuertos_carga"], 5))), headers="keys", tablefmt="fancy_grid"))
            print("Los tres aeropuertos con mayor concurrencia militar son: ")
            print(tabulate(lt.iterator(titulos(titulos_3, primerosyult3(control["model"]["Lista_aeropuertos_militar"], 5))), headers="keys", tablefmt="fancy_grid"))

        elif int(inputs) == 1:
            print_req_1(control)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 6:
            print_req_6(control)

        elif int(inputs) == 7:
            print_req_7(control)

        elif int(inputs) == 8:
            print_req_8(control)

        elif int(inputs) == 9:
            working = False
            print("\nGracias por utilizar el programa")
            
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
    


