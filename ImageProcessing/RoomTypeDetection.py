
from ImageProcessing.Stage import Stage
from Entities.Plan import Plan
import numpy as np

class RoomTypeDetection(Stage):
    _name = 'room_type_detection'

    def __init__(self):
        Stage().__init__()

    def process(self, parent):

        self.update_status(Stage.STATUS_RUNNING)

        self.plan = parent.plan
        self.plan.add_rooms(self.desc)
        self.plan.make_graph()
        self.detect()

        self.desc = parent.desc
        self.update_status(Stage.STATUS_SUCCEEDED)

    def detect(self):
        items = self.plan.graph.shape[0]
        rooms = self.plan.graph.shape[1]

        min_d = []
        for i in range(0, items):
            distances = self.plan.graph[i]
            min_d.append((i, min(distances)))

        closest = sorted(min_d, key=lambda _: _[1])[0]

        i = closest[0]
        min_d = closest[1]
        for j in range(0, rooms):
            if self.plan.graph[i][j] == min_d:
                for num, _ in enumerate(self.desc):
                    if num == j:
                        _.type = 'kitchen'
                        return


