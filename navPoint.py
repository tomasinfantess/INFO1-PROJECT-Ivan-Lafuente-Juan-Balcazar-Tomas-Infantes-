class NavPoint:
    def __init__(self, number, name, latitude, longitude):
        self.number = number
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.neighbors = []

    def __str__(self):
        return f"{self.number} {self.name} {self.latitude} {self.longitude}"

def AddNavNeighbor(n1, n2):
    if n2 in n1.neighbors:
        return False
    n1.neighbors.append(n2)
    return True