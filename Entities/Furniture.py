from collections import OrderedDict

from Entities.Line import Line
from Entities.Point import Point


class Furniture:
    _type = 'furniture'

    def __init__(self, _placement=None, _orientation=None, _t=None):
        self.placement = _placement
        self.orientation = _orientation
        self.furniture_type = _t

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
