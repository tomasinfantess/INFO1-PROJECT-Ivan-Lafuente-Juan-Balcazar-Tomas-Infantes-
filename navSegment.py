class NavSegment:
    def __init__(self, origin_number, destination_number, distance):
        self.origin_number = origin_number
        self.destination_number = destination_number
        self.distance = distance

    def __str__(self):
        return f"{self.origin_number}->{self.destination_number} ({self.distance} km)"