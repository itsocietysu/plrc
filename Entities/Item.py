from collections import OrderedDict

from Entities.Line import Line

class Item:
    _type = 'item'

    def __init__(self, _placement=None, t=None):
        self.placement = [_placement]
        self.item_type = t

    def to_dict(self):
        return OrderedDict([('type', Item._type),
                            ('item_type', self.item_type),
                            ('placement', self.placement[0].to_dict())])

    def from_dict(self, obj):
        if 'type' in obj and obj['type'] == Item._type and 'placement' in obj:
            self.placement = [Line().from_dict(obj['placement'])]
            self.item_type = obj['item_type']

        return self
