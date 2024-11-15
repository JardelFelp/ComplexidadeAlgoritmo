import pandas as pd
import numpy as np
import heapq

# Load the adjacency matrix from the CSV file
file_path = 'matriz_atualizada.csv'
matrix_data = pd.read_csv(file_path, index_col=0)

# Ensure uniqueness and clean up column/index names
matrix_data.columns = range(len(matrix_data.columns))  # Replace column names with indices
matrix_data.index = range(len(matrix_data.index))  # Replace row names with indices


# Convert the DataFrame to a dictionary representation for the graph
def create_graph_from_matrix(matrix):
    graph = {}
    for index, row in matrix.iterrows():
        graph[index] = {}
        for col in matrix.columns:
            weight = row[col]
            if weight > 0:  # Only include edges with positive weights
                graph[index][col] = weight
    return graph


# Dijkstra's algorithm implementation
def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # If the popped node has a greater distance than recorded, skip it
        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances


# Create the graph from the adjacency matrix
graph = create_graph_from_matrix(matrix_data)


# Calculate distances from all nodes to all other nodes
def all_pairs_shortest_paths(graph):
    all_distances = {}
    for node in graph:
        all_distances[node] = dijkstra(graph, node)
    return all_distances


# Compute all pairs shortest paths
distances = all_pairs_shortest_paths(graph)

# Convert the results to a DataFrame
distances_df = pd.DataFrame(distances).T

# Restore original labels to the DataFrame
original_labels = pd.read_csv(file_path, index_col=0).index.tolist()
distances_df.index = original_labels
distances_df.columns = original_labels

# Save the results to a CSV file
output_file_path = 'distance_matriz.csv'
distances_df.to_csv(output_file_path)

print(f"Distances saved to {output_file_path}")
