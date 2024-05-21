import random
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

# Define la zona que delimita tu área de interés (latitud y longitud)
poligono = Polygon([
    (-103.409, 20.666),
    (-103.409, 20.695),
    (-103.359, 20.695),
    (-103.359, 20.666)
])

# Descarga los datos de OSM y los convierte en un grafo
G = ox.graph_from_polygon(poligono, network_type='drive')

# Encuentra el camino inicial del punto A al punto B sin repetir calles y sin repetir calles con el camino de vuelta
def encuentra_ruta_inicial(G, inicio, fin, esq_visitadas):
    # Pila que contiene las combinaciones generadas y la ruta
    stack = [(inicio, [inicio])]
    # Conjunto de aristas visitadas por esta ruta
    esq_visitadas_loc = set(esq_visitadas)

	# Mientras la pila no esté vacía, osea mientras haya nodos por visitar
    while stack:
        # Extrae el ultimo elemento de la pila
        (nodo, ruta) = stack.pop()
        # Si el nodo manejado es el destino
        if nodo == fin:
            # Actualiza el conjunto de aristas visitadas
            esq_visitadas.update(esq_visitadas_loc)
            # Devuelve la ruta
            return ruta
        # Para cada nodo vecino del nodo manejado
        for nodos_h in G.neighbors(nodo):
            borde = (nodo, nodos_h)
            borde_rev = (nodos_h, nodo)
            # Si la arista no ha sido visitada de ida o de vuelta
            if borde not in esq_visitadas_loc and borde_rev not in esq_visitadas_loc:
                # Actualiza el conjunto de aristas visitadas
                esq_visitadas_loc.add(borde)
                # Añade el nodo vecino a la pila
                stack.append((nodos_h, ruta + [nodos_h]))
    # Si no se encontró una ruta válida, devuelve None
    return None

# Función para encontrar caminos válidos de ida y vuelta
def find_valid_routes(G):
    while True:
        # Elige dos nodos al azar dentro del grafo reducido
        nodeA = random.choice(list(G.nodes()))
        nodeB = random.choice(list(G.nodes()))

        # Conjunto compartido de aristas visitadas
        esq_visitadas = set()

        # Encuentra el camino inicial del punto A al punto B  y visceversa, sin repetir calles
        initial_path_A_B = encuentra_ruta_inicial(G, nodeA, nodeB, esq_visitadas)
        initial_path_B_A = encuentra_ruta_inicial(G, nodeB, nodeA, esq_visitadas)

        # Verifica si ambos caminos existen
        if initial_path_A_B and initial_path_B_A:
            return nodeA, nodeB, initial_path_A_B, initial_path_B_A

# Encuentra nodos y rutas válidas
nodeA, nodeB, initial_path_A_B, initial_path_B_A = find_valid_routes(G)

# Visualiza las rutas de ida y vuelta en el mapa
fig, ax = plt.subplots(figsize=(12, 8))

# Dibuja el grafo en el fondo
ox.plot_graph(G, ax=ax, show=False, close=False, node_size=0, edge_color="#D3D3D3")

# Dibuja la ruta de ida y vuelta
ox.plot_graph_route(G, initial_path_A_B, ax=ax, route_color='red', route_linewidth=2, show=False, close=False)
ox.plot_graph_route(G, initial_path_B_A, ax=ax, route_color='orange', route_linewidth=2, show=False, close=False)

# Añade marcadores para el origen y destino
x_origin, y_origin = G.nodes[nodeA]['x'], G.nodes[nodeA]['y']
x_dest, y_dest = G.nodes[nodeB]['x'], G.nodes[nodeB]['y']

# Leyendas para los marcadores y rutas
ax.scatter(x_origin, y_origin, c='blue', s=70, label='Origen', zorder=5)
ax.scatter(x_dest, y_dest, c='red', s=70, label='Destino', zorder=5)
ax.plot([], [], color='red', linewidth=2, label='Ruta de ida')
ax.plot([], [], color='orange', linewidth=2, label='Ruta de vuelta')

# Añade una leyenda
ax.legend()

plt.show()
