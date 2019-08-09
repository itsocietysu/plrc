from collections import OrderedDict

from Entities.Arch import Arch
from Entities.Door import Door
from Entities.Item import Item
from Entities.Wall import Wall
from Entities.Window import Window


class Room:
    _type = 'room'
    _processor_map = {
        'window': lambda _: Window().from_dict(_),
        'door': lambda _: Door().from_dict(_),
        'wall': lambda _: Wall().from_dict(_),
        'item': lambda _: Item().from_dict(_),

        'arch': lambda _: Arch().from_dict(_),

    }

    def __init__(self, _walls=[], _openings=[], _type=None):
        self.walls = _walls
        self.openings = _openings
        self.type = _type

    def to_dict(self):
        walls = [_.to_dict() for _ in self.walls]
        openings = [_.to_dict() for _ in self.openings]

        return OrderedDict([('walls', walls),
                            ('openings', openings),
                            ('type', self.type)])

    def get_bounding_rect(self):
        sx, sy, ex, ey = 10000, 10000, 0, 0
        for w in self.walls:
            l = w.inner_part
            sx = min(sx, l.point_1.x)
            sy = min(sy, l.point_2.y)
            ex = max(ex, l.point_1.x)
            ey = max(ey, l.point_2.y)
        return sx, sy, ex, ey

    def from_dict(self, obj):

        if 'walls' in obj:
            self.walls = [Room._processor_map[_['type']](_) for _ in obj['walls'] if _['type'] in Room._processor_map]

        if 'openings' in obj:
            self.openings = [Room._processor_map[_['type']](_) for _ in obj['openings'] if
                             _['type'] in Room._processor_map]

        if 'type' in obj:
            self.type = obj['type']

        return self
