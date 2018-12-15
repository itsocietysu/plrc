from collections import OrderedDict

from Entities.Line import Line
from Entities.Point import Point

class Item:
    _type = 'item'

    def __init__(self, _placement=None, t=None):
        self.placement = [_placement]
        self.item_type = t
        if _placement:
            self.center = Point(_placement.point_1.x + abs(_placement.point_1.x - _placement.point_2.x),
                                _placement.point_1.y + abs(_placement.point_1.y - _placement.point_2.y))

    def to_dict(self):
        return OrderedDict([('type', Item._type),
                            ('item_type', self.item_type),
                            ('placement', [_.to_dict() for _ in self.placement])])

    def from_dict(self, obj):
        if 'type' in obj and obj['type'] == Item._type and 'placement' in obj:
            self.placement = [Line().from_dict(_) for _ in obj['placement']]
            self.item_type = obj['item_type']

        return self
