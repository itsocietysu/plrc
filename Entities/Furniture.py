from collections import OrderedDict

from Entities.Line import Line
from Entities.Point import Point


class Furniture:
    _type = 'furniture'

    def __init__(self, _placement=None, _orientation=Point(0, 0), _t='empty'):
        self.placement = _placement
        self.orientation = _orientation
        self.furniture_type = _t

    def update_placement(self, point, orientation=Point(1, 1)):
        self.placement.point_1 = point
        self.placement.point_2 = Point(point.x + self.placement.point_2.x * orientation.x,
                                       point.y + self.placement.point_2.y * orientation.y)

    def reorientation(self, orientation):
        self.orientation = orientation
        self.placement.point_2.x *= self.orientation.x
        self.placement.point_2.y *= self.orientation.y

    def to_dict(self):
        return OrderedDict([('type', Furniture._type),
                            ('placement', self.placement.to_dict()),
                            ('orientation', self.orientation.to_dict()),
                            ('furniture_type', self.furniture_type)])

    def from_dict(self, obj):
        if 'type' in obj and obj['type'] == Furniture._type:
            if 'placement' in obj:
                self.placement = Line().from_dict(obj['placement'])

            if 'orientation' in obj:
                self.orientation = Point().from_dict(obj['orientation'])

            if 'furniture_type' in obj:
                self.furniture_type = obj['furniture_type']

        return self
