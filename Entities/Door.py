from collections import OrderedDict

from Entities.Line import Line


class Door:
    _type = 'door'

    def __init__(self, _placement=None, t=None):
        self.placement = [_placement]

    def to_dict(self):
        placement = [_.to_dict() for _ in self.placement]
        return OrderedDict([('type', Door._type),
                            ('placement', placement)])

    def from_dict(self, obj):
        if 'type' in obj and obj['type'] == Door._type:
            if 'placement' in obj:
                self.placement = [Line().from_dict(_) for _ in obj['placement']]

        return self
