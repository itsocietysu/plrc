from collections import OrderedDict

from Entities.Line import Line

class Window:
    _type = 'window'

    def __init__(self, _placement=None):
        self.placement = _placement

    def to_dict(self):
        return OrderedDict([('type', Window._type),
                            ('placement', self.placement.to_dict())])

    def from_dict(self, obj):
        if 'type' in obj and obj['type'] == Window._type and 'placement' in obj:
            self.placement = Line().from_dict(obj['placement'])

        return self
