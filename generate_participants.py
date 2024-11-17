import json
import random

from faker import Faker


def load_district_schools():
    json_file = open('bairros-escolas.json', 'r')
    return json.load(json_file)


def count_schools_rooms(districts):
    rooms = []
    num_participants = 0

    for district in districts:
        for school in district['schools']:
            for room in school['rooms']:
                num_participants += room["capacity"]

                rooms.append({
                    "type_of_test": room["type_of_test"],
                    "capacity": room["capacity"],
                })

    return rooms


def generate_participants(rooms, districts):
    fake = Faker()
    participants = []

    for room in rooms:
        for i in range(room['capacity']):
            district = districts[random.randint(0, len(districts) - 1)]
            participants.append({
                "id": len(participants),
                "district_id": district["id"],
                "name": fake.name(),
                "type_of_test": room["type_of_test"]
            })

    return participants


def export_participants(participants):
    with open("participants.json", "w") as json_file:
        json.dump(participants, json_file, ensure_ascii=False, indent=4)


def main():
    districts = load_district_schools()
    rooms = count_schools_rooms(districts)
    participants = generate_participants(rooms, districts)

    export_participants(participants)


main()