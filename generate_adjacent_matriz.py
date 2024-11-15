import random

from shapely import wkt, Point
import pandas as pd
import json
import googlemaps

# Substitua pela sua chave de API do Google Maps
api_key = 'API_KEY'
gmaps = googlemaps.Client(key=api_key)

isolated_districts = [
    ('Piola', 'Renascer'),
    ('Medianeira', 'Balneário Caverá'),
    ('Centro', 'Ibirapuitã'),
    ('Área Militar', 'Ibirapuitã'),
]


def calcular_distancia(origin, destiny):
    directions_result = gmaps.directions(
        f"{origin} - Alegrete, RS, Brasil",
        f"{destiny} - Alegrete, RS, Brasil",
        mode="driving"
    )

    distance = directions_result[0]['legs'][0]['distance']['value']

    print(f"{origin} - Alegrete, RS, Brasil até {destiny} - Alegrete, RS, Brasil", distance)

    return distance


def is_isolated_district(district01, district02):
    for item in isolated_districts:
        if district01 in item and district02 in item:
            return True

    return False


def load_districts_csv():
    file = open("bairros.csv")

    lines = file.readlines()
    multipolygons = []
    districts = []

    for line in lines:
        [name, wkt_coordinates] = line.split(";")

        multipolygon = wkt.loads(wkt_coordinates)

        multipolygons.append(multipolygon)
        districts.append(name)

    return multipolygons, districts


def load_schools_json():
    json_file = open('escolas.json', 'r')

    return json.load(json_file)


def create_csv_matriz():
    multipolygons, districts = load_districts_csv()

    matriz = [[i for i in districts]]
    matriz[0].insert(0, '')

    for i in range(len(multipolygons)):
        matriz.append([districts[i]])
        for j in range(len(multipolygons)):
            if i == j:
                matriz[i + 1].append(1)
            elif multipolygons[i].intersects(multipolygons[j]) or is_isolated_district(districts[i], districts[j]):
                matriz[i + 1].append(calcular_distancia(districts[i], districts[j]))
            else:
                matriz[i + 1].append(1 if multipolygons[i].intersects(multipolygons[j]) else 0)

    dataframe = pd.DataFrame(matriz)
    dataframe.to_csv("matriz.csv", index=False, header=False)

# create_csv_matriz()

