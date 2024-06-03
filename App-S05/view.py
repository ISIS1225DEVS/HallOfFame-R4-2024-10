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
import folium as fm

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
    print("\nBienvenido")
    print("1- Cargar información")
    print("2- Identificar si hay una ruta entre dos destinos turísticas.")
    print("3- Identificar el itinerario con menos escalas entre dos destinos turísticos.")
    print("4- Hallar la red de distancia mínima desde el aerupuerto de mayor concurrencia comercial.")
    print("5- Hallar la red de distancia mínima desde el aerupuerto de mayor concurrencia de carga.")
    print("6- Hallar la red de tiempo mínimo de respuesta desde el aerupuerto de mayor concurrencia militar.")
    print("7- Obtener los caminos más cortos para la cobertura de los m-aeropuetos más importantes del país.")
    print("8- Obtener el camino más corto en tiempo entre dos destinos turísticos.")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    elapsed, str1, str2, most_com, least_com, most_cargo, least_cargo, most_mil, least_mil = controller.load_data(control, memflag=False)
    headers = ['NOMBRE', 'ICAO', 'CIUDAD', 'CONCURRENCIA']
    most_com_lst = create_tabulate_lists(headers, most_com, 1)
    least_com_lst = create_tabulate_lists(headers, least_com, 1)
    most_cargo_lst = create_tabulate_lists(headers, most_cargo, 2)
    least_cargo_lst = create_tabulate_lists(headers, least_cargo, 2)
    most_mil_lst = create_tabulate_lists(headers, most_mil, 3)
    least_mil_lst = create_tabulate_lists(headers, least_mil, 3)
    print("El tiempo de carga es", elapsed)
    print(str1)
    print(str2)
    print("\nLos primeros cinco aeropuertos con mayor concurrencia comercial son: ")
    print("\n"+tabulate(most_com_lst, headers="firstrow"))
    print("\nLos primeros cinco aeropuertos con menor concurrencia comercial son: ")
    print("\n"+tabulate(least_com_lst, headers="firstrow"))
    print("\nLos primeros cinco aeropuertos con mayor concurrencia de carga son: ")
    print("\n"+tabulate(most_cargo_lst, headers="firstrow"))
    print("\nLos primeros cinco aeropuertos con menor concurrencia de carga son: ")
    print("\n"+tabulate(least_cargo_lst, headers="firstrow"))
    print("\nLos primeros cinco aeropuertos con mayor concurrencia militar son: ")
    print("\n"+tabulate(most_mil_lst, headers="firstrow"))
    print("\nLos primeros cinco aeropuertos con menor concurrencia militar son: ")
    print("\n"+tabulate(least_mil_lst, headers="firstrow")+"\n")

    return control

def create_tabulate_lists(headers, info, type):
    response_lst = [headers]
    if type==1:
        count_str = "com_count"
    elif type == 2:
        count_str = "cargo_count"
    else:
        count_str = "mil_count"   
    
    for airport in info:
        name = airport['NOMBRE']
        code = airport['ICAO']
        city = airport['CIUDAD']
        count = airport[count_str]
        tab_lst = [name, code, city, count]
        response_lst.append(tab_lst)
    return response_lst

def print_req_1(result, elapsed, req):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    if result[0] == -1 or result[1] == -2:
        origin_airport = result[1]
        origin_distance = result[2]
        destination_airport = result[3]
        dest_distance = result[4]
        if result[0] == -1:
            print("\nNo se encontraron aeropuertos con vuelos registrados a menos de 30 km del punto de origen o destino")
            print("\nEl aeropuerto más cercano al punto de origen es {0}, con una distancia de {1} km".format(origin_airport, origin_distance))
            print("\nEl aeropuerto más cercano al punto de destino es {0}, con una distancia de {1} km".format(destination_airport, dest_distance))
            print("\nTiempo de ejecución: {0} ms".format(round(elapsed,3)))
        else:
            print("No se encontró un trayecto posible entre los aeropuertos {0} y {1}.".format(origin_airport, destination_airport))
            print("\nTiempo de ejecución: {0} ms".format(round(elapsed,3)))
    else:
        airports_list = result[0]
        total_dist = round(result[1],2)
        total_time = result[2]
        total_airports = result[3]
        origin_airport = result[4]
        destination_airport = result[5]
        if req == 1:
            prnt_text = "La primera secuencia de vuelos encontrada para llegar del aeropuerto de origen al aeropuerto de destino es la siguiente: "
            file = "req_1.html"
        elif req == 2:
            prnt_text = "La  secuencia de vuelos encontrada para llegar del aeropuerto de origen al aeropuerto de destino con el menor número de escalas es la siguiente: "
            file = "req_2.html"
        elif req == 7:
            prnt_text = "La  secuencia de vuelos encontrada para llegar del aeropuerto de origen al aeropuerto de destino con el menor tiempo de vuelo es la siguiente: "
            file = "req_7.html"
        
        headers = ["NOMBRE ORIGEN", "ICAO ORIGEN","PAIS ORIGEN","CIUDAD ORIGEN", "NOMBRE DESTINO", "ICAO DESTINO","PAIS DESTINO","CIUDAD DESTINO", "DISTANCIA (KM)", "TIEMPO DE VUELO (MINS)"]
        tab_lst = [headers]
        fol_map = fm.Map([4,-72], zoom_start=4)
        for airport in lt.iterator(airports_list):
            airport_lst = [airport["NOMBRE ORIGEN"], 
                           airport["ICAO ORIGEN"],
                           airport["PAIS ORIGEN"],
                           airport["CIUDAD ORIGEN"],
                           airport["NOMBRE DESTINO"], 
                           airport["ICAO DESTINO"],
                           airport["PAIS DESTINO"],
                           airport["CIUDAD DESTINO"],
                           airport["DISTANCIA (KM)"],
                           airport["TIEMPO DE VUELO (MINS)"]]
            org_coord = airport["org_coord"]
            dest_coord = airport["dest_coord"]
            org_info = "{0} ({1})".format(airport["NOMBRE ORIGEN"], airport["ICAO ORIGEN"])
            add_marker_map(fol_map, org_coord, org_info)
            dest_info = "{0} ({1})".format(airport["NOMBRE DESTINO"], airport["ICAO DESTINO"])
            if destination_airport ==  dest_info:
                
                add_marker_map(fol_map, dest_coord, dest_info)
            fm.PolyLine([[org_coord[0], org_coord[1]], [dest_coord[0],dest_coord[1]]], color = "red").add_to(fol_map)
            tab_lst.append(airport_lst)
        fol_map.save(file)
        print("\nTiempo de ejecución: {0} ms".format(round(elapsed,3)))
        print("\nEl aeropuerto más cercano a las coordenadas de origen es: {0}".format(origin_airport))
        print("\nEl aeropuerto más cercano a las coordenadas de destino es: {0}".format(destination_airport))
        print("\n"+prnt_text)
        print("\n"+tabulate(tab_lst, headers="firstrow"))
        print("\nEn total, se visitan {0} aeropuertos, con una distancia total de {1} km y un tiempo de vuelo total de {2} minutos.\n".format(total_airports, total_dist, total_time))

def print_req_3_4_5(control, req):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    result, elapsed = controller.req_3_4_5(control, req)
    concurrency, source_airport, total_weight, total_other_weight, lst, connections_lst = result
    fol_map = fm.Map([4,-72], zoom_start=4)
    print("\nTiempo de ejecución: {0} ms".format(round(elapsed,3)))
    source_name = source_airport["NOMBRE"]
    source_icao = source_airport["ICAO"]
    source_city = source_airport["CIUDAD"]
    source_country = source_airport["PAIS"]
    for connection in lt.iterator(connections_lst):
        org_coord = connection[0]
        dest_coord = connection[1]
        fm.PolyLine([[org_coord[0], org_coord[1]], [dest_coord[0],dest_coord[1]]], color = "red").add_to(fol_map)
    print("\nEl nombre del aeropuerto de máxima concurrencia es: {0},\nsu ICAO es {1},\ny está ubicado en {2}, {3}. Este tiene una concurrencia de {4}.".format(source_name, source_icao, source_city, source_country, concurrency))
    print("\nEl número de caminos desde el aeropuerto de origen es de:", lt.size(lst))
    if (req == "req3") or (req == "req4"):
        if req == "req3":
            file = "req3.html"
        else:
            file = "req4.html"
        print("\nLa distancia total del los caminos sumados es: {0} km" . format(round(total_weight, 2)))
        print("\nEl tiempo total de los caminos sumados es: {0} minutos".format(round( total_other_weight, 2)))
        headers = ["NOMBRE ORIGEN", "ICAO ORIGEN","PAIS ORIGEN","CIUDAD ORIGEN", "NOMBRE DESTINO", 
               "ICAO DESTINO","PAIS DESTINO","CIUDAD DESTINO", "DISTANCIA (KM)", "TIEMPO DE VUELO (MINS)", "TIPOS_DE_AERONAVE"]
        tab = [headers]

        for i in lt.iterator(lst):
            str1 = ""
            for j in lt.iterator(i["airplanes_list"]):
                str1 = str1 + j + ", "
            if len(str1) != 0:
                str1 = str1[0: len(str1)-2]
            tab.append([source_name, source_icao, source_country, source_city, i["NOMBRE"],
                        i["ICAO"], i["PAIS"], i["CIUDAD"], i["weight"], i["other_weight"], str1])
            org_info = "{0} ({1})".format(i["NOMBRE"], i["ICAO"])
            org_coord_new = i["coord"]
            add_marker_map(fol_map, org_coord_new, org_info)
        
        print("\nLa lista de aeropuertos dentro de la red es: ")
        print("\n", tabulate(tab, headers="firstrow"))
        fol_map.save(file)

    else:
        print("\nLa distancia total del los caminos sumados es: {0} km" . format(round(total_other_weight, 2)))
        print("\nEl tiempo total de reacción de todo el recorrido es: {0} minutos".format(round( total_weight)))

        headers = ["NOMBRE ORIGEN", "ICAO ORIGEN","PAIS ORIGEN","CIUDAD ORIGEN", "NOMBRE DESTINO", 
               "ICAO DESTINO","PAIS DESTINO","CIUDAD DESTINO", "DISTANCIA (KM)", "TIEMPO DE VUELO (MINS)", "TIPOS_DE_AERONAVE"]
        tab = [headers]

        for i in lt.iterator(lst):
            str1 = ""
            for j in lt.iterator(i["airplanes_list"]):
                str1 = str1 + j + ", "
            if len(str1) != 0:
                str1 = str1[0: len(str1)-2]
            tab.append([source_name, source_icao, source_country, source_city, i["NOMBRE"],
                        i["ICAO"], i["PAIS"], i["CIUDAD"], i["other_weight"], i["weight"], str1])
            org_info = "{0} ({1})".format(i["NOMBRE"], i["ICAO"])
            org_coord_new = i["coord"]
            add_marker_map(fol_map, org_coord_new, org_info)
        
        print("\nLa lista de aeropuertos dentro de la red es: ")
        print("\n", tabulate(tab, headers="firstrow"))
        fol_map.save("req_5.html")
    

def print_req_6(result, elapsed, num):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    print("\nEl tiempo de ejecución fue de: {} [ms]".format((round(elapsed, 3))))

    airports_dict_list = result[0]
    max_airport = result[1]
    
    max_icao = max_airport["ICAO"]
    max_name = max_airport["NOMBRE"]
    max_city = max_airport["CIUDAD"]
    max_country = max_airport["PAIS"]
    max_concurrency = max_airport["com_count"]
    fol_map = fm.Map([4,-72], zoom_start=4)
    print("\nEl aeropuerto {0} ({1}) situado en {2}, {3} es el de mayor concurrencia comercial, con un conteo total de {4} vuelos entrando y saliendo.\n". 
          format(max_name, max_icao, max_city, max_country, max_concurrency))
    print("\nLos caminos más cortos a los {0} aeropuertos más importantes desde el aeropuerto de mayor concurrencia se presentan a continuación: ".format(num))
    
    i = 1
    for dest_airport in lt.iterator(airports_dict_list):
        if dest_airport!= -1:
            visited_airports = dest_airport["airports_list"]
            edges_list = dest_airport["edges_list"]
            total_dist = round( dest_airport["total_dist"], 2)
            airports_headers = ["NOMBRE", "ICAO", "CIUDAD", "PAIS"]
            edges_headers = ["NOMBRE ORIGEN", "ICAO ORIGEN","PAIS ORIGEN","CIUDAD ORIGEN", "NOMBRE DESTINO", "ICAO DESTINO","PAIS DESTINO","CIUDAD DESTINO"]
            airports_tab_lst = [airports_headers]
            edges_tab_lst = [edges_headers]
            airport_name = dest_airport["NOMBRE"]
            airport_code = dest_airport["ICAO"]
            airport_count = dest_airport["concurrency"]
            
            
            for airport in lt.iterator(visited_airports):
                airport_lst = [airport["NOMBRE"], 
                            airport["ICAO"],
                            airport["CIUDAD"],
                            airport["PAIS"]]
                airport_coord = airport["coord"]
                airport_info = "{0} ({1})".format(airport["NOMBRE"], airport["ICAO"])
                add_marker_map(fol_map, airport_coord, airport_info)
                airports_tab_lst.append(airport_lst)
            
            for edge in lt.iterator(edges_list):
                edge_lst = [edge["NOMBRE ORIGEN"], 
                            edge["ICAO ORIGEN"],
                            edge["PAIS ORIGEN"],
                            edge["CIUDAD ORIGEN"],
                            edge["NOMBRE DESTINO"], 
                            edge["ICAO DESTINO"],
                            edge["PAIS DESTINO"],
                            edge["CIUDAD DESTINO"]]
                org_coord = edge["org_coord"]
                dest_coord = edge["dest_coord"]
                fm.PolyLine([[org_coord[0], org_coord[1]], [dest_coord[0],dest_coord[1]]], color = "red").add_to(fol_map)
                edges_tab_lst.append(edge_lst)
            
            print("\n{0}. {1} ({2}) --- Concurrencia comercial: {3}".format(i, airport_name, airport_code, airport_count ))
            print("\nDistancia desde el aeropuerto de mayor concurrencia: {0} Km".format(total_dist))
            print("\nAeropuertos visitados en el camino: ")
            print("\n"+tabulate(airports_tab_lst, headers="firstrow"))
            print("\nVuelos incluidos en el camino: ")
            print("\n"+tabulate(edges_tab_lst, headers = "firstrow"))
            i+=1
        else:
            print("{0}. {1} ({2}) --- Concurrencia comercial: {3}".format(i, airport_name, airport_code, airport_count ))
            print("\nNo existe un camino entre el aeropuerto de mayor concurrencia y este aeropuerto.")
            i+=1
    fol_map.save("req_6.html")

def add_marker_map (fol_map, coord, coord_info):
    text = fm.Popup(coord_info, min_width=175, max_width=175)
    fm.Marker([coord[0], coord[1]], popup=text, icon = fm.Icon(color="red")).add_to(fol_map)
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
            load_data(control)
        elif int(inputs) == 2:
            origin_lat = float(input("Latitud origen: "))
            origin_lon = float(input("Longitud origen: "))
            dest_lat = float(input("Latitud destino: "))
            des_lon = float(input("Longitud destino: "))
            origin = (origin_lat, origin_lon)
            dest = (dest_lat, des_lon)
            result, elapsed = controller.req_1_2(control, origin, dest, 1)
            print_req_1(result, elapsed, 1)

        elif int(inputs) == 3:
            origin_lat = float(input("Latitud origen: "))
            origin_lon = float(input("Longitud origen: "))
            dest_lat = float(input("Latitud destino: "))
            des_lon = float(input("Longitud destino: "))
            origin = (origin_lat, origin_lon)
            dest = (dest_lat, des_lon)
            result, elapsed = controller.req_1_2(control, origin, dest, 2)
            print_req_1(result, elapsed, 2)

        elif int(inputs) == 4:
            print_req_3_4_5(control, "req3")

        elif int(inputs) == 5:
            print_req_3_4_5(control, "req4")

        elif int(inputs) == 6:
            print_req_3_4_5(control, "req5")

        elif int(inputs) == 7:
            num = int(input("Ingrese el número de aeropuertos más importantes que desea cubrir: "))
            result, elapsed = controller.req_6(control, num)
            print_req_6(result, elapsed, num)

        elif int(inputs) == 8:
            origin_lat = float(input("Latitud origen: "))
            origin_lon = float(input("Longitud origen: "))
            dest_lat = float(input("Latitud destino: "))
            des_lon = float(input("Longitud destino: "))
            origin = (origin_lat, origin_lon)
            dest = (dest_lat, des_lon)
            result, elapsed = controller.req_7(control, origin, dest)
            print_req_1(result, elapsed, 7)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
            
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
