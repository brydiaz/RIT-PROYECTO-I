from email.mime import base
import requests
import lxml
import manejador_json
from datetime import datetime

from bs4 import BeautifulSoup

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

def modulo_de_control():
    if arañador():
          print("oli")
          #Se llama al descargador y su proceso de limpieza
    else:
       return "holi"

def arañador():
    if verficar_base():
      url = manejador_json.obtener_valor("url")
      f = requests.get(url, headers = headers)
      lista_peliculas = []
      soup = BeautifulSoup(f.content, 'lxml')
      peliculas = soup.find('table', {'class': 'table'}).find_all('a')
      pos_en_top = 0
      base_de_datos = open ('base_datos/links.txt','w')
      base_de_datos.write(str(datetime.today())+"\n")
      for anchor in peliculas:
          urls = 'https://www.rottentomatoes.com' + anchor['href']
          lista_peliculas.append(urls)
          pos_en_top += 1
          url_pelicula = urls
          pelicula_en_archivo = requests.get(url_pelicula, headers = headers)
          pelicula_en_soup = BeautifulSoup(pelicula_en_archivo.content, 'lxml')
          contenido_pelicula = pelicula_en_soup.find('div', {'class': 'movie_synopsis clamp clamp-6 js-clamp'}) 
          print("AÑADIDO: "+urls)       
          base_de_datos.write(str(pos_en_top) +' '+ urls+'\n')
          #print('Movie info:' + contenido_pelicula.string.strip())
      f.close()
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

modulo_de_control()