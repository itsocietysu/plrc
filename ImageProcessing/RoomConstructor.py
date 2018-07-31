import cv2
import numpy as np
import json

from Entities.Room import Room
from Entities.Wall import Wall
from Entities.Line import Line
from Entities.Point import Point

from ImageProcessing.Stage import Stage


"""Binarize image and remove basical noize"""
class RoomConstructor(Stage):
    _name = 'room_constructor'

    def __init__(self):
        Stage().__init__()

    def process(self, parent):
        """smooth the data"""
        res = []
        for i, cnt in enumerate(self.img):
            room = Room()
            l = len(cnt) - 1
            prev = cnt[l]
            room.walls = []

            for curr in cnt:
                wall = Wall(Line(Point(prev[0][0], prev[0][1]), Point(curr[0][0], curr[0][1])))
                room.walls.append(wall)
                prev = curr

            with open('%d.json' % i, 'wt') as fp:
               json.dump(room.to_dict(), fp, indent=2)

            res.append(room)

        self.img = res
        self.desc = self.desc
        self.update_status(Stage.STATUS_SUCCEEDED)
