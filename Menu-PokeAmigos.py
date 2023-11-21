import requests
from matplotlib import pyplot as plt
import os
import peticionapi
import re
import numpy as np
import ManejoArchivo as ma

ruta = 'prueba.txt'
DatosPoke = list()

# obtener pokemon por su nombre
def consulta_pokemon():
    nombre_pokemon1 = input("Dame el nombre del pokemon o su número de pokedex: ")
    pokemon1 = peticionapi.Info_Pokemon(nombre_pokemon1.lower())
    if pokemon1==None:
        return
    lista=['height', 'weight', 'stats', 'species', 'stats', 'types','name', 'slot']
    pok=dict()
    for x,y in pokemon1.items():
        #print (x, "-", y, end="\n\n")
        temp=dict()
        if x in lista:
            if x=='species':
                evol=peticionapi.Info_Especie(y['url']) #consulta url de species
                CadEvo=evol['evolves_to']
                listemp=[evol['species']['name']]
                cadExtra=''
                mascad=''
                f=0
                for indice in CadEvo:
                    cadExtra+=(', '*f)+indice['species']['name'] #busca cada evolución intermedia
                    if f==0:
                        f=1
                    if 'evolves_to' in indice: #busca cada evolución final
                        if len(indice['evolves_to'])>0: 
                            for i in range (len(indice['evolves_to'])):
                                mascad+=', '*i+indice['evolves_to'][i]['species']['name']
                if cadExtra!='':
                    listemp.append(cadExtra)
                if mascad!='':    
                    listemp.append(mascad)

                pok['Cadena_evolutiva']=listemp
            elif x=='types':
                for i in range (len(y)):
                    pok['type'+str(i+1)]=y[i]['type']['name']
            elif x=='stats':
                suma=0
                dictstat=dict()
                for diccionarios in y:
                    nombstat = diccionarios['stat']['name']
                    stat = diccionarios['base_stat']
                    suma += diccionarios['base_stat']
                    dictstat[nombstat]=stat
                pok['Suma_stats']=suma
                pok['stats']=dictstat
            else:
                pok[x]=y
    for x,y in pok.items():
        print(x, ":\t\t", y)
    return pok


def Elimina_Poke (Datos):
    f=0
    bus=input("Ingresa el nombre del pokemon a eliminar: ")
    bus=bus.lower()
    for i in range(len(Datos)):
        if Datos[i]['name'] == bus:
            Datos.pop(i)
            f=1
    if f == 0:
        print ("No se encontró el pokemon en el equipo")
    else:
        print (bus, "Eliminado del equipo")


def Agrega_Poke (Data, api):
    if api == None:
        print ("Error de consulta. Intente de nuevo")
    else:
        Data.append(pokemon)
        print(api['name'], 'Agregado al equipo.')


def Grafica_Pesos (stats):
    weightlist = list()
    nameslist = list()
    for i in range(len(stats)):
        w = stats[i]["weight"]
        n = stats[i]["name"]
        nameslist.append(n)
        weightlist.append(w)
    #print(weightlist)
    #print(nameslist)
    x = np.array(nameslist)
    yweight = np.array(weightlist)
    plt.plot(x, yweight, "y", marker = "+")
    plt.title("Pesos")
    plt.xlabel("pokemon")
    plt.savefig("Grafica de pesos.png")
    plt.show()


def Grafica_sum_stats (stats):
    sumstatslist = list()
    nameslist = list()
    for i in range(len(stats)):
        suma = stats[i]["Suma_stats"]
        n = stats[i]["name"]
        nameslist.append(n)
        sumstatslist.append(suma)
    x = np.array(nameslist)
    ysuma = np.array(sumstatslist)
    plt.plot(x, ysuma, "b", marker = "*")
    plt.title("Suma de stats")
    plt.xlabel("Pokemon")
    plt.savefig("Grafica de suma de stats.png")
    plt.show()


def Grafica_stats (stats, poke):
    f=0
    i=-1
    listadestats = list()
    for i in range(len(stats)):
        #print (stats[i])
        if poke == stats[i]['name']:
            f=1
            for x in stats[i]['stats'].values():
                listadestats.append(x)
            break
    if f==0:
        print ("El pokemon no se encontró en el equipo")
        return None
    nombredestats = ["vida", "ataque", "defensa", "ataque\nespecial", "defensa\nespecial", "velocidad"]
    #listadestats = [stats[i]["hp"],stats[i]["attack"],stats[i]["defense"],
    #            stats[i]["special-attack"],stats[i]["special-defense"],stats[i]["speed"]]
    xpoke = np.array(nombredestats)
    ypoke = np.array(listadestats)
    plt.plot(xpoke, ypoke, "g", marker="o")
    plt.title("estadisticas de" "\n" +stats[i]["name"])
    plt.xlabel("estadisticas")
    plt.savefig("Grafica de estadisticas de "+stats[i]['name']+"")
    plt.show()


def Pedir_Opcion():
    opcion=input ("Opción: ")
    patron=r'\d'
    expRe=re.compile(patron)
    opcion+=' '
    cp=expRe.search(opcion)
    if cp == None:
        return
    numero=cp.group()
    #print (cp)
    #print (cp.group())
    return numero
    
    
#Flujo principal
if __name__==('__main__'):    

    msj = '''*** POKEAMIGOS ***
      1) Consulta del equipo (importar equipo)
      2) Guardar equipo (Exportar equipo)
      3) Crear un equipo de cero
      4) Eliminar un pokemon del equipo
      5) Agregar un pokemon al equipo
      6) Comparar el equipo (Graficar)
      7) salir del programa'''

    msj2='''*** Gráfica ***
      1) comparar el peso del equipo
      2) comparar la suma de estadísticas del equipo
      3) comparar las estadísticas de un pokemon concreto'''
    
    print(msj)
    while True:
        try:
            opc = int(Pedir_Opcion())
        except ValueError:
            print("Escribe un numero")
            continue
        except TypeError:
            print ("Escriba un número")
            continue
        else:
            if not (opc > 0 and opc < 8): #usar expresiones regulares para el menu
                print ('elige un número entre 1 y 7')
                continue

        
        if opc == 1:
            DatosPoke = ma.LeerArchivo("prueba.txt")

        if opc == 2:
            if DatosPoke==list():
                print("No hay datos para exportar")
            else:
                ma.CrearArchivo('prueba.txt',DatosPoke)
            
        if opc == 3: #hecho
            DatosPoke=list()
            pokemon=consulta_pokemon()
            Agrega_Poke (DatosPoke, pokemon)
            try:
                ma.CrearArchivo(ruta,DatosPoke)
            except Exception:
                print("ocurrió un error")
                DatosPoke=list()
            else:
                print ("Datos del equipo sobreescritos")

                 
        if opc == 4: #hecho
            try:
                Elimina_Poke (DatosPoke)
            except NameError:
                print ('Los datos del equipo no existen.\nPor favor importe el equipo o cree uno de cero.')
                continue
            
        if opc == 5: #hecho
            try:
                if len(DatosPoke)>6:
                    print ("Máximo de pokemon en el equipo alcanzado, no se puede agregar otro")
                    continue
            except NameError:
                print ('Los datos del equipo no existen.\nPor favor importe el equipo o cree uno de cero.')
                continue
            except Exception as ex:
                print (ex)
                break
            pokemon=consulta_pokemon()
            Agrega_Poke (DatosPoke, pokemon)
            
                
        if opc == 6:
            try:
                type(DatosPoke)==list()
            except NameError:
                print (('Los datos del equipo no existen.\nPor favor importe el equipo o cree uno de cero.'))
                continue
            print (msj2)
            try:
                opc2 = int(Pedir_Opcion())
            except TypeError:
                print ("Ingrese un número\nRegresando al menu principal")
                print (msj)
                continue
            if opc2 == 1:
                Grafica_Pesos (DatosPoke)

            if opc2 == 2:
                Grafica_sum_stats (DatosPoke)

            if opc2 == 3:
                bus=input("Escribe el nombre del pokemon a graficar: ")
                Grafica_stats (DatosPoke, bus)
            
        if opc == 7:
            break
        print(msj)


    for diccionarios in DatosPoke:
        for x,y in diccionarios.items():
            print (x, '\t\t', y)


