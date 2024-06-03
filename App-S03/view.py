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
import folium
from folium.features import CustomIcon

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
    print("10- Cambiar tipo de pruebas (rapidez(almacenamiento)")
    print("11- Cambiar tamaño de muestra")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    control, prueba, tipo_prueba, primerosCo, ultimosCo, primerosCa, ultimosCa, primerosM, ultimosM, total_aeropuertos, total_vuelos= controller.load_data(control)
    
    
    return control, prueba, tipo_prueba, primerosCo, ultimosCo, primerosCa, ultimosCa, primerosM, ultimosM, total_aeropuertos, total_vuelos

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
    print("_"*50)
    print("\nPOR FAVOR ENTREGUE LA SIGUIENTE INFORMACIÓN PARA LA CONSULTA:\n")
    latitud_origen = input("Por favor digite la latitud del punto geográfico de origen... ")
    longitud_origen = input("Por favor digite la longitud del punto geográfico de origen... ")
    
    latitud_destino = input("Por favor digite la latitud del punto geográfico de destino... ")
    longitud_destino = input("Por favor digite la longitud del punto geográfico de destino... ")
    
    kilometros_camino, distance1, distance2, cantidad_paradas , trayectory_time, trayectory_sequence, time, trayectories_times = controller.req_1(control, latitud_origen, longitud_origen, latitud_destino, longitud_destino)
    if kilometros_camino == False and distance1 == False and distance2 == False and cantidad_paradas == False and trayectory_time != False and trayectory_sequence != False:
        print("_"*220)
        print("\n")
        print("SE ENCONTRO EL AEROPUERTO PERO NO SE ENCONTRO NINGÚN CAMINO QUE LO CONECTE CON EL DESTINO")
        print(f"ORIGEN: {trayectory_time} DESTINO: {trayectory_sequence}")
        print("\n")
        print("_"*220)
        return None
    elif (kilometros_camino == False) and (cantidad_paradas != False) and (trayectory_time!= False) and (trayectory_sequence == False):
        print("_"*220)
        print("\n")
        print("NO se encontro un aeropuerto dentro de un rango de 30 km de las coordenadas entregadas por el usuario".center(220))
        print(f"El aeropuerto de origen más cercano fue {cantidad_paradas} a {distance1} km de las coordenadas entregadas".center(220))
        print(f"El aeropuerto de destino más cercano fue {trayectory_time} a {distance2} km de las coordenadas entregadas".center(220))
        print("\n")
        print("_"*220)
        return None
    
    print("Los resultados de la consulta fueron los siguientes: ".center(220))
    print(f"El trayecto desde el aeropuerto de origen hasta el aeropuerto de destino fue de {kilometros_camino} km".center(220))
    print(f"La distancia desde las coordenadas entregadas y el aeropuerto de origen más cercano fue de {distance1} km".center(220))
    print(f"La distancia desde las coordenadas entregadas y el aeropuerto de destino más cercano fue de {distance2} km".center(220))
    print(f"El numéro de aeropuertos que se visitan en el camino encontrado: {cantidad_paradas}".center(220))
    print("\n")
    print("TRAYECTO".center(220))
    print(f"DURACIÓN: {trayectory_time} min".center(220))
    print("\n")
    llaves=["NOMBRE", "CIUDAD", "PAIS", "ICAO"]
    valores_a_imprimir1 = []
    conteo = 0
    for airport in lt.iterator(trayectory_sequence):
        lst_provisional = [conteo, lt.getElement(trayectories_times, conteo+1)]
        for llave in llaves:
            lst_provisional.append(airport[llave])
        valores_a_imprimir1.append(lst_provisional)
        conteo += 1
    print((tabulate(valores_a_imprimir1, headers=["PASO","Tiempo", "NOMBRE", "CIUDAD", "PAIS", "ICAO"])).center(220))
        
    print("_"*50)
    print(f"Se ha demorado un total de {time}[ms]")


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    print("_"*50)
    print("\nPOR FAVOR ENTREGUE LA SIGUIENTE INFORMACIÓN PARA LA CONSULTA:\n")
    latitud_origen = input("Por favor digite la latitud del punto geográfico de origen... ")
    longitud_origen = input("Por favor digite la longitud del punto geográfico de origen... ")
    
    latitud_destino = input("Por favor digite la latitud del punto geográfico de destino... ")
    longitud_destino = input("Por favor digite la longitud del punto geográfico de destino... ")
    
    kilometros_camino, distance1, distance2, cantidad_paradas , trayectory_time, trayectory_sequence, time = controller.req_2(control, latitud_origen, longitud_origen, latitud_destino, longitud_destino)
    if kilometros_camino == False and distance1 == False and distance2 == False and cantidad_paradas == False and trayectory_time != False and trayectory_sequence != False:
        print("_"*220)
        print("\n")
        print("SE ENCONTRO EL AEROPUERTO PERO NO SE ENCONTRO NINGÚN CAMINO QUE LO CONECTE CON EL DESTINO")
        print(f"ORIGEN: {trayectory_time} DESTINO: {trayectory_sequence}")
        print("\n")
        print("_"*220)
        return None
    elif (kilometros_camino == False) and (cantidad_paradas != False) and (trayectory_time!= False) and (trayectory_sequence == False):
        print("_"*220)
        print("\n")
        print("NO se encontro un aeropuerto dentro de un rango de 30 km de las coordenadas entregadas por el usuario".center(220))
        print(f"El aeropuerto de origen más cercano fue {cantidad_paradas} a {distance1} km de las coordenadas entregadas".center(220))
        print(f"El aeropuerto de destino más cercano fue {trayectory_time} a {distance2} km de las coordenadas entregadas".center(220))
        print("\n")
        print("_"*220)
        return None
    
    print("Los resultados de la consulta fueron los siguientes: ".center(220))
    print(f"El trayecto desde el aeropuerto de origen hasta el aeropuerto de destino fue de {kilometros_camino} km".center(220))
    print(f"La distancia desde las coordenadas entregadas y el aeropuerto de origen más cercano fue de {distance1} km".center(220))
    print(f"La distancia desde las coordenadas entregadas y el aeropuerto de destino más cercano fue de {distance2} km".center(220))
    print(f"El numéro de aeropuertos que se visitan en el camino encontrado: {cantidad_paradas}".center(220))
    print("\n")
    print("TRAYECTO".center(220))
    print(f"DURACIÓN: {trayectory_time} min".center(220))
    print("\n")
    llaves=["NOMBRE", "CIUDAD", "PAIS", "ICAO"]
    valores_a_imprimir1 = []
    conteo = 0
    for airport in lt.iterator(trayectory_sequence):
        lst_provisional = [conteo]
        for llave in llaves:
            lst_provisional.append(airport[llave])
        valores_a_imprimir1.append(lst_provisional)
        conteo += 1
    print((tabulate(valores_a_imprimir1, headers=["PASO","NOMBRE", "CIUDAD", "PAIS", "ICAO"])).center(220))
        
    print("_"*50)
    print(f"Se ha demorado un total de {time}[ms]")

def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    vuelos= controller.req_3(control)
    contador= vuelos[0]
    costo=vuelos[1]
    print("Es posible hacer un total de: ",contador, "trayectos desde el aeropuerto con mayor concurrencia")
    print("La distancia total es de ",costo," km")
    


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    trayectos, paths, airportMC, distancia_total_trayectos, pesoMST,cantidad_trayectos, Rprueba, prueba= controller.req_4(control)
    print(f"Se ha demorado un total de {Rprueba} [ms]")
    print("Los resultados de la consulta fueron los siguientes: ".center(220))
    print(f"El aeropuerto de mayor importancia por su concurrencia fue {airportMC}".center(220))
    print(f"La distancia total sumada de todos los trayectos fue de {distancia_total_trayectos} km".center(220))
    print(f"La distancia total de la red de trayectos sin duplicaciones es: {pesoMST} km".center(220))
    print(f"Hay un total de {cantidad_trayectos} trayectos posibles desde {airportMC}".center(220))
   
    print("\n")
    print("TRAYECTOS (Tenga en cuenta que cada trayecto puede tener puntos intermedios, pues hay trayectos dentro de trayectos)".center(220))
    headers = [ "ORIGEN", "->", "DESTINO", "Tiempo (min)", "Distancia (km)", "aeronaves involucradas"]
    list_a_imprimir1 = []
    for trayecto in lt.iterator(trayectos):
        lista_provisional = [trayecto[0],"->", trayecto[1], trayecto[2], trayecto[3]]
        conteo = 1
        aeronaves = []
        for aeronave in lt.iterator(trayecto[4]):
            aeronaves.append(aeronave)
        lista_provisional.append(aeronaves)
        list_a_imprimir1.append(lista_provisional)
    
    
    print((tabulate(list_a_imprimir1, headers=headers, tablefmt= "fancy_grid")).center(220))
    print("\n")
    print("Descripción trayectos : ".center(100))
    for trayecto in lt.iterator(paths):
        lista_provisional = []
        for airport in lt.iterator(trayecto):
            lista_provisional.append(airport)
        print(("->".join(lista_provisional)).center(100))
   
    

def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    nombre_mayor, kilometros_totales, nombres_aeropuertos, trayectos_posibles, trayectory_sequence, total_weights, time = controller.req_5(control)
    return  nombre_mayor, kilometros_totales, nombres_aeropuertos, trayectos_posibles, trayectory_sequence, total_weights, time


def print_req_6(control,M):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    X= controller.req_6(control,M)
    respuesta=X[0]
    print("El aeropuerto con mayor concurrencia comercial es: ", "\n")
    print(respuesta["NOMBRE"], "de la ciudad ",respuesta["CIUDAD"], "ubicado en ",respuesta["PAIS"], "identificado con el codigo: ",respuesta["ICAO"], "y con una concurrencia comercial de: ",respuesta["concurrencia_comercial"])
   


def print_req_7(control):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 7
    print("_"*50)
    print("\nPOR FAVOR ENTREGUE LA SIGUIENTE INFORMACIÓN PARA LA CONSULTA:\n")
    latitud_origen = float(input("Por favor digite la latitud del punto geográfico de origen... "))
    longitud_origen = float(input("Por favor digite la longitud del punto geográfico de origen... "))
    
    latitud_destino = float(input("Por favor digite la latitud del punto geográfico de destino... "))
    longitud_destino = float(input("Por favor digite la longitud del punto geográfico de destino... "))
    trayectory_time, path_distance1, path_distance2, airports_visited, airports_sequence, Rprueba, prueba = controller.req_7(control, latitud_origen, longitud_origen, latitud_destino, longitud_destino)
    print(f"Se ha demorado un total de {Rprueba} [ms]")
    if trayectory_time != False and path_distance1 == False and path_distance2 == False and airports_visited == False and airports_sequence != False:
        print("_"*220)
        print("\n")
        print("SE ENCONTRO EL AEROPUERTO PERO NO SE ENCONTRO NINGÚN CAMINO QUE LO CONECTE CON EL DESTINO")
        print(f"ORIGEN: {trayectory_time} DESTINO: {airports_sequence}")
        print("\n")
        print("_"*220)
        return None
    elif (trayectory_time == False) and (airports_visited!= False) and (airports_sequence != False):
        print("_"*220)
        print("\n")
        print("NO se encontro un aeropuerto dentro de un rango de 30 km de las coordenadas entregadas por el usuario".center(220))
        print(f"El aeropuerto de origen más cercano fue {airports_visited} a {path_distance1} km de las coordenadas entregadas".center(220))
        print(f"El aeropuerto de destino más cercano fue {airports_sequence} a {path_distance2} km de las coordenadas entregadas".center(220))
        print("\n")
        print("_"*220)
        return None
    
    print("Los resultados de la consulta fueron los siguientes: ".center(220))
    print(f"El itinerario más corto entre el punto de origen dado y el punto de destino dado tuvo un tiempo de {trayectory_time} (min)".center(220))
    print(f"La distancia del camino fue de {path_distance1} km".center(220))
    print(f"La distancia total teniendo en cuenta la distancia desde las coordenadas de origen y destino a los aeropuertos fue de {path_distance2}".center(220))
    print(f"En el camino se visitaron {airports_visited} aeropuertos".center(220))

    
    llaves = ["ICAO", "NOMBRE", "CIUDAD", "PAIS"]
    lista_a_imprimir = []
    for airport in lt.iterator(airports_sequence):
        lista_provisional = []
        for llave in llaves:
            
            lista_provisional.append(airport[0][llave])
        lista_provisional.append(airport[1])
        lista_a_imprimir.append(lista_provisional)
    
    print((tabulate(lista_a_imprimir, headers=["ICAO", "NOMBRE", "CIUDAD", "PAIS", "V TIEMPO V"], tablefmt= "fancy_grid")).center(220))
    
    
        
   

def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    print("_"*100)
    print("Por favor digite la opción de requerimiento desea visualizar graficamente: ")
    for i in range(1,8):
        print(f"[{i}] Requerimiento {i}")
    answer= int(input("Por favor digite la opción del requerimiento que desea visualizar: "))
    print("_"*100)
    if answer == 1:
        print("\nPOR FAVOR ENTREGUE LA SIGUIENTE INFORMACIÓN PARA LA CONSULTA:\n")
        latitud_origen = input("Por favor digite la latitud del punto geográfico de origen... ")
        longitud_origen = input("Por favor digite la longitud del punto geográfico de origen... ")
    
        latitud_destino = input("Por favor digite la latitud del punto geográfico de destino... ")
        longitud_destino = input("Por favor digite la longitud del punto geográfico de destino... ")
    
        kilometros_camino, distance1, distance2, cantidad_paradas , trayectory_time, trayectory_sequence, time,  trayectories_times = controller.req_1(control, latitud_origen, longitud_origen, latitud_destino, longitud_destino)
        conteo = 1
        m = folium.Map(location = (lt.getElement(trayectory_sequence, 1)["LATITUD"],lt.getElement(trayectory_sequence, 1)["LONGITUD"]))
        coords = []
        for airport in lt.iterator(trayectory_sequence):
            if conteo < lt.size(trayectory_sequence):
                start = [float(airport["LATITUD"]), float(airport["LONGITUD"])]
                end = [float(lt.getElement(trayectory_sequence, conteo+1)["LATITUD"]), float(lt.getElement(trayectory_sequence, conteo+1)["LONGITUD"])]
                
                
                folium.Marker(
                location=start,
                tooltip="Click me!",
                popup=f"Título: {airport['NOMBRE']}",
                icon=folium.Icon(color="green"),
                ).add_to(m)
                
                folium.Marker(
                location=end,
                tooltip="Click me!",
                popup=f"Título: {lt.getElement(trayectory_sequence, conteo+1)['NOMBRE']}",
                icon=folium.Icon(color="green"),
                ).add_to(m)
                
                folium.PolyLine(
                locations=[start,end], 
                color='blue', 
                weight=5, 
                opacity=0.7, 
                dash_array='10', 
                arrowheads={'fill': True, 'size': 5, 'frequency': 'end'}
                ).add_to(m)
                conteo += 1
            
        #m.save("map_with_arrow.html")
        
        m.show_in_browser()
                
    elif answer == 2:
        print("_"*50)
        print("\nPOR FAVOR ENTREGUE LA SIGUIENTE INFORMACIÓN PARA LA CONSULTA:\n")
        latitud_origen = input("Por favor digite la latitud del punto geográfico de origen... ")
        longitud_origen = input("Por favor digite la longitud del punto geográfico de origen... ")
    
        latitud_destino = input("Por favor digite la latitud del punto geográfico de destino... ")
        longitud_destino = input("Por favor digite la longitud del punto geográfico de destino... ")
        kilometros_camino, distance1, distance2, cantidad_paradas , trayectory_time, trayectory_sequence, time = controller.req_2(control, latitud_origen, longitud_origen, latitud_destino, longitud_destino)
        conteo = 1
        m = folium.Map(location = (lt.getElement(trayectory_sequence, 1)["LATITUD"],lt.getElement(trayectory_sequence, 1)["LONGITUD"]))
        coords = []
        for airport in lt.iterator(trayectory_sequence):
            if conteo < lt.size(trayectory_sequence):
                start = [float(airport["LATITUD"]), float(airport["LONGITUD"])]
                end = [float(lt.getElement(trayectory_sequence, conteo+1)["LATITUD"]), float(lt.getElement(trayectory_sequence, conteo+1)["LONGITUD"])]
                
                
                folium.Marker(
                location=start,
                tooltip="Click me!",
                popup=f"Título: {airport['NOMBRE']}",
                icon=folium.Icon(color="green"),
                ).add_to(m)
                
                folium.Marker(
                location=end,
                tooltip="Click me!",
                popup=f"Título: {lt.getElement(trayectory_sequence, conteo+1)['NOMBRE']}",
                icon=folium.Icon(color="green"),
                ).add_to(m)
                
                folium.PolyLine(
                locations=[start,end], 
                color='blue', 
                weight=5, 
                opacity=0.7, 
                dash_array='10', 
                arrowheads={'fill': True, 'size': 5, 'frequency': 'end'}
                ).add_to(m)
                conteo += 1
        m.show_in_browser()
    
    elif answer == 3:
        vuelos= controller.req_3(control)
        paths = vuelos[2]
        mapa = False
        m = None
        for path in lt.iterator(paths):
            
            conteo = 0
            for icao in path:
                if conteo < len(path)-1:
                    airport = me.getValue(mp.get(control["model"]["airports"], icao))
                    nextAirport = me.getValue(mp.get(control["model"]["airports"], path[conteo+1]))
                    if not mapa:
                        m = folium.Map(location = [airport["LATITUD"],airport["LONGITUD"]])
                        mapa = True
                    
                    start = [float(airport["LATITUD"]), float(airport["LONGITUD"])]
                    end = [float(nextAirport["LATITUD"]), float(nextAirport["LONGITUD"])]
                    
                    
                    folium.Marker(
                    location=start,
                    tooltip="Click me!",
                    popup=f"Título: {airport['NOMBRE']}",
                    icon=folium.Icon(color="green"),
                    ).add_to(m)
                
                    folium.Marker(
                    location=end,
                    tooltip="Click me!",
                    popup=f"Título: {nextAirport['NOMBRE']}",
                    icon=folium.Icon(color="green"),
                    ).add_to(m)
                
                    folium.PolyLine(
                    locations=[start,end], 
                    color='blue', 
                    weight=5, 
                    opacity=0.7, 
                    dash_array='10', 
                    arrowheads={'fill': True, 'size': 5, 'frequency': 'end'}
                    ).add_to(m)
                    conteo += 1
        #m.save("map_with_arrow.html")
        
        m.show_in_browser()
        
        pass
    elif answer == 4:
        trayectos, paths, airportMC, distancia_total_trayectos, pesoMST, cantidad_trayectos,Rprueba, prueba= controller.req_4(control)
        mapa = False
        m = None
        for path in lt.iterator(paths):
            lt.deleteElement(path, lt.size(path))
            conteo = 1
            for icao in lt.iterator(path):
                if conteo < lt.size(path):
                    airport = me.getValue(mp.get(control["model"]["airports"], icao))
                    nextAirport = me.getValue(mp.get(control["model"]["airports"], lt.getElement(path, conteo+1)))
                    if not mapa:
                        m = folium.Map(location = [airport["LATITUD"],airport["LONGITUD"]])
                        mapa = True
                    
                    start = [float(airport["LATITUD"]), float(airport["LONGITUD"])]
                    end = [float(nextAirport["LATITUD"]), float(nextAirport["LONGITUD"])]
                    
                    
                    folium.Marker(
                    location=start,
                    tooltip="Click me!",
                    popup=f"Título: {airport['NOMBRE']}",
                    icon=folium.Icon(color="green"),
                    ).add_to(m)
                
                    folium.Marker(
                    location=end,
                    tooltip="Click me!",
                    popup=f"Título: {nextAirport['NOMBRE']}",
                    icon=folium.Icon(color="green"),
                    ).add_to(m)
                
                    folium.PolyLine(
                    locations=[start,end], 
                    color='blue', 
                    weight=5, 
                    opacity=0.7, 
                    dash_array='10', 
                    arrowheads={'fill': True, 'size': 5, 'frequency': 'end'}
                    ).add_to(m)
                    conteo += 1
        #m.save("map_with_arrow.html")
        
        m.show_in_browser()
                       
                
                
    elif answer == 5:
        nombre_mayor, kilometros_totales, nombres_aeropuertos, trayectos_posibles, trayectory_sequence, total_weights, time = controller.req_5(control)
        paths = trayectory_sequence
        mapa = False
        m = None
        for path in lt.iterator(paths):
            lt.deleteElement(path, lt.size(path))
            conteo = 1
            for airport in lt.iterator(path):
                #print(conteo)
                if conteo < lt.size(path):
                    
                    nextAirport = lt.getElement(path, conteo+1)
                    if not mapa:
                        m = folium.Map(location = [airport["LATITUD"],airport["LONGITUD"]])
                        mapa = True
                    
                    start = [float(airport["LATITUD"]), float(airport["LONGITUD"])]
                    end = [float(nextAirport["LATITUD"]), float(nextAirport["LONGITUD"])]
                    
                    
                    folium.Marker(
                    location=start,
                    tooltip="Click me!",
                    popup=f"Título: {airport['NOMBRE']}",
                    icon=folium.Icon(color="green"),
                    ).add_to(m)
                
                    folium.Marker(
                    location=end,
                    tooltip="Click me!",
                    popup=f"Título: {nextAirport['NOMBRE']}",
                    icon=folium.Icon(color="green"),
                    ).add_to(m)
                
                    folium.PolyLine(
                    locations=[start,end], 
                    color='blue', 
                    weight=5, 
                    opacity=0.7, 
                    dash_array='10', 
                    arrowheads={'fill': True, 'size': 5, 'frequency': 'end'}
                    ).add_to(m)
                    conteo += 1
        #m.save("map_with_arrow.html")
        
        m.show_in_browser()
                       
        
    elif answer == 6:
        M= int(input("Ingrese la cantidad de aeropuertos\n "))
        X= controller.req_6(control,M)
        paths = X[2]
        mapa = False
        m = None
        for path in lt.iterator(paths):
            
            conteo = 0
            for icao in path:
                if conteo < len(path)-1:
                    airport = me.getValue(mp.get(control["model"]["airports"], icao))
                    nextAirport = me.getValue(mp.get(control["model"]["airports"], path[conteo+1]))
                    if not mapa:
                        m = folium.Map(location = [airport["LATITUD"],airport["LONGITUD"]])
                        mapa = True
                    
                    start = [float(airport["LATITUD"]), float(airport["LONGITUD"])]
                    end = [float(nextAirport["LATITUD"]), float(nextAirport["LONGITUD"])]
                    
                    
                    folium.Marker(
                    location=start,
                    tooltip="Click me!",
                    popup=f"Título: {airport['NOMBRE']}",
                    icon=folium.Icon(color="green"),
                    ).add_to(m)
                
                    folium.Marker(
                    location=end,
                    tooltip="Click me!",
                    popup=f"Título: {nextAirport['NOMBRE']}",
                    icon=folium.Icon(color="green"),
                    ).add_to(m)
                
                    folium.PolyLine(
                    locations=[start,end], 
                    color='blue', 
                    weight=5, 
                    opacity=0.7, 
                    dash_array='10', 
                    arrowheads={'fill': True, 'size': 5, 'frequency': 'end'}
                    ).add_to(m)
                    conteo += 1
        #m.save("map_with_arrow.html")
        
        m.show_in_browser()
        
    
    
    elif answer == 7:
        print("_"*50)
        print("\nPOR FAVOR ENTREGUE LA SIGUIENTE INFORMACIÓN PARA LA CONSULTA:\n")
        latitud_origen = float(input("Por favor digite la latitud del punto geográfico de origen... "))
        longitud_origen = float(input("Por favor digite la longitud del punto geográfico de origen... "))
    
        latitud_destino = float(input("Por favor digite la latitud del punto geográfico de destino... "))
        longitud_destino = float(input("Por favor digite la longitud del punto geográfico de destino... "))
        trayectory_time, path_distance1, path_distance2, airports_visited, airports_sequence, Rprueba, prueba = controller.req_7(control, latitud_origen, longitud_origen, latitud_destino, longitud_destino)
        conteo = 1
        m = folium.Map(location = (lt.getElement(airports_sequence, 1)[0]["LATITUD"],lt.getElement(airports_sequence, 1)[0]["LONGITUD"]))
        for airport in lt.iterator(airports_sequence):
            if conteo < lt.size(airports_sequence):
                start = [float(airport[0]["LATITUD"]), float(airport[0]["LONGITUD"])]
                end = [float(lt.getElement(airports_sequence, conteo+1)[0]["LATITUD"]), float(lt.getElement(airports_sequence, conteo+1)[0]["LONGITUD"])]
                
                
                folium.Marker(
                location=start,
                tooltip="Click me!",
                popup=f"Título: {airport[0]['NOMBRE']}",
                icon=folium.Icon(color="green"),
                ).add_to(m)
                
                folium.Marker(
                location=end,
                tooltip="Click me!",
                popup=f"Título: {lt.getElement(airports_sequence, conteo+1)[0]['NOMBRE']}",
                icon=folium.Icon(color="green"),
                ).add_to(m)
                
                folium.PolyLine(
                locations=[start,end], 
                color='blue', 
                weight=5, 
                opacity=0.7, 
                dash_array='10', 
                arrowheads={'fill': True, 'size': 5, 'frequency': 'end'}
                ).add_to(m)
                conteo += 1
            
        m.show_in_browser()


def cambiar_pruebas(respuesta):
    prueba= controller.cambiar_pruebas(respuesta)
    return prueba



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
            data,  prueba, nombre_prueba, primerosCo, ultimosCo, primerosCa, ultimosCa, primerosM, ultimosM, total_aeropuertos, total_vuelos = load_data(control)
            print("RESULTADOS CARGA DE DATOS".center(220))
            print(f"El total de aeropuertos (vertices) cargados fue de: {total_aeropuertos}".center(220))
            print(f"El total de vuelos (arcos) cargados fue de: {total_vuelos}".center(220))
            
            llaves=["concurrencia_comercial", "concurrencia_carga", "concurrencia_militar","NOMBRE", "ICAO", "CIUDAD"]
            valores_a_imprimir1 = []
        
            for offer in lt.iterator(primerosCo):
                lst_provisional = []
                for llave in llaves:
                    lst_provisional.append(offer[llave])
                valores_a_imprimir1.append(lst_provisional)
        
            print("\n")
            print("AVIACIÓN COMERCIAL".center(220))
            print("\nPRIMERAS CINCO OFERTAS (comercial)\n")
            print((tabulate(valores_a_imprimir1, headers=llaves)).center(220))
            
        
            print("\nULTIMAS CINCO OFERTAS (comercial)\n")
        
            valores_a_imprimir1 = []
        
            for offer in lt.iterator(ultimosCo):
                lst_provisional = []
                for llave in llaves:
                    lst_provisional.append(offer[llave])
                valores_a_imprimir1.append(lst_provisional)
            print((tabulate(valores_a_imprimir1, headers=llaves)).center(220))
            
            valores_a_imprimir1 = []
        
            for offer in lt.iterator(primerosCa):
                lst_provisional = []
                for llave in llaves:
                    lst_provisional.append(offer[llave])
                valores_a_imprimir1.append(lst_provisional)
        
            print("\n")
            print("AVIACIÓN CARGA".center(220))
            print("\nPRIMERAS CINCO OFERTAS (carga)\n")
            print((tabulate(valores_a_imprimir1, headers=llaves)).center(220))
            
        
            print("\nULTIMAS CINCO OFERTAS (carga)\n")
        
            valores_a_imprimir1 = []
        
            for offer in lt.iterator(ultimosCa):
                lst_provisional = []
                for llave in llaves:
                    lst_provisional.append(offer[llave])
                valores_a_imprimir1.append(lst_provisional)
            print((tabulate(valores_a_imprimir1, headers=llaves)).center(220))
            
            valores_a_imprimir1 = []
        
            for offer in lt.iterator(primerosM):
                lst_provisional = []
                for llave in llaves:
                    lst_provisional.append(offer[llave])
                valores_a_imprimir1.append(lst_provisional)
        
            print("\n")
            print("AVIACIÓN MILITAR".center(220))
            print("\nPRIMERAS CINCO OFERTAS (militar)\n")
            print((tabulate(valores_a_imprimir1, headers=llaves)).center(220))
            
        
            print("\nULTIMAS CINCO OFERTAS (militar)\n")
        
            valores_a_imprimir1 = []
        
            for offer in lt.iterator(ultimosM):
                lst_provisional = []
                for llave in llaves:
                    lst_provisional.append(offer[llave])
                valores_a_imprimir1.append(lst_provisional)
            print((tabulate(valores_a_imprimir1, headers=llaves)).center(220))
            
            if nombre_prueba == "Rapidez":
                print(f"Se ha demorado un total de {prueba}[ms]")
            else:
                print(f"Se han consumido un total de {prueba}[kB]")
            
            carga = controller.densidad(control["model"]["cargaDistancia"])
            comercial = controller.densidad(control["model"]["comercialDistancia"])
            militar = controller.densidad(control["model"]["militarDistancia"])
            print(f"Grafo vuelos de carga: Vertices= {carga[0]}, Arcos = {carga[1]}, densidad = {carga[2]}")
            print(f"Grafo vuelos de comercial: Vertices= {comercial[0]}, Arcos = {comercial[1]}, densidad = {comercial[2]}")
            print(f"Grafo vuelos de militar: Vertices= {militar[0]}, Arcos = {militar[1]}, densidad = {militar[2]}")
            
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            nombre_mayor, kilometros_totales, nombres_aeropuertos, trayectos_posibles, trayectory_sequence, total_weights, time = print_req_5(control)
            print("El aeropuerto más importante según la concurrencia militar es: ")
            print("--------------------------")
            print("NOMBRE:", nombre_mayor["NOMBRE"])
            print("CODIGO ICAO:", nombre_mayor["ICAO"])
            print("CIUDAD:", nombre_mayor["CIUDAD"])
            print("PAIS:", nombre_mayor["PAIS"])
            print("--------------------------")
            print("Distancia total de los trayectos sumada en el grafo: ", kilometros_totales)
            print("Número total de trayectos posibles: ", trayectos_posibles)
            
            llaves=["NOMBRE", "CIUDAD", "PAIS", "ICAO"]
            valores_a_imprimir1 = []
            conteo = 0
            
            
            for camino in lt.iterator(trayectory_sequence):
                for airport in lt.iterator(camino):
                    lst_provisional = [conteo]
                    for llave in llaves:
                        if airport["ICAO"] != nombre_mayor["ICAO"]:
                            lst_provisional.append(airport[llave])
                        else:
                            lst_provisional.append(f"# {airport[llave]}")
                    valores_a_imprimir1.append(lst_provisional)
                    conteo += 1

            
            print((tabulate(valores_a_imprimir1, headers=["NOMBRE", "CIUDAD", "PAIS", "ICAO"])).center(220))
            print("_" * 50)

            contador_pesos = 1
            suma_de_pesos = 0
            for pesos in lt.iterator(total_weights):
                print(f"Distancia recorrida en el trayecto numero {contador_pesos}: ",  pesos)
                contador_pesos +=1
                suma_de_pesos +=pesos
            print("--------------------------")
            print("Suma de recorridos sumada por trayecto: ", suma_de_pesos)
            print("--------------------------")
            print(f"Se ha demorado un total de {time}[ms]")
            print("--------------------------")
            print(conteo)
            

        elif int(inputs) == 7:
            M= int(input("Ingrese la cantidad de aeropuertos\n "))
            print_req_6(control,M)

        elif int(inputs) == 8:
            print_req_7(control)

        elif int(inputs) == 9:
            print_req_8(control)
        elif int(inputs) == 10:
            print("[1] Rapidez")
            print("[2] Almacenamiento\n")
            respuesta = input("¿Qué opción desea escoger? ")
            while respuesta != "1" and respuesta != "2":
                
                
                print("Opción no disponible\n")
                respuesta = input("¿Qué opción desea escoger? ")
            if respuesta == "1":
                cambiar_pruebas("Rapidez")
            elif respuesta == "2":
                cambiar_pruebas("Almacenamiento")
        elif int(inputs) == 11:
            print("\nPOR FAVOR DIGITE A CONTINUACIÓN EL SUFIJO DEL ARCHIVO PARA EL QUE DESEA MANIPULAR LA MUESTRA\n")
            sufijo = input("sufijo : ")
            
            if sufijo in ["10-por", "20-por", "30-por","40-por","50-por", "60-por", "70-por", "80-por","90-por","small","medium", "large"]:
                controller.cambiarTamañoMuestra(sufijo)
            else:
                print("\n no existen archivos con ese sufijo, intente nuevamente\n")

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
            
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
