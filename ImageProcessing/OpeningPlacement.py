import copy
import numpy as np

from Entities.Room import Room
from Entities.Line import Line
from Entities.Point import Point
from Renderer.Render import render_room
from ImageProcessing.Stage import Stage


class OpeningPlacement(Stage):
    """Place openings in rooms"""
    _name = 'opening_placement'

    WIDER = -11

    def __init__(self):
        Stage().__init__()
        self.shape = ()

    def process(self, parent):
        self.update_status(Stage.STATUS_RUNNING)

        self.shape = (parent.height, parent.width, 3)

        res = []
        for i, room in enumerate(self.img):
            new_room = copy.deepcopy(room)
            for opening in self.desc.openings:
                new_item = self.find_opening_place(new_room, opening)
                if new_item:
                    new_room.openings.append(new_item)
            res.append(new_room)

        for opening in self.desc.openings:
            if opening._type == 'item' or opening._type == 'arch':
                new_item, rect = self.get_opening_rect(opening)

                if new_item.item_type == 'vent_channel' or new_item.item_type == 'water_pipes':
                    parent.plan.add_item(new_item)

        self.desc = res
        self.update_status(Stage.STATUS_SUCCEEDED)

    def get_opening_rect(self, opening, window_shift=-3, door_shift=None):
        new_item = copy.deepcopy(opening)

        p1 = opening.placement[0].point_1
        p2 = opening.placement[0].point_2

        new_item.placement = []
        if not window_shift:
            shift = -((self.shape[1] + self.shape[0]) / 2) / ((abs(p1.x - p2.x) + abs(p1.y - p2.y)) / 2) / 10
        else:
            shift = window_shift

        if opening._type != 'window':
            shift = OpeningPlacement.WIDER

        if door_shift:
            shift = door_shift

        if opening._type == 'item':
            shift = 0

        _sx = int(min(p1.x, p2.x)) - shift
        _ex = int(max(p1.x, p2.x)) + shift
        _sy = int(min(p1.y, p2.y)) - shift
        _ey = int(max(p1.y, p2.y)) + shift

        rect = Line(Point(_sx, _sy), Point(_ex, _ey))
        return new_item, rect

    def is_curve_window(self, placement, walls):
        line_in_room = []
        count_big_angle = 0
        lenght = 0
        for line in placement:
            for wall in walls:
                if wall.inner_part.distance_to_point(line.point_1) == 0:
                    if line_in_room:
                        angle = line.angle_between(line_in_room[-1])
                        if 15 < angle < 75 or 115 < angle < 165:
                            count_big_angle += 1
                    line_in_room.append(line)
                    lenght += line.line_length()

        if line_in_room:
            distance = Line(line_in_room[0].point_1, line_in_room[-1].point_2)
            if distance.line_length() != 0 and lenght / distance.line_length() > 2 and count_big_angle > 2:
                return True

        return False

    def is_curve_door(self, placement, walls):
        line_in_room = []
        lenght = 0
        for line in placement:
            for wall in walls:
                if wall.inner_part.distance_to_point(line.point_1) == 0:
                    line_in_room.append(line)
                    lenght += line.line_length()

        if line_in_room:
            distance = Line(line_in_room[0].point_1, line_in_room[-1].point_2)
            if distance.line_length() != 0 and lenght / distance.line_length() > 1.1:
                return True

        return False

    def find_opening_place(self, room, opening):
        walls = room.walls

        def find_intersections():
            new_item.placement = []
            for wall in walls:
                intersection = wall.inner_part.rectangle_intersection(rect)
                if intersection:
                    new_item.placement.append(intersection)
                    continue

        new_item, rect = self.get_opening_rect(opening)
        if opening._type == 'item' or opening._type == 'arch':
            new_item.placement.append(rect)
            return new_item
        else:
            find_intersections()

        if opening._type == 'window' and new_item.placement and self.is_curve_window(new_item.placement, walls):
            new_item, rect = self.get_opening_rect(opening, window_shift=-25)
            find_intersections()

        if opening._type == 'door' and new_item.placement and self.is_curve_door(new_item.placement, walls):
            new_item, rect = self.get_opening_rect(opening, door_shift=-15)
            opening.placement[0] = rect
            find_intersections()

        return new_item

    def visualize_stage(self):
        img = np.zeros(self.shape, np.uint8)
        for r in self.desc:
            img = render_room(img, Room().from_dict(r.to_dict()), line_w=3)
        return img
