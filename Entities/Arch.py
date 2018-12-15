from collections import OrderedDict

from Entities.Line import Line

class Arch:
    _type = 'arch'

    def __init__(self, _placement=None):
        self.placement = [_placement]

    def to_dict(self):
        placement = [_.to_dict() for _ in self.placement]
        return OrderedDict([('type', Arch._type),
                            ('placement', placement)])

    def from_dict(self, obj):
        if 'type' in obj and obj['type'] == Arch._type and 'placement' in obj:
            self.placement = [Line().from_dict(_) for _ in obj['placement']]

        return self
