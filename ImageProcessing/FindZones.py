import copy
import math

from Entities.Point import Point
from Entities.Line import Line
from Entities.Zone import Zone
from ImageProcessing.Stage import Stage


class FindZones(Stage):
    _name = 'finding_zones'

    def __init__(self):
        Stage().__init__()

    def process(self, parent):
        self.update_status(Stage.STATUS_RUNNING)

        res = []
        for i, room in enumerate(self.desc):
            new_room = copy.deepcopy(room)
            if room.type == 'kitchen':
                zones = self.find_zones(new_room)
                if zones:
                    for z in zones:
                        new_room.zones.append(z)
            res.append(new_room)
        self.desc = res
        self.update_status(Stage.STATUS_SUCCEEDED)

    def find_zones(self, room):
        zones = []

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

        for idx, o in enumerate(openings):
            if o._type == 'door':
                if len(o.placement):
                    placement = Line(o.placement[0].point_1, o.placement[-1].point_2)
                else:
                    continue
                z1 = Zone()
                z2 = Zone()
                delta = 3
                shift = 60
                # down
                if (math.fabs(placement.point_1.y - placement.point_2.y) < delta) and \
                        (placement.point_1.x < placement.point_2.x):
                    z1.points.append(placement.point_1)
                    z1.points.append(placement.point_2)
                    z1.points.append(Point(placement.point_2.x, placement.point_2.y + shift))
                    z1.points.append(Point(placement.point_1.x, placement.point_1.y + shift))
                    z1.zone_type = 'bad_zone'

                    z2.points.append(placement.point_1)
                    z2.points.append(placement.point_2)
                    z2.points.append(Point(placement.point_2.x, placement.point_2.y - shift))
                    z2.points.append(Point(placement.point_1.x, placement.point_1.y - shift))
                    z2.zone_type = 'bad_zone'

                    zones.append(z1)
                    zones.append(z2)

                # up
                if (math.fabs(placement.point_1.y - placement.point_2.y) < delta) and \
                        (placement.point_1.x > placement.point_2.x):
                    z1.points.append(placement.point_1)
                    z1.points.append(placement.point_2)
                    z1.points.append(Point(placement.point_2.x, placement.point_2.y - shift))
                    z1.points.append(Point(placement.point_1.x, placement.point_1.y - shift))
                    z1.zone_type = 'bad_zone'

                    z2.points.append(placement.point_1)
                    z2.points.append(placement.point_2)
                    z2.points.append(Point(placement.point_2.x, placement.point_2.y + shift))
                    z2.points.append(Point(placement.point_1.x, placement.point_1.y + shift))
                    z2.zone_type = 'bad_zone'
                    zones.append(z1)
                    zones.append(z2)
                # left
                if (placement.point_1.y < placement.point_2.y) and \
                        (math.fabs(placement.point_1.x - placement.point_2.x) < delta):
                    z1.points.append(placement.point_1)
                    z1.points.append(placement.point_2)
                    z1.points.append(Point(placement.point_2.x + shift, placement.point_2.y))
                    z1.points.append(Point(placement.point_1.x + shift, placement.point_1.y))
                    z1.zone_type = 'bad_zone'

                    z2.points.append(placement.point_1)
                    z2.points.append(placement.point_2)
                    z2.points.append(Point(placement.point_2.x - shift, placement.point_2.y))
                    z2.points.append(Point(placement.point_1.x - shift, placement.point_1.y))
                    z2.zone_type = 'bad_zone'
                    zones.append(z1)
                    zones.append(z2)
                # right
                if (placement.point_1.y > placement.point_2.y) and \
                        (math.fabs(placement.point_1.x - placement.point_2.x) < delta):
                    z1.points.append(placement.point_1)
                    z1.points.append(placement.point_2)
                    z1.points.append(Point(placement.point_2.x - shift, placement.point_2.y))
                    z1.points.append(Point(placement.point_1.x - shift, placement.point_1.y))
                    z1.zone_type = 'bad_zone'
                    z2.points.append(placement.point_1)
                    z2.points.append(placement.point_2)
                    z2.points.append(Point(placement.point_2.x + shift, placement.point_2.y))
                    z2.points.append(Point(placement.point_1.x + shift, placement.point_1.y))
                    z2.zone_type = 'bad_zone'
                    zones.append(z1)
                    zones.append(z2)

        return zones
