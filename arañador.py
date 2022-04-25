from email.mime import base
import requests
import lxml
import os
import manejador_json
from datetime import datetime
from bs4 import BeautifulSoup
import descargador
from concurrent.futures import thread
from multiprocessing import parent_process
import threading
import random 

def modulo_de_control():
    if arañador():
          print("LINKS ACTUALIZADOS INICIA CALENDARIZADOR")
          #Se llama al descargador
          calendarizador()
    else:
       print("LA BASE DE DATOS, ESTA ACTUALIZADA Y LA COLECCIÓN SE MANTIENE ESTABLE")
       calendarizador()

def arañador():
    if verficar_base():
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
      return True
    else:
          return False
  
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
                return True
          else:
            print("NO SE ACTUALIZA TODAVÍA LA BASE")
            return False
    base_de_datos.close()
def calendarizador():
      contenido = os.listdir('base_datos/coleccion/')
      with open('base_datos/links.txt') as myfile:
            lineas_totales = sum(1 for line in myfile)
      if len(contenido) != lineas_totales:
            f = open('base_datos/links.txt', 'r')
            print('Iniciando descarga')
            descargador.coordinador()

modulo_de_control()