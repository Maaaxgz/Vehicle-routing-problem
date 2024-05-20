import random
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# Especifica la ubicación de interés
location = "Zapopan, Jalisco, México"

# Descarga los datos de OSM y conviértelos en un grafo
G = ox.graph_from_place(location, network_type='drive')

# Elige dos nodos al azar
nodeA = random.choice(list(G.nodes()))
nodeB = random.choice(list(G.nodes()))

# Si no hay camino del nodo A al B o viceversa, elige dos nodos diferentes al azar
while not nx.has_path(G, nodeA, nodeB):
	nodeA = random.choice(list(G.nodes()))
	nodeB = random.choice(list(G.nodes()))

# Calcula la ruta más corta del punto A al punto B
shortest_path_A_B = nx.shortest_path(G, nodeA, nodeB, weight='length')

# Calcula la ruta más corta del punto B al punto A
shortest_path_B_A = nx.shortest_path(G, nodeB, nodeA, weight='length')

# Combina las dos rutas para obtener la ruta completa del punto A al punto B y de regreso al punto A
complete_route = shortest_path_A_B + shortest_path_B_A[1:]

# Visualiza la ruta completa en un mapa
fig, ax = ox.plot_graph_route(G, complete_route, node_size=0)
plt.show()
