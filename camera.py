from haversine import haversine

class Camera:
    def __init__(self, site_id, enforcement, location, direction, speed, coords, distance=None):
        self.site_id = site_id
        self.enforcement = enforcement
        self.location = location
        self.direction = direction
        self.speed = speed
        self.coords = coords
        self.distance = distance

    def refresh(self, position):
        self.distance = haversine(position, self.coords)

    def get_distance(self):
        return self.distance

    def __lt__(self, other):
        return self.distance < other.distance

    def __repr__(self):
        s = """Site {site}:\t{location} ({direction})
        \tPosted speed: {speed}
        \tGPS Coordinates: {coords}
        \tApproximate distance away: {distance} kilometres\n
        """.format(
            site = self.site_id,
            location = self.location,
            direction = self.direction,
            speed = self.speed,
            coords = self.coords,
            distance = "%.3f" % self.distance
        )

        return s