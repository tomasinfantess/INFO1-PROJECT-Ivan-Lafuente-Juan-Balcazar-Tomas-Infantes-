from navPoint import NavPoint
from navSegment import NavSegment
from navAirport import NavAirport
from navPoint import AddNavNeighbor

class AirSpace:
    def __init__(self):
        self.nav_points = []
        self.nav_segments = []
        self.nav_airports = []

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