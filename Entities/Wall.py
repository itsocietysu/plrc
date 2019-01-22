from collections import OrderedDict

from Entities.Line import Line

class Wall:
    _type = 'wall'
    WALL_TYPE_MAP = {
        'wall': 'wall',
        'bearing_wall': 'bearing_wall',
        'outer_wall': 'outer_wall',
    }

    def __init__(self, _inner_part=None, _outer_part=None):
        self.inner_part = _inner_part
        if _outer_part is None:
            _outer_part = _inner_part

        self.outer_part = _outer_part
        self.wall_type = 'wall'
        self.size = None

    def to_dict(self):
        return OrderedDict([('type', self._type),
                            ('wall_type', self.wall_type),
                            ('inner_part', self.inner_part.to_dict()),
                            ('outer_part', self.outer_part.to_dict())])

    def from_dict(self, obj):
        if 'type' in obj and obj['type'] == Wall._type and 'inner_part' in obj and 'outer_part' in obj:
            self.inner_part = Line().from_dict(obj['inner_part'])
            self.outer_part = Line().from_dict(obj['outer_part'])
            self.wall_type = obj['wall_type']

        return self
