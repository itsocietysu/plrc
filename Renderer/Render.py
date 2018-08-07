import cv2

from Entities.Point import Point

COLOR_MAP = {
    'door': (0, 255, 0),
    'balcony_door': (0, 255, 0),
    'balcony_wall': (100, 50, 200),
    'window': (255, 0, 0),
    'vent_channel': (255, 255, 0),
    'wall': (0, 0, 255)
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

            cv2.line(img, p1, p2, tc(COLOR_MAP[wall._type]), line_w)

        for o in room.openings:
            p1 = o.placement.point_1.mult(scale).add(shift).int_tuple()
            p2 = o.placement.point_2.mult(scale).add(shift).int_tuple()

            cv2.line(img, p1, p2, tc(COLOR_MAP[o._type]), line_w)

    return img