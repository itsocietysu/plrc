from collections import OrderedDict

from Entities.Point import Point

class Line:
    _type = 'line'

    def __init__(self, _pt1=None, _pt2=None):
        self.point_1 = _pt1
        self.point_2 = _pt2

    def translate(self, pt):
        self.point_1.add(pt)
        self.point_2.add(pt)

        return self

    def scale(self, a):
        self.point_1.mult(a)
        self.point_2.mult(a)

        return self

    def to_dict(self):
        return OrderedDict([('type', Line._type), ('point_1', self.point_1.to_dict()), ('point_2', self.point_2.to_dict())])

    def from_dict(self, obj):
        if 'type' in obj and obj['type'] == Line._type and 'point_1' in obj and 'point_2' in obj:
            self.point_1 = Point().from_dict(obj['point_1'])
            self.point_2 = Point().from_dict(obj['point_2'])

        return self
