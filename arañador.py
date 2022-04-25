import requests
from datetime import datetime
from bs4 import BeautifulSoup
import descargador
import os



def modulo_de_control():
      
    calendarizador()

def arañador():

      base_de_datos = open ('base_datos/links.txt','w')
      base_de_datos.write(str(datetime.today())+"\n")
      referencias = open("links_para_buscar.txt")
      link_a_buscar = referencias.readline()
      peliculas = []
      while link_a_buscar != '':
            print("PELICULAS ESCANEADAS EN: " +link_a_buscar)
            reqs = requests.get(link_a_buscar)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            tabla = soup.find('table', {'class': 'table'}).find_all('a')

            for pelicula in tabla:
                  if pelicula['href'] not in peliculas:
                        base_de_datos.write('https://www.rottentomatoes.com'+pelicula['href']+"\n")
                        peliculas.append(pelicula['href'])
            link_a_buscar = referencias.readline()
      base_de_datos.close()
      referencias.close()

  
def verficar_base():
      
    base_de_datos = open ('base_datos/links.txt','r')   
    fecha_de_busqueda = base_de_datos.readline()
    
    if fecha_de_busqueda == "":  
          base_de_datos.close()
          return True
    else:
          fecha_limpia = ""
          for i in fecha_de_busqueda:
              if i != "\n":
                    fecha_limpia += i
          fecha = datetime.strptime(fecha_limpia, '%Y-%m-%d %H:%M:%S.%f')
          delta = datetime.today() - fecha
          if delta.days > 7:
                base_de_datos.close()
                return True
          else:
                base_de_datos.close()
                return False
            
def calendarizador():

      if verficar_base():
            print('INICIANDO DESCARGA')
            arañador()
            descargador.coordinador()
      elif verificar_archivo_nuevo():
            print("VERIFICADO ARCHIVOS NUEVOS")
      
      print("LA BASE DE DATOS, ESTA ACTUALIZADA Y LA COLECCIÓN SE MANTIENE ESTABLE")
            
            
            
            
def verificar_archivo_nuevo():

      directorio = 'base_datos/coleccion'
      contenido = os.listdir(directorio)
      links = open('base_datos/links.txt','r')
      link = links.readline()
      link = links.readline()
      nombre_links = []
      while link != "":
            nombre_links.append(link[33:].strip())
            link = links.readline()
      control = False
      for i in nombre_links:
            nombre = i[:len(i)] +'.txt'
            if nombre not in contenido:
                  print("NUEVO DETECTADO! EMPEZANDO DESCARGA DE "+ nombre)
                  descargador.descargar_info("https://www.rottentomatoes.com/m/"+i[:len(i)])
                  control = True
      return control
      
modulo_de_control()