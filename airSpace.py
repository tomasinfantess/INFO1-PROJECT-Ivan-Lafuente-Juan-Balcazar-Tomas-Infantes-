from navPoint import NavPoint
from navSegment import NavSegment
from navAirport import NavAirport
from navPoint import AddNavNeighbor

class AirSpace:
    def __init__(self):
        self.nav_points = []
        self.nav_segments = []
        self.nav_airports = []

    def has_segment_between(self, node1, node2):
        for segment in self.nav_segments:
            if (segment.origin_number == node1.number and segment.destination_number == node2.number):
                return True
        return False

    def load_nav_points(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) >= 4:
                    number = int(parts[0])
                    name = parts[1]
                    latitude = float(parts[2])
                    longitude = float(parts[3])
                    self.nav_points.append(NavPoint(number, name, latitude, longitude))

    def load_nav_segments(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) >= 3:
                    origin = int(parts[0])
                    destination = int(parts[1])
                    distance = float(parts[2])
                    self.nav_segments.append(NavSegment(origin, destination, distance))

    def load_nav_airports(self, file_path):
        with open(file_path, 'r') as file:
            current_airport = None
            for line in file:
                line = line.strip()
                if line:
                    if line.isupper() or line.startswith('LE'):  # Airport code detection
                        current_airport = NavAirport(line)
                        self.nav_airports.append(current_airport)
                    elif current_airport:
                        if line.endswith('.D'):  # SID
                            nav_point = self.find_nav_point_by_name(line)
                            if nav_point:
                                current_airport.add_sid(nav_point)
                        elif line.endswith('.A'):  # STAR
                            nav_point = self.find_nav_point_by_name(line)
                            if nav_point:
                                current_airport.add_star(nav_point)

    def find_nav_point_by_number(self, number):
        for point in self.nav_points:
            if point.number == number:
                return point
        return None

    def find_nav_point_by_name(self, name):
        for point in self.nav_points:
            if point.name == name:
                return point
        return None

    def build_neighbors(self):
        for segment in self.nav_segments:
            origin = self.find_nav_point_by_number(segment.origin_number)
            destination = self.find_nav_point_by_number(segment.destination_number)
            if origin and destination:
                AddNavNeighbor(origin, destination)

    def get_airport_by_name(self, name):
        for airport in self.nav_airports:
            if airport.name == name:
                return airport
        return None



    def find_shortest_path_with_avoidances(self, origin_name, destination_name, avoid_nodes=None, avoid_segments=None):
        """Find shortest path while avoiding specified nodes and segments"""
        if avoid_nodes is None:
            avoid_nodes = []
        if avoid_segments is None:
            avoid_segments = []

        # Convert airspace to temporary graph without avoided elements
        temp_graph = Graph()

        # Add nodes except avoided ones
        for point in self.nav_points:
            if point.name not in avoid_nodes:
                x = point.longitude * 10
                y = point.latitude * 10
                AddNode(temp_graph, Node(point.name, x, y))

        # Add segments except avoided ones
        for segment in self.nav_segments:
            origin = self.find_nav_point_by_number(segment.origin_number)
            destination = self.find_nav_point_by_number(segment.destination_number)

            if (origin and destination and
                    origin.name not in avoid_nodes and
                    destination.name not in avoid_nodes and
                    f"{origin.name}_{destination.name}" not in avoid_segments and
                    f"{destination.name}_{origin.name}" not in avoid_segments):
                segment_name = f"{origin.name}_{destination.name}"
                AddSegment(temp_graph, segment_name, origin.name, destination.name)

        # Find path in the temporary graph
        return FindShortestPath(temp_graph, origin_name, destination_name)