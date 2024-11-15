import json
import pandas as pd


def get_tests_and_rooms(districts):
    types = []
    rooms = []

    for district in districts:
        for school in district["schools"]:
            for room in school["rooms"]:
                rooms.append({
                    "district_id": district["id"],
                    "school_id": school["id"],
                    "room_id": room["id"],
                    "type_of_test": room["type_of_test"],
                    "capacity": room["capacity"]
                })

                if room["type_of_test"] not in types:
                    types.append(room["type_of_test"])

    return types, rooms


def district_with_schools(district):
    return len(district["schools"])


def get_districts_with_test(rooms, type_of_test):
    return list({room["district_id"] for room in rooms if room["type_of_test"] == type_of_test})


# Function to calculate the minimum distance from each district to the districts with schools
def calculate_minimum_distance_by_index(distance_matrix, school_district_indices):
    minimum_distances = {}
    for i, district in enumerate(distance_matrix.index):
        # Select the distances from the current district to the school districts (based on indices)
        distances_to_schools = distance_matrix.iloc[i, school_district_indices]
        # Calculate the minimum distance
        minimum_distances[i] = int(distances_to_schools.min())
    return minimum_distances


def order_by_distance(distance_matrix, districts_with_schools):
    # Calculate the minimum distances using the indices
    minimum_distances = calculate_minimum_distance_by_index(distance_matrix, districts_with_schools)

    # Sort the districts by minimum distance in descending order
    sorted_districts = sorted(minimum_distances.items(), key=lambda x: x[1], reverse=True)

    return [i for i, item in sorted_districts]


def main():
    distance_matrix = pd.read_csv("distance_matriz.csv", index_col=0)
    districts = json.load(open("bairros-escolas.json", "r"))
    participants = json.load(open("participants.json", "r"))
    types_tests, rooms = get_tests_and_rooms(districts)
    distance_matrix_items = distance_matrix.to_numpy().tolist()
    result = []

    for type_of_test in types_tests:
        districts_with_test = get_districts_with_test(rooms, type_of_test)
        district_distance_order = order_by_distance(distance_matrix, districts_with_test)
        rooms_with_test = [room for room in rooms if room["type_of_test"] == type_of_test]

        print(rooms_with_test)

        for district in district_distance_order:
            district_participants = [
                item for item in participants
                if item["district_id"] == district and item["type_of_test"] == type_of_test
            ]
            distance_matrix_to_test = sorted([
                (index, item)
                for index, item in enumerate(distance_matrix_items[district])
                if index in districts_with_test
            ], key=lambda x: x[1])

            for participant in district_participants:
                for test_district_index, distance in distance_matrix_to_test:
                    # Buscar uma sala disponível no bairro mais próximo
                    available_room = next(
                        (room for room in rooms_with_test if
                         room["district_id"] == test_district_index and room["capacity"] > 0),
                        None
                    )

                    if available_room:
                        # Alocar o participante
                        result.append({
                            "participant_id": participant["id"],
                            "district_id": test_district_index,
                            "school_id": available_room["school_id"],
                            "room_id": available_room["room_id"],
                            "type_of_test": type_of_test,
                            "distance": distance
                        })
                        available_room["capacity"] -= 1  # Reduzir a capacidade da sala
                        break

        # Salvar ou exibir o resultado final
        print(json.dumps(result, indent=4))
        with open("allocation_result.json", "w") as output_file:
            json.dump(result, output_file, indent=4)


main()