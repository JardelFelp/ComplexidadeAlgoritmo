import random
import json
from shapely import wkt


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


TEST_TYPE_OPTIONS = [
    'Mathematics',
    'Portuguese'
]


def generate_rooms():
    rooms = []
    num_of_rooms = random.randint(2, 4)

    for i in range(num_of_rooms):
        rooms.append({
            "type_of_test": TEST_TYPE_OPTIONS[random.randint(0, len(TEST_TYPE_OPTIONS) - 1)],
            "capacity": random.randint(3, 6) * 5,
            "id": i
        })

    return rooms


def create_schools_json():
    multipolygons, districts = load_districts_csv()
    schools = load_schools_json()
    result = []

    for i in range(len(districts)):
        temporary_result = {
            "id": i,
            "name": districts[i],
            "schools": []
        }

        schools_count = 0

        for j in range(len(schools)):
            if schools[j]['district'] == districts[i]:
                schools[j]['id'] = schools_count
                schools[j]['rooms'] = generate_rooms()
                temporary_result['schools'].append(schools[j])

                schools_count += 1

        result.append(temporary_result)

    with open("bairros-escolas.json", "w") as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)