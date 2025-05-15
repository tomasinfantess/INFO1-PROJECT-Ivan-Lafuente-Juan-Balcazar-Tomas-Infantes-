from path import *
from node import Node

def test_path_functions():
    # Crear nodos de prueba
    n1 = Node("A", 0, 0)
    n2 = Node("B", 3, 4)
    n3 = Node("C", 6, 8)

    # Probar AddNodeToPath y CostToNode
    path = Path([n1], 0)
    path = AddNodeToPath(path, n2, 5.0)
    assert len(path.nodes) == 2
    assert path.cost == 5.0
    assert CostToNode(path, n2) == 5.0

    # Probar ContainsNode
    assert ContainsNode(path, n1) is True
    assert ContainsNode(path, n3) is False

    print("All path tests passed!")

test_path_functions()