import matplotlib.pyplot as plt
from segment import Segment
from node import Node, AddNeighbor, Distance
from path import Path, AddNodeToPath, ContainsNode, CostToNode


class Graph:
    def __init__(self):
        self.nodes = []
        self.segments = []


def AddNode(g, n):
    if n in g.nodes:
        return False
    g.nodes.append(n)
    return True


def AddSegment(g, name, origin_name, destination_name):
    origin = None
    destination = None

    for node in g.nodes:
        if node.name == origin_name:
            origin = node
        if node.name == destination_name:
            destination = node

    if origin is None or destination is None:
        return False

    segment = Segment(name, origin, destination)
    g.segments.append(segment)
    AddNeighbor(origin, destination)
    return True


def GetClosest(g, x, y):
    closest = None
    min_distance = float('inf')

    for node in g.nodes:
        distance = ((node.x - x) ** 2 + (node.y - y) ** 2) ** 0.5
        if distance < min_distance:
            min_distance = distance
            closest = node

    return closest


def Plot(g):
    plt.figure(figsize=(8, 6))

    for segment in g.segments:
        plt.plot([segment.origin.x, segment.destination.x],
                 [segment.origin.y, segment.destination.y],
                 'gray', linestyle='-')
        mid_x = (segment.origin.x + segment.destination.x) / 2
        mid_y = (segment.origin.y + segment.destination.y) / 2
        plt.text(mid_x, mid_y, f"{segment.cost:.1f}", fontsize=8)

    for node in g.nodes:
        plt.plot(node.x, node.y, 'ro')
        plt.text(node.x, node.y, node.name, fontsize=10)

    plt.grid(True)
    plt.show()


def PlotNode(g, name_origin):
    origin = None
    for node in g.nodes:
        if node.name == name_origin:
            origin = node
            break

    if origin is None:
        return False

    plt.figure(figsize=(8, 6))

    for node in g.nodes:
        plt.plot(node.x, node.y, 'o', color='gray')
        plt.text(node.x, node.y, node.name, fontsize=10)

    plt.plot(origin.x, origin.y, 'o', color='blue')
    plt.text(origin.x, origin.y, origin.name, fontsize=10)

    for neighbor in origin.neighbors:
        plt.plot(neighbor.x, neighbor.y, 'o', color='green')
        plt.text(neighbor.x, neighbor.y, neighbor.name, fontsize=10)

        plt.plot([origin.x, neighbor.x],
                 [origin.y, neighbor.y],
                 'r-', linewidth=2)

        mid_x = (origin.x + neighbor.x) / 2
        mid_y = (origin.y + neighbor.y) / 2
        plt.text(mid_x, mid_y, f"{((origin.x - neighbor.x) ** 2 + (origin.y - neighbor.y) ** 2) ** 0.5:.1f}",
                 fontsize=8)

    plt.grid(True)
    plt.show()
    return True


def FindShortestPath(g, origin_name, destination_name):
    origin = None
    destination = None

    for node in g.nodes:
        if node.name == origin_name:
            origin = node
        if node.name == destination_name:
            destination = node

    if origin is None or destination is None:
        return None

    paths = []
    initial_path = Path([origin], 0)
    paths.append(initial_path)

    while paths:
        # Find the path with minimum estimated cost
        min_cost = float('inf')
        min_path = None
        min_index = -1

        for i, path in enumerate(paths):
            last_node = path.nodes[-1]
            estimated_cost = path.cost + Distance(last_node, destination)
            if estimated_cost < min_cost:
                min_cost = estimated_cost
                min_path = path
                min_index = i

        if min_path is None:
            break

        current_path = paths.pop(min_index)
        last_node = current_path.nodes[-1]

        if last_node == destination:
            return current_path

        for neighbor in last_node.neighbors:
            if not ContainsNode(current_path, neighbor):
                segment_cost = None
                for segment in g.segments:
                    if segment.origin == last_node and segment.destination == neighbor:
                        segment_cost = segment.cost
                        break

                if segment_cost is not None:
                    new_path = AddNodeToPath(current_path, neighbor, segment_cost)
                    paths.append(new_path)

    return None