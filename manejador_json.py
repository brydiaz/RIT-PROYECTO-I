import json


def obtener_valor(llave):
    with open('confg.json') as file:
        data = json.load(file)
        return data[llave]
