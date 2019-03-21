class Trap:
    def __init__(self, direction, location, speed):
        self.direction = self.format_direction(direction)
        self.location = location
        self.speed = speed

        self.order = {"Northbound": 1, "Southbound": 2, "Eastbound": 3, "Westbound": 4}
    
    def format_direction(self, direction):
        mappings = {"NB": "Northbound", "EB": "Eastbound", "SB": "Southbound", "WB": "Westbound"}
        return mappings[direction]

    def get_speed(self):
        return self.speed

    def __lt__(self, other):
        return self.order[self.direction] < other.order[other.direction]

    def __repr__(self):
        return "{}\n  {}\n  Posted Speed: {} kilometres\n".format(self.location, self.direction, self.speed)