
from collections import OrderedDict

from Entities.Point import Point

from shapely.geometry import LineString
from shapely.geometry import Point as ShapelyPoint


class Line:
    _type = 'line'

    def __init__(self, _pt1=None, _pt2=None):
        self.point_1 = _pt1
        self.point_2 = _pt2

    def translate(self, pt):
        self.point_1.add(pt)
        self.point_2.add(pt)

        return self

    def scale(self, a):
        self.point_1.mult(a)
        self.point_2.mult(a)

        return self

    def to_dict(self):
        return OrderedDict([('type', Line._type), ('point_1', self.point_1.to_dict()), ('point_2', self.point_2.to_dict())])

    def from_dict(self, obj):
        if 'type' in obj and obj['type'] == Line._type and 'point_1' in obj and 'point_2' in obj:
            self.point_1 = Point().from_dict(obj['point_1'])
            self.point_2 = Point().from_dict(obj['point_2'])

        return self

    def segment_intersection(self, line2):
        line1 = self
        l1 = LineString([(line1.point_1.x, line1.point_1.y), (line1.point_2.x, line1.point_2.y)])
        l2 = LineString([(line2.point_1.x, line2.point_1.y), (line2.point_2.x, line2.point_2.y)])
        intersection = l1.intersection(l2)

        if type(intersection) == ShapelyPoint:
            return Point(intersection.x, intersection.y)

        if type(intersection) == LineString:
            return Line(Point(float(intersection.coords[0][0]), float(intersection.coords[0][1])),
                        Point(float(intersection.coords[1][0]), float(intersection.coords[1][1])))

        return None

    def rectangle_intersection(self, rect):
        segment = self

        def is_point_inside_rectangle(point):
            sp = rect.point_1
            ep = rect.point_2
            if sp.x <= point.x <= ep.x and sp.y <= point.y <= ep.y:
                return True
            return False

        point1_inside = is_point_inside_rectangle(segment.point_1)
        point2_inside = is_point_inside_rectangle(segment.point_2)

        if not point1_inside and not point2_inside:
            return None

        if point1_inside and point2_inside:
            return segment

        if point1_inside:
            inside_point = segment.point_1
        if point2_inside:
            inside_point = segment.point_2

        p1 = rect.point_1
        p2 = rect.point_2

        p = [Point(p1.x, p1.y), Point(p1.x, p2.y), Point(p2.x, p2.y), Point(p2.x, p1.y)]
        lines_rect = [Line(p[0], p[1]), Line(p[1], p[2]), Line(p[2], p[3]), Line(p[3], p[0])]

        for line in lines_rect:
            intersection = segment.segment_intersection(line)
            if type(intersection) == Point:
                return Line(inside_point, intersection)

        return None
