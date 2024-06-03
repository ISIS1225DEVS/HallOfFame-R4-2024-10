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
import New_Functions as nf
import hash_table_lp as ht
import scc as scc
import djk_2 as djk
import arboles_rojo_negro as arbol
import grafos as gr
import prim as prim
from tabulate import tabulate

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
    control= controller.new_controller()
    return control


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Identificar si hay una ruta entre dos destinos turísticos")
    print("3- Identificar el itinerario con menos escalas entre dos destinos turísticos")
    print("4- Determinar la red de trayectos comerciales de cobertura máxima desde el aeropuerto con mayor concurrencia")
    print("5- Determinar la red de trayectos de carga de distancia mínima partiendo del aeropuerto con mayor concurrencia")
    print("6- Determinar la red de respuesta militar de menor tiempo partiendo desde el aeropuerto con mayor importancia militar")
    print("7- Obtener los caminos más cortos para la cobertura de los M aeropuertos más importantes del país")
    print("8- Obtener el camino más corto en tiempo para llegar entre dos puntos turísticos")
    print("9- Graficar los resultados para cada uno de los requerimientos")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    return controller.load_data(control)


def print_data(control):
    """
        Función que imprime un dato dado su ID
    """
    print("El número de aeropuertos cargados es", nf.get_size(control['aeropuertos_lista']))
    print("El total de vuelos es", nf.get_size(ht.keySet(control['vuelos'])))
    headers = ["Nombre", "ICAO", "Ciudad", "Concurrencia Comercial"]
    lista_comerciales, lista_militar, lista_carga = controller.print_data(control)
    print("Concurrencia aviones comerciales: ")
    print(tabulate(lista_comerciales, headers=headers, tablefmt="grid"))
    print("Concurrencia aviones militar: ")
    print(tabulate(lista_militar, headers=headers, tablefmt="grid"))
    print("Concurrencia aviones de carga: ")
    print(tabulate(lista_carga, headers=headers, tablefmt="grid"))

def print_req_1(control, o1, o2, d1, d2):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    time, r= controller.req_1(control, o1, o2, d1, d2)
    if len(r)==5:
        tiempo, distancia, total_aeropuertos, para_tabular, header= r
        print('Tiempo de ejecución: ', time)
        print('Tiempo del trayecto: {} minutos. '.format(tiempo))
        print('Distancia total del trayecto: {} km. '.format(distancia))
        print('Se visitan {} aeropuertos.'.format(total_aeropuertos))
        print(tabulate(para_tabular, headers=header, tablefmt='fancygrid'))
    else:
        aod, ao, add, ad= r 
        print('No se encontro un aeropuerto dentro del rango de busqueda.')
        print('El aeropuerto de origen más cercano es {} a una distancia de {} km de las coordenadas de origen.'.format(ao,aod))
        print('El aeropuerto de destino más cercano es {} a una distancia de {} km de las coordenadas de destino.'.format(ad,add))


def print_req_2(control, o1, o2, d1, d2):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    tiempo, info = controller.req_2(control, o1, o2, d1, d2)
    if len(info)==5:
        print("Tiempo de ejecución ", tiempo)
        print("El camino tomo", info[0], "minutos")
        print("Distancia total del camino", info[1])
        print("Se visitan", info[2], "aeropuertos")
        print(tabulate(info[3], headers=info[4], tablefmt='fancygrid'))
    else:
        distance1, ao,  distance2, ad = info 
        print('No se encontro un aeropuerto dentro del rango de busqueda.')
        print('El aeropuerto de origen más cercano es {} a una distancia de {} km de las coordenadas de origen.'.format(ao,distance1))
        print('El aeropuerto de destino más cercano es {} a una distancia de {} km de las coordenadas de destino.'.format(ad,distance2))


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    info = controller.req_3(control)
    print("Timepo de ejecución ", info[0])
    print("El aeropuerto más concurrido es", info[1]['elements'][1], "con el código", info[1]['elements'][0],
          "en", info[1]['elements'][2], info[1]['elements'][3], "con una concurrencia de", info[1]['elements'][4])
    print("La distancia total del trayecto es", info[2])
    print("Hay", info[3], "diferentes trayectos desde el aeropuerto", info[1]['elements'][1])
    headers = ['Origen', 'Destino', 'Distancia', 'Tiempo', 'Trayecto']
    tabla = []
    for i in range(0, info[3]):
        value = nf.getElement(info[4], i)
        nuevo = []
        for j in range(0, 5):
            info1 = nf.getElement(value, j)
            if j == 4:
                info1 = info1['elements']
            nuevo.append(info1)
        tabla.append(nuevo)
    print(tabulate(tabla, headers=headers, tablefmt="grid"))
        

def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    info = controller.req_4(control)
    print("Timepo de ejecución ", info[0])
    print("El aeropuerto más concurrido es", info[1]['elements'][1], "con el código", info[1]['elements'][0],
          "en", info[1]['elements'][2], info[1]['elements'][3], "con una concurrencia de", info[1]['elements'][4])
    print("La distancia total del trayecto es", info[2])
    print("Hay", info[3], "diferentes trayectos desde el aeropuerto", info[1]['elements'][1])
    headers = ['Origen', 'Destino', 'Distancia', 'Tiempo', 'Trayecto']
    tabla = []
    for i in range(0, info[3]):
        value = nf.getElement(info[4], i)
        nuevo = []
        for j in range(0, 5):
            info1 = nf.getElement(value, j)
            if j == 4:
                info1 = info1['elements']
            nuevo.append(info1)
        tabla.append(nuevo)
    print(tabulate(tabla, headers=headers, tablefmt="grid"))


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    time, r = controller.req_5(control)
    info, concurrencia, distancia_total, num_trayectos, tabla= r
    para_tabular,headers = tabla
    print('Tiempo de ejecución: ', time)
    print('El aeropuerto mas concurrido es: {}, con una concurrencia de: {} vuelos. '.format(info, concurrencia))
    print('Distancia total de los trayectos: {} km. '.format(round(distancia_total,2)))
    print('El numero de trayectos posibles es: {}.'.format(round(num_trayectos,2)))
    print(tabulate(para_tabular, headers=headers))


def print_req_6(control, numero):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    info = controller.req_6(control, numero)
    
    print("Timepo de ejecución ", info[0])
    print("El aeropuerto más concurrido es", info[1]['elements'][1], "con el código", info[1]['elements'][0],
          "en", info[1]['elements'][2], info[1]['elements'][3], "con una concurrencia de", info[1]['elements'][4])
    headers = ['# Aeropuertos', 'Aeropuertos', 'Vuelos', 'Distancia']
    tabla = []
    for i in range(0, nf.get_size(info[2])):
            value = nf.getElement(info[2], i)
            nuevo = []
            for j in range(0, 4):
                info1 = nf.getElement(value, j)
                if j == 1 or j == 2:
                    info1 = info1['elements']
                nuevo.append(info1)
            tabla.append(nuevo)
    print(tabulate(tabla, headers=headers, tablefmt="grid"))


def print_req_7(control,origen,destino):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    time, r= controller.req_7(control, origen, destino)
    if len(r)==5:
        tiempo_total, distancia_total, total_aeropuertos, tabla, distancia= r
        para_tabular, headers= tabla
        print('Tiempo de ejecución: ', time)
        print('Tiempo del trayecto: {} minutos. '.format(tiempo_total))
        print('Distancia total del trayecto: {} km. '.format(distancia_total))
        print('Distancia del trayecto: {} km (sin contar la distancia hasta y desde los aeropuertos).'.format(distancia))
        print('Se visitan {} aeropuertos.'.format(total_aeropuertos))
        print(tabulate(para_tabular, headers=headers, tablefmt='fancygrid'))
    else:
        aod, ao, add, ad= r 
        print('No se encontro un aeropuerto dentro del rango de busqueda.')
        print('El aeropuerto de origen más cercano es {} a una distancia de {} km de las coordenadas de origen.'.format(ao,aod))
        print('El aeropuerto de destino más cercano es {} a una distancia de {} km de las coordenadas de destino.'.format(ad,add))
        
        
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
            print_data(control)
        
        elif int(inputs) == 2:
            o1= float(input('Ingrese la latitud del punto de origen (usar punto): '))
            o2= float(input('Ingrese la longitud del punto de origen (usar punto): '))
            d1= float(input('Ingrese la latitud del punto de destino (usar punto): '))
            d2= float(input('Ingrese la longitud del punto de destino (usar punto): '))  
            print_req_1(control, o1,o2,d1,d2)

        elif int(inputs) == 3:
            o1= float(input('Ingrese la latitud del punto de origen (usar punto): '))
            o2= float(input('Ingrese la longitud del punto de origen (usar punto): '))
            d1= float(input('Ingrese la latitud del punto de destino (usar punto): '))
            d2= float(input('Ingrese la longitud del punto de destino (usar punto): '))  
            print_req_2(control, o1, o2, d1, d2)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            numero = int(input("Número de aeropuertos para revisar: "))
            print_req_6(control, numero)

        elif int(inputs) == 8:
            o1= float(input('Ingrese la latitud del punto de origen (usar punto): '))
            o2= float(input('Ingrese la longitud del punto de origen (usar punto): '))
            d1= float(input('Ingrese la latitud del punto de destino (usar punto): '))
            d2= float(input('Ingrese la longitud del punto de destino (usar punto): '))  
            print_req_7(control, (o1,o2),(d1,d2))

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
            
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
