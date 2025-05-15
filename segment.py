class Segment:
    def __init__(self, name, origin, destination):
        self.name = name
        self.origin = origin
        self.destination = destination
        self.cost = ((origin.x - destination.x)**2 + (origin.y - destination.y)**2)**0.5