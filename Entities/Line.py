import numpy as np
from collections import OrderedDict
from shapely.geometry import LineString
from shapely.geometry import Point as ShapelyPoint

from Entities.Point import Point


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

        if point1_inside and point2_inside:
            return segment

        p1 = rect.point_1
        p2 = rect.point_2

        p = [Point(p1.x, p1.y), Point(p1.x, p2.y), Point(p2.x, p2.y), Point(p2.x, p1.y)]
        lines_rect = [Line(p[0], p[1]), Line(p[1], p[2]), Line(p[2], p[3]), Line(p[3], p[0])]

        if not point1_inside and not point2_inside:

            intersection_segment = Line()
            for line in lines_rect:
                intersection = segment.segment_intersection(line)
                if type(intersection) == Point:
                    if not intersection_segment.point_1:
                        intersection_segment.point_1 = intersection
                    else:
                        intersection_segment.point_2 = intersection
                if intersection_segment.point_1 and intersection_segment.point_2:
                    return intersection_segment

            return None

        if point1_inside:
            inside_point = segment.point_1

        if point2_inside:
            inside_point = segment.point_2

        for line in lines_rect:
            intersection = segment.segment_intersection(line)
            if type(intersection) == Point:
                return Line(inside_point, intersection)
        return None

    def is_point_of_line(self, point):
        intersection = LineString([(self.point_1.x, self.point_1.y),
                                   (self.point_2.x, self.point_2.y)]).intersection(ShapelyPoint(point.x, point.y))
        if type(intersection) == ShapelyPoint:
            return Point(intersection.x, intersection.y)

        return None

    def angle_between(self, line):
        line1 = self
        line2 = line
        l1 = complex((line1.point_2.x - line1.point_1.x), (line1.point_2.y - line1.point_1.y))
        l2 = complex((line2.point_2.x - line2.point_1.x), (line2.point_2.y - line2.point_1.y))
        a1 = np.angle(l1, deg=True)
        a2 = np.angle(l2, deg=True)
        return abs(a1 - a2)

    def distance_to_point(self, point):
        line = self
        l = LineString([(line.point_1.x, line.point_1.y), (line.point_2.x, line.point_2.y)])
        p = ShapelyPoint(point.x, point.y)
        return l.distance(p)

    def line_length(self):
        return pow((pow(self.point_1.x - self.point_2.x, 2) + pow(self.point_1.y - self.point_2.y, 2)), 1 / 2)
