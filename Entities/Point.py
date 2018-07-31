from collections import OrderedDict

class Point:
    _type = 'point'

    def __init__(self, _x=None, _y=None):
        self.x = _x
        self.y = _y

    def add(self, pt):
        self.x += pt.x
        self.y += pt.y

        return self

    def mult(self, a):
        self.x *= a
        self.y *= a

        return self

    def int_tuple(self):
        return (int(self.x), int(self.y))

    def to_dict(self):
        return OrderedDict([('type', Point._type), ('x', self.x), ('y', self.y)])

    def from_dict(self, obj):
        if 'type' in obj and obj['type'] == Point._type and 'x' in obj and 'y' in obj:
            self.x = float(obj['x'])
            self.y = float(obj['y'])

        return self
