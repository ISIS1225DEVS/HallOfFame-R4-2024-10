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
from DISClib.ADT import orderedmap as om
assert cf
from tabulate import tabulate

default_limit = 1000 
sys.setrecursionlimit(default_limit*10)

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


# Imprimir menú

def print_menu():
    print("\nBIENVENIDO")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Configuración")
    print("0- Salir\n")


# Funciones para la carga de datos

def load_data(control, memflag):
    """
    Carga los datos
    """
    analyzer, time, memory = controller.load_data(control, memflag)
    print("Datos cargados correctamente...\n")

    # Imprimir número de vuelos y aeropuertos
    print('Total de aeropuertos cargados: ' + str(controller.get_data_size(analyzer['airports'], mp)))
    print('   · Vuelos comerciales: ' + str(controller.totalFlights(analyzer['commercial'])))
    print('   · Vuelos de carga: ' + str(controller.totalFlights(analyzer['merchandise'])))
    print('   · Vuelos militares: ' + str(controller.totalFlights(analyzer['military'])))

    # Imprimir 5 primeros y 5 últimos aeropuertos con mayor concurrencia
    print('\n--- VUELOS COMERCIALES ---')
    print_airports(me.getValue(controller.get_entry(analyzer['best_airports'], om, 'commercial')), 5, 'load_data')
    print('\n--- VUELOS DE CARGA ---')
    print_airports(me.getValue(controller.get_entry(analyzer['best_airports'], om, 'merchandise')), 5, 'load_data')
    print('\n--- VUELOS MILITARES ---')
    print_airports(me.getValue(controller.get_entry(analyzer['best_airports'], om, 'military')), 5, 'load_data')

    delta_time = f"{time:.3f}"
    delta_memory = f"{memory:.3f}"

    print("\nTiempo de ejecución:", str(delta_time), "[ms]")
    print("Memoria utilizada:", str(delta_memory), "[kb]")


# Funciones para imprimir datos

def print_data(control, id, type):
    """
    Función que imprime datos dado su ID
    """
    if type == 'load_data':
        airport = controller.get_data(control, id)

        data = tabulate([
            ('Nombre del aeropuerto: ', airport['NOMBRE']),
            ('Identificador ICAO: ', airport['ICAO']),
            ('Ciudad: ', airport['CIUDAD']),
            ('Concurrencia: ', airport['CONCURRENCIA'])
        ])

    elif type == 'important_airport':
        airport = id

        data = tabulate([
            ('Nombre del aeropuerto: ', airport['NOMBRE']),
            ('Identificador ICAO: ', airport['ICAO']),
            ('País: ', airport['PAIS']),
            ('Ciudad: ', airport['CIUDAD']),
            ('Concurrencia: ', airport['CONCURRENCIA'])
        ])

    elif type == 'req_3':
        flight = id

        

    elif type == 'req_6_airports':
        airport = id

        data = tabulate([
            ('Nombre del aeropuerto: ', airport['NOMBRE']),
            ('Identificador ICAO: ', airport['ICAO']),
            ('País: ', airport['PAIS']),
            ('Ciudad: ', airport['CIUDAD'])
        ])

    elif type == 'req_6_flights':
        data = [ ('Origen', '', 'Destino') ]

        while not qu.isEmpty(control):
            flight = qu.dequeue(control)
            data.append((flight['ORIGEN'], '--->', flight['DESTINO']))
        
        data = tabulate(data, headers='firstrow', tablefmt='fancy_grid')
        
    print(data)


def print_airports(control, sample, type):
    """
    Función que imprime las n ofertas de la lista
    """
    size = controller.get_data_size(control, lt)
    
    if size == 1:
        print('\nEl único aeropuerto encontrado es: ')
        print_data(control, 1, type)

    elif size <= sample*2:
        print("\nLos", size, "aeropuertos son:")
        i = 1
        while i <= size:
            print_data(control, i, type)
            i += 1

    else:
        print("\nLos", sample, "primeros aeropuertos son:")
        i = 1
        while i <= sample:
            print_data(control, i, type)
            i += 1

        print("\nLos", sample, "últimos aeropuertos son:")
        i = size - sample + 1
        while i <= size:
            print_data(control, i, type)
            i += 1



# Funciones de requerimientos

def print_req_1(control, origin, destination, memflag, req_8):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    req_1,airports, stadistics, time, memory = controller.req_1(control, origin, destination, memflag, req_8)
    
    if stadistics is None:
        print('\nAlguno de los aeropuertos supera los 30 Kilómetros de distancia.')

        print('\n--- AEROPUERTO DE ORIGEN MÁS CERCANO ---')
        print(f' · Distancia: {req_1[0]:.2f} [Km]')
        print_data(None, airports[0], 'req_6_airports')

        print('\n--- AEROPUERTO DE DESTINO MÁS CERCANO ---')
        print(f' · Distancia: {req_1[1]:.2f} [Km]')
        print_data(None, airports[1], 'req_6_airports')

    elif req_1 is None:
        print('\n--- AEROPUERTO DE ORIGEN ---')
        print_data(None, airports[0], 'req_6_airports')

        print('\nNo se ha encontrado una ruta entre estos dos aeropuertos.')

        print('\n--- AEROPUERTO DE DESTINO ---')
        print_data(None, airports[1], 'req_6_airports')

    else:
        print('\n--- AEROPUERTO DE ORIGEN ---')
        print_data(None, airports[0], 'req_6_airports')

        print('\n--- AEROPUERTOS INTERMEDIOS ---')
        if qu.isEmpty(req_1):
            print('No hay aeropuertos intermedios.')

        while not qu.isEmpty(req_1):
            airport = qu.dequeue(req_1)
            print_data(None, airport, 'req_6_airports')

        print('\n--- AEROPUERTO DE DESTINO ---')
        print_data(None, airports[1], 'req_6_airports')
        
        print(f'\n· Número de aeropuertos visitados: {stadistics[1]}')
        print(f'· Distancia total del trayecto: {stadistics[0]:.2f} [Km]')
        print(f'· Tiempo total del trayecto: {stadistics[2]:.3f} [Min]')


    delta_time = f"{time:.3f}"
    delta_memory = f"{memory:.3f}"

    print("\nTiempo de ejecución:", str(delta_time), "[ms]")
    print("Memoria utilizada:", str(delta_memory), "[kb]")

def print_req_2(control, origin, destination, memflag, req_8):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    req_2, airports, stadistics, time, memory = controller.req_2(control, origin, destination, memflag, req_8)

    if stadistics is None:
        print('\nAlguno de los aeropuertos supera los 30 Kilómetros de distancia.')

        print('\n--- AEROPUERTO DE ORIGEN MÁS CERCANO ---')
        print(f' · Distancia: {req_2[0]:.2f} [Km]')
        print_data(None, airports[0], 'req_6_airports')

        print('\n--- AEROPUERTO DE DESTINO MÁS CERCANO ---')
        print(f' · Distancia: {req_2[1]:.2f} [Km]')
        print_data(None, airports[1], 'req_6_airports')

    elif req_2 is None:
        print('\n--- AEROPUERTO DE ORIGEN ---')
        print_data(None, airports[0], 'req_6_airports')

        print('\nNo se ha encontrado una ruta entre estos dos aeropuertos.')

        print('\n--- AEROPUERTO DE DESTINO ---')
        print_data(None, airports[1], 'req_6_airports')

    else:
        print('\n--- AEROPUERTO DE ORIGEN ---')
        print_data(None, airports[0], 'req_6_airports')

        print('\n--- AEROPUERTOS INTERMEDIOS ---')
        if qu.isEmpty(req_2):
            print('No hay aeropuertos intermedios.')

        while not qu.isEmpty(req_2):
            airport = qu.dequeue(req_2)
            print_data(None, airport, 'req_6_airports')

        print('\n--- AEROPUERTO DE DESTINO ---')
        print_data(None, airports[1], 'req_6_airports')

        print(f'\n· Número de aeropuertos visitados: {stadistics[1]}')
        print(f'· Distancia total del trayecto: {stadistics[0]:.2f} [Km]')



    delta_time = f"{time:.3f}"
    delta_memory = f"{memory:.3f}"

    print("\nTiempo de ejecución:", str(delta_time), "[ms]")
    print("Memoria utilizada:", str(delta_memory), "[kb]")


def print_req_3(control, memflag, req_8):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    req_3, important_airport, stadistics, time, memory = controller.req_3(control, memflag, req_8)

    total_flights = stadistics[0]
    total_distance = stadistics[1]

    print('\n--- AEROPUERTO CON MAYOR CONCURRENCIA COMERCIAL ---')
    print_data(None, important_airport, 'important_airport')

    print('\n--- COBERTURA COMERCIAL EN LA MENOR DISTANCIA ---')

    number = 1
    
    for path in lt.iterator(req_3):

        if not qu.isEmpty(path):
            print(f'\n--- TRAYECTO {number} ---')
            number += 1

        while not qu.isEmpty(path):
            # Obtener el vuelo a imprimir
            flight = qu.dequeue(path)

            print('· Aeropuerto de origen: ')
            print_data(None, flight['ORIGEN'], 'req_6_airports')

            print('· Aeropuerto de destino: ')
            print_data(None, flight['DESTINO'], 'req_6_airports')

            print(f"--> Distancia recorrida: {flight['DISTANCIA']:.2f} [Km]\n")

    print(f'Número de vuelos: {total_flights}')
    print(f'Distancia total recorrida: {total_distance:.2f} [Km]')
        
    delta_time = f"{time:.3f}"
    delta_memory = f"{memory:.3f}"

    print("\nTiempo de ejecución:", str(delta_time), "[ms]")
    print("Memoria utilizada:", str(delta_memory), "[kb]")


def print_req_4(control, memflag, req_8):
    
    req_4, important_airport, total_flights, total_distance, time, memory = controller.req_4(control, memflag, req_8)

    print('\n--- AEROPUERTO CON MAYOR CONCURRENCIA DE CARGA ---')
    print_data(None, important_airport, 'important_airport')

    print('\n--- COBERTURA DE CARGA EN LA MENOR DISTANCIA ---')

    number = 1
    
    for path in lt.iterator(req_4):

        if not qu.isEmpty(path):
            print(f'\n--- TRAYECTO {number} ---')
            number += 1

        while not qu.isEmpty(path):
            # Obtener el vuelo a imprimir
            flight = qu.dequeue(path)

            print('· Aeropuerto de origen: ')
            print_data(None, flight['ORIGEN'], 'req_6_airports')

            print('· Aeropuerto de destino: ')
            print_data(None, flight['DESTINO'], 'req_6_airports')

            print(f"--> Distancia recorrida: {flight['DISTANCIA']:.2f} [Km]\n")

    print(f'Número de vuelos: {total_flights}')
    print(f'Distancia total recorrida: {total_distance:.2f} [Km]')
        
    delta_time = f"{time:.3f}"
    delta_memory = f"{memory:.3f}"

    print("\nTiempo de ejecución:", str(delta_time), "[ms]")
    print("Memoria utilizada:", str(delta_memory), "[kb]")




def print_req_5(control, memflag, req_8):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    req_5, important_airport, stadistics, time, memory = controller.req_5(control, memflag, req_8)

    total_flights = stadistics[0]
    total_distance = stadistics[1]

    print('\n--- AEROPUERTO CON MAYOR CONCURRENCIA COMERCIAL ---')
    print_data(None, important_airport, 'important_airport')

    print('\n--- COBERTURA COMERCIAL EN LA MENOR DISTANCIA ---')

    number = 1
    
    for path in lt.iterator(req_5):

        if not qu.isEmpty(path):
            print(f'\n--- TRAYECTO {number} ---')
            number += 1

        while not qu.isEmpty(path):
            # Obtener el vuelo a imprimir
            flight = qu.dequeue(path)

            print('· Aeropuerto de origen: ')
            print_data(None, flight['ORIGEN'], 'req_6_airports')

            print('· Aeropuerto de destino: ')
            print_data(None, flight['DESTINO'], 'req_6_airports')

            print(f"--> Distancia recorrida: {flight['DISTANCIA']:.2f} [Km]\n")

    print(f'Número de vuelos: {total_flights}')
    print(f'Distancia total recorrida: {total_distance:.2f} [Km]')
        
    delta_time = f"{time:.3f}"
    delta_memory = f"{memory:.3f}"

    print("\nTiempo de ejecución:", str(delta_time), "[ms]")
    print("Memoria utilizada:", str(delta_memory), "[kb]")


def print_req_6(control, num_airports, memflag, req_8):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    req_6, colombian_airports, time, memory = controller.req_6(control, num_airports, memflag, req_8)

    print('\n--- AEROPUERTO CON MAYOR CONCURRENCIA COMERCIAL ---')
    print_data(None, lt.removeFirst(colombian_airports), 'important_airport')
    
    i = 1

    while i <= controller.get_data_size(colombian_airports, lt):
        # Obtener el aeropuerto que se desea cubrir
        airport = controller.get_data(colombian_airports, i)
        print('\n--- ' + airport['NOMBRE'] + ' ---\n')

        # Obtener las rutas para cubrir ese aeropuerto
        airport_coverage = controller.get_data(req_6, i)

        # Vericar que la distancia no sea infinita, es decir, que exista camino para llegar
        if airport_coverage['DISTANCE'] != 0:

            distance = f"{airport_coverage['DISTANCE']:.2f} [Km]"
            print('Distancia total: ' + distance)

            # Imprimir aeropuertos para llegar
            print('\nEl camino tiene un total de ' + str(controller.get_data_size(airport_coverage['AIRPORTS'], qu)) + ' aeropuerto(s).')
            while not qu.isEmpty(airport_coverage['AIRPORTS']):
                airport = qu.dequeue(airport_coverage['AIRPORTS'])
                print_data(None, airport, 'req_6_airports') 

            # Imprimir vuelos para llegar
            print('\nSe deben tomar ' + str(controller.get_data_size(airport_coverage['FLIGHTS'], qu)) + ' vuelo(s).')
            print_data(airport_coverage['FLIGHTS'], None, 'req_6_flights')

        else:
            print('No hay manera de llegar a este aeropuerto.')

        i += 1

    delta_time = f"{time:.3f}"
    delta_memory = f"{memory:.3f}"

    print("\nTiempo de ejecución:", str(delta_time), "[ms]")
    print("Memoria utilizada:", str(delta_memory), "[kb]")


def print_req_7(control, origin, destination, memflag, req_8):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    req_7, airports, stadistics, time, memory = controller.req_7(control, origin, destination, memflag, req_8)

    if stadistics is None:
        print('\nAlguno de los aeropuertos supera los 30 Kilómetros de distancia.')

        print('\n--- AEROPUERTO DE ORIGEN MÁS CERCANO ---')
        print(f' · Distancia: {req_7[0]:.2f} [Km]')
        print_data(None, airports[0], 'req_6_airports')

        print('\n--- AEROPUERTO DE DESTINO MÁS CERCANO ---')
        print(f' · Distancia: {req_7[1]:.2f} [Km]')
        print_data(None, airports[1], 'req_6_airports')

    elif req_7 is None:
        print('\n--- AEROPUERTO DE ORIGEN ---')
        print_data(None, airports[0], 'req_6_airports')

        print('\nNo se ha encontrado una ruta entre estos dos aeropuertos.')

        print('\n--- AEROPUERTO DE DESTINO ---')
        print_data(None, airports[1], 'req_6_airports')

    else:
        print('\n--- AEROPUERTO DE ORIGEN ---')
        print_data(None, airports[0], 'req_6_airports')

        print('\n--- AEROPUERTOS INTERMEDIOS ---')
        if qu.isEmpty(req_7):
            print('No hay aeropuertos intermedios.')

        while not qu.isEmpty(req_7):
            airport = qu.dequeue(req_7)
            print_data(None, airport, 'req_6_airports')

        print('\n--- AEROPUERTO DE DESTINO ---')
        print_data(None, airports[1], 'req_6_airports')

        print(f'\n· Número de aeropuertos visitados: {stadistics[2]}')
        print(f'· Distancia total del trayecto: {stadistics[1]:.2f} [Km]')
        print(f'· Tiempo total del trayecto: {stadistics[0]:.3f} [Min]')


    delta_time = f"{time:.3f}"
    delta_memory = f"{memory:.3f}"

    print("\nTiempo de ejecución:", str(delta_time), "[ms]")
    print("Memoria utilizada:", str(delta_memory), "[kb]")


# Funciones auxiliares

def execute_req_8():
    """
    Función que activa o desactiva solución del Requerimiento 8
    """
    print("\n¿Desea visualizar el mapa interactivo de cada requerimiento? (y/n)")
    
    req_8 = input('Respuesta: ')
    req_8 = castBoolean(req_8.lower())

    return req_8

def choose_memory_measurement():
    """
    Función que permite elegir si se desea medir la memoria
    """
    print("\n¿Desea observar el uso de memoria? (y/n)")
    
    memflag = input('Respuesta: ')
    memflag = castBoolean(memflag.lower())

    return memflag

def choose_sort_algorithm():
    """
    Función que permite elegir el algoritmo de ordenamiento
    """
    print("""\nSeleccione el algoritmo de ordenamiento:
    1. Selection Sort
    2. Insertion Sort
    3. Shell Sort
    4. Merge Sort
    5. Quick Sort\n""")
    
    choice = int(input('Seleccione una opción: '))

    return choice

def castBoolean(value):
    """
    Convierte un valor a booleano
    """
    if value in ('si', 's', 'yes', 'y', '1'):
        return True
    else:
        return False
    
def settings():
    """
    Configura las condiciones de la aplicación
    """
    print("""\nPor favor, elija que desea modificar:
    1. Algoritmo de ordenamiento
    2. Medición de memoria
    3. Visualización mapa interactivo
    0. Cancelar\n""")
    
    choice = int(input("Seleccione una opción: "))

    if choice == 1: # Cambiar algoritmo de ordenamiento
        algorithm = choose_sort_algorithm()
        selected_algo = controller.set_sort_algorithm(algorithm)
        print("Eligió la configuración - " + selected_algo)
        return None, None

    elif choice == 2: # Cambiar medicion de memoria
        memflag = choose_memory_measurement()
        return memflag, choice
    
    elif choice == 3: # Ejecutar req 8
        req_8 = execute_req_8()
        return req_8, choice

    else:
        print('Regresando al menú principal...')
        return None, None
        

# Parametros para la ejecucion del programa
control = None
req_8 = None
memflag = None

def menu_cycle(control, req_8, memflag):
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')

        if int(inputs) == 1: # Carga de datos
            if memflag == None:
                memflag = choose_memory_measurement()

            if req_8 == None:
                req_8 = execute_req_8()

            print("\nCargando información de los archivos ....\n")
            control = new_controller()

            load_data(control, memflag)

        elif int(inputs) == 2: # Requerimiento 1
            print('A continuación deberá ingresar el punto de origen.')
            origin_lat = input('Latitud: ')
            origin_lon = input('Longitud: ')

            # Establecer punto de origen
            origin = { 'LATITUD': origin_lat, 'LONGITUD': origin_lon }

            print('\nA continuación deberá ingresar el punto de destino.')
            destination_lat = input('Latitud: ')
            destination_lon = input('Longitud: ')

            # Establecer punto de destino
            destination = { 'LATITUD': destination_lat, 'LONGITUD': destination_lon }

            print("\nBuscando...")
            print_req_1(control, origin, destination, memflag, req_8)

        elif int(inputs) == 3: # Requerimiento 2
            print('A continuación deberá ingresar el punto de origen.')
            origin_lat = input('Latitud: ')
            origin_lon = input('Longitud: ')

            # Establecer punto de origen
            origin = { 'LATITUD': origin_lat, 'LONGITUD': origin_lon }

            print('\nA continuación deberá ingresar el punto de destino.')
            destination_lat = input('Latitud: ')
            destination_lon = input('Longitud: ')

            # Establecer punto de destino
            destination = { 'LATITUD': destination_lat, 'LONGITUD': destination_lon }

            print("\nBuscando...")
            print_req_2(control, origin, destination, memflag, req_8)

        elif int(inputs) == 4: # Requerimiento 3
            print("Buscando...")
            print_req_3(control, memflag, req_8)

        elif int(inputs) == 5: # Requerimiento 4
            print("Buscando...")
            print_req_4(control, memflag, req_8)

        elif int(inputs) == 6: # Requerimiento 5
            print("Buscando...")
            print_req_5(control, memflag, req_8)
            print("Buscando...")
            print_req_5(control, memflag, req_8)

        elif int(inputs) == 7: # Requerimiento 6
            num_airports = input('Ingrese la cantidad de aeropuertos que desea cubrir: ')
            print("Buscando...")
            print_req_6(control, num_airports, memflag, req_8)

        elif int(inputs) == 8: # Requerimiento 7
            print('A continuación deberá ingresar el punto de origen.')
            origin_lat = input('Latitud: ')
            origin_lon = input('Longitud: ')

            # Establecer punto de origen
            origin = { 'LATITUD': origin_lat, 'LONGITUD': origin_lon }

            print('\nA continuación deberá ingresar el punto de destino.')
            destination_lat = input('Latitud: ')
            destination_lon = input('Longitud: ')

            # Establecer punto de destino
            destination = { 'LATITUD': destination_lat, 'LONGITUD': destination_lon }

            print("\nBuscando...")
            print_req_7(control, origin, destination, memflag, req_8)

        elif int(inputs) == 9: # Configuraciones
            change, choice = settings()

            if choice == 2:
                memflag = change

            if choice == 3:
                req_8 = change

        elif int(inputs) == 0: # Salir
            working = False
            print("\nGracias por utilizar el programa")
            
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)

# main del reto
if __name__ == "__main__":
    menu_cycle(control, req_8, memflag)