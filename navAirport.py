class NavAirport:
    def __init__(self, name):
        self.name = name
        self.sids = []  # List of NavPoints
        self.stars = []  # List of NavPoints

    def add_sid(self, nav_point):
        self.sids.append(nav_point)

    def add_star(self, nav_point):
        self.stars.append(nav_point)

    def __str__(self):
        return f"{self.name} (SIDs: {len(self.sids)}, STARs: {len(self.stars)})"