import random
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

# Define la zona que delimita el mapa
poligono = Polygon([
	(-103.409, 20.666),
	(-103.409, 20.695),
	(-103.359, 20.695),
	(-103.359, 20.666)
])

# Descarga los datos de OSM y los convierte en un grafo
G = ox.graph_from_polygon(poligono, network_type='drive')

# Encuentra el camino inicial del punto A al B sin repetir calles
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
def verificar_ruta_valida(G):
	while True:
		# Elige dos nodos al azar dentro del grafo reducido
		nodo_a = random.choice(list(G.nodes()))
		nodo_b = random.choice(list(G.nodes()))

		# Conjunto compartido de aristas visitadas
		esq_visitadas = set()

		# Encuentra el camino inicial del punto A al punto B  y visceversa, sin repetir calles
		ruta_inicial_ab = encuentra_ruta_inicial(G, nodo_a, nodo_b, esq_visitadas)
		ruta_inicial_ba = encuentra_ruta_inicial(G, nodo_b, nodo_a, esq_visitadas)

		# Verifica si ambos caminos existen
		if ruta_inicial_ab and ruta_inicial_ba:
			return nodo_a, nodo_b, ruta_inicial_ab, ruta_inicial_ba

# Función para imprimir el mapa en blanco
def mostrar_mapa():
	fig, ax = plt.subplots(figsize=(12, 8))
	ox.plot_graph(G, ax=ax, show=False, close=False, node_size=0, edge_color="#3F4E4F")
	plt.title('Mapa de la Zona de Interés', fontsize=15, fontweight='bold')
	plt.show()

# Función para calcular la distancia de una ruta
def calcular_distancia_ruta(G, ruta):
	# Inicializa la distancia total
	distancia_total = 0
	# Iterara sobre cada nodo de la ruta
	for i in range(len(ruta) - 1):
		# Obtiene el nodo origen y el contiguo
		nodo_origen = ruta[i]
		nodo_destino = ruta[i + 1]
		# Obtiene la lopngitud de la arista, osea la distancia de la calle
		edge_data = G.get_edge_data(nodo_origen, nodo_destino)
		# Suma la longitud de la arista a la distancia total
		distancia_total += edge_data[0]['length']
	return distancia_total

# Función para mostrar la ruta inicial
def mostrar_ruta_i():
	# Encuentra nodos y rutas válidas
	nodo_a, nodo_b, ruta_inicial_ab, ruta_inicial_ba = verificar_ruta_valida(G)

	# Calcula la distancia de las rutas generadas
	distancia_ida = calcular_distancia_ruta(G, ruta_inicial_ab)
	distancia_vuelta = calcular_distancia_ruta(G, ruta_inicial_ba)
	distancia_total = distancia_ida + distancia_vuelta

	# Visualiza las rutas de ida y vuelta en el mapa
	fig, ax = plt.subplots(figsize=(12, 8))

	# Dibuja el grafo en el fondo
	ox.plot_graph(G, ax=ax, show=False, close=False, node_size=0, edge_color="#D3D3D3")

	# Dibuja la ruta de ida y vuelta
	ox.plot_graph_route(G, ruta_inicial_ab, ax=ax, route_color='red', route_linewidth=2, show=False, close=False)
	ox.plot_graph_route(G, ruta_inicial_ba, ax=ax, route_color='orange', route_linewidth=2, show=False, close=False)

	# Añade marcadores para el origen y destino
	x_origin, y_origin = G.nodes[nodo_a]['x'], G.nodes[nodo_a]['y']
	x_dest, y_dest = G.nodes[nodo_b]['x'], G.nodes[nodo_b]['y']

	# Leyendas para los marcadores y rutas
	plt.title('Ruta Inicial', fontsize=15, fontweight='bold')
	ax.scatter(x_origin, y_origin, c='blue', s=70, label='Origen', zorder=5)
	ax.scatter(x_dest, y_dest, c='red', s=70, label='Destino', zorder=5)
	ax.plot([], [], color='red', linewidth=2, label='Ruta de ida')
	ax.plot([], [], color='orange', linewidth=2, label='Ruta de vuelta')
	ax.legend()
 
	plt.figtext(0.5, 0.05, f'Distancia de ida: {distancia_ida:.2f} m, Distancia de vuelta: {distancia_vuelta:.2f} m, Distancia total: {distancia_total:.2f} m', wrap=True, horizontalalignment='center', fontsize=11)

	plt.show()

def mostrar_ruta_f():
	pass
