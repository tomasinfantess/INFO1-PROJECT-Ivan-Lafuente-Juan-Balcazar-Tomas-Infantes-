class Path:
    def __init__(self, nodes=None, cost=0.0):
        self.nodes = nodes if nodes is not None else []
        self.cost = cost

def AddNodeToPath(path, node, cost):
    """
    Adds a node to the path and updates the total cost.
    Returns the new path.
    """
    new_path = Path(path.nodes.copy(), path.cost)
    new_path.nodes.append(node)
    new_path.cost += cost
    return new_path

def ContainsNode(path, node):
    """
    Returns True if the node is in the path, False otherwise.
    """
    return node in path.nodes

def CostToNode(path, node):
    """
    Returns the total cost from the origin of the path to the node.
    Returns -1 if the node is not in the path.
    """
    if node not in path.nodes:
        return -1
    return path.cost

def PlotPath(graph, path):
    """
    Plots the path in the graph.
    """
    # Implementación para mostrar el camino en el gráfico.
    pass

def DijkstraShortestPath(graph, origin_name, destination_name):
    """Find shortest path using Dijkstra's algorithm"""
    # Implementation of Dijkstra's algorithm
    pass