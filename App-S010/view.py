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
import threading

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
default_limit = 1000
sys.setrecursionlimit(default_limit*10)

def new_controller():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    control=controller.new_controller()
    return control


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ruta entre dos destinos turísticos")
    print("3- Itinerario con menos escalas entre dos destinos turísticos")
    print("4- Red de trayectos comerciales de cobertura máxima desde el aeropuerto con mayor concurrencia")
    print("5- Red de trayectos de carga de distancia mínima partiendo del aeropuerto con mayor concurrencia")
    print("6- Red de respuesta militar de menor tiempo partiendo desde el aeropuerto con mayor importancia militar")
    print("7- Los caminos más cortos para la cobertura de los M aeropuertos más importantes del país")
    print("8- el camino más corto en tiempo para llegar entre dos puntos turísticos")
    print("9- Grafica de los resultados")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    data= controller.load_data(control)
    # data[0] es size_aerop, data[1] size_vuelos, data[2] deltatime
    return data

def print_terminar_carga_datos(data,control):
    result=controller.load_terminar_carga_datos(control)
    #[0] es 1st comercial,[1] last_com,[2] 1st_carga, [3]last_carga,
    #[4] 1st_mili, [5]last_mili,[6] deltatime 

    print("Total de aeropuertos cargados: "+str(data[0]))
    print("Total de vuelos cargados: "+str(data[1]))
    
    print_comerical(result[0],result[1],control)
    print("\n\n")
    print_carga(result[2],result[3],control)
    print("\n\n")
    print_militar(result[4],result[5],control)  
    print("\n\n")
    
    print("Tiempo de carga archivos: "+str(round(data[2],2)))
    print("tiempo de carga de datos: " +str(round(result[6],2)))


def print_comerical(first,last,control):
    size1=lt.size(first)
    size2=lt.size(last)
    if size1:
        print("\n\nEstos son los aeropuertos con MAYOR concurrencia COMERCIAL: \n")
        headers= ["ICAO","Nombre", "Ciudad", "Concurrencia"]
        table=[]
        for aerop in lt.iterator(first):
            #cada aerop es un {aerop:areopuerto,conc:concurrencia}          
            ans= [aerop["aerop"]["ICAO"],aerop["aerop"]["NOMBRE"],aerop["aerop"]["CIUDAD"],aerop["conc"]]
            
            table.append(ans)
        print(tabulate(table, headers=headers,tablefmt="github"))
    else:
        print("error")

    if size2:
        print("\n\nEstos son los aeropuertos con MENOR concurrencia COMERCIAL: \n")
        headers= ["ICAO","Nombre", "Ciudad", "Concurrencia"]
        table=[]
        for aerop in lt.iterator(last):
            #cada aerop es un {aerop:str,conc:int}          
            ans= [aerop["aerop"]["ICAO"],aerop["aerop"]["NOMBRE"],aerop["aerop"]["CIUDAD"],aerop["conc"]]
            
            table.append(ans)
        print(tabulate(table, headers=headers,tablefmt="github"))
    else: 
        print("error")

def print_carga(first,last,control):
    size1=lt.size(first)
    size2=lt.size(last)
    if size1:
        print("\n\nEstos son los aeropuertos con MAYOR concurrencia de CARGA: \n")
        headers= ["ICAO","Nombre", "Ciudad", "Concurrencia"]
        table=[]
        for aerop in lt.iterator(first):
            #cada aerop es un {aerop:str,conc:int}          
            ans= [aerop["aerop"]["ICAO"],aerop["aerop"]["NOMBRE"],aerop["aerop"]["CIUDAD"],aerop["conc"]]
            
            table.append(ans)
        print(tabulate(table, headers=headers,tablefmt="github"))
    else: 
        print("error")

    if size2:
        print("\n\nEstos son los aeropuertos con MENOR concurrencia de CARGA: \n")
        headers= ["ICAO","Nombre", "Ciudad", "Concurrencia"]
        table=[]
        for aerop in lt.iterator(last):
            #cada aerop es un {aerop:str,conc:int}          
            ans= [aerop["aerop"]["ICAO"],aerop["aerop"]["NOMBRE"],aerop["aerop"]["CIUDAD"],aerop["conc"]]
            table.append(ans)
        print(tabulate(table, headers=headers,tablefmt="github"))
    else: 
        print("error")

def print_militar(first,last,control):
    size1=lt.size(first)
    size2=lt.size(last)
    if size1:
        print("\n\nEstos son los aeropuertos con MAYOR concurrencia MILITAR: \n")
        headers= ["ICAO","Nombre", "Ciudad", "Concurrencia"]
        table=[]
        for aerop in lt.iterator(first):
            #cada aerop es un {aerop:str,conc:int}          
            ans= [aerop["aerop"]["ICAO"],aerop["aerop"]["NOMBRE"],aerop["aerop"]["CIUDAD"],aerop["conc"]]
            
            table.append(ans)
        print(tabulate(table, headers=headers,tablefmt="github"))
    else: 
        print("error")

    if size2:
        print("\n\nEstos son los aeropuertos con MENOR concurrencia MILITAR: \n")
        headers= ["ICAO","Nombre", "Ciudad", "Concurrencia"]
        table=[]
        for aerop in lt.iterator(last):
            #cada aerop es un {aerop:str,conc:int}          
            ans= [aerop["aerop"]["ICAO"],aerop["aerop"]["NOMBRE"],aerop["aerop"]["CIUDAD"],aerop["conc"]]
            
            table.append(ans)
        print(tabulate(table, headers=headers,tablefmt="github"))
    else: 
        print("error")


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control,o_latitud,o_longitud,d_latitud,d_longitud):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    result= controller.req_1(control,o_latitud,o_longitud,d_latitud,d_longitud)
    #[0]result, [1] no_airports, [2] time_total, [3] dist_vuelos,[4] o_dist,[5]d_dist,[6] deltatime
    
    print("\n\nTiempo de ejecución del requerimiento: "+str(round(result[6],2)))

    if result[1]!=0:
        print("\nEsta fue la ruta encontrada: \n")
        headers= ["ICAO","Nombre", "Ciudad", "País"]
        table=[]
        for aerop in lt.iterator(result[0]):        
            ans= [aerop["ICAO"],aerop["NOMBRE"],aerop["CIUDAD"],aerop["PAIS"]]
            table.append(ans)
        print(tabulate(table, headers=headers,tablefmt="github"))

        print("\nAeropuertos visitados en el camino: "+str(result[1]))
        aerop_o=lt.getElement(result[0],1)
        aerop_d=lt.getElement(result[0],lt.size(result[0]))
        
        print("\nDISTANCIA: ")
        print("De punto origen a {0}: {1} km".format(aerop_o["ICAO"],round(result[4],2)))
        print("Viaje de {0} a {1}: {2} km".format(aerop_o["ICAO"],aerop_d["ICAO"],round(result[3],2)))
        print("{0} a destino: {1} km".format(aerop_d["ICAO"],round(result[5],2)))
        print("DISTANCIA TOTAL: {0} km".format(round(result[3]+result[4]+result[5],2)))

        print("\nTIEMPO TOTAL: {0} min\n".format(result[2]))
    else:
        print("\n\n")
        for i in lt.iterator(result[0]):
            print(i)
        




def print_req_2(control,o_latitud,o_longitud,d_latitud,d_longitud):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    result= controller.req_2(control,o_latitud,o_longitud,d_latitud,d_longitud)
    #[0]result, [1] no_airports, [2] time_total, [3] dist_vuelos,[4] o_dist,[5]d_dist,[6] deltatime
    
    print("\n\nTiempo de ejecución del requerimiento: "+str(round(result[6],2)))
    
    if result[1]!=0:
        print("\nEsta fue la ruta encontrada: \n")
        headers= ["ICAO","Nombre", "Ciudad", "País"]
        table=[]
        for aerop in lt.iterator(result[0]):        
            ans= [aerop["ICAO"],aerop["NOMBRE"],aerop["CIUDAD"],aerop["PAIS"]]
            table.append(ans)
        print(tabulate(table, headers=headers,tablefmt="github"))

        print("\nAeropuertos visitados en el camino: "+str(result[1]))
        aerop_o=lt.getElement(result[0],1)
        aerop_d=lt.getElement(result[0],lt.size(result[0]))
        print("\nDISTANCIA: ")
        print("De punto origen a {0}: {1} km".format(aerop_o["ICAO"],round(result[4],2)))
        print("Viaje de {0} a {1}: {2} km".format(aerop_o["ICAO"],aerop_d["ICAO"],round(result[3],2)))
        print("{0} a destino: {1} km".format(aerop_d["ICAO"],round(result[5],2)))
        print("DISTANCIA TOTAL: {0} km".format(round(result[3]+result[4]+result[5],2)))

        print("\nTIEMPO TOTAL: {0} min\n".format(result[2]))
    else:
        print("\n\n")
        for i in lt.iterator(result[0]):
            print(i)


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    deltatime, aerop_mayor_concurrencia, dist_trayectos, trayectos_posibles, encontrados = controller.req_3(control)
    
    headers = ["Origen/Destino", "ICAO","Nombre", "Ciudad", "País", "Distancia Total (km)", "Tiempo Total"]
    for vuelo in lt.iterator(encontrados):
        origen = ["Origen", vuelo["origen"]["ICAO"], vuelo["origen"]["CIUDAD"], vuelo["origen"]["PAIS"]]
        destino = ["Destino", vuelo["destino"]["ICAO"], vuelo["destino"]["CIUDAD"], vuelo["destino"]["PAIS"], vuelo["distancia"], str(vuelo["tiempo"])]
        tabla = [origen, destino]
        print(tabulate(tabla, headers=headers,tablefmt="github"))
        print("\n")
    
    print("El tiempo transcurrido (ms) es " + str(deltatime))
    
    print("La información del aeropuerto más importante según la concurrencia comercial es: ", str(aerop_mayor_concurrencia["aerop"]["ICAO"]), "; ", 
            str(aerop_mayor_concurrencia["aerop"]["NOMBRE"]), "; ", str(aerop_mayor_concurrencia["aerop"]["CIUDAD"]), "; ", str(aerop_mayor_concurrencia["aerop"]["PAIS"]), 
            "; ", str(aerop_mayor_concurrencia["conc"]))
    
    print("La suma de la distancia total de los trayectos (km) es " + str(dist_trayectos))
    print("El número total de trayectos posibles es " + str(trayectos_posibles))


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    result=controller.req_4(control)
    #[0]results, [1]importante, [2]dist_total, [3] no_trayectos, [4]deltatime
    
    headers= ["","ICAO","Nombre", "Ciudad", "País"]
    for camino in lt.iterator(result[0]):
        ori=camino["origen"]
        des=camino["destino"]
        
        origen=["Origen",ori["ICAO"],ori["NOMBRE"],ori["CIUDAD"],ori["PAIS"]]
        destino=["Destino",des["ICAO"],des["NOMBRE"],des["CIUDAD"],des["PAIS"]]
        table=[origen,destino]
        print(tabulate(table, headers=headers,tablefmt="github"))
        print("Distancia:{0} km, Tiempo: {1} min, Tipos de aeronave utilizados: {2}.".format(round(camino["distancia"],2),camino["tiempo"],camino["tipo_avion"]["elements"]))
        print("\n")

    print("\n\n\nTiempo de ejecución del requerimiento: "+str(round(result[4],2)))
    
    print("\nEl areopuerto más importante es:")
    headers= ["ICAO","Nombre", "Ciudad", "País","Concurrencia"]
    table=[[result[1]["aerop"]["ICAO"],result[1]["aerop"]["NOMBRE"],result[1]["aerop"]["CIUDAD"],result[1]["aerop"]["PAIS"],result[1]["conc"]]]
    print(tabulate(table, headers=headers,tablefmt="github"))

    print("\nTrayectos posibles: "+str(result[3]))
    print("Distancia total de los trayectos: "+str(round(result[2],2))+" km\n\n")

   
        






def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    tiempo, max_aereo, concurrencia, dist_total, trayectos, lista = controller.req_5(control)
    print("-" * 20)
    print(f"Tiempo que usa el algoritmo: {tiempo} ms")
    print("Aeropuerto militar más concurrido:")
    print(f"  Identificador ICAO: {max_aereo}")
    print(f"  Nombre: {concurrencia['value']['NOMBRE']}")
    print(f"  Ciudad: {concurrencia['value']['CIUDAD']}")
    print(f"  País: {concurrencia['value']['PAIS']}")
    print(f"  Valor de concurrencia militar: {concurrencia['Conc']}")
    print(f"Distancia total de los trayectos sumada: {dist_total} km")
    print(f"Número total de trayectos posibles desde {max_aereo}: {trayectos}")

    print("-" * 20)
    print("TRAYECTOS")
    table = []
    head = ["Origen", "Destino", "Distancia recorrida (km)", "Tiempo (minutos)", "Avión"]
    for viaje in lt.iterator(lista):
        dic = [
            f"{viaje['origin']} ({viaje['origin_name']}, {viaje['origin_city']}, {viaje['origin_country']})",
            f"{viaje['destination']} ({viaje['destination_name']}, {viaje['destination_city']}, {viaje['destination_country']})",
            viaje['weight']['weight'], viaje['tiempo'], viaje['aircraft']
        ]
        table.append(dic)

    tabla = tabulate(table, headers=head, tablefmt='github')
    print(tabla)


def print_req_6(control,m):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    tiempo, max_aereo, lista = controller.req_6(control, m)
    print("-" * 20)
    print(f"Tiempo que usa el algoritmo: {tiempo:.2f} ms")
    print(f"Aeropuerto más importante según la concurrencia comercial:")
    print(f"  Identificador ICAO: {max_aereo['value']['ICAO']}")
    print(f"  Nombre: {max_aereo['value']['NOMBRE']}")
    print(f"  Ciudad: {max_aereo['value']['CIUDAD']}")
    print(f"  País: {max_aereo['value']['PAIS']}")
    print(f"  Valor de concurrencia comercial: {max_aereo['Conc']}")

    print("-" * 20)
    print("CAMINOS DESDE EL AEROPUERTO MÁS IMPORTANTE")
    table = []
    head = ["Total Aeropuertos", "Aeropuertos", "Vuelos", "Distancia (km)"]
    for path_info in lt.iterator(lista):
        total_airports = path_info['total_airports']
        airports = [f"{airport['ICAO']} ({airport['CIUDAD']}, {airport['PAIS']})" for airport in
                    lt.iterator(path_info['airports'])]
        flights = [f"{flight['source']} -> {flight['destination']}" for flight in lt.iterator(path_info['flights'])]
        distance = path_info['distance']
        table.append([total_airports, airports, flights, distance])

    tabla = tabulate(table, headers=head, tablefmt='github')
    print(tabla)


def print_req_7(control, origen_lat, origen_lon, destino_lat, destino_lon):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    deltatime, distancia, tiempo, num_aerop_camino, camino_final, error_str, success, origen, destino = controller.req_7(control, origen_lat, origen_lon, destino_lat, destino_lon)
    print("\n")
    if not success:
        for string in lt.iterator(error_str):
            print(string)
    else:
        headers = ["ICAO","Nombre", "Ciudad", "País"]
        table = []
        
        for vuelo in lt.iterator(camino_final):
            info = [vuelo["icao"], vuelo["nombre"], vuelo["ciudad"], vuelo["pais"]]
            table.append(info)
        
        info_d = [destino["ICAO"], destino["NOMBRE"], destino["CIUDAD"], destino["PAIS"]]
        table.append(info_d)
        
        print(tabulate(table, headers=headers,tablefmt="github"))
        
        print("\n")
        
        print("El tiempo transcurrido (ms) es " + str(deltatime))
        print("La  la distancia total (km) es " + str(distancia))
        print("El tiempo de los trayectos en total es " + str(tiempo))
        print("El numero de aeropuertos en el camino es " + str(num_aerop_camino))


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
            print_terminar_carga_datos(data,control)

        elif int(inputs) == 2:

            print("Para el punto de ORIGEN,ingrese...")
            o_latitud=float(input("Latitud: "))
            o_longitud=float(input("Longitud: "))
            print("Para el punto de DESTINO,ingrese...")
            d_latitud=float(input("Latitud: "))
            d_longitud=float(input("Longitud: "))
            print_req_1(control,o_latitud,o_longitud,d_latitud,d_longitud)

        elif int(inputs) == 3:
            print("Para el punto de ORIGEN,ingrese...")
            o_latitud=float(input("Latitud: "))
            o_longitud=float(input("Longitud: "))
            print("Para el punto de DESTINO,ingrese...")
            d_latitud=float(input("Latitud: "))
            d_longitud=float(input("Longitud: "))
            print_req_2(control,o_latitud,o_longitud,d_latitud,d_longitud)


        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            m = input("Ingrese el número de aereopuertos que desea cubrir: ")
            print_req_6(control,m)

        elif int(inputs) == 8:
            origen_lat = float(input("Dame la Latitud del origen: "))
            origen_lon = float(input("Dame la Longitud del origen: "))
            destino_lat = float(input("Dame la Latitud del destino: "))
            destino_lon = float(input("Dame la Longitud del destino: "))
            print_req_7(control, origen_lat, origen_lon, destino_lat, destino_lon)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
            
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
