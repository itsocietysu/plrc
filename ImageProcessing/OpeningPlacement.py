import copy

from ImageProcessing.Stage import Stage

from Entities.Line import Line

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
            new_room = copy.deepcopy(room)
            for opening in self.desc.openings:
                new_items = self.find_opening_place(new_room.walls, opening)
                if new_items:
                    for new_item in new_items:
                        new_room.openings.append(new_item)
            res.append(new_room)
        self.desc = res
        self.update_status(Stage.STATUS_SUCCEEDED)

    def find_opening_place(self, walls, opening):

        def item_in_wall(placement):
            for w in walls:
                if type(placement.segment_intersection(w.inner_part)) == Line:
                    return True
            return False

        new_items = []
        shift = 0
        if opening._type != 'window':
            shift = OpeningPlacement.WIDER

        p1 = opening.placement.point_1
        p2 = opening.placement.point_2

        _sx = int(min(p1.x, p2.x)) - shift
        _ex = int(max(p1.x, p2.x)) + shift
        _sy = int(min(p1.y, p2.y)) - shift
        _ey = int(max(p1.y, p2.y)) + shift

        p = [Point(_sx, _sy), Point(_sx, _ey), Point(_ex, _ey), Point(_ex, _sy)]
        lines = [Line(p[0], p[1]), Line(p[1], p[2]), Line(p[2], p[3]), Line(p[3], p[0])]

        if opening._type == 'item':
            new_item = copy.deepcopy(opening)
            new_item.placement.point_1 = Point(_sx, _sy)
            new_item.placement.point_2 = Point(_ex, _ey)
            new_items.append(new_item)

        else:
            intersection_points = []
            for wall in walls:
                intersection = wall.inner_part.rectangle_intersection(Line(p[0], p[2]))
                if intersection:
                    if item_in_wall(intersection):
                        new_item = copy.deepcopy(opening)
                        new_item.placement = intersection
                        new_items.append(new_item)
                    continue

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
                        new_items.append(new_item)

        return new_items
