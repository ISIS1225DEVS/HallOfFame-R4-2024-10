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
import model
"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
default_limit = 1000
sys.setrecursionlimit(default_limit*10)
##########################################################################################################################
##########################################################################################################################

def new_controller():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    return controller.new_controller()

##########################################################################################################################
##########################################################################################################################

def print_menu():
    """
    Función que imprime el menú de opciones del reto 4
    """
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

##########################################################################################################################
##########################################################################################################################

def print_data(sublist, dic):
    """
    Imprime la tabla apartir de las llaves que se quieran extraer
    """
    headers = {key:[] for key in dic}
    
    for job in lt.iterator(sublist):
        for key in headers:
            headers[key].append(job[dic[key]])
    
    print(tabulate(headers, headers="keys", tablefmt="rounded_grid", showindex="always",
                   colalign=("left", "left", "left"), numalign="left", stralign="left") + "\n")

##########################################################################################################################
##########################################################################################################################

def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    
    return controller.load_data(control)

##########################################################################################################################
##########################################################################################################################

# inicio de código sacado de ChatGpt
def imprimir_titulo(titulo):
    # ANSI escape codes para colores
    rojo = '\033[91m'
    negrita = '\033[1m'
    reset = '\033[0m'

    # Crear bordes
    longitud = len(titulo) + 4
    borde_superior = f"+{'-' * longitud}+"
    borde_inferior = borde_superior

    # Imprimir el título con bordes y colores
    print(f"{rojo}{negrita}{borde_superior}")
    print(f"|  {titulo}  |")
    print(f"{borde_inferior}{reset}")
# fin de código de ChatGpt

##########################################################################################################################
##########################################################################################################################

def print_option_1(control):
    """
    Función que imprime la opción 1 del menú de opciones
    """
    # TODO: Completar la funcion de carga de datos
    print("Cargando información de los archivos ....\n")
    data = load_data(control)
    
    dic = {
        "Nombre del aeropuerto":"NOMBRE",
        "ICAO":"ICAO",
        "Ciudad":"CIUDAD",
        "Concurrencia":"CONCURRENCE",
    }
    data_structs= control["model"]
    imprimir_titulo("Tabla de los primeros y ultimos aeropuertos con mayor concurrencia comercial")
    lista_comercial =  model.get_n_first_last_concurrence(data_structs,data_structs["airports_comercial_map"],5)
    print_data(lista_comercial,dic)
    
    imprimir_titulo("Tabla de los primeros y ultimos aeropuertos con mayor concurrencia de carga")
    lista_carga = model.get_n_first_last_concurrence(data_structs,data_structs["airports_carga_map"],5)
    print_data(lista_carga,dic)
    
    imprimir_titulo("Tabla de los primeros y ultimos aeropuertos con mayor concurrencia militar")
    lista_militar = model.get_n_first_last_concurrence(data_structs,data_structs["airports_militar_map"],5)
    print_data(lista_militar,dic)
        
    print("El número total de aeropuertos cargados es de: ",data[1])
    print("El número total de vuelos cargados en el archivo es de: ",data[2])
    print("Tiempo: ",data[3])
    
    return data[0]

##########################################################################################################################
##########################################################################################################################

def print_req_1(control):
    """
    Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    
    origen_latitud = float(input("Ingresa la latitud del punto de origen: "))
    origen_longitud = float(input("Ingresa la longitud del punto de origen: "))
    destino_latitud = float(input("Ingresa la latitud del punto de destino: "))
    destino_longitud = float(input("Ingresa la longitud del punto de destino: "))
    method = int(input("""Seleccione el metodo con el cual desea realizar la busqueda: \n
                        1. bfs \n
                        2. dfs \n"""))
    data = controller.req_1(control,origen_latitud,origen_longitud,destino_latitud,destino_longitud,method)
    
    dic = {
        "ICAO":"ICAO",
        "Nombre del aeropuerto":"NOMBRE",
        "Ciudad":"CIUDAD",
        "País":"PAIS",
    }
    
    if data[1] is not None :
        delta,distancia_total,total_airports,respuesta,tiempo_total = data
        imprimir_titulo("Camino encontrado desde el sitio de origen al aeropuerto de destino")
        print_data(respuesta,dic)
        print("Tiempo: ",delta)
        print("La distancia total que tomará el camino entre el punto de origen y el de destino es de: ",distancia_total)
        print("El número total de aeropuertos que se visitan del camino encontrado es de: ",total_airports)
        print("El tiempo del trayecto es de: ",tiempo_total)
        respuesta= print_check(respuesta)
        return respuesta
    
    else: 
        print("Tiempo: ",data[0])
        print("No existe una ruta entre el sitio de origen al sitio de destino")
        
        return None
    
##########################################################################################################################
##########################################################################################################################

def print_req_2(control):
    """
    Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    origen_latitud = float(input("Ingresa la latitud del punto de origen: "))
    origen_longitud = float(input("Ingresa la longitud del punto de origen: "))
    destino_latitud = float(input("Ingresa la latitud del punto de destino: "))
    destino_longitud = float(input("Ingresa la longitud del punto de destino: "))
    
    data = controller.req_2(control,origen_latitud,origen_longitud,destino_latitud,destino_longitud)
    
    dic = {
        "ICAO":"ICAO",
        "Nombre del aeropuerto":"NOMBRE",
        "Ciudad":"CIUDAD",
        "País":"PAIS",
    }
    if data[1] is not None :
        delta,distancia_total,total_airports,respuesta,tiempo_total = data
        imprimir_titulo("Camino encontrado desde el sitio de origen al aeropuerto de destino")
        print_data(respuesta,dic)
        print("Tiempo: ",delta)
        print("La distancia total que tomará el camino entre el punto de origen y el de destino es de: ",distancia_total)
        print("El número total de aeropuertos que se visitan en el camino encontrado es de: ",total_airports)
        print("El tiempo del trayecto es de: ",tiempo_total)
        
        respuesta = print_check(respuesta)
        
        return respuesta
        
    else: 
        print("Tiempo: ",data[0])
        print("No existe una ruta entre el sitio de origen al sitio de destino")
        
        return None

##########################################################################################################################
##########################################################################################################################

def print_req_3(control):
    """
    Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    delta,data,data_aeropuerto_mayor,total_trayectos,distancia_total = controller.req_3(control)
    imprimir_titulo("Secuencia de trayectos encontrados")
    dic = {
        "ICAO_O":"ICAO_origen",
        "Airport_O":"name_origen",
        "City_O":"ciudad_origen",
        "País_O":"pais_origen",
        "ICAO_D":"ICAO_destino",
        "Airport_D":"name_destino",
        "City_D":"ciudad_destino",
        "País_D":"pais_destino",
        "Distance": "distancia",
        "Time" : "tiempo",
        "Aeronave" : "aeronave"
        
    }
    
    print_data(data,dic)
    
    imprimir_titulo("Aeropuerto más importante según la concurrencia y tipo de vuelo comercial")
    dic = {
        "ICAO":"ICAO",
        "Nombre del aeropuerto":"NOMBRE",
        "Ciudad":"CIUDAD",
        "País":"PAIS",
        "concurrencia":"CONCURRENCE"
    }
    print_data(data_aeropuerto_mayor,dic)
    print("Tiempo: ",delta)
    print("La distancia total de los trayectos sumada es de: ",distancia_total)
    print("El número total de trayectos posibles es de: ",total_trayectos)
    data = print_check(data)
    return data

##########################################################################################################################
##########################################################################################################################

def print_req_4(control):
    """
    Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    
    delta,data,data_aeropuerto_mayor,total_trayectos,distancia_total = controller.req_4(control)
    imprimir_titulo("Secuencia de trayectos encontrados")
    dic = {
        "ICAO_O":"ICAO_origen",
        "Airport_O":"name_origen",
        "City_O":"ciudad_origen",
        "País_O":"pais_origen",
        "ICAO_D":"ICAO_destino",
        "Airport_D":"name_destino",
        "City_D":"ciudad_destino",
        "País_D":"pais_destino",
        "Distance": "distancia",
        "Time" : "tiempo",
        "Aeronave" : "aeronave"
        
    }
    
    print_data(data,dic)
    
    imprimir_titulo("Aeropuerto más importante según la concurrencia y tipo de vuelo carga")
    dic = {
        "ICAO":"ICAO",
        "Nombre del aeropuerto":"NOMBRE",
        "Ciudad":"CIUDAD",
        "País":"PAIS",
        "concurrencia":"CONCURRENCE"
    }
    print_data(data_aeropuerto_mayor,dic)
    print("Tiempo: ",delta)
    print("La distancia total de los trayectos sumada es de: ",distancia_total)
    print("El número total de trayectos posibles es de: ",total_trayectos)
    data = print_check(data)
    return data
    

##########################################################################################################################
##########################################################################################################################

def print_req_5(control):
    """
    Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    
    delta,data,data_aeropuerto_mayor,total_trayectos,distancia_total = controller.req_5(control)
    imprimir_titulo("Secuencia de trayectos encontrados")
    dic = {
        "ICAO_O":"ICAO_origen",
        "Airport_O":"name_origen",
        "City_O":"ciudad_origen",
        "País_O":"pais_origen",
        "ICAO_D":"ICAO_destino",
        "Airport_D":"name_destino",
        "City_D":"ciudad_destino",
        "País_D":"pais_destino",
        "Distance": "distancia",
        "Time" : "tiempo",
        "Aeronave" : "aeronave"
        
    }
    
    print_data(data,dic)
    
    imprimir_titulo("Aeropuerto más importante según la concurrencia y tipo de vuelo militar")
    dic = {
        "ICAO":"ICAO",
        "Nombre del aeropuerto":"NOMBRE",
        "Ciudad":"CIUDAD",
        "País":"PAIS",
        "concurrencia":"CONCURRENCE"
    }
    print_data(data_aeropuerto_mayor,dic)
    print("Tiempo: ",delta)
    print("La distancia total de los trayectos sumada es de: ",distancia_total)
    print("El número total de trayectos posibles es de: ",total_trayectos)
    data = print_check(data)
    return data

##########################################################################################################################
##########################################################################################################################

def print_req_6(control):
    """
    Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    num = int(input("Digite la cantidad de aeropuertos a cubrir: "))
    
    delta,data,airport_mayor = controller.req_6(control,num)
    
    if len(data) >0:
        dic3 = {
        "ICAO":"ICAO",
        "Nombre del aeropuerto":"NOMBRE",
        "Ciudad":"CIUDAD",
        "País":"PAIS",
        "concurrencia":"CONCURRENCE"
    }
        dic = {
                    "Origen":"vertexA",
                    "destino":"vertexB",
                }
        
        dic2 = {
            "ICAO":"ICAO",
            "Nombre":"name",
            "Ciudad":"ciudad",
            "Pais":"pais"
            
        }
        imprimir_titulo("Información del aeropuerto de mayor concurrencia comercial")
        print_data(airport_mayor,dic3)
        print(" ")
        imprimir_titulo("Información de cada uno de los caminos desde el aeropuerto con mayor concurrencia comercial")
        for airport in lt.iterator(data):
            print("######################################################################################################")
            print("El total de aeropuertos en el camino es de: ",airport["total"],"\n")
            print("Aeropuertos: ")
            print_data(airport["airports"],dic2)
            print("Vuelos: ")
            print_data(airport["ruta"],dic)
            print("La distancia total del camino es de: ",airport["distancia"],"\n")
            print("######################################################################################################")
        print("Tiempo: ",delta)
        data = print_check(data)
        return data

    else:
        print("Tiempo: ",delta)
        return None
    
##########################################################################################################################
##########################################################################################################################

def print_req_7(control):
    """
    Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    origen_latitud = float(input("Ingresa la latitud del punto de origen: "))
    origen_longitud = float(input("Ingresa la longitud del punto de origen: "))
    destino_latitud = float(input("Ingresa la latitud del punto de destino: "))
    destino_longitud = float(input("Ingresa la longitud del punto de destino: "))
    data = controller.req_7(control,origen_latitud,origen_longitud,destino_latitud,destino_longitud)
    
    if data[1] is not None :
        delta,distancia_total,total_airports,respuesta,tiempo_total = data
        imprimir_titulo("Camino encontrado desde el sitio de origen al aeropuerto de destino")
        dic= {"ICAO_O" : "ICAO_origen",
        "Airport_O":"Airport_O",
        "Ciudad_O":"Ciudad_O",
        "Pais_O":"Pais_O",
        "ICAO_D" :"ICAO_destino",
        "Airport_D":"Airport_D",
        "Ciudad_D":"Ciudad_D",
        "Pais_D":"Pais_D",
        "tiempo":"tiempo",
        "distancia":"distancia"}
        print_data(respuesta,dic)
        print("Tiempo: ",delta)
        print("La distancia total que tomará el camino entre el punto de origen y el de destino es de: ",distancia_total)
        print("El número total de aeropuertos que se visitan del camino encontrado es de: ",total_airports)
        print("El tiempo del trayecto es de: ",tiempo_total)
        respuesta = print_check(respuesta)
        return respuesta
    
        
        
    
    else: 
        print("Tiempo: ",data[0])
        print("No existe una ruta entre el sitio de origen al sitio de destino")
        return None
    
##########################################################################################################################
##########################################################################################################################

##########################################################################################################################
##########################################################################################################################

def print_req_8(control,respuesta):
    """
    Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    
    controller.req_8(control,respuesta)
    print("Se ha creado el mapa con exito!!!\n")

respuesta_re8= mp.newMap()

def print_check(lista):
    """
    Revisa si la función tiene mas de 10 elementos. Si es así, solo imprime 10 elementos.
    """
    if lt.size(lista) > 1000:
        sublista = controller.get_first_last_n(lista, 10)
        return sublista
    else:
        return lista
##########################################################################################################################
##########################################################################################################################

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
            print_option_1(control)
            
        elif int(inputs) == 2:
            data_req1=print_req_1(control)
            mp.put(respuesta_re8,1,data_req1)
            
        elif int(inputs) == 3:
            data_req2=print_req_2(control)
            mp.put(respuesta_re8,2,data_req2)
            
        elif int(inputs) == 4:
            data_req3=print_req_3(control)
            mp.put(respuesta_re8,3,data_req3)

        elif int(inputs) == 5:
            data_req4=print_req_4(control)
            mp.put(respuesta_re8,4,data_req4)
            
        elif int(inputs) == 6:
            data_req5=print_req_5(control)
            mp.put(respuesta_re8,5,data_req5)
            
        elif int(inputs) == 7:
            data_req6=print_req_6(control)
            mp.put(respuesta_re8,6,data_req6)

        elif int(inputs) == 8:
            data_req7=print_req_7(control)
            mp.put(respuesta_re8,7,data_req7)

        elif int(inputs) == 9:
            print_req_8(control,respuesta_re8)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
            
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
