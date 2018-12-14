import copy

from ImageProcessing.Stage import Stage

from Entities.Line import Line

from Entities.Point import Point

"""Binarize image and remove basical noize"""
class OpeningPlacement(Stage):
    _name = 'opening_placement'

    WIDER = -5

    def __init__(self):
        Stage().__init__()

    def process(self, parent):
        """smooth the data"""
        self.parent = parent
        res = []
        for i, room in enumerate(self.img):
            new_room = copy.deepcopy(room)
            for opening in self.desc.openings:
                new_item = self.find_opening_place(new_room.walls, opening)
                if new_item:
                    new_room.openings.append(new_item)
            res.append(new_room)
        self.desc = res
        self.update_status(Stage.STATUS_SUCCEEDED)

    def find_opening_place(self, walls, opening):

        new_item = copy.deepcopy(opening)

        p1 = opening.placement[0].point_1
        p2 = opening.placement[0].point_2

        new_item.placement = []

        shift = OpeningPlacement.WIDER
        _sx = int(min(p1.x, p2.x)) - shift
        _ex = int(max(p1.x, p2.x)) + shift
        _sy = int(min(p1.y, p2.y)) - shift
        _ey = int(max(p1.y, p2.y)) + shift

        rect = Line(Point(_sx, _sy), Point(_ex, _ey))

        if opening._type == 'item' or opening._type == 'arch':
            new_item.placement.append(rect)
            if new_item.item_type == 'vent_channel' or new_item.item_type == 'water_pipes':
                self.parent.plan.add_item(new_item)

        else:
            for wall in walls:
                intersection = wall.inner_part.rectangle_intersection(rect)
                if intersection:
                    new_item.placement.append(intersection)
                    continue

        return new_item
