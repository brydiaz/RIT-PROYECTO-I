from email.mime import base
import readline
import threading
import requests
import re
from bs4 import BeautifulSoup
import preprocesamiento
 
descargados = []
base1 = []
base2 = []
base3 = []
base4 = []
base5 = []

def descargar_info(url):
    try:
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'html.parser')
        descripcion = soup.find('div', {'id': 'movieSynopsis'}).get_text().strip()
        descripcion += '\n'
        informacion_general = soup.find('ul', {'class': 'content-meta info'}).get_text()
        info_en_lista = informacion_general.strip().split('\n')
        info_completa = []
        for i in info_en_lista:
            if i.strip() != '':
                info_completa.append(i.strip())
        informacion_final = []
        for i in info_completa:
            if i[len(i)-1] != ':':
                i += '\n'
                informacion_final.append(i)
        nombre = url[33:]
        f = open ('base_datos/coleccion/'+nombre+'.txt','w')
        f.write(descripcion)
        for i in informacion_final:
            f.write(i)
        f.close()
        texto_limpio = preprocesamiento.limpiar('base_datos/coleccion/'+nombre+'.txt')
        f = open ('base_datos/coleccion/preprocesado/'+nombre+'.txt','w')
        f.write(texto_limpio)
        f.close()
    except:
        print("Error en url")
        
def descargar(numero_de_base):
    
    if numero_de_base == 1:
        for i in base1:
            descargar_info(i)
            print("HILO ENCARGADO:"+str(numero_de_base)+" DESCARGANDO: "+i)
    elif numero_de_base == 2:
        for i in base2:
            descargar_info(i)
            print("HILO ENCARGADO:"+str(numero_de_base)+" DESCARGANDO: "+i)
    elif numero_de_base == 3:
        for i in base3:
            descargar_info(i)
            print("HILO ENCARGADO:"+str(numero_de_base)+" DESCARGANDO: "+i)
    elif numero_de_base == 4:
        for i in base4:
            descargar_info(i)
            print("HILO ENCARGADO:"+str(numero_de_base)+" DESCARGANDO: "+i)
    elif numero_de_base == 5:
        for i in base5:
            descargar_info(i)
            print("HILO ENCARGADO:"+str(numero_de_base)+" DESCARGANDO: "+i)

def coordinador():
    f = open('base_datos/links.txt','r')
    links = f.read().split('\n')
    cont = 0
    len_links = len(links)//5
    for i in links:
        if cont < len_links:
            base1.append(i)
        elif len_links < cont < len_links*2:
                base2.append(i) 
        elif len_links*2 < cont < len_links*3:
                base3.append(i)
        elif len_links*3 < cont < len_links*4:
                base4.append(i)
        elif len_links*4 < cont < len_links*5:
                base5.append(i)    
        cont += 1
    for x in range(0, 5):
        escritor = threading.Thread(target=descargar, args=[x])
        escritor.start()
    