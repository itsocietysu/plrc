from collections import OrderedDict

from Entities.Line import Line

WALL_TYPE_MAP = {
    'wall':         'wall',
    'bearing_wall': 'bearing_wall',
    'outer_wall':   'outer_wall',
    'none': 'none'
}


class Wall:
    _type = 'wall'

    def __init__(self, _inner_part=None, _outer_part=None):
        self.inner_part = _inner_part
        self.wall_type = None
        self.size = None

    def to_dict(self):
        return OrderedDict([('type', self._type),
                            ('wall_type', self.wall_type),
                            ('inner_part', self.inner_part.to_dict()),
                            ('size', self.size)])

    def from_dict(self, obj):
        if 'type' in obj and obj['type'] == Wall._type and 'inner_part' in obj:
            self.inner_part = Line().from_dict(obj['inner_part'])
            self.wall_type = obj['wall_type']
            self.size = obj['size']

        return self
