from segment import Segment
from node import Node

# Crear 3 nodos
n1 = Node('A', 0, 0)
n2 = Node('B', 3, 4)
n3 = Node('C', 6, 0)

# Crear segmentos
s1 = Segment('AB', n1, n2)
s2 = Segment('BC', n2, n3)

# Mostrar información
print("Segmento 1:")
print(f"Nombre: {s1.name}")
print(f"Origen: {s1.origin.name}")
print(f"Destino: {s1.destination.name}")
print(f"Costo: {s1.cost:.2f}")

print("\nSegmento 2:")
print(f"Nombre: {s2.name}")
print(f"Origen: {s2.origin.name}")
print(f"Destino: {s2.destination.name}")
print(f"Costo: {s2.cost:.2f}")