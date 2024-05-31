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
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    control = controller.new_controller()
    return control


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
    print("10- Ejecutar bono tuplas")
    print("0- Salir")


def load_data(control, resp):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    flights, airports, time, memoria = controller.load_data(control, resp)
    return flights, airports, time, memoria


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
    
    latitud_origen = input("Digite la latitud del punto de origen: ")
    longitud_origen = input("Digite la longitud del punto de origen: ")
    latitud_destino = input("Digite la latitud del punto de destino: ")
    longitud_destino = input("Digite la longitud del punto de destino: ")
    memoria = input("Quiere ver la memoria almacenada? Diga True o False")
    tiempo_total, ae_origen, ae_destino, lista_aeropuertos, cantidad_aeropuerto_visitados, tiempo_entre_trayectos, distancia_trayecto, checking, tiempo_total_trayecto = controller.req_1(control, latitud_origen, longitud_origen, latitud_destino, longitud_destino)
    tiempo_total = round(float(tiempo_total), 2)
    print("El tiempo total de ejecución fue de: " + str(tiempo_total) + " ms.")
    if checking == False:
        print("")
        print("No se encontró un aeropuerto cercano a menos de 30km desde la ubicación ofrecida.")
        ae_destino = round(float(ae_destino), 2)
        print("Sin embargo, el aeropuerto más cercano fue " + str(ae_origen) + str(" a una distancia de ") + str(ae_destino))
    elif checking == None:
        print("")
        print("Se encontró un aeropuerto a una distancia menor de 30km.")
        print("Sin embargo, no hay un camino que lleve desde dicho diccionario hasta la posición de destino. ")
        round(float(ae_destino), 2)
        print("El aeropuerto más cercano fue " + str(ae_origen) + str(" a una distancia de ") + str(ae_destino))
    elif checking == True:
        print("")
        distancia_trayecto = round(float(distancia_trayecto), 2)
        print("La distancia total para ir de ambos lugares es: " + str(distancia_trayecto) + "km. ")
        print("El tiempo total del trayecto es: " + str(tiempo_total_trayecto) + " minutos")
        print("La cantidad de aeropuertos visitados fue de: " + str(cantidad_aeropuerto_visitados))
        mostrar_req1(control, lista_aeropuertos, ae_origen, ae_destino)
        
        print("\nTiempo entre trayectos: \n")
        for z in lt.iterator(tiempo_entre_trayectos):
            print(z)
                
def mostrar_req1(control, lst, ae_origen, ae_destino):
    aeropuertos_id = control["model"]["airports_id"]
    lista = []
    resultado = []
    
    #para el de origen
    print("\n Aeropuerto de origen: \n")
    icao = me.getValue(mp.get(aeropuertos_id, ae_origen))["ICAO"]
    nombre = me.getValue(mp.get(aeropuertos_id, ae_origen))["NOMBRE"]
    ciudad = me.getValue(mp.get(aeropuertos_id, ae_origen))["CIUDAD"]
    pais = me.getValue(mp.get(aeropuertos_id, ae_origen))["PAIS"]
    resultado = [icao, nombre, ciudad, pais]
    print(tabulate([resultado], headers=["ICAO", "NOMBRE", "Ciudad", "PAIS"], tablefmt="rounded_grid"))
    
    print("\n Aeropuertos intermedios: ")
    lista = []
    resultado = []
    for x in lt.iterator(lst):
        if ((x != ae_origen) and (x != ae_destino)):
            icao = me.getValue(mp.get(aeropuertos_id, x))["ICAO"]
            nombre = me.getValue(mp.get(aeropuertos_id, x))["NOMBRE"]
            ciudad = me.getValue(mp.get(aeropuertos_id, x))["CIUDAD"]
            pais = me.getValue(mp.get(aeropuertos_id, x))["PAIS"]
            resultado = [icao, nombre, ciudad, pais]
            lista.append(resultado)
    
    print(tabulate(lista, headers=["ICAO", "NOMBRE", "Ciudad", "PAIS"], tablefmt="rounded_grid"))
    
    print("\n Aeropuerto de destino: \n")
    lista = []
    resultado = []
    icao = me.getValue(mp.get(aeropuertos_id, ae_destino))["ICAO"]
    nombre = me.getValue(mp.get(aeropuertos_id, ae_destino))["NOMBRE"]
    ciudad = me.getValue(mp.get(aeropuertos_id, ae_destino))["CIUDAD"]
    pais = me.getValue(mp.get(aeropuertos_id, ae_destino))["PAIS"]
    resultado = [icao, nombre, ciudad, pais]
    print(tabulate([resultado], headers=["ICAO", "NOMBRE", "Ciudad", "PAIS"], tablefmt="rounded_grid"))
        

def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    latitud_origen = input("Digite la latitud del punto de origen: ")
    longitud_origen = input("Digite la longitud del punto de origen: ")
    latitud_destino = input("Digite la latitud del punto de destino: ")
    longitud_destino = input("Digite la longitud del punto de destino: ")
    memoria = input("Quiere ver la memoria almacenada? Diga True o False")
    tiempo_total, ae_origen, ae_destino, lista_aeropuertos, cantidad_aeropuerto_visitados, tiempo_entre_trayectos, distancia_trayecto, checking, tiempo_total_trayecto = controller.req_2(control, latitud_origen, longitud_origen, latitud_destino, longitud_destino)
    tiempo_total = round(float(tiempo_total), 2)
    print("El tiempo total de ejecución fue de: " + str(tiempo_total) + " ms.")
    if checking == False:
        print("")
        print("No se encontró un aeropuerto cercano a menos de 30km desde la ubicación ofrecida.")
        ae_destino = round(float(ae_destino), 2)
        print("Sin embargo, el aeropuerto más cercano fue " + str(ae_origen) + str(" a una distancia de ") + str(ae_destino))
    elif checking == None:
        print("")
        print("Se encontró un aeropuerto a una distancia menor de 30km.")
        print("Sin embargo, no hay un camino que lleve desde dicho diccionario hasta la posición de destino. ")
        round(float(ae_destino), 2)
        print("El aeropuerto más cercano fue " + str(ae_origen) + str(" a una distancia de ") + str(ae_destino))
    elif checking == True:
        print("")
        distancia_trayecto = round(float(distancia_trayecto), 2)
        print("La distancia total para ir de ambos lugares es: " + str(distancia_trayecto) + "km. ")
        print("El tiempo total del trayecto es de: " + str(tiempo_total_trayecto) + " minutos")
        print("La cantidad de aeropuertos visitados fue de: " + str(cantidad_aeropuerto_visitados))
        mostrar_req2(control, lista_aeropuertos, ae_origen, ae_destino)
        
        print("\nTiempo entre trayectos: \n")
        for z in lt.iterator(tiempo_entre_trayectos):
            print(z)
                
def mostrar_req2(control, lst, ae_origen, ae_destino):
    aeropuertos_id = control["model"]["airports_id"]
    lista = []
    resultado = []
    
    #para el de origen
    print("\n Aeropuerto de origen: \n")
    icao = me.getValue(mp.get(aeropuertos_id, ae_origen))["ICAO"]
    nombre = me.getValue(mp.get(aeropuertos_id, ae_origen))["NOMBRE"]
    ciudad = me.getValue(mp.get(aeropuertos_id, ae_origen))["CIUDAD"]
    pais = me.getValue(mp.get(aeropuertos_id, ae_origen))["PAIS"]
    resultado = [icao, nombre, ciudad, pais]
    print(tabulate([resultado], headers=["ICAO", "NOMBRE", "Ciudad", "PAIS"], tablefmt="rounded_grid"))
    
    print("\n Aeropuertos intermedios: ")
    lista = []
    resultado = []
    for x in lt.iterator(lst):
        if ((x != ae_origen) and (x != ae_destino)):
            icao = me.getValue(mp.get(aeropuertos_id, x))["ICAO"]
            nombre = me.getValue(mp.get(aeropuertos_id, x))["NOMBRE"]
            ciudad = me.getValue(mp.get(aeropuertos_id, x))["CIUDAD"]
            pais = me.getValue(mp.get(aeropuertos_id, x))["PAIS"]
            resultado = [icao, nombre, ciudad, pais]
            lista.append(resultado)
    
    print(tabulate(lista, headers=["ICAO", "NOMBRE", "Ciudad", "PAIS"], tablefmt="rounded_grid"))
    
    print("\n Aeropuerto de destino: \n")
    lista = []
    resultado = []
    icao = me.getValue(mp.get(aeropuertos_id, ae_destino))["ICAO"]
    nombre = me.getValue(mp.get(aeropuertos_id, ae_destino))["NOMBRE"]
    ciudad = me.getValue(mp.get(aeropuertos_id, ae_destino))["CIUDAD"]
    pais = me.getValue(mp.get(aeropuertos_id, ae_destino))["PAIS"]
    resultado = [icao, nombre, ciudad, pais]
    print(tabulate([resultado], headers=["ICAO", "NOMBRE", "Ciudad", "PAIS"], tablefmt="rounded_grid"))


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    aeropuertos_id = control["model"]["airports_id"]
    memoria = input("Quiere ver la memoria almacenada? Diga True o False")
    tiempo_total, aeropuerto_mayor_ocurrencias, cantidad_ocurrencias, cantidad_trayectos, respuesta = controller.req_3(control)
    tiempo_total = round(float(tiempo_total), 2)
    print("El tiempo total de ejecución fue de: " + str(tiempo_total) + " ms.")
    
    print("El aeropuerto más importante según la concurrencia comercial fue: ")
    
    icao = me.getValue(mp.get(aeropuertos_id, aeropuerto_mayor_ocurrencias))["ICAO"]
    nombre = me.getValue(mp.get(aeropuertos_id, aeropuerto_mayor_ocurrencias))["NOMBRE"]
    ciudad = me.getValue(mp.get(aeropuertos_id, aeropuerto_mayor_ocurrencias))["CIUDAD"]
    pais = me.getValue(mp.get(aeropuertos_id, aeropuerto_mayor_ocurrencias))["PAIS"]
    resultado = [icao, nombre, ciudad, pais, cantidad_ocurrencias]
    print(tabulate([resultado], headers=["ICAO", "NOMBRE", "Ciudad", "PAIS", "CANTIDAD OCURRENCIAS"], tablefmt="rounded_grid"))
    
    print("El número total de trayectos es: " + str(cantidad_trayectos))
    
    print("\n A continuación, la secuencia de trayectos encontrados: \n")
    
    mostrar_req3(control["model"], respuesta)
    
def mostrar_req3(data_structs, lst):
    aeropuertos_id = data_structs["airports_id"]
    
    lista = []
    resultado = []
    distancia_recorrida_total = 0
    for x in lt.iterator(lst):
        aeropuerto_origen = x["aeropuerto origen"]
        nombre_origen = me.getValue(mp.get(aeropuertos_id, aeropuerto_origen))["NOMBRE"]
        pais_origen = me.getValue(mp.get(aeropuertos_id, aeropuerto_origen))["PAIS"]
        ciudad_origen = me.getValue(mp.get(aeropuertos_id, aeropuerto_origen))["CIUDAD"]
        string_origen = aeropuerto_origen + " - " + nombre_origen + " - " + pais_origen + " - " + ciudad_origen
        aeropuerto_destino = x["aeropuerto destino"]
        nombre_destino = me.getValue(mp.get(aeropuertos_id, aeropuerto_destino))["NOMBRE"]
        pais_destino = me.getValue(mp.get(aeropuertos_id, aeropuerto_destino))["PAIS"]
        ciudad_destino = me.getValue(mp.get(aeropuertos_id, aeropuerto_destino))["CIUDAD"]
        string_destino = aeropuerto_destino + " - " + nombre_destino + " - " + pais_destino + " - " + ciudad_destino
        
        
        distancia_recorrida = round(float(x["distancia recorrida"]), 2)
        distancia_recorrida_total += float(x["distancia recorrida"])
        tiempo_trayecto = x["tiempo trayecto"]
        aeronaves = x["aeronaves"]
        
        resultado = [string_origen, string_destino, distancia_recorrida, tiempo_trayecto]
        lista.append(resultado)
    
    print(tabulate(lista, headers=["Origen - Nombre Origen - Pais Origen - Ciudad Origen", "Destino - Nombre Destino - Pais destino - Ciudad Destino", "Distancia Recorrida", "Duración"], tablefmt="rounded_grid"))
    print("")
    print("La suma de las distancias de los trayectos es: " +str(round(distancia_recorrida_total, 3)))


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    aeropuertos_id = control["model"]["airports_id"]
    memoria = input("Quiere ver la memoria almacenada? Diga True o False")
    tiempo_total, aeropuerto_mayor_ocurrencias, cantidad_ocurrencias, cantidad_trayectos, respuesta, dist_tot = controller.req_4(control)
    tiempo_total = round(float(tiempo_total), 2)
    print("El tiempo total de ejecución fue de: " + str(tiempo_total) + " ms.")
    print("La distancia de la red de aeropuertos es: " + str(round(float(dist_tot), 2)) + " km")
    print("El aeropuerto más importante según la concurrencia de carga fue: ")
    
    icao = me.getValue(mp.get(aeropuertos_id, aeropuerto_mayor_ocurrencias))["ICAO"]
    nombre = me.getValue(mp.get(aeropuertos_id, aeropuerto_mayor_ocurrencias))["NOMBRE"]
    ciudad = me.getValue(mp.get(aeropuertos_id, aeropuerto_mayor_ocurrencias))["CIUDAD"]
    pais = me.getValue(mp.get(aeropuertos_id, aeropuerto_mayor_ocurrencias))["PAIS"]
    resultado = [icao, nombre, ciudad, pais, cantidad_ocurrencias]
    print(tabulate([resultado], headers=["ICAO", "NOMBRE", "Ciudad", "PAIS", "CANTIDAD OCURRENCIAS"], tablefmt="rounded_grid"))
    
    print("El número total de trayectos es: " + str(cantidad_trayectos))
    
    print("\n A continuación, la secuencia de trayectos encontrados: \n")
    
    mostrar_req4(control["model"], respuesta)
    
def mostrar_req4(data_structs, lst):
    aeropuertos_id = data_structs["airports_id"]
    
    lista = []
    resultado = []
    for x in lt.iterator(lst):
        aeropuerto_origen = x["aeropuerto origen"]
        nombre_origen = me.getValue(mp.get(aeropuertos_id, aeropuerto_origen))["NOMBRE"]
        pais_origen = me.getValue(mp.get(aeropuertos_id, aeropuerto_origen))["PAIS"]
        ciudad_origen = me.getValue(mp.get(aeropuertos_id, aeropuerto_origen))["CIUDAD"]
        string_origen = aeropuerto_origen + " - " + nombre_origen + " - " + pais_origen + " - " + ciudad_origen
        aeropuerto_destino = x["aeropuerto destino"]
        nombre_destino = me.getValue(mp.get(aeropuertos_id, aeropuerto_destino))["NOMBRE"]
        pais_destino = me.getValue(mp.get(aeropuertos_id, aeropuerto_destino))["PAIS"]
        ciudad_destino = me.getValue(mp.get(aeropuertos_id, aeropuerto_destino))["CIUDAD"]
        string_destino = aeropuerto_destino + " - " + nombre_destino + " - " + pais_destino + " - " + ciudad_destino
        
        
        distancia_recorrida = round(float(x["distancia recorrida"]), 2)
        tiempo_trayecto = x["tiempo trayecto"]
        aeronaves = x["aeronaves"]
        
        resultado = [string_origen, string_destino, distancia_recorrida, tiempo_trayecto, aeronaves]
        lista.append(resultado)
    
    print(tabulate(lista, headers=["Origen - Nombre Origen - Pais Origen - Ciudad Origen", "Destino - Nombre Destino - Pais destino - Ciudad Destino", "Distancia Recorrida", "Duración", "Aeronaves"], tablefmt="rounded_grid"))
    


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    aeropuertos_id = control["model"]["airports_id"]
    tiempo_total, aeropuerto_mayor_ocurrencias, cantidad_ocurrencias, cantidad_trayectos, respuesta, distancia_total_trayectos = controller.req_5(control)
    tiempo_total = round(float(tiempo_total), 2)
    print("El tiempo total de ejecución fue de: " + str(tiempo_total) + " ms.")
    print("La distancia de la red de aeropuertos es: " + str(round(float(distancia_total_trayectos), 2)) + " km")
    print("El aeropuerto más importante según la concurrencia de carga fue: ")
    
    icao = me.getValue(mp.get(aeropuertos_id, aeropuerto_mayor_ocurrencias))["ICAO"]
    nombre = me.getValue(mp.get(aeropuertos_id, aeropuerto_mayor_ocurrencias))["NOMBRE"]
    ciudad = me.getValue(mp.get(aeropuertos_id, aeropuerto_mayor_ocurrencias))["CIUDAD"]
    pais = me.getValue(mp.get(aeropuertos_id, aeropuerto_mayor_ocurrencias))["PAIS"]
    resultado = [icao, nombre, ciudad, pais, cantidad_ocurrencias]
    print(tabulate([resultado], headers=["ICAO", "NOMBRE", "Ciudad", "PAIS", "CANTIDAD OCURRENCIAS"], tablefmt="rounded_grid"))
    
    print("El número total de trayectos es: " + str(cantidad_trayectos))
    
    print("\n A continuación, la secuencia de trayectos encontrados: \n")

    lista = []
    resultado = []
    for x in lt.iterator(respuesta):
        aeropuerto_origen = x["aeropuerto origen"]
        nombre_origen = me.getValue(mp.get(aeropuertos_id, aeropuerto_origen))["NOMBRE"]
        pais_origen = me.getValue(mp.get(aeropuertos_id, aeropuerto_origen))["PAIS"]
        ciudad_origen = me.getValue(mp.get(aeropuertos_id, aeropuerto_origen))["CIUDAD"]
        string_origen = aeropuerto_origen + " - " + nombre_origen + " - " + pais_origen + " - " + ciudad_origen
        aeropuerto_destino = x["aeropuerto destino"]
        nombre_destino = me.getValue(mp.get(aeropuertos_id, aeropuerto_destino))["NOMBRE"]
        pais_destino = me.getValue(mp.get(aeropuertos_id, aeropuerto_destino))["PAIS"]
        ciudad_destino = me.getValue(mp.get(aeropuertos_id, aeropuerto_destino))["CIUDAD"]
        string_destino = aeropuerto_destino + " - " + nombre_destino + " - " + pais_destino + " - " + ciudad_destino
        
        
        distancia_recorrida = round(float(x["distancia recorrida"]), 2)
        tiempo_trayecto = x["tiempo trayecto"]
        aeronaves = x["aeronaves"]
        
        resultado = [string_origen, string_destino, distancia_recorrida, tiempo_trayecto, aeronaves]
        lista.append(resultado)
    
    print(tabulate(lista, headers=["Origen - Nombre - Pais - Ciudad Origen", "Destino - Nombre - Pais - Ciudad", "Distancia", "Tiempo", "Aeronaves"], tablefmt="rounded_grid"))
    


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    aeropuertos_id = control["model"]["airports_id"]
    vuelos = control["model"]["flights"]
    M = int(input("Digite el número de aereopuertos: "))
    tiempo_total, aeropuerto_mayor_ocurrencias, cantidad_ocurrencias, lst_retornar = controller.req_6(control, M)
    tiempo_total = round(float(tiempo_total), 2)
    print("El tiempo total de ejecución fue de: " + str(tiempo_total) + " ms.")
    
    print("El aeropuerto más importante según la concurrencia de carga fue: ")
    
    icao = me.getValue(mp.get(aeropuertos_id, aeropuerto_mayor_ocurrencias))["ICAO"]
    nombre = me.getValue(mp.get(aeropuertos_id, aeropuerto_mayor_ocurrencias))["NOMBRE"]
    ciudad = me.getValue(mp.get(aeropuertos_id, aeropuerto_mayor_ocurrencias))["CIUDAD"]
    pais = me.getValue(mp.get(aeropuertos_id, aeropuerto_mayor_ocurrencias))["PAIS"]
    resultado = [icao, nombre, ciudad, pais, cantidad_ocurrencias]
    print(tabulate([resultado], headers=["ICAO", "NOMBRE", "Ciudad", "PAIS", "CANTIDAD OCURRENCIAS"], tablefmt="rounded_grid"))
    i = 1
    for camino in lt.iterator(lst_retornar):
        ae_origen, ae_destino, lista_aeropuertos, cantidad_aeropuerto_visitados, tiempo_entre_trayectos, distancia_trayecto = camino
        print(".........................................................")
        print("")
        print("Camino #"+str(i)+": "+ ae_origen +"-"+ ae_destino)
        print("El número total de trayectos es: " + str(cantidad_aeropuerto_visitados))
        print("\n Aeropuertos intermedios: ")
        lista = []
        resultado = []
        contador = 0
        if lt.size(lista_aeropuertos) > 1:
            for x_vertice in lt.iterator(lista_aeropuertos):
                x = x_vertice['vertexA']
                if contador < lt.size(lista_aeropuertos):
                    if ((x!= ae_origen) and (x!= ae_destino)):
                        icao = me.getValue(mp.get(aeropuertos_id, x))["ICAO"]
                        nombre = me.getValue(mp.get(aeropuertos_id, x))["NOMBRE"]
                        ciudad = me.getValue(mp.get(aeropuertos_id, x))["CIUDAD"]
                        pais = me.getValue(mp.get(aeropuertos_id, x))["PAIS"]
                        resultado = [icao, nombre, ciudad, pais]
                        lista.append(resultado)
                        contador +=1
                else:
                    x = x_vertice['vertexB']
                    if ((x!= ae_origen) and (x!= ae_destino)):
                        icao = me.getValue(mp.get(aeropuertos_id, x))["ICAO"]
                        nombre = me.getValue(mp.get(aeropuertos_id, x))["NOMBRE"]
                        ciudad = me.getValue(mp.get(aeropuertos_id, x))["CIUDAD"]
                        pais = me.getValue(mp.get(aeropuertos_id, x))["PAIS"]
                        resultado = [icao, nombre, ciudad, pais]
                        lista.append(resultado)
                        contador +=1
            
            print(tabulate(lista, headers=["ICAO", "NOMBRE", "Ciudad", "PAIS"], tablefmt="rounded_grid"))
            
            print("\n Vuelos incluidos en su camino:")
            print(ae_origen)
            print("->")
            for elem in lista:
                print(elem[0])
                print("->")
            print(ae_destino)
        else:
            print('\nNo hay aeropuertos intermedios\n')
            print("\n Vuelos incluidos en su camino:")
            print(ae_origen)
            print("->")
            print(ae_destino)
            
            
        print("\n Aereopuerto de destino: ")
        icao = me.getValue(mp.get(aeropuertos_id, ae_destino))["ICAO"]
        nombre = me.getValue(mp.get(aeropuertos_id, ae_destino))["NOMBRE"]
        ciudad = me.getValue(mp.get(aeropuertos_id, ae_destino))["CIUDAD"]
        pais = me.getValue(mp.get(aeropuertos_id, ae_destino))["PAIS"]
        resultado_destino = [icao, nombre, ciudad, pais]
        print(tabulate([resultado_destino], headers=["ICAO", "NOMBRE", "Ciudad", "PAIS"], tablefmt="rounded_grid"))
        
        distancia_trayecto = round(float(distancia_trayecto), 2)
        print("La distancia total para ir de ambos lugares es: " + str(distancia_trayecto) + "km. ")
        
        
        print("")
        i +=1


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    latitud_origen = input('Ingrese la latitud del punto de origen para la búsqueda: ')
    longitud_origen = input('Ingrese la longitud del punto de origen para la búsqueda: ')
    latitud_destino = input('Ingrese la latitud del punto de destino para la búsqueda: ')
    longitud_destino = input('Ingrese la longitud del punto de destino para la búsqueda: ')
    time, ae_origen, ae_destino, duracion, distancia, num_aeropuertos, respuesta, cheking, tiempo_trayecto, distancia_entre_trayectos = controller.req_7(control, latitud_origen, longitud_origen, latitud_destino, longitud_destino)
    tiempo_total = round(float(time), 2)
    print("El tiempo total de ejecución fue de: " + str(tiempo_total) + " ms.")
    if cheking == False:
        print("No se encontró un aeropuerto cercano a menos de 30km desde la ubicación ofrecida.")
        ae_destino = round(float(ae_destino), 2)
        print("Sin embargo, el aeropuerto más cercano fue " + str(ae_origen) + str(" a una distancia de ") + str(ae_destino))    
    elif cheking == None:
        print("")
        print("Se encontró un aeropuerto a una distancia menor de 30km.")
        print("Sin embargo, no hay un camino que lleve desde dicho diccionario hasta la posición de destino. ")
        round(float(ae_destino), 2)
        print("El aeropuerto más cercano fue " + str(ae_origen) + str(" a una distancia de ") + str(ae_destino))
    elif cheking == True:
        print("")
        distancia = round(float(distancia), 2)
        print("La distancia total para ir del lugar de origen al destino es: " + str(distancia) + " km. ")
        print("El tiempo total para ir del lugar de origen al destino es: " + str(tiempo_trayecto) + " min. ")
        print("La cantidad de aeropuertos visitados fue de: " + str(num_aeropuertos+1))
        mostrar_req7(control, respuesta, ae_origen, ae_destino)
        
        print("\nTiempo entre trayectos: \n")
        for z in lt.iterator(duracion):
            print(str(z) + ' min')  
        print("\nDistancia entre trayectos: \n")
        for e in lt.iterator(distancia_entre_trayectos):
            print(str(e) + ' km')  
        print('\n')
        
def mostrar_req7(control, respuesta, ae_origen, ae_destino):
    aeropuertos_id = control["model"]["airports_id"]
    lista = []
    resultado = []
    
    #para el de origen
    print("\n Aeropuerto de origen: \n")
    icao = me.getValue(mp.get(aeropuertos_id, ae_origen))["ICAO"]
    nombre = me.getValue(mp.get(aeropuertos_id, ae_origen))["NOMBRE"]
    ciudad = me.getValue(mp.get(aeropuertos_id, ae_origen))["CIUDAD"]
    pais = me.getValue(mp.get(aeropuertos_id, ae_origen))["PAIS"]
    resultado = [icao, nombre, ciudad, pais]
    print(tabulate([resultado], headers=["ICAO", "NOMBRE", "Ciudad", "PAIS"], tablefmt="rounded_grid"))
    
    print("\n Aeropuertos intermedios: ")
    lista = []
    resultado = []
    contador = 0
    if lt.size(respuesta) > 1:
        for x_vertice in lt.iterator(respuesta):
            x = x_vertice['vertexA']
            if contador < lt.size(respuesta):
                if ((x!= ae_origen) and (x!= ae_destino)):
                    icao = me.getValue(mp.get(aeropuertos_id, x))["ICAO"]
                    nombre = me.getValue(mp.get(aeropuertos_id, x))["NOMBRE"]
                    ciudad = me.getValue(mp.get(aeropuertos_id, x))["CIUDAD"]
                    pais = me.getValue(mp.get(aeropuertos_id, x))["PAIS"]
                    resultado = [icao, nombre, ciudad, pais]
                    lista.append(resultado)
                    contador +=1
            else:
                x = x_vertice['vertexB']
                if ((x!= ae_origen) and (x!= ae_destino)):
                    icao = me.getValue(mp.get(aeropuertos_id, x))["ICAO"]
                    nombre = me.getValue(mp.get(aeropuertos_id, x))["NOMBRE"]
                    ciudad = me.getValue(mp.get(aeropuertos_id, x))["CIUDAD"]
                    pais = me.getValue(mp.get(aeropuertos_id, x))["PAIS"]
                    resultado = [icao, nombre, ciudad, pais]
                    lista.append(resultado)
                    contador +=1
        
        print(tabulate(lista, headers=["ICAO", "NOMBRE", "Ciudad", "PAIS"], tablefmt="rounded_grid"))
    else:
        print('\nNo hay aeropuertos intermedios\n')
    
    print("\n Aeropuerto de destino: \n")
    lista = []
    resultado = []
    icao = me.getValue(mp.get(aeropuertos_id, ae_destino))["ICAO"]
    nombre = me.getValue(mp.get(aeropuertos_id, ae_destino))["NOMBRE"]
    ciudad = me.getValue(mp.get(aeropuertos_id, ae_destino))["CIUDAD"]
    pais = me.getValue(mp.get(aeropuertos_id, ae_destino))["PAIS"]
    resultado = [icao, nombre, ciudad, pais]
    print(tabulate([resultado], headers=["ICAO", "NOMBRE", "Ciudad", "PAIS"], tablefmt="rounded_grid"))
    
def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass

def print_tuplas(control):
    camino_t, cantidad_aeropuerto_visitados_t, distancia_entre_trayectos_t, camino, cantidad_aeropuerto_visitados, distancia_entre_trayectos, lst_tuple, lst = controller.bono_tuplas(control)
    print("")
    print("\nDijskstra\n")
    print('Para el algorimo de Dijskstra con tuplas se obtuvo el siguiente resultado: \n')
    print('Un total de: ' + str(cantidad_aeropuerto_visitados_t) + ' aeropuertos visitados')
    print('Los trayectos fueron los siguientes: ')
    for d in lt.iterator(distancia_entre_trayectos_t):
        print(d)
    print('\nPara el algorimo de Dijskstra sin las tuplas se obtuvo el siguiente resultado: \n')
    print('Un total de: ' + str(cantidad_aeropuerto_visitados) + ' aeropuertos visitados')
    print('Los trayectos fueron los siguientes: ')
    for r in lt.iterator(distancia_entre_trayectos):
        print(r)
    print("\nPrim\n")
    print('Para el algoritmo de Prim con tuplas se obtulo la siguiente lista de aeropuertos hacia donde hay conexión: \n')
    print(lst_tuple)
    print('\nPara el algoritmo de Prim sin las tuplas se obtulo la siguiente lista de aeropuertos hacia donde hay conexión: \n')
    print(lst)

def mostrar_info(control):
    l1, l2, l3 = controller.mostrar_info(control)
    return l1, l2 ,l3

def print_first_last(lst, control):
    aeropuertos_id = control["model"]["airports_id"]
    lista = []
    resultado = []
    for x in lt.iterator(lst):
        name = me.getValue(mp.get(aeropuertos_id, x["nombre"]))["NOMBRE"]
        ciudad = me.getValue(mp.get(aeropuertos_id, x["nombre"]))["CIUDAD"]
        concurrencia = x["cantidad"]
        resultado = [name, x["nombre"], ciudad, concurrencia]
        lista.append(resultado)
    
    print(tabulate(lista, headers=["Nombre", "ICAO", "Ciudad", "Concurrencia"], tablefmt="rounded_grid"))
# Se crea el controlador asociado a la vista


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
            
            resp = input("Quiere ver la memoria almacenada? Diga True o False. ")
            resp = controller.convertir_bool(resp)
            
            control = new_controller()
            
            print("Cargando información de los archivos ....\n")
            
            data = load_data(control, resp)
            print("Cantidad de vuelos cargados: " + str(data[0]))
            print("Cantidad de aeropuertos cargados: " + str(data[1]))
            print("El tiempo de la carga de datos fue: " + str(round(float(data[2]), 2)))
            
            if resp == True:
                print("La memoria en Kb fue: " + str(round(float(data[3]), 2)))
            
            l1, l2, l3 = mostrar_info(control)
            
            sublista_militares_first = lt.subList(l1, 1, 5)
            sublista_militares_last = lt.subList(l1, lt.size(l1) - 4, 5)
            sublista_comercial_first = lt.subList(l2, 1, 5)
            sublista_comercial_last = lt.subList(l2, lt.size(l2) - 4, 5)
            sublista_carga_first = lt.subList(l3, 1, 5)
            sublista_carga_last = lt.subList(l3, lt.size(l3) - 4, 5)
            
            print("\n Primeros 5 aeropuertos mayor concurrencia comercial: \n")
            print_first_last(sublista_comercial_first, control)
            print("\n Últimos 5 aeropuertos mayor concurrencia comercial: \n")
            print_first_last(sublista_comercial_last, control)
            print("\n Primeros 5 aeropuertos mayor concurrencia carga: \n")
            print_first_last(sublista_carga_first, control)
            print("\n Últimos 5 aeropuertos mayor concurrencia carga: \n")
            print_first_last(sublista_carga_last, control)
            print("\n Primeros 5 aeropuertos mayor concurrencia militar: \n")
            print_first_last(sublista_militares_first, control)
            print("\n Últimos 5 aeropuertos mayor concurrencia: \n")
            print_first_last(sublista_militares_last, control)
            print("\n")
            
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)
        
        elif int(inputs) == 10:
            print_tuplas(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
            
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)