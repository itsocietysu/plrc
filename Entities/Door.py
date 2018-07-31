from collections import OrderedDict

from Entities.Line import Line

class Door:
    _type = 'door'

    def __init__(self, _placement=None, _opened=None):
        self.placement = _placement
        self.opened = _opened

    def to_dict(self):
        if self.opened == None:
            self.opened = self.placement

        return OrderedDict([('type', Door._type),
                            ('placement', self.placement.to_dict()),
                            ('opened', self.opened.to_dict())])

    def from_dict(self, obj):
        if 'type' in obj and obj['type'] == Door._type:
            if 'placement' in obj:
                self.placement = Line().from_dict(obj['placement'])

            if 'opened' in obj:
                self.opened = Line().from_dict(obj['opened'])

        return self
