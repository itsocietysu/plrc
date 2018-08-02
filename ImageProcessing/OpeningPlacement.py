import copy
import numpy as np

from ImageProcessing.Stage import Stage

from Renderer.Render import render_room

from Entities.Point import Point

"""Binarize image and remove basical noize"""
class OpeningPlacement(Stage):
    _name = 'opening_placement'

    WIDER = -10

    def __init__(self):
        Stage().__init__()

    def process(self, parent):
        """smooth the data"""
        res = []
        for i, room in enumerate(self.img):
            blank = np.zeros((parent.height, parent.width), np.uint8)
            render_room(blank, room, gray=True)

            new_room = copy.deepcopy(room)
            for opening in self.desc.openings:
                shift = 0
                if opening._type == 'door':
                    shift = OpeningPlacement.WIDER

                p1 = opening.placement.point_1
                p2 = opening.placement.point_2
                _sx = int(min(p1.x, p2.x)) - shift
                _ex = int(max(p1.x, p2.x)) + shift

                _sy = int(min(p1.y, p2.y)) - shift
                _ey = int(max(p1.y, p2.y)) + shift

                rect_img = blank[_sy:_ey, _sx:_ex]

                maskRect = np.where(rect_img != 0)
                maskPts = np.hstack((maskRect[1][:, np.newaxis], maskRect[0][:, np.newaxis]))
                sx, sy, ex, ey = parent.width, parent.height, 0, 0
                if len(maskPts):
                    for _ in maskPts:
                        sx = min(sx, _[0])
                        sy = min(sy, _[1])
                        ex = max(ex, _[0])
                        ey = max(ey, _[1])

                    sy += p1.y - shift
                    sx += p1.x - shift
                    ex += p1.x - shift
                    ey += p1.y - shift

                    new_item = copy.deepcopy(opening)
                    new_item.placement.point_1 = Point(sx, sy)
                    new_item.placement.point_2 = Point(ex, ey)

                    new_room.openings.append(new_item)

            blank = np.zeros((parent.height, parent.width, 3), np.uint8)
            render_room(blank, new_room)

            res.append(new_room)

        self.desc = res
        self.update_status(Stage.STATUS_SUCCEEDED)
