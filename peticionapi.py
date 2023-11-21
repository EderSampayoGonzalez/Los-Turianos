import requests

def Info_Pokemon (nombre_pokemon):
    base = "https://pokeapi.co/api/v2/"
    url = base + f"pokemon/{nombre_pokemon}/"
    try:
        response = requests.get(url)
        #print (response)
    except Exception as ex:
        print(ex)
        
    else:       
        if response.status_code == 200:
            print("consulta exitosa")
            data = response.json()
            return data
        else:    
            return None

def Info_Especie (link):
    try:
        response = requests.get(link)
    except Exception as ex:
        print(ex)
    else:       
        if response.status_code == 200:
            #print("consulta exitosa")
            speciesdat = response.json()
            if 'evolution_chain' in speciesdat.keys():
                #print ("se va aconsultar la cadena")
                cadevolutiva=Info_Especie(speciesdat['evolution_chain']['url'])
                #print (cadevolutiva)
                return cadevolutiva['chain']
            else:
                return speciesdat
        else:    
            return None
    #for x,y in speciesdat.items ():
    #    print (x, '\t', y)
        

