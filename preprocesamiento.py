from tracemalloc import stop
import nltk as nl
import sys

puntuaciones = [",",".",";",'"',"?","¿","(",")","[","]","''",":"]


def cargar_stop_words(path):
    f = open(path, 'r')
    lista = f.read().split('\n')
    f.close()
    return lista

def quitar_puntuaciones(texto):
    texto_sin_puntuacion = []
    for i in texto:
        if i not in puntuaciones:
            texto_sin_puntuacion.append(i)
    return texto_sin_puntuacion

def quitar_stop_words(texto, stop_words):
    texto_sin_stop_words = []
    for i in texto:
        if i.lower() not in stop_words:
            texto_sin_stop_words.append(i)
    return texto_sin_stop_words

def quitar_sufijos(texto):
    ss = nl.SnowballStemmer(language='english')
    lista_sin_sufijos = []
    for i in texto:
        lista_sin_sufijos.append(ss.stem(i))
    return lista_sin_sufijos


def limpiar(nombre_archivo):

    f = open(nombre_archivo, "r")
    texto = f.read()
    texto_sin_comillas = texto.replace('"','')
    lista_palabras = nl.word_tokenize(texto_sin_comillas)
    lista_sin_puntuacion = quitar_puntuaciones(lista_palabras)
    stopwords = cargar_stop_words('base_datos/stopwords.txt')
    lista_sin_stop_words = quitar_stop_words(lista_sin_puntuacion, stopwords)
    lista_texto_limpio = quitar_sufijos(lista_sin_stop_words)
    texto_limpio = ""
    for i in lista_texto_limpio:
        i+= '\n'
        texto_limpio += i
    f.close()
    return texto_limpio
    
