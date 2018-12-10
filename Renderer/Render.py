import cv2
import math

from Entities.Point import Point

COLOR_MAP = {
    'door': (0, 255, 0),
    'balcony_door': (0, 255, 0),
    'balcony_wall': (100, 50, 200),
    'window': (255, 0, 0),
    'vent_channel': (255, 255, 0),
    'wall': (100, 0, 100),
    'outer_wall': (0, 0, 255),
    'bearing_wall': (0, 0, 200),

    'none': (100, 100, 100),

    'water_pipes': (255, 255, 3),
    'toilet': (255, 255, 10),
    'bathroom': (255, 255, 20),
    'shower_cabin': (255, 255, 30),
    'sink': (255, 255, 40),
    'washer': (255, 255, 70),
    'storeroom': (255, 255, 80),

    'arch': (0, 255, 255),

    'kitchen_sink': (255, 255, 50),
    'dishwasher': (255, 0, 150),
    'stove': (0, 0, 255),
    'refrigerator': (255, 0, 0),
}


def render_room(img, room, line_w=1, shift=Point(0, 0), scale=1, gray=False):
    def tc(c):
        if gray:
            return (c[0] + c[1] + c[2]) / 3
        return c

    if room:
        for wall in room.walls:
            p1 = wall.inner_part.point_1.mult(scale).add(shift).int_tuple()
            p2 = wall.inner_part.point_2.mult(scale).add(shift).int_tuple()

            cv2.line(img, p1, p2, tc(COLOR_MAP[wall.wall_type]), line_w)
            

        for o in room.openings:
            for p in o.placement:
                p1 = p.point_1.mult(scale).add(shift).int_tuple()
                p2 = p.point_2.mult(scale).add(shift).int_tuple()

                if o._type == 'item':
                    if o.item_type == 'test' or o.item_type == 'test2':
                        continue
                    cv2.rectangle(img, p1, p2, tc(COLOR_MAP[o.item_type]), line_w)
                else:
                    cv2.line(img, p1, p2, tc(COLOR_MAP[o._type]), line_w)

        for f in room.furniture:
            p1 = f.placement.point_1.mult(scale).add(shift).int_tuple()
            p2 = f.placement.point_2.mult(scale).add(shift).int_tuple()

            if f._type == 'furniture':
                if f.furniture_type == 'stove':
                    cv2.rectangle(img, p1, p2, tc(COLOR_MAP[f.furniture_type]), line_w)
                    cv2.line(img, p1, p2, tc(COLOR_MAP[f.furniture_type]), line_w)
                if f.furniture_type == 'dishwasher':
                    cv2.rectangle(img, p1, p2, tc(COLOR_MAP[f.furniture_type]), line_w)
                    cv2.line(img, Point(p1[0], p2[1]).int_tuple(), Point(p2[0], p1[1]).int_tuple(),
                             tc(COLOR_MAP[f.furniture_type]), line_w)
                if f.furniture_type == 'refrigerator':
                    cv2.line(img, p1, p2, tc(COLOR_MAP[f.furniture_type]), line_w)
                    cv2.line(img, Point(p1[0], p2[1]).int_tuple(), Point(p2[0], p1[1]).int_tuple(),
                             tc(COLOR_MAP[f.furniture_type]), line_w)
                    cv2.rectangle(img, p1, p2, tc(COLOR_MAP[f.furniture_type]), line_w)
                if f.furniture_type == 'kitchen_sink':
                    cv2.rectangle(img, p1, p2, tc(COLOR_MAP[f.furniture_type]), line_w)
                    r = int(math.fabs(p2[1] - p1[1]) / 2)
                    center = (int((p2[0] + p1[0]) / 2), int((p2[1] + p1[1]) / 2))
                    cv2.circle(img, center, r, tc(COLOR_MAP[f.furniture_type]), line_w)
                else:
                    cv2.rectangle(img, p1, p2, tc(COLOR_MAP[f.furniture_type]), line_w)
    return img
