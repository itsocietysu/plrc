import numpy as np


class Plan:
    _type = 'plan'

    def __init__(self):
        self.items = []
        self.rooms = []
        self.graph = None

    def add_rooms(self, rooms):
        self.rooms = rooms

    def add_item(self, item):
        self.items.append(item)

    def make_graph(self):
        self.graph = np.zeros((len(self.items), len(self.rooms)))
        for i, item in enumerate(self.items):
            for j, room in enumerate(self.rooms):
                min_distance = 100000
                for wall in room.walls:
                    distance = wall.inner_part.distance_to_point(item.center)
                    if distance < min_distance:
                        min_distance = distance
                self.graph[i][j] = min_distance
