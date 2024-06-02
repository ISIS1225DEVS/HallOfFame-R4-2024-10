"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrollado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
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
 * along withthis program.If not, see <http://www.gnu.org/licenses/>.
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
import controller

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
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    loaded = controller.load_data(control)
    return loaded

def Datesort(lista):
    listaord = controller.Datesort(lista)
    return listaord

def printSorted(head, data):
    HoT = controller.tabulation3(data, head)
    print(tabulate(HoT, headers = "keys", tablefmt="pretty"))

def print_data(control, data):
    print("La cantidad de aeropuertos cargados es: ",data[1][0])
    print("La cantidad de vuelos cargados es: ", data[1][1])
    #COMERCIAL
    print("Información 5 aeropuertos con más concurrencia de tipo comercial: ")
    print(tabulate(data[1][2], headers = "keys", tablefmt="pretty"))
    print("Información 5 aeropuertos con menos concurrencia de tipo comercial: ")
    print(tabulate(data[1][3], headers = "keys", tablefmt="pretty"))
    #CARGA
    print("Información 5 aeropuertos con más concurrencia de tipo carga: ")
    print(tabulate(data[1][4], headers = "keys", tablefmt="pretty"))
    print("Información 5 aeropuertos con menos concurrencia de tipo carga: ")
    print(tabulate(data[1][5], headers = "keys", tablefmt="pretty"))
    #MILITAR
    print("Información 5 aeropuertos con más concurrencia de tipo militar: ")
    print(tabulate(data[1][6], headers = "keys", tablefmt="pretty"))
    print("Información 5 aeropuertos con menos concurrencia de tipo militar: ")
    print(tabulate(data[1][7], headers = "keys", tablefmt="pretty"))

def print_req_1(control, origen, destino):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    resultado = controller.req_1(control, origen, destino)
    #totalDistance, OriginaInfo, DestInfo, valuesList, numAeropuertos
    print(f"Distancia total {resultado[0]}")
    print("Información Origen: ")
    print(tabulate(resultado[1], headers = "keys", tablefmt="pretty"))
    print("Información Destino: ")
    print(tabulate(resultado[2], headers = "keys", tablefmt="pretty"))
    print("Información Escalas: ")
    print(tabulate(resultado[3], headers = "keys", tablefmt="pretty"))
    print(f"Número Aeropuertos visitados {resultado[4]}")

    pass



def print_req_2(control, origen, destino):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    #cv = [(4.601992771389502;-74.06610470441926), (10.507688799813222;-75.4706488665794)]
    
    resultado = controller.req_2(control, origen, destino)
    # NumeroDeEscalas, OriginInfo, DestinoInfo,  Dics con info de escalas involucradas, distancia total
    print(f"Numero de escalas total {resultado[0]}")
    print("Información Origen: ")
    print(tabulate(resultado[1], headers = "keys", tablefmt="pretty"))
    print("Información Destino: ")
    print(tabulate(resultado[2], headers = "keys", tablefmt="pretty"))
    print("Información Escalas: ")
    print(tabulate(resultado[3], headers = "keys", tablefmt="pretty"))
    print(f"Distancia total viaje {resultado[4]}")

    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    print("Procesando requerimiento.....")
    resultado = controller.req_3(control)
    #TopKeyInfo, Top, totalDistance, numTotal, listaTrayectos

    print("Información del aeropuerto más importante según la concurrencia: ")
    print(tabulate(resultado[0], headers = "keys", tablefmt="pretty"))
    print(f"Con un valor de concurrencia de {int(resultado[1])} ocurrencias")
    print(f"Distancia total  de los trayectos (origen): {resultado[2]} Km")
    print("*" * 60)
    print(f"Número total de trayectos posibles: {resultado[3]} trayectos")
    print("-+-" * 20)
    print("Información secuencia de trayectos encontrados: ")
    print(tabulate(resultado[4], headers = "keys", tablefmt="pretty"))

    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    print("Procesando requerimiento.....")
    resultado = controller.req_4(control)
    print("El aeropuerto más importante según la concurrencia de tipo carga:")
    print(tabulate(resultado[0], headers = "keys", tablefmt="pretty"))
    print("La distancia total de los aeropuertos más importantes según la concurrencia es: ",resultado[1])
    print("El número de trayectos posibles desde el aeropuerto de mayor importancia es: ",resultado[2])
    print("Información de los trayectos encontrados: ")
    print(tabulate(resultado[3], headers = "keys", tablefmt="pretty"))


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    print("Procesando requerimiento.....")
    lista = controller.req_5(control)

    print(f"Aeropuerto más impotante: ")
    print(tabulate(lista[0], headers = "keys", tablefmt="pretty"))    
    print(f"Distancia total: {lista[1]}")
    print(f"Cantidad de trayectos recorridos: {lista[2]}")
    print("Información de trayectos: ")
    print(tabulate(lista[3], headers = "keys", tablefmt="pretty"))

    pass


def print_req_6(control, M):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    resultado = controller.req_6(control, M)
    print("El aeropuerto con mayor concurrencia comercial es: ")
    print(tabulate(resultado[0], headers = "keys", tablefmt="pretty"))
    print("La cantidad de vueloves saliendo y llegando a este aeropuerto es: ",resultado[1])
    print("Información de los caminos desde el aeropuerto de mayor concurrencia comercial: ")
    for i in range(0,len(resultado[2])):
        element = resultado[2][i]
        for key in element:
            if key == "AeropuertosIncluidos" or key == "VuelosIncluidos":
                resultado[2][i][key] = element[key]["elements"]
    print(tabulate(resultado[2], headers = "keys", tablefmt="pretty"))

def print_req_7(control, origen, destino):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    resultado = controller.req_7(control, origen, destino)
    print("El tiempo total del camino es: ",resultado[0])
    print("La distancia total del camino es: ",resultado[1])
    print("El número de aeropuertos visitados en el camino encontrado es: ",resultado[2])
    print("Información de los aeropuertos visitados: ")
    print(tabulate(resultado[3], headers = "keys", tablefmt="pretty"))
    print("Información de los trayectos: ")
    print(tabulate(resultado[4], headers = "keys", tablefmt="pretty"))


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
            data = load_data(control)
            print_data(control,data)
        elif int(inputs) == 2:
            origen = tuple(input("Ingrese el punto de origen (una localización geográfica con latitud y longitud con un punto y coma como separador): ").split(";"))
            destino = tuple(input("Ingrese el punto de destino (una localización geográfica con latitud y longitud con un punto y coma como separador): ").split(";"))
            print_req_1(control, origen, destino)

        elif int(inputs) == 3:
            origen = tuple(input("Ingrese el punto de origen (una localización geográfica con latitud y longitud con un punto y coma como separador): ").split(";"))
            destino = tuple(input("Ingrese el punto de destino (una localización geográfica con latitud y longitud con un punto y coma como separador): ").split(";"))
            print_req_2(control, origen, destino)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            cantidad = int(input("Ingrese la cantidad de aeropuertos más importantes en Colombia que desea cubrir: "))
            print_req_6(control, cantidad)

        elif int(inputs) == 8:
            origen = tuple(input("Ingrese el punto de origen (una localización geográfica con latitud y longitud con un punto y coma como separador): ").split(";"))
            destino = tuple(input("Ingrese el punto de destino (una localización geográfica con latitud y longitud con un punto y coma como separador): ").split(";"))
            print_req_7(control, origen, destino)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
            
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)