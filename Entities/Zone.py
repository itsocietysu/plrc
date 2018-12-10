from collections import OrderedDict

from Entities.Line import Line
from Entities.Point import Point


class Zone:
    _type = 'zone'

    def __init__(self, _points=[], _t=None, _sides_num=0):
        self.points = _points
        self.zone_type = _t
        self.sides_num = _sides_num

    def to_dict(self):
        return OrderedDict([('type', Zone._type),
                            ('sides_num', self.sides_num),
                            ('zone_type', self.zone_type),
                            ('points', [p.to_dict() for p in self.points]),
                            ])

    def from_dict(self, obj):
        if 'type' in obj and obj['type'] == Zone._type and 'points' in obj:

            if 'points' in obj:
                for p in obj['points']:
                    self.points.append(Point().from_dict(p))

            if 'sides_num' in obj:
                self.sides_num = obj['sides_num']

            if 'zone_type' in obj:
                self.zone_type = obj['zone_type']

        return self
