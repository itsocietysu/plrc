import copy
import math
import numpy as np
from ImageProcessing.Stage import Stage
from Entities.Point import Point
from Entities.Line import Line
from Entities.Zone import Zone


class FindZones(Stage):
    _name = 'finding_zones'

    def __init__(self):
        Stage().__init__()

    def process(self, parent):
        """smooth the data"""
        res = []
        for i, room in enumerate(self.desc):
            new_room = copy.deepcopy(room)
            if i == 4: # !!!DEBUG!!!
                zones = self.find_zones(new_room)
                if zones:
                    for z in zones:
                        new_room.zones.append(z)
            res.append(new_room)
        self.desc = res
        self.update_status(Stage.STATUS_SUCCEEDED)

    def find_zones(self, room):
        zones = []
        """
           Идём по списку стен, рассматривая их попарно.
           если в некоторый момент некоторое delta превышено,
           то фиксируем точку поворота.
           Доходим до состыковки с начальной точки, нулевая зона построена
        """
        walls = room.walls
        openings = room.openings
        zone_0 = Zone()

        for idx, wall in enumerate(walls):
            # The very first point is always included
            if idx == 0:
                zone_0.points.append(wall.inner_part.point_1)
            # Definition of first wall
            cur_wall = wall
            # Definition of second wall
            next_wall = walls[(idx + 1) % len(walls)]

            zone_0.points.append(cur_wall.inner_part.point_2)
            zone_0.sides_num += 1

        zone_0.zone_type = 'ok_zone'
        if zone_0.points[0].x == zone_0.points[-1].x and zone_0.points[0].y == zone_0.points[-1].y:
            del zone_0.points[-1]
        zones.append(zone_0)
        """
           Проходим по всем openings.
           Проверяем дверь или окно.
           В зависимости от пред.шага отделяем зону.
           Добавляем зону в zones
        """

        for idx, o in enumerate(openings):
            if o._type == 'door':
                z1 = Zone()
                z2 = Zone()
                delta = 3
                shift = 60
                # down
                if (math.fabs(o.placement.point_1.y - o.placement.point_2.y) < delta) and \
                        (o.placement.point_1.x < o.placement.point_2.x):
                    z1.points.append(o.placement.point_1)
                    z1.points.append(o.placement.point_2)
                    z1.points.append(Point(o.placement.point_2.x, o.placement.point_2.y + shift))
                    z1.points.append(Point(o.placement.point_1.x, o.placement.point_1.y + shift))
                    z1.zone_type = 'bad_zone'

                    z2.points.append(o.placement.point_1)
                    z2.points.append(o.placement.point_2)
                    z2.points.append(Point(o.placement.point_2.x, o.placement.point_2.y - shift))
                    z2.points.append(Point(o.placement.point_1.x, o.placement.point_1.y - shift))
                    z2.zone_type = 'bad_zone'

                    zones.append(z1)
                    zones.append(z2)

                # up
                if (math.fabs(o.placement.point_1.y - o.placement.point_2.y) < delta) and \
                        (o.placement.point_1.x > o.placement.point_2.x):
                    z1.points.append(o.placement.point_1)
                    z1.points.append(o.placement.point_2)
                    z1.points.append(Point(o.placement.point_2.x, o.placement.point_2.y - shift))
                    z1.points.append(Point(o.placement.point_1.x, o.placement.point_1.y - shift))
                    z1.zone_type = 'bad_zone'

                    z2.points.append(o.placement.point_1)
                    z2.points.append(o.placement.point_2)
                    z2.points.append(Point(o.placement.point_2.x, o.placement.point_2.y + shift))
                    z2.points.append(Point(o.placement.point_1.x, o.placement.point_1.y + shift))
                    z2.zone_type = 'bad_zone'
                    zones.append(z1)
                    zones.append(z2)
                # left
                if (o.placement.point_1.y < o.placement.point_2.y) and \
                        (math.fabs(o.placement.point_1.x - o.placement.point_2.x) < delta):
                    z1.points.append(o.placement.point_1)
                    z1.points.append(o.placement.point_2)
                    z1.points.append(Point(o.placement.point_2.x + shift, o.placement.point_2.y))
                    z1.points.append(Point(o.placement.point_1.x + shift, o.placement.point_1.y))
                    z1.zone_type = 'bad_zone'

                    z2.points.append(o.placement.point_1)
                    z2.points.append(o.placement.point_2)
                    z2.points.append(Point(o.placement.point_2.x - shift, o.placement.point_2.y))
                    z2.points.append(Point(o.placement.point_1.x - shift, o.placement.point_1.y))
                    z2.zone_type = 'bad_zone'
                    zones.append(z1)
                    zones.append(z2)
                # right
                if (o.placement.point_1.y > o.placement.point_2.y) and \
                        (math.fabs(o.placement.point_1.x - o.placement.point_2.x) < delta):
                    z1.points.append(o.placement.point_1)
                    z1.points.append(o.placement.point_2)
                    z1.points.append(Point(o.placement.point_2.x - shift, o.placement.point_2.y))
                    z1.points.append(Point(o.placement.point_1.x - shift, o.placement.point_1.y))
                    z1.zone_type = 'bad_zone'
                    z2.points.append(o.placement.point_1)
                    z2.points.append(o.placement.point_2)
                    z2.points.append(Point(o.placement.point_2.x + shift, o.placement.point_2.y))
                    z2.points.append(Point(o.placement.point_1.x + shift, o.placement.point_1.y))
                    z2.zone_type = 'bad_zone'
                    zones.append(z1)
                    zones.append(z2)
                """
                   Итог: имеем массив зон, каждая из которых представлена списком точек.
                """

        return zones
