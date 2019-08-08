import copy
import math

from Entities.Furniture import Furniture
from Entities.Line import Line
from Entities.Point import Point
from ImageProcessing.Save import Save
from ImageProcessing.Stage import Stage


SIZE = 20

FURNITURE_TYPE_MAP = {
    'kitchen_sink': Line(Point(0, 0), Point(SIZE, SIZE)),
    'dishwasher': Line(Point(0, 0), Point(SIZE, SIZE)),
    'washer': Line(Point(0, 0), Point(SIZE, SIZE)),
    'refrigerator': Line(Point(0, 0), Point(SIZE, SIZE)),
    'stove': Line(Point(0, 0), Point(SIZE, SIZE)),
    'empty': Line(Point(0, 0), Point(SIZE, SIZE)),
}

FURNITURE_ORIENTATION_MAP = {
    'north': Point(0, -1),
    'south': Point(0, 1),
    'west': Point(-1, 0),
    'east': Point(1, 0),
    'north-west': Point(-1, -1),
    'south-west': Point(-1, 1),
    'north-east': Point(1, -1),
    'south-east': Point(1, 1),
}

D = 5


# TODO
def check_bad_zones():
    return


def simple_placement(furniture, start_point, placement_orientation, len_x, len_y, delta=0):
    if len_x > len_y:
        start_point.x += placement_orientation.x * delta
    else:
        start_point.y += placement_orientation.y * delta
    p = copy.deepcopy(start_point)
    # update start point
    if len_x > len_y:
        start_point.x += placement_orientation.x * furniture.placement.point_2.x
        start_point.y += placement_orientation.y * furniture.placement.point_1.y
    else:
        start_point.x += placement_orientation.x * furniture.placement.point_1.x
        start_point.y += placement_orientation.y * furniture.placement.point_2.y
    # point 1
    p.x += placement_orientation.x * furniture.placement.point_1.x
    p.y += placement_orientation.x * furniture.placement.point_1.y
    furniture.placement.point_1.x = p.x
    furniture.placement.point_1.y = p.y
    # point 2
    p.x += placement_orientation.x * furniture.placement.point_2.x
    p.y += placement_orientation.x * furniture.placement.point_2.y
    furniture.placement.point_2.x = p.x
    furniture.placement.point_2.y = p.y


def place_furniture(furniture, room):
    walls = room.walls
    delta = 3
    min_wall_len = 473
    angles = []

    for idx, wall in enumerate(walls):
        # Definition of first wall
        cur_wall = wall
        # Definition of second wall
        next_wall = walls[(idx + 1) % len(walls)]
        if ((math.fabs(cur_wall.inner_part.point_2.x - next_wall.inner_part.point_2.x) < delta) and
            (math.fabs(cur_wall.inner_part.point_2.y - next_wall.inner_part.point_2.y) > delta)) \
                or \
                ((math.fabs(cur_wall.inner_part.point_2.y - next_wall.inner_part.point_2.y) < delta) and
                 (math.fabs(cur_wall.inner_part.point_2.x - next_wall.inner_part.point_2.x) > delta)):
            angles.append(cur_wall.inner_part.point_2)

    nw_angle = room.zones[0].points[0]

    for a in angles:
        nw_angle.x = min(nw_angle.x, a.x)
        nw_angle.y = min(nw_angle.y, a.y)

    ne_angle = Point()
    sw_angle = Point()
    for idx, a in enumerate(angles):
        if ((a.x - angles[(idx + 1) % len(angles)].x) < delta) and (
                (a.y - angles[(idx + 1) % len(angles)].y) < delta):
            if idx == 0:
                sw_angle = angles[(idx + 1) % len(angles)]
                ne_angle = angles[-1]
            else:
                sw_angle = angles[(idx + 1) % len(angles)]
                ne_angle = angles[(idx - 1) % len(angles)]
            break

    se_angle = Point()
    for a in angles:
        if a.x >= se_angle.x and a.y >= se_angle.y:
            se_angle.x = a.x
            se_angle.y = a.y

    len_x = math.fabs(nw_angle.x - ne_angle.x)  #
    len_y = math.fabs(nw_angle.y - sw_angle.y)  #

    if len_x >= min_wall_len and len_y >= min_wall_len:

        for f in furniture:
            simple_placement(f, nw_angle, FURNITURE_ORIENTATION_MAP['north-west'], len_x, len_y)
    else:

        furniture_len = 0
        shift = 100
        i = 0
        start_point = copy.deepcopy(nw_angle)
        if len_x >= len_y:

            while i < len(furniture):
                f = furniture[i]
                furniture_len += f.placement.point_2.x
                if furniture_len >= min_wall_len:
                    furniture_len -= f.placement.point_2.x
                    break
                simple_placement(f, start_point, FURNITURE_ORIENTATION_MAP['south-east'], len_x, len_y)
                i += 1

            if i < len(furniture):

                start_point.x = furniture[0].placement.point_1.x
                start_point.y = furniture[0].placement.point_2.y + shift
                while i < len(furniture):
                    f = furniture[i]
                    simple_placement(f, start_point, FURNITURE_ORIENTATION_MAP['south-east'], len_x - furniture_len,
                                     len_y)
                    i += 1
        else:
            while i < len(furniture):
                f = furniture[i]
                furniture_len += f.placement.point_2.y
                if furniture_len < min_wall_len:
                    furniture_len -= f.placement.point_2.y
                    break
                simple_placement(f, nw_angle, FURNITURE_ORIENTATION_MAP['south-east'], len_x, len_y)
                i += 1

                if i <= len(furniture):

                    start_point.x = furniture[0].placement.point_1.x + shift
                    start_point.y = furniture[0].placement.point_2.y
                    while i < len(furniture):
                        f = furniture[i]
                        simple_placement(f, start_point, FURNITURE_ORIENTATION_MAP['south-east'], len_x,
                                         len_y - furniture_len)
                        i += 1
    return furniture


def furniture_angle(room, furniture, size, point):
    d = D
    rect_size = Point(0, 0)
    rect_size.x += (d + size) * 3
    rect_size.y += (d + size) * 4
    rect = Line(point, Point(point.x + rect_size.x, point.y + rect_size.y))
    #for wall in room.walls:
    #    if wall.inner_part.rectangle_intersection(rect):
    #        return None

    empty_box = Point(point.x, point.y)
    furniture[0].update_placement(Point(empty_box.x + d, empty_box.y + size + d))
    furniture[1].update_placement(Point(empty_box.x + d, furniture[0].placement.point_2.y + d))
    furniture[2].update_placement(Point(empty_box.x + d, furniture[1].placement.point_2.y + d))

    furniture[3].update_placement(Point(empty_box.x + size + d, empty_box.y + 2 * d))
    furniture[4].update_placement(Point(furniture[3].placement.point_2.x + d, empty_box.y + 2 * d))

    return furniture


def furniture_line(room, furniture, point):
    d = D
    rect_size = Point(0, 0)
    point.x += d
    point.y -= d
    for f in furniture:
        rect_size.x += d + f.placement.point_2.x
        rect_size.y -= (d + f.placement.point_2.y)
    rect = Line(point, Point(point.x + rect_size.x, point.y + rect_size.y))
    #for wall in room.walls:
    #    if wall.inner_part.rectangle_intersection(rect):
    #        return None
    furniture[0].update_placement(Point(point.x + d, point.y + 2 * d))
    for i in range(1, len(furniture)):
        furniture[i].update_placement(Point(point.x + d, furniture[i - 1].placement.point_2.y + d))
    return furniture


def furniture_placement(parent, furniture, room, size):
    zone = room.zones[0]
    f_line = None
    f_angle = None
    i = 5

    if parent.parameters_file:
        f = parent.parameters_file
        for num in range(0, len(f) - 1):
            if f[num] == '#zone':
                i = f[num + 1]

    point = zone.points[i]
    if not f_line:
        f = copy.deepcopy(furniture)
        f_line = furniture_line(room, f, point)
    if not f_angle:
        f = copy.deepcopy(furniture)
        f_angle = furniture_angle(room, f, size, point)

    return f_line, f_angle


def define_furniture_size(room):
    for o in room.openings:
        if o._type == 'door' and o.placement:
            l = Line(o.placement[0].point_1, o.placement[-1].point_2)
            return 0.5 * l.line_length()


class FurniturePlacement(Stage):
    _name = 'furniture_placement'

    def __init__(self):
        Stage().__init__()

    def process(self, parent):
        self.update_status(Stage.STATUS_RUNNING)

        res = []
        for i, room in enumerate(self.desc):
            new_room = copy.deepcopy(room)
            if room.type == 'kitchen':
                size = define_furniture_size(room)
                furniture = [
                    Furniture(Line(Point(0, 0), Point(size, size)), FURNITURE_ORIENTATION_MAP['north'], 'kitchen_sink'),
                    Furniture(Line(Point(0, 0), Point(size, size)), FURNITURE_ORIENTATION_MAP['north'], 'dishwasher'),
                    Furniture(Line(Point(0, 0), Point(size, size)), FURNITURE_ORIENTATION_MAP['north'], 'washer'),
                    Furniture(Line(Point(0, 0), Point(size, size)), FURNITURE_ORIENTATION_MAP['north'], 'stove'),
                    Furniture(Line(Point(0, 0), Point(size, size)), FURNITURE_ORIENTATION_MAP['north'], 'refrigerator')]
                f_line, f_angle = furniture_placement(parent, furniture, new_room, size)
                if f_line:
                    new_room.furniture = f_line
            new_room.walls = room.walls
            new_room.openings = room.openings
            res.append(new_room)
        Save().save(parent.out_dir, 'furniture_%i' % 1, res)

        res = []
        for i, room in enumerate(self.desc):
            new_room = copy.deepcopy(room)
            if room.type == 'kitchen':
                size = define_furniture_size(room)
                furniture = [
                    Furniture(Line(Point(0, 0), Point(size, size)), FURNITURE_ORIENTATION_MAP['north'], 'kitchen_sink'),
                    Furniture(Line(Point(0, 0), Point(size, size)), FURNITURE_ORIENTATION_MAP['north'], 'dishwasher'),
                    Furniture(Line(Point(0, 0), Point(size, size)), FURNITURE_ORIENTATION_MAP['north'], 'washer'),
                    Furniture(Line(Point(0, 0), Point(size, size)), FURNITURE_ORIENTATION_MAP['north'], 'stove'),
                    Furniture(Line(Point(0, 0), Point(size, size)), FURNITURE_ORIENTATION_MAP['north'], 'refrigerator')]
                f_line, f_angle = furniture_placement(parent, furniture, new_room, size)
                if f_angle:
                    new_room.furniture = f_angle

            new_room.walls = room.walls
            new_room.openings = room.openings
            res.append(new_room)
        Save().save(parent.out_dir, 'furniture_%i' % 2, res)

        self.desc = res
        self.update_status(Stage.STATUS_SUCCEEDED)
