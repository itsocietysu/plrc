import copy
import numpy as np

from ImageProcessing.Stage import Stage

from Entities.Line import Line

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
        blank = np.zeros((parent.height, parent.width), np.uint8)
        for i, room in enumerate(self.img):
            render_room(blank, room, gray=True)
            new_room = copy.deepcopy(room)
            for opening in self.desc.openings:
                new_item = self.find_opening_place(new_room.walls, opening)
                if new_item:
                    new_room.openings.append(new_item)
                render_room(blank, new_room)
            res.append(new_room)
        self.desc = res
        self.update_status(Stage.STATUS_SUCCEEDED)

    def find_opening_place(self, walls, opening):
        shift = 0
        if opening._type == 'door':
            shift = OpeningPlacement.WIDER

        p1 = opening.placement.point_1
        p2 = opening.placement.point_2

        _sx = int(min(p1.x, p2.x)) - shift
        _ex = int(max(p1.x, p2.x)) + shift
        _sy = int(min(p1.y, p2.y)) - shift
        _ey = int(max(p1.y, p2.y)) + shift

        points = []
        points.append(Point(_sx, _sy))
        points.append(Point(_sx, _ey))
        points.append(Point(_ex, _ey))
        points.append(Point(_ex, _sy))

        lines = []
        lines.append(Line(points[0], points[1]))
        lines.append(Line(points[1], points[2]))
        lines.append(Line(points[2], points[3]))
        lines.append(Line(points[3], points[0]))

        intersection_points = []
        for wall in walls:
            for line in lines:
                intersection = wall.inner_part.segment_intersection(line)

                if type(intersection) == Line:
                    intersection_points.append(intersection.point_1)
                    intersection_points.append(intersection.point_2)

                if type(intersection) == Point:
                    intersection_points.append(intersection)

                if len(intersection_points) == 2:
                    new_item = copy.deepcopy(opening)
                    new_item.placement.point_1 = intersection_points[0]
                    new_item.placement.point_2 = intersection_points[1]
                    return new_item
        return False
